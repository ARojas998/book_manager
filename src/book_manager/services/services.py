
"""Servicios: lógica de negocio del sistema de gestión de libros."""



from typing import List
from decimal import Decimal

from ..entities.entities import (
    Genero,
    Editorial,
    Moneda,
    TipoCotizacion,
    Libro,
    Precio,
    Stock,
    CotizacionDolar
)
from ..repositories.repositories import (
    RepositorioGenero,
    RepositorioEditorial,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioTipoCotizacion,
    RepositorioCotizacionDolar,
    RepositorioStock,
)


# ============================================================
# Excepciones de servicio
# ============================================================

class ErrorServicio(Exception):
    """Excepción base para errores de la lógica de negocio."""


class EntidadNoEncontradaError(ErrorServicio):
    """Se lanza cuando no existe la entidad solicitada."""


class OperacionInvalidaError(ErrorServicio):
    """Se lanza cuando una operación incumple una regla de negocio."""


# ============================================================
# ServicioGenero
# ============================================================

class ServicioGenero:
    """Lógica de negocio para administrar géneros."""

    def __init__(
        self,
        repositorio_genero: RepositorioGenero,
        repositorio_libro: RepositorioLibro,
    ) -> None:
        self._repositorio_genero = repositorio_genero
        self._repositorio_libro = repositorio_libro

    def crear(self, nombre: str) -> Genero:
        """Crea un género si su nombre todavía no existe."""
        nombre_normalizado = nombre.strip().casefold()

        if any(
            genero.nombre.casefold() == nombre_normalizado
            for genero in self._repositorio_genero.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe un género llamado '{nombre}'."
            )

        return self._repositorio_genero.crear(Genero(nombre.strip()))

    def obtener(self, id_genero: int) -> Genero:
        """Obtiene un género por su identificador."""
        genero = self._repositorio_genero.leer_por_id(id_genero)

        if genero is None:
            raise EntidadNoEncontradaError(
                f"No existe el género con ID {id_genero}."
            )

        return genero

    def listar(self) -> List[Genero]:
        """Devuelve todos los géneros registrados."""
        return self._repositorio_genero.leer_todos()

    def actualizar_nombre(
        self,
        id_genero: int,
        nuevo_nombre: str,
    ) -> Genero:
        """Actualiza el nombre de un género sin generar duplicados."""
        genero = self.obtener(id_genero)
        nombre_normalizado = nuevo_nombre.strip().casefold()

        if any(
            otro.id_genero != id_genero
            and otro.nombre.casefold() == nombre_normalizado
            for otro in self._repositorio_genero.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe un género llamado '{nuevo_nombre}'."
            )

        genero.nombre = nuevo_nombre.strip()
        return self._repositorio_genero.actualizar(genero)

    def eliminar(self, id_genero: int) -> bool:
        """Impide eliminar géneros utilizados por libros."""
        self.obtener(id_genero)

        esta_en_uso = any(
            libro.genero.id_genero == id_genero
            for libro in self._repositorio_libro.leer_todos()
        )

        if esta_en_uso:
            raise OperacionInvalidaError(
                "No se puede eliminar un género que tiene libros asociados."
            )

        return self._repositorio_genero.eliminar(id_genero)


# ============================================================
# ServicioEditorial
# ============================================================

class ServicioEditorial:
    """Lógica de negocio para administrar editoriales."""

    def __init__(
        self,
        repositorio_editorial: RepositorioEditorial,
        repositorio_libro: RepositorioLibro,
    ) -> None:
        self._repositorio_editorial = repositorio_editorial
        self._repositorio_libro = repositorio_libro

    def crear(self, nombre: str) -> Editorial:
        """Crea una editorial si su nombre todavía no existe."""
        nombre_normalizado = nombre.strip().casefold()

        if any(
            editorial.nombre.casefold() == nombre_normalizado
            for editorial in self._repositorio_editorial.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe una editorial llamada '{nombre}'."
            )

        return self._repositorio_editorial.crear(
            Editorial(nombre.strip())
        )

    def obtener(self, id_editorial: int) -> Editorial:
        """Obtiene una editorial por su identificador."""
        editorial = self._repositorio_editorial.leer_por_id(id_editorial)

        if editorial is None:
            raise EntidadNoEncontradaError(
                f"No existe la editorial con ID {id_editorial}."
            )

        return editorial

    def listar(self) -> List[Editorial]:
        """Devuelve todas las editoriales registradas."""
        return self._repositorio_editorial.leer_todos()

    def actualizar_nombre(
        self,
        id_editorial: int,
        nuevo_nombre: str,
    ) -> Editorial:
        """Actualiza el nombre de una editorial sin generar duplicados."""
        editorial = self.obtener(id_editorial)
        nombre_normalizado = nuevo_nombre.strip().casefold()

        if any(
            otra.id_editorial != id_editorial
            and otra.nombre.casefold() == nombre_normalizado
            for otra in self._repositorio_editorial.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe una editorial llamada '{nuevo_nombre}'."
            )

        editorial.nombre = nuevo_nombre.strip()
        return self._repositorio_editorial.actualizar(editorial)

    def eliminar(self, id_editorial: int) -> bool:
        """Impide eliminar editoriales utilizadas por libros."""
        self.obtener(id_editorial)

        esta_en_uso = any(
            libro.editorial.id_editorial == id_editorial
            for libro in self._repositorio_libro.leer_todos()
        )

        if esta_en_uso:
            raise OperacionInvalidaError(
                "No se puede eliminar una editorial que tiene libros asociados."
            )

        return self._repositorio_editorial.eliminar(id_editorial)


# ============================================================
# ServicioMoneda
# ============================================================

class ServicioMoneda:
    """Lógica de negocio para administrar monedas."""

    def __init__(
        self,
        repositorio_moneda: RepositorioMoneda,
        repositorio_precio: RepositorioPrecio,
    ) -> None:
        self._repositorio_moneda = repositorio_moneda
        self._repositorio_precio = repositorio_precio

    def crear(self, codigo: str, nombre: str, simbolo: str) -> Moneda:
        """Crea una moneda si su código no está registrado."""
        codigo_normalizado = codigo.strip().upper()

        if any(
            moneda.codigo == codigo_normalizado
            for moneda in self._repositorio_moneda.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe una moneda con código '{codigo_normalizado}'."
            )

        return self._repositorio_moneda.crear(
            Moneda(codigo_normalizado, nombre.strip(), simbolo.strip())
        )

    def obtener(self, id_moneda: int) -> Moneda:
        """Obtiene una moneda por su identificador."""
        moneda = self._repositorio_moneda.leer_por_id(id_moneda)

        if moneda is None:
            raise EntidadNoEncontradaError(
                f"No existe la moneda con ID {id_moneda}."
            )

        return moneda

    def obtener_por_codigo(self, codigo: str) -> Moneda:
        """Busca una moneda por su código, sin distinguir mayúsculas."""
        codigo_normalizado = codigo.strip().upper()

        for moneda in self._repositorio_moneda.leer_todos():
            if moneda.codigo == codigo_normalizado:
                return moneda

        raise EntidadNoEncontradaError(
            f"No existe una moneda con código '{codigo_normalizado}'."
        )

    def listar(self) -> List[Moneda]:
        """Devuelve todas las monedas registradas."""
        return self._repositorio_moneda.leer_todos()

    def actualizar(
        self,
        id_moneda: int,
        nombre: str = None,
        simbolo: str = None,
    ) -> Moneda:
        """Actualiza el nombre o símbolo de una moneda."""
        moneda = self.obtener(id_moneda)

        if nombre is not None:
            moneda.nombre = nombre.strip()

        if simbolo is not None:
            moneda.simbolo = simbolo.strip()

        return self._repositorio_moneda.actualizar(moneda)

    def eliminar(self, id_moneda: int) -> bool:
        """Impide eliminar monedas utilizadas por precios."""
        self.obtener(id_moneda)

        esta_en_uso = any(
            precio.moneda.id_moneda == id_moneda
            for precio in self._repositorio_precio.leer_todos()
        )

        if esta_en_uso:
            raise OperacionInvalidaError(
                "No se puede eliminar una moneda utilizada por precios."
            )

        return self._repositorio_moneda.eliminar(id_moneda)


# ============================================================
# ServicioTipoCotizacion
# ============================================================

class ServicioTipoCotizacion:
    """Lógica de negocio para administrar tipos de cotización."""

    def __init__(
        self,
        repositorio_tipo_cotizacion: RepositorioTipoCotizacion,
        repositorio_cotizacion: RepositorioCotizacionDolar,
    ) -> None:
        self._repositorio_tipo_cotizacion = repositorio_tipo_cotizacion
        self._repositorio_cotizacion = repositorio_cotizacion

    def crear(self, nombre: str) -> TipoCotizacion:
        """Crea un tipo si su nombre no está registrado."""
        nombre_normalizado = nombre.strip().casefold()

        if any(
            tipo.nombre.casefold() == nombre_normalizado
            for tipo in self._repositorio_tipo_cotizacion.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe un tipo de cotización llamado '{nombre}'."
            )

        return self._repositorio_tipo_cotizacion.crear(
            TipoCotizacion(nombre.strip())
        )

    def obtener(self, id_tipo: int) -> TipoCotizacion:
        """Obtiene un tipo de cotización por su identificador."""
        tipo = self._repositorio_tipo_cotizacion.leer_por_id(id_tipo)

        if tipo is None:
            raise EntidadNoEncontradaError(
                f"No existe el tipo de cotización con ID {id_tipo}."
            )

        return tipo

    def listar(self) -> List[TipoCotizacion]:
        """Devuelve todos los tipos de cotización registrados."""
        return self._repositorio_tipo_cotizacion.leer_todos()

    def actualizar_nombre(
        self,
        id_tipo: int,
        nuevo_nombre: str,
    ) -> TipoCotizacion:
        """Actualiza el nombre sin permitir duplicados."""
        tipo = self.obtener(id_tipo)
        nombre_normalizado = nuevo_nombre.strip().casefold()

        if any(
            otro.id_tipo != id_tipo
            and otro.nombre.casefold() == nombre_normalizado
            for otro in self._repositorio_tipo_cotizacion.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe un tipo de cotización llamado '{nuevo_nombre}'."
            )

        tipo.nombre = nuevo_nombre.strip()
        return self._repositorio_tipo_cotizacion.actualizar(tipo)
    
    def eliminar(self, id_tipo: int) -> bool:
        """Impide eliminar tipos que tengan cotizaciones históricas."""
        self.obtener(id_tipo)

        historico = self._repositorio_cotizacion.leer_historico_por_tipo(
            id_tipo
        )

        if historico:
            raise OperacionInvalidaError(
                "No se puede eliminar un tipo con cotizaciones asociadas."
            )

        return self._repositorio_tipo_cotizacion.eliminar(id_tipo)



# ============================================================
# ServicioPrecio
# ============================================================

class ServicioPrecio:
    """Lógica de negocio para administrar precios de libros."""

    def __init__(
        self,
        repositorio_precio: RepositorioPrecio,
        repositorio_libro: RepositorioLibro,
        repositorio_moneda: RepositorioMoneda,
    ) -> None:
        self._repositorio_precio = repositorio_precio
        self._repositorio_libro = repositorio_libro
        self._repositorio_moneda = repositorio_moneda

    def crear(
        self,
        id_libro: int,
        id_moneda: int,
        valor: Decimal,
    ) -> Precio:
        """Registra un precio para un libro y una moneda."""
        libro = self._repositorio_libro.leer_por_id(id_libro)

        if libro is None:
            raise EntidadNoEncontradaError(
                f"No existe el libro con ID {id_libro}."
            )

        moneda = self._repositorio_moneda.leer_por_id(id_moneda)

        if moneda is None:
            raise EntidadNoEncontradaError(
                f"No existe la moneda con ID {id_moneda}."
            )

        precios = self._repositorio_precio.leer_todos()

        if any(
            precio.libro.id_libro == id_libro
            and precio.moneda.id_moneda == id_moneda
            for precio in precios
        ):
            raise OperacionInvalidaError(
                "Ya existe un precio para ese libro y esa moneda."
            )

        return self._repositorio_precio.crear(
            Precio(libro, moneda, valor)
        )

    def obtener(self, id_precio: int) -> Precio:
        """Obtiene un precio por su identificador."""
        precio = self._repositorio_precio.leer_por_id(id_precio)

        if precio is None:
            raise EntidadNoEncontradaError(
                f"No existe el precio con ID {id_precio}."
            )

        return precio

    def listar(self) -> List[Precio]:
        """Devuelve todos los precios registrados."""
        return self._repositorio_precio.leer_todos()

    def actualizar_valor(
        self,
        id_precio: int,
        nuevo_valor: Decimal,
    ) -> Precio:
        """Actualiza el importe de un precio existente."""
        precio = self.obtener(id_precio)
        precio.valor = nuevo_valor

        return self._repositorio_precio.actualizar(precio)

    def eliminar(self, id_precio: int) -> bool:
        """Elimina un precio existente."""
        self.obtener(id_precio)
        return self._repositorio_precio.eliminar(id_precio)


# ============================================================
# ServicioStock
# ============================================================

class ServicioStock:
    """Lógica de negocio para administrar el stock de libros."""

    def __init__(
        self,
        repositorio_stock: RepositorioStock,
        repositorio_libro: RepositorioLibro,
    ) -> None:
        self._repositorio_stock = repositorio_stock
        self._repositorio_libro = repositorio_libro

    def crear(
        self,
        libro_id: int,
        cantidad: int,
        cantidad_minima: int,
    ) -> Stock:
        """Registra el stock de un libro que todavía no lo tiene."""
        libro = self._repositorio_libro.leer_por_id(libro_id)

        if libro is None:
            raise EntidadNoEncontradaError(
                f"No existe el libro con ID {libro_id}."
            )

        stock_existente = self._repositorio_stock.leer_por_libro(
            libro_id
        )

        if stock_existente is not None:
            raise OperacionInvalidaError(
                f"El libro con ID {libro_id} ya tiene stock registrado."
            )

        stock = Stock(libro, cantidad, cantidad_minima)
        return self._repositorio_stock.crear(stock)

    def obtener_por_libro(self, libro_id: int) -> Stock:
        """Obtiene el stock mediante el ID del libro."""
        stock = self._repositorio_stock.leer_por_libro(libro_id)

        if stock is None:
            raise EntidadNoEncontradaError(
                f"No existe stock para el libro con ID {libro_id}."
            )

        return stock

    def actualizar(
        self,
        libro_id: int,
        cantidad: int,
        cantidad_minima: int,
    ) -> Stock:
        """Actualiza las cantidades del stock de un libro."""
        stock = self.obtener_por_libro(libro_id)
        stock.cantidad = cantidad
        stock.cantidad_minima = cantidad_minima

        return self._repositorio_stock.actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:
        """Elimina el registro de stock de un libro."""
        self.obtener_por_libro(libro_id)
        return self._repositorio_stock.eliminar(libro_id)


# ============================================================
# ServicioLibro
# ============================================================

class ServicioLibro:
    """Lógica de negocio para administrar libros."""

    def __init__(
        self,
        repositorio_libro: RepositorioLibro,
        repositorio_editorial: RepositorioEditorial,
        repositorio_genero: RepositorioGenero,
        repositorio_precio: RepositorioPrecio,
        repositorio_stock: RepositorioStock,
    ) -> None:
        self._repositorio_libro = repositorio_libro
        self._repositorio_editorial = repositorio_editorial
        self._repositorio_genero = repositorio_genero
        self._repositorio_precio = repositorio_precio
        self._repositorio_stock = repositorio_stock

    def crear(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        id_editorial: int,
        id_genero: int,
    ) -> Libro:
        """Crea un libro validando sus relaciones y su ISBN."""
        isbn_normalizado = isbn.strip()

        if any(
            libro.isbn == isbn_normalizado
            for libro in self._repositorio_libro.leer_todos()
        ):
            raise OperacionInvalidaError(
                f"Ya existe un libro con ISBN '{isbn_normalizado}'."
            )

        editorial = self._repositorio_editorial.leer_por_id(id_editorial)
        if editorial is None:
            raise EntidadNoEncontradaError(
                f"No existe la editorial con ID {id_editorial}."
            )

        genero = self._repositorio_genero.leer_por_id(id_genero)
        if genero is None:
            raise EntidadNoEncontradaError(
                f"No existe el género con ID {id_genero}."
            )

        libro = Libro(
            isbn_normalizado,
            titulo.strip(),
            autor.strip(),
            editorial,
            genero,
        )

        return self._repositorio_libro.crear(libro)

    def obtener(self, id_libro: int) -> Libro:
        """Obtiene un libro por su identificador."""
        libro = self._repositorio_libro.leer_por_id(id_libro)

        if libro is None:
            raise EntidadNoEncontradaError(
                f"No existe el libro con ID {id_libro}."
            )

        return libro

    def listar(self) -> List[Libro]:
        """Devuelve todos los libros registrados."""
        return self._repositorio_libro.leer_todos()

    def actualizar(
        self,
        id_libro: int,
        isbn: str = None,
        titulo: str = None,
        autor: str = None,
        id_editorial: int = None,
        id_genero: int = None,
    ) -> Libro:
        """Actualiza los datos de un libro existente."""
        libro = self.obtener(id_libro)

        if isbn is not None:
            isbn_normalizado = isbn.strip()

            if any(
                otro.id_libro != id_libro
                and otro.isbn == isbn_normalizado
                for otro in self._repositorio_libro.leer_todos()
            ):
                raise OperacionInvalidaError(
                    f"Ya existe un libro con ISBN '{isbn_normalizado}'."
                )

            libro.isbn = isbn_normalizado

        if titulo is not None:
            libro.titulo = titulo.strip()

        if autor is not None:
            libro.autor = autor.strip()

        if id_editorial is not None:
            editorial = self._repositorio_editorial.leer_por_id(
                id_editorial
            )
            if editorial is None:
                raise EntidadNoEncontradaError(
                    f"No existe la editorial con ID {id_editorial}."
                )
            libro.editorial = editorial

        if id_genero is not None:
            genero = self._repositorio_genero.leer_por_id(id_genero)
            if genero is None:
                raise EntidadNoEncontradaError(
                    f"No existe el género con ID {id_genero}."
                )
            libro.genero = genero

        return self._repositorio_libro.actualizar(libro)

    def eliminar(self, id_libro: int) -> bool:
        """Impide eliminar libros con precios o stock asociados."""
        self.obtener(id_libro)

        tiene_precios = any(
            precio.libro.id_libro == id_libro
            for precio in self._repositorio_precio.leer_todos()
        )

        tiene_stock = (
            self._repositorio_stock.leer_por_libro(id_libro) is not None
        )

        if tiene_precios or tiene_stock:
            raise OperacionInvalidaError(
                "No se puede eliminar un libro que tenga precios o stock asociados."
            )

        return self._repositorio_libro.eliminar(id_libro)


# ============================================================
# ServicioCotizacionDolar
# ============================================================

class ServicioCotizacionDolar:
    """Lógica de negocio para administrar cotizaciones del dólar."""

    def __init__(
        self,
        repositorio_cotizacion: RepositorioCotizacionDolar,
        repositorio_tipo: RepositorioTipoCotizacion,
    ) -> None:
        self._repositorio_cotizacion = repositorio_cotizacion
        self._repositorio_tipo = repositorio_tipo

    def registrar(
        self,
        id_tipo: int,
        fecha,
        compra: Decimal,
        venta: Decimal,
    ) -> CotizacionDolar:
        """Registra una cotización para un tipo y una fecha."""
        tipo = self._repositorio_tipo.leer_por_id(id_tipo)

        if tipo is None:
            raise EntidadNoEncontradaError(
                f"No existe el tipo de cotización con ID {id_tipo}."
            )

        existente = self._repositorio_cotizacion.leer_por_tipo_y_fecha(
            id_tipo, fecha
        )

        if existente is not None:
            raise OperacionInvalidaError(
                "Ya existe una cotización para ese tipo y esa fecha."
            )

        cotizacion = CotizacionDolar(tipo, fecha, compra, venta)
        return self._repositorio_cotizacion.crear(cotizacion)

    def obtener(self, id_tipo: int, fecha) -> CotizacionDolar:
        """Obtiene una cotización por tipo y fecha."""
        cotizacion = (
            self._repositorio_cotizacion.leer_por_tipo_y_fecha(
                id_tipo, fecha
            )
        )

        if cotizacion is None:
            raise EntidadNoEncontradaError(
                "No existe una cotización para ese tipo y esa fecha."
            )

        return cotizacion

    def obtener_historico(self, id_tipo: int) -> List[CotizacionDolar]:
        """Devuelve el historial de un tipo de cotización."""
        tipo = self._repositorio_tipo.leer_por_id(id_tipo)

        if tipo is None:
            raise EntidadNoEncontradaError(
                f"No existe el tipo de cotización con ID {id_tipo}."
            )

        return self._repositorio_cotizacion.leer_historico_por_tipo(
            id_tipo
        )

    def obtener_ultima(self, id_tipo: int):
        """Devuelve la cotización más reciente de un tipo."""
        historico = self.obtener_historico(id_tipo)

        if not historico:
            raise EntidadNoEncontradaError(
                "El tipo de cotización no tiene registros históricos."
            )

        return max(historico, key=lambda cotizacion: cotizacion.fecha)

    def actualizar(
        self,
        id_tipo: int,
        fecha,
        compra: Decimal = None,
        venta: Decimal = None,
    ) -> CotizacionDolar:
        """Actualiza los valores de una cotización existente."""
        cotizacion = self.obtener(id_tipo, fecha)

        if compra is not None:
            cotizacion.compra = compra

        if venta is not None:
            cotizacion.venta = venta

        return self._repositorio_cotizacion.actualizar(cotizacion)

    def eliminar(self, id_tipo: int, fecha) -> bool:
        """Elimina una cotización identificada por tipo y fecha."""
        self.obtener(id_tipo, fecha)

        return self._repositorio_cotizacion.eliminar(id_tipo, fecha)
