
import abc
import csv
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import TypeVar, Generic, List, Optional, Callable

from ..entities.entities import (
    Libro,
    Genero,
    Editorial,
    Moneda,
    TipoCotizacion,
    Precio,
    Stock,
    CotizacionDolar,
)


T = TypeVar("T")


# ============================================================
# 1. INTERFACES PROVISTAS POR LA CATEDRA
# ============================================================

class IRepositorio(abc.ABC, Generic[T]):
    """Interfaz para repositorios con operaciones CRUD."""

    @abc.abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una entidad."""
        pass

    @abc.abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        """Lee una entidad por su ID."""
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[T]:
        """Lee todas las entidades."""
        pass

    @abc.abstractmethod
    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente."""
        pass

    @abc.abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad por su ID."""
        pass


class IRepositorioStock(abc.ABC):
    """Interfaz para repositorios de Stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        pass


class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para repositorios de cotizaciones del dólar."""

    @abc.abstractmethod
    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: date
    ) -> Optional[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(
        self, tipo_id: int
    ) -> List[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def actualizar(
        self, cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def eliminar(self, tipo_id: int, fecha: date) -> bool:
        pass


# ============================================================
# 2. REPOSITORIO CSV GENERICO
# ============================================================

class RepositorioCSV(Generic[T]):
    """
    Implementa operaciones CRUD sobre un archivo CSV.

    Cada repositorio concreto define cómo convertir sus
    entidades a filas CSV y cómo reconstruirlas.
    """

    def __init__(
        self,
        archivo: str,
        columnas: List[str],
        atributo_id: str,
        serializar: Callable[[T], dict],
        deserializar: Callable[[dict], T],
        asignar_id: Callable[[T, int], None],
    ):
        self.archivo = Path(archivo)
        self.columnas = columnas
        self.atributo_id = atributo_id
        self.serializar = serializar
        self.deserializar = deserializar
        self.asignar_id = asignar_id

        self.archivo.parent.mkdir(parents=True, exist_ok=True)

        if not self.archivo.exists():
            self._guardar_filas([])

    def _leer_filas(self) -> List[dict]:
        """Lee las filas almacenadas en el CSV."""
        with self.archivo.open(
            "r", newline="", encoding="utf-8-sig"
        ) as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)

    def _guardar_filas(self, filas: List[dict]) -> None:
        """Escribe las filas completas en el CSV."""
        with self.archivo.open(
            "w", newline="", encoding="utf-8"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=self.columnas,
                extrasaction="ignore",
            )
            escritor.writeheader()
            escritor.writerows(filas)

    def _guardar_entidades(self, entidades: List[T]) -> None:
        """Convierte entidades a filas y guarda el CSV."""
        filas = [self.serializar(e) for e in entidades]
        self._guardar_filas(filas)

    def _id_de(self, entidad: T) -> Optional[int]:
        return getattr(entidad, self.atributo_id)

    def leer_todos(self) -> List[T]:
        """Devuelve todas las entidades almacenadas."""
        return [
            self.deserializar(fila)
            for fila in self._leer_filas()
        ]

    def leer_por_id(self, id: int) -> Optional[T]:
        """Busca una entidad por su identificador."""
        for entidad in self.leer_todos():
            if self._id_de(entidad) == id:
                return entidad
        return None

    def crear(self, entidad: T) -> T:
        """Asigna un ID si falta y guarda una entidad nueva."""
        entidades = self.leer_todos()
        identificador = self._id_de(entidad)

        if identificador is not None:
            if any(
                self._id_de(e) == identificador
                for e in entidades
            ):
                raise ValueError(
                    f"Ya existe una entidad con ID {identificador}."
                )
        else:
            ids = [
                self._id_de(e)
                for e in entidades
                if self._id_de(e) is not None
            ]
            nuevo_id = max(ids, default=0) + 1
            self.asignar_id(entidad, nuevo_id)

        entidades.append(entidad)
        self._guardar_entidades(entidades)
        return entidad

    def actualizar(self, entidad: T) -> T:
        """Reemplaza una entidad existente."""
        identificador = self._id_de(entidad)

        if identificador is None:
            raise ValueError(
                "No se puede actualizar una entidad sin ID."
            )

        entidades = self.leer_todos()

        for indice, existente in enumerate(entidades):
            if self._id_de(existente) == identificador:
                entidades[indice] = entidad
                self._guardar_entidades(entidades)
                return entidad

        raise ValueError(
            f"No existe una entidad con ID {identificador}."
        )

    def eliminar(self, id: int) -> bool:
        """Elimina una entidad por su ID."""
        entidades = self.leer_todos()
        restantes = [
            entidad
            for entidad in entidades
            if self._id_de(entidad) != id
        ]

        if len(restantes) == len(entidades):
            return False

        self._guardar_entidades(restantes)
        return True


# ============================================================
# 3. REPOSITORIOS CONCRETOS
# ============================================================

class RepositorioGenero(RepositorioCSV[Genero], IRepositorio[Genero]):
    def __init__(self, archivo="src/book_manager/migrations/csv/generos.csv"):
        super().__init__(
            archivo,
            ["id_genero", "nombre"],
            "id_genero",
            lambda e: {
                "id_genero": e.id_genero,
                "nombre": e.nombre,
            },
            lambda f: Genero(
                f["nombre"], int(f["id_genero"])
            ),
            lambda e, i: setattr(e, "id_genero", i),
        )


class RepositorioEditorial(
    RepositorioCSV[Editorial], IRepositorio[Editorial]
):
    def __init__(
        self,
        archivo="src/book_manager/migrations/csv/editoriales.csv",
    ):
        super().__init__(
            archivo,
            ["id_editorial", "nombre", "pais"],
            "id_editorial",
            lambda e: {
                "id_editorial": e.id_editorial,
                "nombre": e.nombre,
                "pais": e.pais or "",
            },
            lambda f: Editorial(
                f["nombre"],
                f["pais"] or None,
                int(f["id_editorial"]),
            ),
            lambda e, i: setattr(e, "id_editorial", i),
        )


class RepositorioMoneda(RepositorioCSV[Moneda], IRepositorio[Moneda]):
    def __init__(self, archivo="src/book_manager/migrations/csv/monedas.csv"):
        super().__init__(
            archivo,
            ["id_moneda", "codigo", "nombre", "simbolo"],
            "id_moneda",
            lambda e: {
                "id_moneda": e.id_moneda,
                "codigo": e.codigo,
                "nombre": e.nombre,
                "simbolo": e.simbolo,
            },
            lambda f: Moneda(
                f["codigo"],
                f["nombre"],
                f["simbolo"],
                int(f["id_moneda"]),
            ),
            lambda e, i: setattr(e, "id_moneda", i),
        )


class RepositorioTipoCotizacion(
    RepositorioCSV[TipoCotizacion],
    IRepositorio[TipoCotizacion],
):
    def __init__(
        self,
        archivo="src/book_manager/migrations/csv/tipos_cotizacion.csv",
    ):
        super().__init__(
            archivo,
            ["id_tipo", "nombre"],
            "id_tipo",
            lambda e: {
                "id_tipo": e.id_tipo,
                "nombre": e.nombre,
            },
            lambda f: TipoCotizacion(
                f["nombre"], int(f["id_tipo"])
            ),
            lambda e, i: setattr(e, "id_tipo", i),
        )


class RepositorioLibro(RepositorioCSV[Libro], IRepositorio[Libro]):
    def __init__(
        self,
        repositorio_editorial: RepositorioEditorial,
        repositorio_genero: RepositorioGenero,
        archivo="src/book_manager/migrations/csv/libros.csv",
    ):
        self.repositorio_editorial = repositorio_editorial
        self.repositorio_genero = repositorio_genero

        super().__init__(
            archivo,
            [
                "id_libro", "isbn", "titulo", "autor",
                "id_editorial", "id_genero",
            ],
            "id_libro",
            lambda e: {
                "id_libro": e.id_libro,
                "isbn": e.isbn,
                "titulo": e.titulo,
                "autor": e.autor,
                "id_editorial": e.editorial.id_editorial,
                "id_genero": e.genero.id_genero,
            },
            self._deserializar,
            lambda e, i: setattr(e, "id_libro", i),
        )

    def _deserializar(self, fila: dict) -> Libro:
        editorial = self.repositorio_editorial.leer_por_id(
            int(fila["id_editorial"])
        )
        genero = self.repositorio_genero.leer_por_id(
            int(fila["id_genero"])
        )

        if editorial is None or genero is None:
            raise ValueError(
                "No se puede reconstruir el libro: "
                "no se encontró su editorial o género."
            )

        return Libro(
            fila["isbn"],
            fila["titulo"],
            fila["autor"],
            editorial,
            genero,
            int(fila["id_libro"]),
        )


class RepositorioPrecio(RepositorioCSV[Precio], IRepositorio[Precio]):
    def __init__(
        self,
        repositorio_libro: RepositorioLibro,
        repositorio_moneda: RepositorioMoneda,
        archivo="src/book_manager/migrations/csv/precios.csv",
    ):
        self.repositorio_libro = repositorio_libro
        self.repositorio_moneda = repositorio_moneda

        super().__init__(
            archivo,
            ["id_precio", "id_libro", "id_moneda", "valor"],
            "id_precio",
            lambda e: {
                "id_precio": e.id_precio,
                "id_libro": e.libro.id_libro,
                "id_moneda": e.moneda.id_moneda,
                "valor": str(e.valor),
            },
            self._deserializar,
            lambda e, i: setattr(e, "id_precio", i),
        )

    def _deserializar(self, fila: dict) -> Precio:
        libro = self.repositorio_libro.leer_por_id(
            int(fila["id_libro"])
        )
        moneda = self.repositorio_moneda.leer_por_id(
            int(fila["id_moneda"])
        )

        if libro is None or moneda is None:
            raise ValueError(
                "No se puede reconstruir el precio: "
                "no se encontró su libro o moneda."
            )

        return Precio(
            libro,
            moneda,
            Decimal(fila["valor"]),
            int(fila["id_precio"]),
        )


# ============================================================
# 4. REPOSITORIO ESPECIAL DE STOCK
# ============================================================

class RepositorioStock(IRepositorioStock):
    """
    El stock se identifica por el ID del libro, no por ISBN.
    Se guarda un único registro de stock por libro.
    """

    def __init__(
        self,
        repositorio_libro: RepositorioLibro,
        archivo="src/book_manager/migrations/csv/stocks.csv",
    ):
        self.repositorio_libro = repositorio_libro
        self.archivo = Path(archivo)
        self.archivo.parent.mkdir(parents=True, exist_ok=True)

        if not self.archivo.exists():
            self._guardar_filas([])

    def _leer_filas(self) -> List[dict]:
        with self.archivo.open(
            "r", newline="", encoding="utf-8-sig"
        ) as archivo:
            return list(csv.DictReader(archivo))

    def _guardar_filas(self, filas: List[dict]) -> None:
        with self.archivo.open(
            "w", newline="", encoding="utf-8"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=[
                    "libro_id", "cantidad", "cantidad_minima"
                ],
            )
            escritor.writeheader()
            escritor.writerows(filas)

    def crear(self, stock: Stock) -> Stock:
        libro_id = stock.libro.id_libro

        if libro_id is None:
            raise ValueError(
                "El libro debe estar guardado antes de registrar su stock."
            )

        if self.leer_por_libro(libro_id) is not None:
            raise ValueError(
                f"Ya existe un stock para el libro ID {libro_id}."
            )

        filas = self._leer_filas()
        filas.append({
            "libro_id": libro_id,
            "cantidad": stock.cantidad,
            "cantidad_minima": stock.cantidad_minima,
        })
        self._guardar_filas(filas)
        return stock

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        for fila in self._leer_filas():
            if int(fila["libro_id"]) == libro_id:
                libro = self.repositorio_libro.leer_por_id(libro_id)

                if libro is None:
                    raise ValueError(
                        f"No se encontró el libro ID {libro_id}."
                    )

                return Stock(
                    libro,
                    int(fila["cantidad"]),
                    int(fila["cantidad_minima"]),
                )

        return None

    def actualizar(self, stock: Stock) -> Stock:
        libro_id = stock.libro.id_libro

        if libro_id is None:
            raise ValueError("El libro del stock no tiene ID.")

        filas = self._leer_filas()

        for fila in filas:
            if int(fila["libro_id"]) == libro_id:
                fila["cantidad"] = stock.cantidad
                fila["cantidad_minima"] = stock.cantidad_minima
                self._guardar_filas(filas)
                return stock

        raise ValueError(
            f"No existe stock para el libro ID {libro_id}."
        )

    def eliminar(self, libro_id: int) -> bool:
        filas = self._leer_filas()
        restantes = [
            fila for fila in filas
            if int(fila["libro_id"]) != libro_id
        ]

        if len(restantes) == len(filas):
            return False

        self._guardar_filas(restantes)
        return True


# ============================================================
# 5. REPOSITORIO ESPECIAL DE COTIZACION DEL DOLAR
# ============================================================

class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
    """
    Cada cotización se identifica por tipo de cotización y fecha.
    El histórico se conserva en el archivo CSV.
    """

    def __init__(
        self,
        repositorio_tipo: RepositorioTipoCotizacion,
        archivo="src/book_manager/migrations/csv/cotizaciones_dolar.csv",
    ):
        self.repositorio_tipo = repositorio_tipo
        self.archivo = Path(archivo)
        self.archivo.parent.mkdir(parents=True, exist_ok=True)

        if not self.archivo.exists():
            self._guardar_filas([])

    def _leer_filas(self) -> List[dict]:
        with self.archivo.open(
            "r", newline="", encoding="utf-8-sig"
        ) as archivo:
            return list(csv.DictReader(archivo))

    def _guardar_filas(self, filas: List[dict]) -> None:
        with self.archivo.open(
            "w", newline="", encoding="utf-8"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo,
                fieldnames=[
                    "tipo_id", "fecha", "compra", "venta"
                ],
            )
            escritor.writeheader()
            escritor.writerows(filas)

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        tipo_id = cotizacion.tipo_cotizacion.id_tipo

        if tipo_id is None:
            raise ValueError(
                "El tipo de cotización debe estar guardado primero."
            )

        if self.leer_por_tipo_y_fecha(
            tipo_id, cotizacion.fecha
        ) is not None:
            raise ValueError(
                "Ya existe una cotización para ese tipo y fecha."
            )

        filas = self._leer_filas()
        filas.append({
            "tipo_id": tipo_id,
            "fecha": cotizacion.fecha.isoformat(),
            "compra": str(cotizacion.compra),
            "venta": str(cotizacion.venta),
        })
        self._guardar_filas(filas)
        return cotizacion

    def leer_por_tipo_y_fecha(
        self, tipo_id: int, fecha: date
    ) -> Optional[CotizacionDolar]:
        for fila in self._leer_filas():
            if (
                int(fila["tipo_id"]) == tipo_id
                and date.fromisoformat(fila["fecha"]) == fecha
            ):
                tipo = self.repositorio_tipo.leer_por_id(tipo_id)

                if tipo is None:
                    raise ValueError(
                        f"No se encontró el tipo de cotización ID {tipo_id}."
                    )

                return CotizacionDolar(
                    tipo,
                    fecha,
                    Decimal(fila["compra"]),
                    Decimal(fila["venta"]),
                )

        return None

    def leer_historico_por_tipo(
        self, tipo_id: int
    ) -> List[CotizacionDolar]:
        cotizaciones = []

        for fila in self._leer_filas():
            if int(fila["tipo_id"]) == tipo_id:
                cotizacion = self.leer_por_tipo_y_fecha(
                    tipo_id,
                    date.fromisoformat(fila["fecha"]),
                )

                if cotizacion is not None:
                    cotizaciones.append(cotizacion)

        return sorted(
            cotizaciones,
            key=lambda c: c.fecha,
            reverse=True,
        )

    def actualizar(
        self, cotizacion: CotizacionDolar
    ) -> CotizacionDolar:
        tipo_id = cotizacion.tipo_cotizacion.id_tipo

        if tipo_id is None:
            raise ValueError("El tipo de cotización no tiene ID.")

        filas = self._leer_filas()

        for fila in filas:
            if (
                int(fila["tipo_id"]) == tipo_id
                and date.fromisoformat(fila["fecha"])
                == cotizacion.fecha
            ):
                fila["compra"] = str(cotizacion.compra)
                fila["venta"] = str(cotizacion.venta)
                self._guardar_filas(filas)
                return cotizacion

        raise ValueError(
            "No existe la cotización para actualizar."
        )

    def eliminar(self, tipo_id: int, fecha: date) -> bool:
        filas = self._leer_filas()
        restantes = [
            fila for fila in filas
            if not (
                int(fila["tipo_id"]) == tipo_id
                and date.fromisoformat(fila["fecha"]) == fecha
            )
        ]

        if len(restantes) == len(filas):
            return False

        self._guardar_filas(restantes)
        return True


