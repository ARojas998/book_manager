
"""Interfaz de consola del sistema de gestión de libros."""

from datetime import date
from decimal import Decimal, InvalidOperation

from ..repositories.repositories import (
    RepositorioGenero,
    RepositorioEditorial,
    RepositorioMoneda,
    RepositorioTipoCotizacion,
    RepositorioLibro,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioCotizacionDolar,
)

from ..services.services import (
    ServicioGenero,
    ServicioEditorial,
    ServicioMoneda,
    ServicioTipoCotizacion,
    ServicioLibro,
    ServicioPrecio,
    ServicioStock,
    ServicioCotizacionDolar,
    ErrorServicio,
)


def crear_servicios():
    """Construye los repositorios y servicios del sistema."""

    # Repositorios de las entidades principales.
    repo_generos = RepositorioGenero()
    repo_editoriales = RepositorioEditorial()
    repo_monedas = RepositorioMoneda()
    repo_tipos = RepositorioTipoCotizacion()

    # Repositorios que necesitan otras entidades.
    repo_libros = RepositorioLibro(
        repo_editoriales,
        repo_generos,
    )
    repo_precios = RepositorioPrecio(
        repo_libros,
        repo_monedas,
    )
    repo_stock = RepositorioStock(repo_libros)
    repo_cotizaciones = RepositorioCotizacionDolar(repo_tipos)

    # Servicios: concentran las validaciones de negocio.
    servicios = {
        "generos": ServicioGenero(
            repo_generos,
            repo_libros,
        ),
        "editoriales": ServicioEditorial(
            repo_editoriales,
            repo_libros,
        ),
        "monedas": ServicioMoneda(
            repo_monedas,
            repo_precios,
        ),
        "tipos_cotizacion": ServicioTipoCotizacion(
            repo_tipos,
            repo_cotizaciones,
        ),
        "libros": ServicioLibro(
            repo_libros,
            repo_editoriales,
            repo_generos,
            repo_precios,
            repo_stock,
        ),
        "precios": ServicioPrecio(
            repo_precios,
            repo_libros,
            repo_monedas,
        ),
        "stock": ServicioStock(
            repo_stock,
            repo_libros,
        ),
        "cotizaciones": ServicioCotizacionDolar(
            repo_cotizaciones,
            repo_tipos,
        ),
    }

    return servicios


def leer_texto(mensaje):
    """Solicita un texto no vacío."""
    while True:
        valor = input(mensaje).strip()

        if valor:
            return valor

        print("El valor no puede estar vacío.")


def leer_entero(mensaje):
    """Solicita un número entero válido."""
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Ingresá un número entero válido.")


def leer_decimal(mensaje):
    """Solicita un número decimal y lo convierte a Decimal."""
    while True:
        entrada = input(mensaje).strip().replace(",", ".")

        try:
            return Decimal(entrada)
        except InvalidOperation:
            print("Ingresá un número válido, por ejemplo: 1250.50.")


def leer_fecha(mensaje):
    """Solicita una fecha en formato AAAA-MM-DD."""
    while True:
        try:
            return date.fromisoformat(input(mensaje).strip())
        except ValueError:
            print("Fecha inválida. Usá el formato AAAA-MM-DD.")


def mostrar_menu_principal():
    """Muestra las opciones principales del sistema."""

    print("\n" + "=" * 45)
    print("       SISTEMA DE GESTIÓN DE LIBROS")
    print("=" * 45)
    print("1. Géneros")
    print("2. Editoriales")
    print("3. Monedas")
    print("4. Tipos de cotización")
    print("5. Libros")
    print("6. Precios")
    print("7. Stock")
    print("8. Cotizaciones del dólar")
    print("0. Salir")
    print("=" * 45)



def ejecutar_menu_principal():
    """Controla la navegación del menú principal."""

    servicios = crear_servicios()

    nombres = {
        "1": "Géneros",
        "2": "Editoriales",
        "3": "Monedas",
        "4": "Tipos de cotización",
        "5": "Libros",
        "6": "Precios",
        "7": "Stock",
        "8": "Cotizaciones del dólar",
    }

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccioná una opción: ").strip()

        if opcion == "0":
            print("Cerrando el sistema. ¡Hasta luego!")
            break

        elif opcion in nombres:
            ejecutar_menu_crud(nombres[opcion], servicios)

        else:
            print("Opción inválida. Ingresá un número del 0 al 8.")



def mostrar_menu_crud(nombre):
    """Muestra las operaciones disponibles para una entidad."""

    print("\n" + "=" * 40)
    print(f"       GESTIÓN DE {nombre.upper()}")
    print("=" * 40)
    print("1. Listar registros")
    print("2. Crear registro")
    print("3. Modificar registro")
    print("4. Eliminar registro")
    print("0. Volver al menú principal")
    print("=" * 40)

def ejecutar_menu_crud(nombre, servicios):
    """Controla el menú CRUD de la entidad seleccionada."""

    while True:
        mostrar_menu_crud(nombre)
        opcion = input("Seleccioná una opción: ").strip()

        if opcion == "0":
            print("Volviendo al menú principal...")
            break

        elif nombre == "Géneros":
            if opcion == "1":
                listar_generos(servicios)
            elif opcion == "2":
                crear_genero(servicios)
            elif opcion == "3":
                modificar_genero(servicios)
            elif opcion == "4":
                eliminar_genero(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")

        elif nombre == "Editoriales":
            if opcion == "1":
                listar_editoriales(servicios)
            elif opcion == "2":
                crear_editorial(servicios)
            elif opcion == "3":
                modificar_editorial(servicios)
            elif opcion == "4":
                eliminar_editorial(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")
        
        elif nombre == "Monedas":
            if opcion == "1":
                listar_monedas(servicios)
            elif opcion == "2":
                crear_moneda(servicios)
            elif opcion == "3":
                modificar_moneda(servicios)
            elif opcion == "4":
                eliminar_moneda(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")
        
        elif nombre == "Tipos de cotización":
            if opcion == "1":
                listar_tipos_cotizacion(servicios)
            elif opcion == "2":
                crear_tipo_cotizacion(servicios)
            elif opcion == "3":
                modificar_tipo_cotizacion(servicios)
            elif opcion == "4":
                eliminar_tipo_cotizacion(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")
        
        elif nombre == "Libros":
            if opcion == "1":
                listar_libros(servicios)
            elif opcion == "2":
                crear_libro(servicios)
            elif opcion == "3":
                modificar_libro(servicios)
            elif opcion == "4":
                eliminar_libro(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")
        
        elif nombre == "Precios":
            if opcion == "1":
                listar_precios(servicios)
            elif opcion == "2":
                crear_precio(servicios)
            elif opcion == "3":
                modificar_precio(servicios)
            elif opcion == "4":
                eliminar_precio(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")
        
        elif nombre == "Stock":
            if opcion == "1":
                listar_stock(servicios)
            elif opcion == "2":
                crear_stock(servicios)
            elif opcion == "3":
                modificar_stock(servicios)
            elif opcion == "4":
                eliminar_stock(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")
        
        elif nombre == "Cotizaciones del dólar":
            if opcion == "1":
                listar_cotizaciones(servicios)
            elif opcion == "2":
                crear_cotizacion(servicios)
            elif opcion == "3":
                modificar_cotizacion(servicios)
            elif opcion == "4":
                eliminar_cotizacion(servicios)
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")

        else:
            if opcion in {"1", "2", "3", "4"}:
                print(
                    "Las operaciones de esta entidad "
                    "se implementarán próximamente."
                )
            else:
                print("Opción inválida. Ingresá un número del 0 al 4.")

def listar_generos(servicios):
    """Muestra todos los géneros registrados."""

    generos = servicios["generos"].listar()

    print("\n--- LISTADO DE GÉNEROS ---")

    if not generos:
        print("No hay géneros registrados.")
        return

    for genero in generos:
        print(f"ID: {genero.id_genero} | Nombre: {genero.nombre}")


def crear_genero(servicios):
    """Registra un nuevo género."""

    print("\n--- ALTA DE GÉNERO ---")
    nombre = leer_texto("Nombre del género: ")

    try:
        genero = servicios["generos"].crear(nombre)
        print(f"Género creado correctamente: {genero.nombre}")
    except ErrorServicio as error:
        print(f"No se pudo crear el género: {error}")


def modificar_genero(servicios):
    """Modifica el nombre de un género existente."""

    print("\n--- MODIFICACIÓN DE GÉNERO ---")
    id_genero = leer_entero("ID del género que querés modificar: ")

    try:
        genero = servicios["generos"].obtener(id_genero)
        print(f"Género actual: {genero.nombre}")

        nuevo_nombre = leer_texto("Nuevo nombre: ")
        servicios["generos"].actualizar_nombre(id_genero, nuevo_nombre)

        print("Género modificado correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar el género: {error}")


def eliminar_genero(servicios):
    """Elimina un género después de pedir confirmación."""

    print("\n--- BAJA DE GÉNERO ---")
    id_genero = leer_entero("ID del género que querés eliminar: ")

    try:
        genero = servicios["generos"].obtener(id_genero)
        print(f"Género seleccionado: {genero.nombre}")

        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["generos"].eliminar(id_genero)
            print("Género eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar el género: {error}")


def listar_editoriales(servicios):
    """Muestra las editoriales registradas."""

    editoriales = servicios["editoriales"].listar()

    print("\n--- LISTADO DE EDITORIALES ---")

    if not editoriales:
        print("No hay editoriales registradas.")
        return

    for editorial in editoriales:
        pais = getattr(editorial, "pais", None) or "No especificado"
        print(
            f"ID: {editorial.id_editorial} | "
            f"Nombre: {editorial.nombre} | "
            f"País: {pais}"
        )


def crear_editorial(servicios):
    """Registra una editorial nueva."""

    print("\n--- ALTA DE EDITORIAL ---")
    nombre = leer_texto("Nombre de la editorial: ")

    try:
        editorial = servicios["editoriales"].crear(nombre)
        print(f"Editorial creada correctamente: {editorial.nombre}")
    except ErrorServicio as error:
        print(f"No se pudo crear la editorial: {error}")


def modificar_editorial(servicios):
    """Modifica el nombre de una editorial."""

    print("\n--- MODIFICACIÓN DE EDITORIAL ---")
    id_editorial = leer_entero("ID de la editorial: ")

    try:
        editorial = servicios["editoriales"].obtener(id_editorial)
        print(f"Nombre actual: {editorial.nombre}")

        nuevo_nombre = leer_texto("Nuevo nombre: ")

        servicios["editoriales"].actualizar_nombre(
            id_editorial,
            nuevo_nombre,
        )

        print("Editorial modificada correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar la editorial: {error}")


def eliminar_editorial(servicios):
    """Elimina una editorial después de confirmar."""

    print("\n--- BAJA DE EDITORIAL ---")
    id_editorial = leer_entero("ID de la editorial: ")

    try:
        editorial = servicios["editoriales"].obtener(id_editorial)
        print(f"Editorial seleccionada: {editorial.nombre}")

        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["editoriales"].eliminar(id_editorial)
            print("Editorial eliminada correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar la editorial: {error}")


def listar_monedas(servicios):
    """Muestra todas las monedas registradas."""

    monedas = servicios["monedas"].listar()

    print("\n--- LISTADO DE MONEDAS ---")

    if not monedas:
        print("No hay monedas registradas.")
        return

    for moneda in monedas:
        print(
            f"ID: {moneda.id_moneda} | "
            f"Código: {moneda.codigo} | "
            f"Nombre: {moneda.nombre} | "
            f"Símbolo: {moneda.simbolo}"
        )


def crear_moneda(servicios):
    """Registra una nueva moneda."""

    print("\n--- ALTA DE MONEDA ---")
    codigo = leer_texto("Código de la moneda (ej. ARS): ").upper()
    nombre = leer_texto("Nombre de la moneda: ")
    simbolo = leer_texto("Símbolo de la moneda (ej. $): ")

    try:
        moneda = servicios["monedas"].crear(
            codigo,
            nombre,
            simbolo,
        )
        print(f"Moneda creada correctamente: {moneda.codigo}")
    except ErrorServicio as error:
        print(f"No se pudo crear la moneda: {error}")


def modificar_moneda(servicios):
    """Modifica el nombre o símbolo de una moneda."""

    print("\n--- MODIFICACIÓN DE MONEDA ---")
    id_moneda = leer_entero("ID de la moneda: ")

    try:
        moneda = servicios["monedas"].obtener(id_moneda)
        print(
            f"Moneda actual: {moneda.codigo} - "
            f"{moneda.nombre} ({moneda.simbolo})"
        )

        print("Dejá vacío un campo para conservar su valor actual.")
        nuevo_nombre = input("Nuevo nombre: ").strip()
        nuevo_simbolo = input("Nuevo símbolo: ").strip()

        servicios["monedas"].actualizar(
            id_moneda,
            nombre=nuevo_nombre or None,
            simbolo=nuevo_simbolo or None,
        )

        print("Moneda modificada correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar la moneda: {error}")


def eliminar_moneda(servicios):
    """Elimina una moneda después de confirmar."""

    print("\n--- BAJA DE MONEDA ---")
    id_moneda = leer_entero("ID de la moneda: ")

    try:
        moneda = servicios["monedas"].obtener(id_moneda)
        print(f"Moneda seleccionada: {moneda.codigo} - {moneda.nombre}")

        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["monedas"].eliminar(id_moneda)
            print("Moneda eliminada correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar la moneda: {error}")


def listar_tipos_cotizacion(servicios):
    """Muestra los tipos de cotización registrados."""

    tipos = servicios["tipos_cotizacion"].listar()

    print("\n--- LISTADO DE TIPOS DE COTIZACIÓN ---")

    if not tipos:
        print("No hay tipos de cotización registrados.")
        return

    for tipo in tipos:
        print(f"ID: {tipo.id_tipo} | Nombre: {tipo.nombre}")


def crear_tipo_cotizacion(servicios):
    """Registra un nuevo tipo de cotización."""

    print("\n--- ALTA DE TIPO DE COTIZACIÓN ---")
    nombre = leer_texto("Nombre del tipo de cotización: ")

    try:
        tipo = servicios["tipos_cotizacion"].crear(nombre)
        print(f"Tipo creado correctamente: {tipo.nombre}")
    except ErrorServicio as error:
        print(f"No se pudo crear el tipo: {error}")


def modificar_tipo_cotizacion(servicios):
    """Modifica el nombre de un tipo de cotización."""

    print("\n--- MODIFICACIÓN DE TIPO DE COTIZACIÓN ---")
    id_tipo = leer_entero("ID del tipo de cotización: ")

    try:
        tipo = servicios["tipos_cotizacion"].obtener(id_tipo)
        print(f"Nombre actual: {tipo.nombre}")

        nuevo_nombre = leer_texto("Nuevo nombre: ")

        servicios["tipos_cotizacion"].actualizar_nombre(
            id_tipo,
            nuevo_nombre,
        )

        print("Tipo de cotización modificado correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar el tipo: {error}")


def eliminar_tipo_cotizacion(servicios):
    """Elimina un tipo de cotización después de confirmar."""

    print("\n--- BAJA DE TIPO DE COTIZACIÓN ---")
    id_tipo = leer_entero("ID del tipo de cotización: ")

    try:
        tipo = servicios["tipos_cotizacion"].obtener(id_tipo)
        print(f"Tipo seleccionado: {tipo.nombre}")

        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["tipos_cotizacion"].eliminar(id_tipo)
            print("Tipo de cotización eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar el tipo: {error}")


def listar_libros(servicios):
    """Muestra todos los libros registrados."""

    libros = servicios["libros"].listar()

    print("\n--- LISTADO DE LIBROS ---")

    if not libros:
        print("No hay libros registrados.")
        return

    for libro in libros:
        print(
            f"ID: {libro.id_libro} | "
            f"ISBN: {libro.isbn} | "
            f"Título: {libro.titulo} | "
            f"Autor: {libro.autor} | "
            f"Editorial: {libro.editorial.nombre} | "
            f"Género: {libro.genero.nombre}"
        )


def crear_libro(servicios):
    """Registra un libro asociado a una editorial y un género."""

    print("\n--- ALTA DE LIBRO ---")

    isbn = leer_texto("ISBN: ")
    titulo = leer_texto("Título: ")
    autor = leer_texto("Autor: ")

    print("\nEditoriales disponibles:")
    for editorial in servicios["editoriales"].listar():
        print(f"{editorial.id_editorial}. {editorial.nombre}")

    id_editorial = leer_entero("ID de la editorial: ")

    print("\nGéneros disponibles:")
    for genero in servicios["generos"].listar():
        print(f"{genero.id_genero}. {genero.nombre}")

    id_genero = leer_entero("ID del género: ")

    try:
        libro = servicios["libros"].crear(
            isbn,
            titulo,
            autor,
            id_editorial,
            id_genero,
        )
        print(f"Libro creado correctamente: {libro.titulo}")
        print(f"ID asignado: {libro.id_libro}")

    except ErrorServicio as error:
        print(f"No se pudo crear el libro: {error}")


def modificar_libro(servicios):
    """Modifica los datos de un libro existente."""

    print("\n--- MODIFICACIÓN DE LIBRO ---")
    id_libro = leer_entero("ID del libro: ")

    try:
        libro = servicios["libros"].obtener(id_libro)

        print(f"ISBN actual: {libro.isbn}")
        print(f"Título actual: {libro.titulo}")
        print(f"Autor actual: {libro.autor}")
        print(f"Editorial actual: {libro.editorial.nombre}")
        print(f"Género actual: {libro.genero.nombre}")

        print("\nDejá vacío un campo para conservar su valor.")

        isbn = input("Nuevo ISBN: ").strip() or None
        titulo = input("Nuevo título: ").strip() or None
        autor = input("Nuevo autor: ").strip() or None

        print("\nEditoriales disponibles:")
        for editorial in servicios["editoriales"].listar():
            print(f"{editorial.id_editorial}. {editorial.nombre}")

        entrada_editorial = input(
            "Nuevo ID de editorial: "
        ).strip()
        id_editorial = int(entrada_editorial) if entrada_editorial else None

        print("\nGéneros disponibles:")
        for genero in servicios["generos"].listar():
            print(f"{genero.id_genero}. {genero.nombre}")

        entrada_genero = input("Nuevo ID de género: ").strip()
        id_genero = int(entrada_genero) if entrada_genero else None

        servicios["libros"].actualizar(
            id_libro,
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            id_editorial=id_editorial,
            id_genero=id_genero,
        )

        print("Libro modificado correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar el libro: {error}")
    except ValueError:
        print("Ingresá un identificador numérico válido.")

def eliminar_libro(servicios):
    """Elimina un libro después de confirmar."""

    print("\n--- BAJA DE LIBRO ---")
    id_libro = leer_entero("ID del libro: ")

    try:
        libro = servicios["libros"].obtener(id_libro)

        print(f"Libro seleccionado: {libro.titulo}")
        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["libros"].eliminar(id_libro)
            print("Libro eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar el libro: {error}")


def listar_precios(servicios):
    """Muestra los precios registrados."""

    precios = servicios["precios"].listar()

    print("\n--- LISTADO DE PRECIOS ---")

    if not precios:
        print("No hay precios registrados.")
        return

    for precio in precios:
        print(
            f"ID: {precio.id_precio} | "
            f"Libro: {precio.libro.titulo} | "
            f"Moneda: {precio.moneda.codigo} | "
            f"Valor: {precio.valor}"
        )


def crear_precio(servicios):
    """Registra un precio para un libro y una moneda."""

    print("\n--- ALTA DE PRECIO ---")

    print("\nLibros disponibles:")
    for libro in servicios["libros"].listar():
        print(f"{libro.id_libro}. {libro.titulo}")

    id_libro = leer_entero("ID del libro: ")

    print("\nMonedas disponibles:")
    for moneda in servicios["monedas"].listar():
        print(
            f"{moneda.id_moneda}. "
            f"{moneda.codigo} - {moneda.nombre}"
        )

    id_moneda = leer_entero("ID de la moneda: ")
    valor = leer_decimal("Valor del precio: ")

    try:
        precio = servicios["precios"].crear(
            id_libro,
            id_moneda,
            valor,
        )
        print(f"Precio creado correctamente: {precio.valor}")

    except ErrorServicio as error:
        print(f"No se pudo crear el precio: {error}")


def modificar_precio(servicios):
    """Modifica el valor de un precio existente."""

    print("\n--- MODIFICACIÓN DE PRECIO ---")
    id_precio = leer_entero("ID del precio: ")

    try:
        precio = servicios["precios"].obtener(id_precio)

        print(f"Libro: {precio.libro.titulo}")
        print(f"Moneda: {precio.moneda.codigo}")
        print(f"Valor actual: {precio.valor}")

        nuevo_valor = leer_decimal("Nuevo valor: ")

        servicios["precios"].actualizar_valor(
            id_precio,
            nuevo_valor,
        )

        print("Precio modificado correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar el precio: {error}")

def eliminar_precio(servicios):
    """Elimina un precio después de confirmar."""

    print("\n--- BAJA DE PRECIO ---")
    id_precio = leer_entero("ID del precio: ")

    try:
        precio = servicios["precios"].obtener(id_precio)

        print(f"Libro: {precio.libro.titulo}")
        print(f"Moneda: {precio.moneda.codigo}")
        print(f"Valor: {precio.valor}")

        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["precios"].eliminar(id_precio)
            print("Precio eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar el precio: {error}")

def listar_stock(servicios):
    """Muestra el stock de los libros que lo tienen registrado."""

    libros = servicios["libros"].listar()

    print("\n--- LISTADO DE STOCK ---")

    encontrados = 0

    for libro in libros:
        try:
            stock = servicios["stock"].obtener_por_libro(
                libro.id_libro
            )

            print(
                f"ID libro: {libro.id_libro} | "
                f"Título: {libro.titulo} | "
                f"Cantidad: {stock.cantidad} | "
                f"Cantidad mínima: {stock.cantidad_minima}"
            )
            encontrados += 1

        except ErrorServicio:
            continue

    if encontrados == 0:
        print("No hay registros de stock.")


def crear_stock(servicios):
    """Registra el stock de un libro."""

    print("\n--- ALTA DE STOCK ---")
    print("Libros disponibles:")

    for libro in servicios["libros"].listar():
        print(f"{libro.id_libro}. {libro.titulo}")

    id_libro = leer_entero("ID del libro: ")
    cantidad = leer_entero("Cantidad actual: ")
    cantidad_minima = leer_entero("Cantidad mínima: ")

    try:
        stock = servicios["stock"].crear(
            id_libro,
            cantidad,
            cantidad_minima,
        )

        print(
            f"Stock creado correctamente: "
            f"{stock.cantidad} unidades."
        )

    except ErrorServicio as error:
        print(f"No se pudo crear el stock: {error}")


def modificar_stock(servicios):
    """Modifica las cantidades de stock de un libro."""

    print("\n--- MODIFICACIÓN DE STOCK ---")
    id_libro = leer_entero("ID del libro: ")

    try:
        stock = servicios["stock"].obtener_por_libro(id_libro)

        print(f"Cantidad actual: {stock.cantidad}")
        print(f"Cantidad mínima actual: {stock.cantidad_minima}")

        cantidad = leer_entero("Nueva cantidad actual: ")
        cantidad_minima = leer_entero("Nueva cantidad mínima: ")

        servicios["stock"].actualizar(
            id_libro,
            cantidad,
            cantidad_minima,
        )

        print("Stock modificado correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar el stock: {error}")


def eliminar_stock(servicios):
    """Elimina el stock asociado a un libro."""

    print("\n--- BAJA DE STOCK ---")
    id_libro = leer_entero("ID del libro: ")

    try:
        stock = servicios["stock"].obtener_por_libro(id_libro)

        print(f"Cantidad actual: {stock.cantidad}")
        print(f"Cantidad mínima: {stock.cantidad_minima}")

        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["stock"].eliminar(id_libro)
            print("Stock eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar el stock: {error}")

def listar_cotizaciones(servicios):
    """Muestra el historial de cotizaciones del dólar."""

    tipos = servicios["tipos_cotizacion"].listar()

    print("\n--- LISTADO DE COTIZACIONES DEL DÓLAR ---")

    encontradas = 0

    for tipo in tipos:
        cotizaciones = servicios["cotizaciones"].obtener_historico(
            tipo.id_tipo
        )

        for cotizacion in cotizaciones:
            print(
                f"Tipo: {tipo.nombre} | "
                f"Fecha: {cotizacion.fecha} | "
                f"Compra: {cotizacion.compra} | "
                f"Venta: {cotizacion.venta}"
            )
            encontradas += 1

    if encontradas == 0:
        print("No hay cotizaciones registradas.")


def crear_cotizacion(servicios):
    """Registra una cotización para un tipo y una fecha."""

    print("\n--- ALTA DE COTIZACIÓN ---")
    print("Tipos de cotización disponibles:")

    for tipo in servicios["tipos_cotizacion"].listar():
        print(f"{tipo.id_tipo}. {tipo.nombre}")

    id_tipo = leer_entero("ID del tipo de cotización: ")
    fecha = leer_fecha("Fecha (AAAA-MM-DD): ")
    compra = leer_decimal("Precio de compra: ")
    venta = leer_decimal("Precio de venta: ")

    try:
        cotizacion = servicios["cotizaciones"].registrar(
            id_tipo,
            fecha,
            compra,
            venta,
        )

        print("Cotización registrada correctamente.")
        print(f"Fecha: {cotizacion.fecha}")
        print(f"Compra: {cotizacion.compra}")
        print(f"Venta: {cotizacion.venta}")

    except ErrorServicio as error:
        print(f"No se pudo registrar la cotización: {error}")


def modificar_cotizacion(servicios):
    """Modifica los valores de una cotización existente."""

    print("\n--- MODIFICACIÓN DE COTIZACIÓN ---")

    id_tipo = leer_entero("ID del tipo de cotización: ")
    fecha = leer_fecha("Fecha de la cotización (AAAA-MM-DD): ")

    try:
        cotizacion = servicios["cotizaciones"].obtener(
            id_tipo,
            fecha,
        )

        print(f"Compra actual: {cotizacion.compra}")
        print(f"Venta actual: {cotizacion.venta}")
        print("Dejá vacío un campo para conservar su valor.")

        entrada_compra = input("Nuevo precio de compra: ").strip()
        entrada_venta = input("Nuevo precio de venta: ").strip()

        compra = (
            leer_decimal("Nuevo precio de compra: ")
            if entrada_compra
            else None
        )
        venta = (
            leer_decimal("Nuevo precio de venta: ")
            if entrada_venta
            else None
        )

        servicios["cotizaciones"].actualizar(
            id_tipo,
            fecha,
            compra=compra,
            venta=venta,
        )

        print("Cotización modificada correctamente.")

    except ErrorServicio as error:
        print(f"No se pudo modificar la cotización: {error}")


def eliminar_cotizacion(servicios):
    """Elimina una cotización después de confirmar."""

    print("\n--- BAJA DE COTIZACIÓN ---")

    id_tipo = leer_entero("ID del tipo de cotización: ")
    fecha = leer_fecha("Fecha de la cotización (AAAA-MM-DD): ")

    try:
        cotizacion = servicios["cotizaciones"].obtener(
            id_tipo,
            fecha,
        )

        print(f"Fecha: {cotizacion.fecha}")
        print(f"Compra: {cotizacion.compra}")
        print(f"Venta: {cotizacion.venta}")

        confirmacion = input(
            "¿Confirmás la eliminación? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            servicios["cotizaciones"].eliminar(id_tipo, fecha)
            print("Cotización eliminada correctamente.")
        else:
            print("Operación cancelada.")

    except ErrorServicio as error:
        print(f"No se pudo eliminar la cotización: {error}")
