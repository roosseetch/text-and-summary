import subprocess
import sys

from alembic.config import Config
from alembic import command

from app.main import ROOT


alembic_cfg = Config(ROOT / "alembic.ini")

subprocess.run([sys.executable, "./start_db_session.py"])
command.upgrade(alembic_cfg, "head")
