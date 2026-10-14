
from datetime import date
from decimal import Decimal

from ..entities.entities import (
    Genero,
    Editorial,
    Moneda,
    TipoCotizacion,
    Libro,
    Precio,
    Stock,
    CotizacionDolar,
)
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


def import_default_data():
    """Carga los datos predeterminados sin duplicar registros."""

    repo_generos = RepositorioGenero()
    repo_editoriales = RepositorioEditorial()
    repo_monedas = RepositorioMoneda()
    repo_tipos_cotizacion = RepositorioTipoCotizacion()

    repo_libros = RepositorioLibro(
        repo_editoriales,
        repo_generos,
    )
    repo_precios = RepositorioPrecio(
        repo_libros,
        repo_monedas,
    )
    repo_stock = RepositorioStock(repo_libros)
    repo_cotizaciones = RepositorioCotizacionDolar(
        repo_tipos_cotizacion,
    )

    # Datos base: nombre -> atributos de cada entidad.
    generos = [
        "Novela",
        "Ciencia ficción",
        "Fantasía",
        "Historia",
        "Ciencia",
        "Filosofía",
        "Psicología",
        "Programación",
        "Economía",
        "Biografía",
    ]

    editoriales = [
        ("Penguin Random House", "España"),
        ("Planeta", "España"),
        ("Anagrama", "España"),
        ("Alfaguara", "España"),
        ("Salamandra", "España"),
        ("Debolsillo", "España"),
        ("Tusquets", "España"),
        ("Siglo XXI", "Argentina"),
        ("Paidós", "Argentina"),
        ("O'Reilly Media", "Estados Unidos"),
    ]

    monedas = [
        ("ARS", "Peso argentino", "$"),
        ("USD", "Dólar estadounidense", "US$"),
        ("EUR", "Euro", "€"),
        ("GBP", "Libra esterlina", "£"),
        ("JPY", "Yen japonés", "¥"),
        ("BRL", "Real brasileño", "R$"),
        ("CLP", "Peso chileno", "$"),
        ("UYU", "Peso uruguayo", "$U"),
        ("CAD", "Dólar canadiense", "C$"),
        ("CHF", "Franco suizo", "CHF"),
    ]

    tipos_cotizacion = [
        "Oficial",
        "Blue",
        "Mayorista",
        "Minorista",
        "MEP",
        "Contado con liquidación",
        "Tarjeta",
        "Ahorro",
        "Cripto",
        "Turista",
    ]

    # Cargar solo los registros que todavía no existen.
    for nombre in generos:
        if not any(g.nombre == nombre for g in repo_generos.leer_todos()):
            repo_generos.crear(Genero(nombre))

    for nombre, pais in editoriales:
        if not any(
            e.nombre == nombre
            for e in repo_editoriales.leer_todos()
        ):
            repo_editoriales.crear(Editorial(nombre, pais))

    for codigo, nombre, simbolo in monedas:
        if not any(
            m.codigo == codigo
            for m in repo_monedas.leer_todos()
        ):
            repo_monedas.crear(Moneda(codigo, nombre, simbolo))

    for nombre in tipos_cotizacion:
        if not any(
            t.nombre == nombre
            for t in repo_tipos_cotizacion.leer_todos()
        ):
            repo_tipos_cotizacion.crear(TipoCotizacion(nombre))

    # Libros de ejemplo con ISBN reales
    libros = [
        ("9780140449136", "La República", "Platón",
         "Siglo XXI", "Filosofía"),
        ("9788491050291", "1984", "George Orwell",
         "Debolsillo", "Ciencia ficción"),
        ("9788497592208", "Cien años de soledad", "Gabriel García Márquez",
         "Alfaguara", "Novela"),
        ("9788497593793", "El amor en los tiempos del cólera",
         "Gabriel García Márquez", "Debolsillo", "Novela"),
        ("9780307474728", "Crónica de una muerte anunciada",
         "Gabriel García Márquez", "Debolsillo", "Novela"),
        ("9788445071414", "El hobbit", "J. R. R. Tolkien",
         "Planeta", "Fantasía"),
        ("9788497594258", "Fahrenheit 451", "Ray Bradbury",
         "Debolsillo", "Ciencia ficción"),
        ("9788497593060", "El principito", "Antoine de Saint-Exupéry",
         "Salamandra", "Fantasía"),
        ("9788437604947", "Don Quijote de la Mancha", "Miguel de Cervantes",
         "Anagrama", "Novela"),
        ("9780262033848", "Introduction to Algorithms",
         "Thomas H. Cormen", "O'Reilly Media", "Programación"),
    ]

    editoriales_existentes = {
        editorial.nombre: editorial
        for editorial in repo_editoriales.leer_todos()
    }
    generos_existentes = {
        genero.nombre: genero
        for genero in repo_generos.leer_todos()
    }
    libros_existentes = {
        libro.isbn: libro
        for libro in repo_libros.leer_todos()
    }

    for isbn, titulo, autor, nombre_editorial, nombre_genero in libros:
        if isbn in libros_existentes:
            continue

        editorial = editoriales_existentes.get(nombre_editorial)
        genero = generos_existentes.get(nombre_genero)

        if editorial is None or genero is None:
            print(
                f"No se pudo cargar '{titulo}': "
                "editorial o género no encontrado."
            )
            continue

        libro = Libro(
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            editorial=editorial,
            genero=genero,
        )
        repo_libros.crear(libro)
        libros_existentes[isbn] = libro

        # Precios de demostración: ISBN, moneda y valor.
    precios = [
        ("9780140449136", "ARS", "18000.00"),
        ("9788491050291", "ARS", "14500.00"),
        ("9788497592208", "ARS", "22000.00"),
        ("9788497593793", "ARS", "19500.00"),
        ("9780307474728", "ARS", "16000.00"),
        ("9788445071414", "ARS", "21000.00"),
        ("9788497594258", "ARS", "17500.00"),
        ("9788497593060", "ARS", "12000.00"),
        ("9788437604947", "ARS", "25000.00"),
        ("9780262033848", "USD", "85.00"),
    ]

    monedas_existentes = {
        moneda.codigo: moneda
        for moneda in repo_monedas.leer_todos()
    }

    precios_existentes = {
        (precio.libro.isbn, precio.moneda.codigo)
        for precio in repo_precios.leer_todos()
    }

    libros_existentes = {
        libro.isbn: libro
        for libro in repo_libros.leer_todos()
    }

    for isbn, codigo_moneda, valor in precios:
        clave = (isbn, codigo_moneda)

        if clave in precios_existentes:
            continue

        libro = libros_existentes.get(isbn)
        moneda = monedas_existentes.get(codigo_moneda)

        if libro is None or moneda is None:
            print(f"No se pudo cargar el precio del libro {isbn}.")
            continue

        repo_precios.crear(
            Precio(libro, moneda, Decimal(valor))
        )
        precios_existentes.add(clave)

    # Stock de demostración: ISBN, cantidad y cantidad mínima.
    stocks = [
        ("9780140449136", 12, 3),
        ("9788491050291", 8, 2),
        ("9788497592208", 15, 4),
        ("9788497593793", 7, 2),
        ("9780307474728", 10, 3),
        ("9788445071414", 6, 2),
        ("9788497594258", 9, 3),
        ("9788497593060", 20, 5),
        ("9788437604947", 5, 2),
        ("9780262033848", 4, 1),
    ]

    for isbn, cantidad, cantidad_minima in stocks:
        libro = libros_existentes.get(isbn)

        if libro is None:
            print(f"No se pudo cargar el stock del libro {isbn}.")
            continue

        stock_existente = repo_stock.leer_por_libro(libro.id_libro)

        if stock_existente is not None:
            continue

        repo_stock.crear(
            Stock(libro, cantidad, cantidad_minima)
        )

        # Cotizaciones históricas del dólar minorista.
    # Valores de compra y venta expresados con dos decimales.
    cotizaciones = [
        ("30-09-2026", "1486.11", "1539.87"),
        ("29-09-2026", "1492.37", "1543.93"),
        ("28-09-2026", "1495.19", "1550.12"),
        ("25-09-2026", "1493.40", "1545.12"),
        ("24-09-2026", "1486.50", "1538.39"),
        ("23-09-2026", "1483.12", "1536.17"),
        ("22-09-2026", "1482.03", "1533.83"),
        ("21-09-2026", "1482.51", "1534.22"),
        ("18-09-2026", "1482.29", "1534.00"),
        ("17-09-2026", "1480.41", "1531.98"),
    ]

    # Usamos el tipo Minorista para estas cotizaciones.
    tipo_minorista = next(
        (
            tipo
            for tipo in repo_tipos_cotizacion.leer_todos()
            if tipo.nombre == "Minorista"
        ),
        None,
    )

    if tipo_minorista is None:
        print("No se encontró el tipo de cotización Minorista.")
    else:
        for fecha_texto, compra, venta in cotizaciones:
            fecha = date.fromisoformat(
                "-".join(reversed(fecha_texto.split("-")))
            )

            cotizacion_existente = repo_cotizaciones.leer_por_tipo_y_fecha(
                tipo_minorista.id_tipo,
                fecha,
            )

            if cotizacion_existente is not None:
                continue

            repo_cotizaciones.crear(
                CotizacionDolar(
                    tipo_minorista,
                    fecha,
                    Decimal(compra),
                    Decimal(venta),
                )
            )

    print(
        "Datos base, libros, precios, stock y cotizaciones cargados correctamente."
    )