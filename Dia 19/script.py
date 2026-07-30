import logging
from logging.handlers import RotatingFileHandler

# Configuración con codificación explícita y límite de tamaño (5MB max, guarda 3 respaldos)
file_handler = RotatingFileHandler(
    "pipeline.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[file_handler, console_handler],
)