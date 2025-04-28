
#%%
import pandas as pd
from pathlib import Path

#%%
class Loaders:
    def base_std_loader():
        # Carrega a base padrão para o processo de registro (sempre .xlsx)    
        # Obtém o diretório raiz da aplicação
        app_dir = Path(__file__).resolve().parent.parent.parent  # Ajustar para subir um nível adicional se necessário
        base_std_path = app_dir / 'data' / 'base_std.xlsx'  # Caminho absoluto para o arquivo base_std.xlsx dentro do diretório 'data'
        base_std = pd.read_excel(base_std_path)  # Carrega a base padrão para o processo de registro (sempre .xlsx)
        return base_std  # Retorna base_std
    
    def base_client_loader(file_path_client):
        # Verifica e tratar possíveis erros de codificação em caso de arquivos .csv 
        if file_path_client.endswith('.csv'):
            try:
                base_client = pd.read_csv(file_path_client, sep = ';', dtype='str') # Tenta abrir com codificação original (utf-8 padrão)
            except UnicodeDecodeError:
                try:
                    base_client = pd.read_csv(file_path_client, sep=';', dtype='str', encoding='latin1')  # Tenta abrir com codificação latin1
                except Exception as e:
                    print(f"Erro de encoding ao carregar o arquivo: {e}")
        else:
            base_client = pd.read_excel(file_path_client, dtype=str)
        return base_client
    
    def base_return_loader(file_path_return):
        # Carrega a base de retorno (sempre .txt)
        base_return = pd.read_csv(file_path_return, sep='\t', dtype=str)  # Usa o caminho de data_return
        return base_return  # Retorna base_client e base_return