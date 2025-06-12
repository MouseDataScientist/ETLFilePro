# %%
# PROCESSO DE REGISTRO
class Registry:
    @classmethod
    def leopoldina(cls, base_std, base_client):
         
        base_std = base_std.reindex(base_client.index) # Deixa a base_std com o mesmo tamanho da base_client

        for col in base_client.select_dtypes(include=["float64"]).columns:
            base_client[col] = base_client[col].astype("string")

        # Filtrar na base do cliente o NOME do CLIENTE ou DEVEDOR independente da posição da string e maiúsculas ou minúsculas
        base_name = base_client.filter(
            regex=(
            r'(?i)^NOME[\s_.\\/-]?$|'  # Apenas "NOME" com ou sem caracteres especiais
            r'(^NOME[\s_.\\/-]*(CLIENTE(S)?|DEV(EDOR)?(ES)?)$)|'  # "NOME" seguido de "CLIENTE" ou "DEVEDOR"
            r'(^CLIENTE(S)?[\s_.\\/-]*NOME$)|'  # "CLIENTE" seguido de "NOME"
            r'(^DEV(EDOR)?(ES)?[\s_.\\/-]*NOME$)|'  # "DEVEDOR" seguido de "NOME"
            r'(^CLIENTE(S)?$)|'  # Apenas "CLIENTE"
            r'(^DEV(EDOR)?(ES)?$)'  # Apenas "DEVEDOR"
            ),
            axis=1
        )   
        if not base_name.empty:
            nome_devedor = base_name.columns[0]
            base_std['DESTINATARIO'] = base_client[nome_devedor].values
        else:
            raise ValueError('Nenhuma coluna NOME_CLIENTE encontrada em base_client')
        
        # Filtrar na base do cliente o CPF do DEVEDOR independente da posição da string
        base_cpf = base_client.filter(regex=r'(?i)CPF([\s_.\\/-]?)', axis=1)
        if not base_cpf.empty:
            cpf = base_cpf.columns[0]
            base_std['CPF_CNPJ_DESTINATARIO'] = base_client[cpf].values
            base_std['ID'] = base_client[cpf].values
        else:
            raise ValueError('Nenhuma coluna CPF encontrada em base_client')
        
        # Filtrar na base do cliente o NOME da ASSESSORIA ou CREDOR, independente da posição da string e maiúsculas ou minúsculas
        base_credor = base_client.filter(
            regex=(
            r'(?i)'  # Ignorar maiúsculas/minúsculas
            r'(^NOME[\s_.\\/-]*(?:ASSESSORIA(A)?(S)?|CREDOR(ES)?)$)|'  # "NOME" seguido de "ASSESSORIA" ou "CREDOR"
            r'(^ASSESSORIA(A)?(S)?[\s_.\\/-]*NOME$)|'  # "ASSESSORIA" seguido de "NOME"
            r'(^CREDOR(ES)?[\s_.\\/-]*NOME$)|'  # "CREDOR" seguido de "NOME"
            r'(^ASSESSORIA(A)?(S)?$)|'  # Apenas "ASSESSORIA"
            r'(^CREDOR(ES)?$)'  # Apenas "CREDOR"
            ),
            axis=1
        )

        # Caso a condição acima não seja atendida, filtrar o NOME do ESCRITÓRIO ou RAZÃO SOCIAL
        if base_credor.columns.empty:
            base_credor = base_client.filter(
                regex=(
                r'(?i)'  # Ignorar maiúsculas/minúsculas
                r'(^NOME[\s_.\\/-]*(?:ESCRIT(Ó|O)RIO|RAZ(Ã|A)O[\s_.\\/-]*SOCIAL)$)|'  # "NOME" seguido de "ESCRITÓRIO" ou "RAZÃO SOCIAL"
                r'(^ESCRIT(Ó|O)RIO[\s_.\\/-]*NOME$)|'  # "ESCRITÓRIO" seguido de "NOME"
                r'(^RAZ(Ã|A)O[\s_.\\/-]*SOCIAL[\s_.\\/-]*NOME$)|'  # "RAZÃO SOCIAL" seguido de "NOME"
                r'(^ESCRIT(Ó|O)RIO$)|'  # Apenas "ESCRITÓRIO"
                r'(^RAZ(Ã|A)O[\s_.\\/-]*SOCIAL$)'  # Apenas "RAZÃO SOCIAL"
                ),
                axis=1
            )
            if base_credor.columns.empty:
                raise ValueError('Nenhuma coluna NOME_ESCRITÓRIO encontrada em base_client')
            else:
                nome_escritorio = base_credor.columns[0]
                base_std['NOME_REMETENTE'] = base_client[nome_escritorio].values       
        else:
            nome_escritorio = base_credor.columns[0]
            base_std['NOME_REMETENTE'] = base_client[nome_escritorio].values

        # Filtrar na base do cliente o CNPJ do ESCRITÓRIO, ASSESSORIA ou CREDOR, independente da posição da string
        base_cnpj = base_client.filter(
            regex=(
                r'(?i)'  # Ignorar maiúsculas/minúsculas
                r'(?:^CNPJ$|'  # Apenas "CNPJ"
                r'^CNPJ[\s_.\\/-]*(?:ASSESSORIA(S)?|ESCRIT[ÓO]RIO)$|'  # "CNPJ" seguido de "ASSESSORIA(S)" ou "ESCRITÓRIO"
                r'^(?:ASSESSORIA(S)?|ESCRIT[ÓO]RIO)[\s_.\\/-]*CNPJ$)'  # "ASSESSORIA(S)" ou "ESCRITÓRIO" seguido de "CNPJ"
            ),
            axis=1
        )
        if not base_cnpj.empty:
            cnpj = base_cnpj.columns[0]
            base_std['CNPJ_REMETENTE'] = base_client[cnpj].values

       # Remove caracteres não numéricos
        base_std['CPF_CNPJ_DESTINATARIO'] = base_std['CPF_CNPJ_DESTINATARIO'].str.replace(r'\D', '', regex=True)

        # Converte nulos para string vazia
        base_std['CPF_CNPJ_DESTINATARIO'] = base_std['CPF_CNPJ_DESTINATARIO'].fillna("")

        # Remove linhas onde CPF está vazio
        base_std = base_std[base_std['CPF_CNPJ_DESTINATARIO'] != ""]

        # Preenche 'APRESENTANTE' com o valor da primeira linha
        base_std['APRESENTANTE'] = base_std['APRESENTANTE'].ffill()

        registers = base_std.shape[0] # Pega o número de registros (linhas) do arquivo

        return base_std, registers

# PROCESSO DE RETORNO
class Return:
    @classmethod
    def leopoldina(cls, base_client, base_return):
        base_client.dropna(how='all', inplace=True) # Drop de linhas vazias

        # Mapeamento entre colunas de base_return e base_client
        mapeamento = {
            'DATA_PROTOCOLO': 'dt_protocolo',
            'PROTOCOLO': 'nro_protocolo',
            'DATA_REGISTRO': 'dt_registro',
            'NUMERO_REGISTRO': 'nro_registro',
            'SELO': 'nro_selo'
        }
        # Verificar se todas as chaves de mapeamento NÃO estão em base_client
        if not any(key in base_client for key in mapeamento.keys()):
            for baseclient, basereturn in mapeamento.items():
                base_client.loc[:, baseclient] = base_return[basereturn].values
        else:
            # Verifica se a coluna 'DATA_REGISTRO.1' existe em base_client
            if 'DATA_REGISTRO.1' not in base_client.columns:
                if 'DATA_PROTOCOLO' not in base_client.columns:
                    # Levanta um erro caso 'CODIGO' também não exista em base_client
                    raise ValueError("DATA REGISTRO não encontrada em na base do cliente.")
            else:
                base_client.rename(columns={'DATA_REGISTRO.1': 'DATA_PROTOCOLO'}, inplace=True)
            # Verifica se a coluna 'PROTOCOLO' existe em base_client
            if 'PROTOCOLO' not in base_client.columns:
                # Se 'PROTOCOLO' não existir, busca pela coluna 'CODIGO' em base_client
                if 'CODIGO' in base_client.columns:
                    # Substitui 'PROTOCOLO' por 'CODIGO' no mapeamento
                    mapeamento['CODIGO'] = mapeamento.pop('PROTOCOLO')
                else:
                    # Levanta um erro caso 'CODIGO' também não exista em base_client
                    raise ValueError("Nem 'PROTOCOLO' nem 'CODIGO' foram encontrados na base do cliente.")
                
            for baseclient, basereturn in mapeamento.items():
                base_client.loc[:, baseclient] = base_return[basereturn].values

        registers = base_client.shape[0]
        
        return base_client, registers