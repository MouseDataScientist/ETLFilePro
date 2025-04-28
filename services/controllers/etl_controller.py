# %%
import importlib

def processes(base_std=None, base_client=None, base_return=None, client_name=None, process_type=None, procedure_type=None):
    client_name = client_name.lower()
    client_module = importlib.import_module(f"services.clients.{client_name}")
    client_process = getattr(client_module, process_type, None)
    method = getattr(client_process, procedure_type, None)

    if process_type == "Registry":
        result = method(base_std, base_client)
    elif process_type == "Return":
        result = method(base_client, base_return) if not client_name=="cls_documentos" else method(base_return)
    else:
        result = method(base_client)
    return result