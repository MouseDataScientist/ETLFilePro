# %%
def clients(client_id):
    
    # Dicionário de clientes com chaves como strings
    client_data = {
        "59": "EXSEN",
        "60": "CLS_DOCUMENTOS",
        "66": "REDE_BRASIL",
        "81": "SETRA_BPO"
    }
    # Retorna o nome do cliente correspondente ao identificador fornecido
    return client_data.get(client_id, "Cliente não encontrado!")