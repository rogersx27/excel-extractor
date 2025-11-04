"""Script rápido para probar que los logs ya no se duplican."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from logger import setup_logger

# Crear varios loggers
logger1 = setup_logger("test1")
logger2 = setup_logger("test2")
logger3 = setup_logger("test1")  # Mismo nombre que logger1

# Probar logging
logger1.info("Mensaje 1 desde logger1")
logger2.info("Mensaje 2 desde logger2")
logger3.info("Mensaje 3 desde logger3 (mismo nombre que logger1)")

print("\n✅ Si cada mensaje aparece UNA SOLA VEZ, el fix funcionó correctamente")
print("❌ Si los mensajes se duplican, todavía hay problema")
