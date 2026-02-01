import sys
from pathlib import Path

# Adicionar diretórios ao Python path
root_dir = Path(__file__).parent.parent
api_dir = Path(__file__).parent

sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(api_dir))

# Agora importar a app
from src.api.main import app

# Handler para Vercel
handler = app