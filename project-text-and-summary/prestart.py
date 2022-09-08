import subprocess
import sys

from alembic.config import Config
from alembic import command

from app.core.config import settings


alembic_cfg = Config(settings.ROOT / "alembic.ini")

subprocess.run([sys.executable, "./start_db_session.py"])
command.upgrade(alembic_cfg, "head")
