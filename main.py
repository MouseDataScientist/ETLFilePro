import sys
import os

# Adiciona o diretório pai (project_directory) ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui')))

from ui.interface import run_interface

if __name__ == "__main__":
    run_interface()