from tkinter import DISABLED, NORMAL, END
import os

class Logger:
    def __init__(self, log_area, client_id, client_name, process_type, procedure_type, registers):
        self.log_area = log_area
        self.client_id = client_id
        self.client_name = client_name
        self.process_type = process_type
        self.procedure_type = procedure_type
        self.registers = registers
        self.log_message = None
        self.log_messages = []

    def configure_log_area(self):
        """Configura a área de log."""
        self.log_area.config(state=NORMAL)
        self.log_area.tag_configure('label', foreground='black', font=('Arial', 10, 'bold'))
        self.log_area.tag_configure('value', foreground='blue', font=('Arial', 10, 'bold'))

    def add_log_message(self, label, value):
        """Adiciona uma mensagem ao log."""
        self.log_messages.append((label, value))

    def display_log(self):
        """Exibe as mensagens armazenadas no log."""
        self.configure_log_area()
        self.log_area.delete('1.0', END)  # Limpa o log anterior

        for label, value in self.log_messages:
            self.log_area.insert(END, label, 'label')
            self.log_area.insert(END, f"{value}\n\n", 'value')

        self.log_area.config(state=DISABLED)
        self.log_area.yview(END)

    def log_error(self, message):
        """Registra uma mensagem de erro no log."""
        self.add_log_message("Erro: ", message)
        self.display_log()

    def processes_log(self):
        """Registra as informações de processamento no log."""
        self.log_messages = [
            ("Cliente ID: ", self.client_id),
            ("Cliente Nome: ", self.client_name),
            ("Registros: ", self.registers)
        ]
        self.display_log()

    def save_log(self, full_path):
        """Adiciona informações de salvamento ao log e exibe."""
        self.add_log_message("Salvo em: ", full_path)
        self.display_log()

        # Adiciona o link ABRIR DIRETÓRIO
        self.log_area.config(state=NORMAL)
        self.log_area.insert(END, "ABRIR DIRETÓRIO", "link")
        self.log_area.tag_configure("link", foreground="red", font=('Arial', 12, 'bold'), underline=True)
        self.log_area.tag_bind("link", "<Button-1>", lambda event: os.startfile(os.path.dirname(full_path)))
        self.log_area.config(state=DISABLED)