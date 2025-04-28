# %%
from pathlib import Path
from datetime import datetime

#%%
def date_directories():
    # Informações da data atual
    today = datetime.now()
    # Mapeamento de meses
    MONTH_NAMES = {
    '01': '01-Janeiro', '02': '02-Fevereiro', '03': '03-Março', '04': '04-Abril',
    '05': '05-Maio', '06': '06-Junho', '07': '07-Julho', '08': '08-Agosto',
    '09': '09-Setembro', '10': '10-Outubro', '11': '11-Novembro', '12': '12-Dezembro'
    }
    mont_name = MONTH_NAMES[f"{today.month:02d}"]
    day_str = f"{today.day:02d}"
    date_dir = Path(mont_name) / day_str
    return date_dir 
   
def home_directories(process_type, procedure_type):
    if (process_type=="Registry" or process_type=="Return") and procedure_type=="leopoldina":
        home_dir = Path.home() / 'Onedrive - Grafica PrintPost' / 'REGISTRO EM CARTÓRIO'
    elif process_type=="Separations" and (procedure_type=="carta_simples" or procedure_type=="email"):
        home_dir = Path.home() / 'Onedrive - Grafica PrintPost' / 'DISPAROS'
    return home_dir

def client_directories(client_id, client_name):
    client_dir = f"{client_id}-{client_name}"
    return client_dir

def processes_directories(process_type, procedure_type):
    if process_type=="Registry":
        return 'TABULACAO'
    elif process_type=="Return":
        return 'ARQUIVO PLATAFORMA', 'RETORNO' 
                
    else:
        if  procedure_type=="carta_simples":
            return 'CARTA SIMPLES'
        elif procedure_type=="carta_registrada":
            return 'CARTA REGISTRADA'
        elif procedure_type=="email":
            return 'EMAIL'
        elif procedure_type=="leopoldina":
            return "LEOPOLDINA"
        else:
            return "CAMECSP"
        
def file_name(file_path):
    path = Path(file_path)
    file_name = path.stem
    file_extension = path.suffix
    return file_name, file_extension
    
class SaveFile:
    def __init__(self, file_path, client_id, client_name, process_type, procedure_type, etl_file, dataframes, return_file=None):
        self.file_path=file_path
        self.client_id=client_id
        self.client_name=client_name
        self.process_type=process_type
        self.procedure_type=procedure_type
        self.etl_file=etl_file
        self.dataframes=dataframes
        self.return_file=return_file

    def save_processes(self):
        home_dir = home_directories(self.process_type, self.procedure_type)
        client_dir = client_directories(self.client_id, self.client_name) 
        process_dir = processes_directories(self.process_type, self.procedure_type)
        date_dir = date_directories()
        name, extension = file_name(self.file_path)

        # Cria os diretórios
        if isinstance(process_dir, tuple):
            client_file_dir = home_dir / client_dir / process_dir[0] / date_dir
            client_file_dir.mkdir(parents=True, exist_ok=True)
            return_file_dir = home_dir / client_dir / process_dir[1] / date_dir
            return_file_dir.mkdir(parents=True, exist_ok=True)
        else:
            client_file_dir = home_dir / client_dir / process_dir / date_dir
            client_file_dir.mkdir(parents=True, exist_ok=True)

        if self.process_type == "Return":
            if self.client_name == "CLS_DOCUMENTOS":
                full_client_file_dir = client_file_dir / f"{name}.xlsx"
                self.etl_file.to_excel(full_client_file_dir, index=False)
                full_return_file_dir = return_file_dir / f"{name}.txt"
                self.return_file.to_csv(full_return_file_dir, sep='\t', index=False)
            else:
                if extension.lower() == ".csv":
                    full_client_file_dir = client_file_dir / f"{name}.csv"
                    self.etl_file.to_csv(full_client_file_dir, sep=";", index=False)
                elif extension.lower() in [".xlsx", ".txt"]:
                    full_client_file_dir = client_file_dir / f"{name}.xlsx"
                    self.etl_file.to_excel(full_client_file_dir, index=False)
                full_return_file_dir = return_file_dir / f"{name}.txt"
                self.return_file.to_csv(full_return_file_dir, sep='\t', index=False)

        elif self.process_type == "Registry":
            full_client_file_dir = client_file_dir / f"{name}.txt"
            self.etl_file.to_csv(full_client_file_dir, sep='\t', index=False)
        else:
            if self.procedure_type == "email":
                for item in self.dataframes:
                    client = item["CLIENTE"]
                    sub_client = item["SUB CLIENTE"]
                    df = item["DATAFRAME"]
                    full_client_file_dir = client_file_dir / f"{client}{sub_client}.xlsx"
                    df.to_excel(full_client_file_dir, index=False)
            else:
                for item in self.dataframes:
                    client = item["CLIENTE"]
                    df = item["DATAFRAME"]
                    full_client_file_dir = client_file_dir / f"{client}.xlsx"
                    df.to_excel(full_client_file_dir, index=False)
        return full_client_file_dir