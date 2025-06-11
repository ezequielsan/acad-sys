import logging
import os

# Cria diretório de logs se não existir
def ensure_log_dir():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs')
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

log_dir = ensure_log_dir()

LOG_FILE = os.path.join(log_dir, 'api.log')

# Configuração explícita do logger nomeado
logger = logging.getLogger('acad_sys_api')
logger.setLevel(logging.INFO)

# Evita adicionar múltiplos handlers em reloads
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
