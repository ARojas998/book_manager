
"""Punto de entrada del sistema de gestión de libros."""

from .ui.console import ejecutar_menu_principal
from .preload_data.preload_data import (
    import_default_data as cargar_datos_iniciales,
)


def main(import_default_data=True):
    """Ejecuta el sistema y permite controlar la precarga de datos."""
    if import_default_data:
        cargar_datos_iniciales()

    ejecutar_menu_principal()


if __name__ == "__main__":
    main()
