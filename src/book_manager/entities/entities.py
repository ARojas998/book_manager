
from datetime import date
from decimal import Decimal, InvalidOperation
import re


def _validar_texto(valor: str, campo: str) -> str:
    """Valida un texto obligatorio y elimina espacios externos."""
    if not isinstance(valor, str):
        raise ValueError(f"{campo} debe ser un texto.")

    valor = valor.strip()

    if not valor:
        raise ValueError(f"{campo} no puede estar vacío.")

    return valor


def _validar_id(valor: int | None, campo: str) -> int | None:
    """Valida un identificador entero positivo o None."""
    if valor is None:
        return None

    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"{campo} debe ser un entero.")

    if valor <= 0:
        raise ValueError(f"{campo} debe ser mayor que cero.")

    return valor


def _validar_entero_no_negativo(valor: int, campo: str) -> int:
    """Valida un entero mayor o igual a cero."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"{campo} debe ser un entero.")

    if valor < 0:
        raise ValueError(f"{campo} no puede ser negativo.")

    return valor


def _validar_decimal_positivo(
    valor: Decimal | str | int,
    campo: str,
) -> Decimal:
    """Valida un importe positivo con hasta dos decimales."""
    if isinstance(valor, (bool, float)):
        raise ValueError(
            f"{campo} debe ingresarse como Decimal, texto o entero."
        )

    try:
        valor = Decimal(str(valor))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{campo} debe ser un número válido.") from None

    if not valor.is_finite():
        raise ValueError(f"{campo} debe ser un número finito.")

    if valor <= 0:
        raise ValueError(f"{campo} debe ser mayor que cero.")

    if valor.normalize().as_tuple().exponent < -2:
        raise ValueError(f"{campo} admite como máximo dos decimales.")

    return valor


class Genero:
    def __init__(self, nombre: str, id_genero: int | None = None):
        self.__id_genero = None
        self.__nombre = ""
        self.id_genero = id_genero
        self.nombre = nombre

    @property
    def id_genero(self) -> int | None:
        return self.__id_genero

    @id_genero.setter
    def id_genero(self, valor: int | None) -> None:
        self.__id_genero = _validar_id(valor, "ID del género")

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = _validar_texto(valor, "Nombre del género")


class Editorial:
    def __init__(
        self,
        nombre: str,
        pais: str | None = None,
        id_editorial: int | None = None,
    ):
        self.__id_editorial = None
        self.__nombre = ""
        self.__pais = None
        self.id_editorial = id_editorial
        self.nombre = nombre
        self.pais = pais

    @property
    def id_editorial(self) -> int | None:
        return self.__id_editorial

    @id_editorial.setter
    def id_editorial(self, valor: int | None) -> None:
        self.__id_editorial = _validar_id(valor, "ID de la editorial")

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = _validar_texto(valor, "Nombre de la editorial")

    @property
    def pais(self) -> str | None:
        return self.__pais

    @pais.setter
    def pais(self, valor: str | None) -> None:
        if valor is None:
            self.__pais = None
        else:
            self.__pais = _validar_texto(valor, "País")


class Moneda:
    def __init__(
        self,
        codigo: str,
        nombre: str,
        simbolo: str,
        id_moneda: int | None = None,
    ):
        self.__id_moneda = None
        self.__codigo = ""
        self.__nombre = ""
        self.__simbolo = ""
        self.id_moneda = id_moneda
        self.codigo = codigo
        self.nombre = nombre
        self.simbolo = simbolo

    @property
    def id_moneda(self) -> int | None:
        return self.__id_moneda

    @id_moneda.setter
    def id_moneda(self, valor: int | None) -> None:
        self.__id_moneda = _validar_id(valor, "ID de la moneda")

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        valor = _validar_texto(valor, "Código de moneda")

        if not re.fullmatch(r"[A-Za-z]{3}", valor):
            raise ValueError(
                "El código de moneda debe contener tres letras."
            )

        self.__codigo = valor.upper()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = _validar_texto(valor, "Nombre de la moneda")

    @property
    def simbolo(self) -> str:
        return self.__simbolo

    @simbolo.setter
    def simbolo(self, valor: str) -> None:
        self.__simbolo = _validar_texto(valor, "Símbolo de la moneda")


class TipoCotizacion:
    def __init__(self, nombre: str, id_tipo: int | None = None):
        self.__id_tipo = None
        self.__nombre = ""
        self.id_tipo = id_tipo
        self.nombre = nombre

    @property
    def id_tipo(self) -> int | None:
        return self.__id_tipo

    @id_tipo.setter
    def id_tipo(self, valor: int | None) -> None:
        self.__id_tipo = _validar_id(valor, "ID del tipo de cotización")

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = _validar_texto(
            valor, "Nombre del tipo de cotización"
        )


class Libro:
    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        editorial: Editorial,
        genero: Genero,
        id_libro: int | None = None,
    ):
        self.__id_libro = None
        self.__isbn = ""
        self.__titulo = ""
        self.__autor = ""
        self.__editorial = None
        self.__genero = None
        self.id_libro = id_libro
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.genero = genero

    @property
    def id_libro(self) -> int | None:
        return self.__id_libro

    @id_libro.setter
    def id_libro(self, valor: int | None) -> None:
        self.__id_libro = _validar_id(valor, "ID del libro")

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        self.__isbn = _validar_texto(valor, "ISBN")

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self.__titulo = _validar_texto(valor, "Título")

    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self.__autor = _validar_texto(valor, "Autor")

    @property
    def editorial(self) -> Editorial:
        return self.__editorial

    @editorial.setter
    def editorial(self, valor: Editorial) -> None:
        if not isinstance(valor, Editorial):
            raise ValueError("La editorial debe ser un objeto Editorial.")

        self.__editorial = valor

    @property
    def genero(self) -> Genero:
        return self.__genero

    @genero.setter
    def genero(self, valor: Genero) -> None:
        if not isinstance(valor, Genero):
            raise ValueError("El género debe ser un objeto Genero.")

        self.__genero = valor


class Precio:
    def __init__(
        self,
        libro: Libro,
        moneda: Moneda,
        valor: Decimal | str | int,
        id_precio: int | None = None,
    ):
        self.__id_precio = None
        self.__libro = None
        self.__moneda = None
        self.__valor = Decimal("0")
        self.id_precio = id_precio
        self.libro = libro
        self.moneda = moneda
        self.valor = valor

    @property
    def id_precio(self) -> int | None:
        return self.__id_precio

    @id_precio.setter
    def id_precio(self, valor: int | None) -> None:
        self.__id_precio = _validar_id(valor, "ID del precio")

    @property
    def libro(self) -> Libro:
        return self.__libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        if not isinstance(valor, Libro):
            raise ValueError("El libro debe ser un objeto Libro.")

        self.__libro = valor

    @property
    def moneda(self) -> Moneda:
        return self.__moneda

    @moneda.setter
    def moneda(self, valor: Moneda) -> None:
        if not isinstance(valor, Moneda):
            raise ValueError("La moneda debe ser un objeto Moneda.")

        self.__moneda = valor

    @property
    def valor(self) -> Decimal:
        return self.__valor

    @valor.setter
    def valor(self, valor: Decimal | str | int) -> None:
        self.__valor = _validar_decimal_positivo(valor, "Precio")


class Stock:
    def __init__(
        self,
        libro: Libro,
        cantidad: int,
        cantidad_minima: int,
    ):
        self.__libro = None
        self.__cantidad = 0
        self.__cantidad_minima = 0
        self.libro = libro
        self.cantidad = cantidad
        self.cantidad_minima = cantidad_minima

    @property
    def libro(self) -> Libro:
        return self.__libro

    @libro.setter
    def libro(self, valor: Libro) -> None:
        if not isinstance(valor, Libro):
            raise ValueError("El libro debe ser un objeto Libro.")

        self.__libro = valor

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self.__cantidad = _validar_entero_no_negativo(
            valor, "Cantidad en stock"
        )

    @property
    def cantidad_minima(self) -> int:
        return self.__cantidad_minima

    @cantidad_minima.setter
    def cantidad_minima(self, valor: int) -> None:
        self.__cantidad_minima = _validar_entero_no_negativo(
            valor, "Cantidad mínima"
        )


class CotizacionDolar:
    def __init__(
        self,
        tipo_cotizacion: TipoCotizacion,
        fecha: date,
        compra: Decimal | str | int,
        venta: Decimal | str | int,
    ):
        self.__tipo_cotizacion = None
        self.__fecha = date.today()
        self.__compra = Decimal("0")
        self.__venta = Decimal("0")
        self.tipo_cotizacion = tipo_cotizacion
        self.fecha = fecha
        self.compra = compra
        self.venta = venta

    @property
    def tipo_cotizacion(self) -> TipoCotizacion:
        return self.__tipo_cotizacion

    @tipo_cotizacion.setter
    def tipo_cotizacion(self, valor: TipoCotizacion) -> None:
        if not isinstance(valor, TipoCotizacion):
            raise ValueError(
                "El tipo debe ser un objeto TipoCotizacion."
            )

        self.__tipo_cotizacion = valor

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: date) -> None:
        if not isinstance(valor, date):
            raise ValueError("La fecha debe ser un objeto date.")

        if valor > date.today():
            raise ValueError("La fecha no puede estar en el futuro.")

        self.__fecha = valor

    @property
    def compra(self) -> Decimal:
        return self.__compra

    @compra.setter
    def compra(self, valor: Decimal | str | int) -> None:
        valor = _validar_decimal_positivo(valor, "Cotización de compra")

        if valor > self.__venta and self.__venta > 0:
            raise ValueError(
                "La cotización de compra no puede superar la de venta."
            )

        self.__compra = valor

    @property
    def venta(self) -> Decimal:
        return self.__venta

    @venta.setter
    def venta(self, valor: Decimal | str | int) -> None:
        valor = _validar_decimal_positivo(valor, "Cotización de venta")

        if self.__compra > 0 and valor < self.__compra:
            raise ValueError(
                "La cotización de venta no puede ser inferior a la compra."
            )

        self.__venta = valor
