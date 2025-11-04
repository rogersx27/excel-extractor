"""Punto de entrada principal de la aplicación."""
import logging

from config import DEBUG, LOG_LEVEL, LOGS_DIR

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Función principal."""
    logger.info("Iniciando aplicación...")
    logger.debug(f"Modo debug: {DEBUG}")

    # Tu código aquí
    print("Hola desde el proyecto Python!")

    logger.info("Aplicación finalizada.")


if __name__ == "__main__":
    main()
