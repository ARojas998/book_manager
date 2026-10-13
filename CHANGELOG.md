# Changelog

## [Ejercicio 03]
- Implementación de interfaces de repositorios genéricos, de stock y de cotizaciones del dólar.
- Implementación de repositorios CSV con operaciones CRUD.
- Persistencia de géneros, editoriales, monedas, tipos de cotización, libros y precios.
- Implementación de repositorios específicos para stock y cotizaciones históricas del dólar.
- Gestión de relaciones entre libros, editoriales, géneros, precios y monedas mediante identificadores.
- Validación funcional de operaciones CRUD y de la recuperación de entidades relacionadas.
- Corrección de la búsqueda de stock para utilizar `libro_id`, respetando la interfaz provista por la cátedra.

## [Ejercicio 02]

- Implementación de las ocho clases entidad: `Libro`, `Genero`, `Editorial`, `Moneda`, `TipoCotizacion`, `Precio`, `Stock` y `CotizacionDolar`.
- Aplicación de encapsulación mediante atributos privados y propiedades.
- Incorporación de validaciones para tipos de datos, campos obligatorios, identificadores, cantidades y valores monetarios.
- Representación de importes mediante `Decimal` para evitar los problemas de precisión de `float`.
- Verificación de la creación de objetos, las relaciones entre entidades y el rechazo de datos inválidos.

## [Ejercicio 01]

- Inicialización del repositorio Git para el proyecto Book Manager.
- Creación de la rama `Sprint_1`.
- Creación de la estructura de directorios y archivos del proyecto.
- Incorporación del README inicial con el objetivo y el contexto del Sprint 1.