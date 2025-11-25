import logging
import os

LOG_Nome_Arquivo = 'controle_financeiro.log'
LOG_Nivel = logging.INFO

def setup_logging():
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=LOG_Nivel,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            filename=LOG_Nome_Arquivo,
            filemode='a'
        )

def get_logger(name):
    return logging.getLogger(name)

setup_logging()