# %%
import pandas as pd
import numpy as np

#%%
class Registry:
    @classmethod
    def leopoldina(cls, base_std, base_client):
        # Cria um Dataframe com dados filtrados para registro cartorário
        df_semprivativo = base_client[(base_client["PRIVATIVO"] == "") | (base_client["PRIVATIVO"].isna())]
        df_registrada = df_semprivativo[df_semprivativo["TIPO POSTAGEM"] == "CARTA REGISTRADA COM AR"].copy()
        df_registrada['DEST. CPF/CNPF'] = df_registrada['DEST. CPF/CNPF'].apply(
            lambda x: f"{int(float(x))}" if pd.notnull(x) else None
        )

        # Deixa a base_std com o mesmo tamanho da base_client
        base_std = base_std.reindex(df_registrada.index)
      
        # Preenche dados da base_std com os dados do Dataframe filtrado
        base_std['ID'] = df_registrada["ID OBJETO"].values
        base_std['APRESENTANTE'] = "DOC DOC EXPRESS SERVICO DE IMPRESSAO EIRELI - ME"
        base_std['NOME_REMETENTE'] = "Cls Organizacao e Administracao de Documentos LTDA"
        base_std['CNPJ_REMETENTE'] = "15556308000195"
        base_std['DESTINATARIO'] = df_registrada["DESTINATARIO"].values
        base_std['CPF_CNPJ_DESTINATARIO'] = df_registrada["DEST. CPF/CNPF"].values

        registers = base_std.shape[0] # Recebe a quantidade de linhas da base_std preenchida

        return base_std, str(registers)
    
class Return:
    @classmethod
    def leopoldina(cls, base_return):
        # Mapeamento entre colunas de base_return e base_client
        mapeamento = {
            'id': 'ID',
            'nro_registro': 'PROTOCOLO',
            'nro_selo': 'SELO'
        }

        base_return = base_return[mapeamento.keys()].rename(columns=mapeamento)
        registers = base_return.shape[0]
        
        return base_return, str(registers)
#%%
class Separations:
    @classmethod
    def _process_cartas(cls, base_client, tipo_postagem):
        # Lista para armazenar os dataframes por cliente
        dataframes = []
        # Lista para consolidar a contagem de cartas por cliente e tipo de postagem
        consolidated_data = []
        # Filtragem: privativos em branco ou NaN
        df_sem_privativo = base_client[(base_client["PRIVATIVO"] == "") | (base_client["PRIVATIVO"].isna())]
        # Filtragem: tipo de postagem
        df_filtrado = df_sem_privativo[df_sem_privativo["TIPO POSTAGEM"] == tipo_postagem]
        # Itera pelos clientes únicos
        for cliente in df_filtrado['CLIENTE'].unique():
            df_cliente = df_filtrado[df_filtrado['CLIENTE'] == cliente]
            # Contar o número de cartas correspondentes
            carta_count = len(df_cliente)
            # Adicionar os dados consolidados
            consolidated_data.append({
                "CLIENTE": cliente,
                "CARTAS": carta_count
            })
            # Adiciona o dataframe com o nome do cliente
            dataframes.append({
                "CLIENTE": cliente,
                "DATAFRAME": df_cliente
            })
        # Criar um DataFrame consolidado
        df_consolidado = pd.DataFrame(consolidated_data)
        quantities = f"Clientes: {len(df_consolidado['CLIENTE'].unique())}"
        return df_consolidado, dataframes, quantities

    @classmethod
    def carta_simples(cls, base_client):
        return cls._process_cartas(base_client, "CARTA SIMPLES COM AR")

    @classmethod
    def carta_registrada(cls, base_client):
        return cls._process_cartas(base_client, "CARTA REGISTRADA COM AR")
    
    @classmethod
    def email(cls, base_client):
        # Lista para armazenar os dataframes por cliente e subcliente
        dataframes = []
        # Lista para consolidar a contagem de emails por cliente e subcliente
        consolidated_data = []
        # Filtragem: privativos em branco ou NaN
        df_sem_privativo = base_client[(base_client["PRIVATIVO"] == "") | (base_client["PRIVATIVO"].isna())]
        # Filtragem: tipo de postagem "EMAIL"
        df_email = df_sem_privativo[df_sem_privativo["TIPO POSTAGEM"] == "EMAIL"].copy()
        # Ajustar a coluna "DEST. CPF/CNPF"
        df_email['DEST. CPF/CNPF'] = df_email['DEST. CPF/CNPF'].apply(
            lambda x: f"{int(float(x))}" if pd.notnull(x) else None
        )
        # Iterar por cliente e subcliente
        for cliente in df_email["CLIENTE"].unique():
            df_cliente = df_email[df_email["CLIENTE"] == cliente]
            for subcliente in df_cliente["SUB CLIENTE"].unique():
                df_subcliente = df_cliente[df_cliente["SUB CLIENTE"] == subcliente]
                # Contar o número de emails correspondentes
                email_count = len(df_subcliente)
                # Adicionar os dados consolidados
                consolidated_data.append({
                    "CLIENTE": cliente,
                    "SUB CLIENTE": subcliente,
                    "QUANTIDADE EMAILS": email_count
                })
                # Adicionar o dataframe individual à lista
                dataframes.append({
                    "CLIENTE": cliente,
                    "SUB CLIENTE": subcliente,
                    "DATAFRAME": df_subcliente
                })
        # Criar um DataFrame consolidado
        df_consolidado = pd.DataFrame(consolidated_data)
        # Quantidade de clientes e sub clientes
        quantities = f"Clientes: {len(df_consolidado['CLIENTE'].unique())} | Sub-Clientes: {len(df_consolidado['SUB CLIENTE'])}"
        # Retornar o DataFrame consolidado e a lista de DataFrames
        return df_consolidado, dataframes, quantities