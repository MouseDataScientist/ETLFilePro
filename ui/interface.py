from tkinter import Tk, ttk, Frame, LabelFrame, Radiobutton, StringVar, Button, Text, filedialog, PhotoImage
from tkinter import DISABLED, NORMAL
from pandastable import Table
from email_module import create_email_tab
from models.clients import clients
from services.controllers.etl_controller import processes
from services.loaders.file_loaders import Loaders
from utils.save_file import SaveFile
from utils.logger import Logger
import sys, os, traceback

def run_interface():
    class App:
        def __init__(self):
            self.window = Tk()  # Inicializa a janela Tkinter
            self.screen()
            self.create_notebook()  # Cria as guias
            self.screen_frames()
            self.widgets_frame_1()
            self.widgets_frame_3()
            self.window.mainloop()
            
        #CONFIG JANELA
        def screen(self):
            self.window.title("Print Post Processos")
            self.window.configure(background="#57a5d2")
            self.window.resizable(True, True)

            # Definir tamanho da janela
            largura = 1200
            altura = 600

            # Pegar a resolução máxima do monitor
            screen_width = self.window.winfo_screenwidth()  # Obtém a largura da tela
            screen_height = self.window.winfo_screenheight()  # Obtém a altura da tela

            # Calcular posição x e y para centralizar a janela
            x = (screen_width - largura) // 2
            y = (screen_height - altura) // 2

            # Definir a geometria da janela (tamanho + posição centralizada)
            self.window.geometry(f"{largura}x{altura}+{x}+{y}")

            # Definir o tamanho máximo e mínimo da janela
            self.window.maxsize(screen_width, screen_height)
            self.window.minsize(width=1200, height=600)

            # Detectar caminho do ícone mesmo em .exe com PyInstaller
            if hasattr(sys, '_MEIPASS'):
                icon_path = os.path.join(sys._MEIPASS, 'assets', 'icons', 'icon.png')
            else:
                icon_path = os.path.join('assets', 'icons', 'icon.png')

            # Usar imagem como ícone
            icon_img = PhotoImage(file=icon_path)
            self.window.iconphoto(False, icon_img)
            self.window.icon_img = icon_img  # Evita que o garbage collector delete a imagem

        # GUIAS (Notebook)
        def create_notebook(self):
            self.notebook = ttk.Notebook(self.window)  # Cria o Notebook
            self.notebook.place(relwidth=1, relheight=1)  # Preenche a janela principal
            
            self.registry_tab = Frame(self.notebook, bg="#57a5d2") # Cria os frames das abas
            self.email_tab = Frame(self.notebook, bg="#57a5d2")  # Guia para o E-mail

            # Adiciona as abas ao Notebook
            self.notebook.add(self.registry_tab, text="Processo")
            self.notebook.add(self.email_tab, text="E-mail")

            # Adiciona widgets à aba de e-mail usando a função importada
            create_email_tab(self.email_tab)

        # PAINÉIS
        def screen_frames(self):
            # Painel 1
            self.frame_1 = Frame(self.registry_tab, bd=4, bg="#70ebca", 
                                highlightbackground="black", highlightthickness=2)
            self.frame_1.place(relx=0.006, rely=0.01, relwidth=0.340, relheight=0.42)

            # Painel 2
            self.frame_2 = Frame(self.registry_tab, bd=4, bg="#d5eaf4", 
                                highlightbackground="black", highlightthickness=2)
            self.frame_2.place(relx=0.35, rely=0.01, relwidth=0.645, relheight=0.5)

            # Painel 3
            self.frame_3 = Frame(self.registry_tab, bd=4, bg="#8ec6e4", 
                                highlightbackground="black", highlightthickness=2)
            self.frame_3.place(relx=0.006, rely=0.435, relwidth=0.340, relheight=0.559)

            # Painel 4
            self.frame_4 = Frame(self.registry_tab, bd=4, bg="#d5eaf4", 
                                highlightbackground="black", highlightthickness=2)
            self.frame_4.place(relx=0.35, rely=0.516, relwidth=0.645, relheight=0.478)

        # WIDGETS PAINEL 1
        def widgets_frame_1(self):
            # Radio Frame Clientes
            self.client_id = StringVar(value=" ") 

            self.radio_frame_client = LabelFrame(self.frame_1,
                                        text="Clientes",
                                        bg=self.frame_1['bg'], 
                                        fg="darkblue", 
                                        font=("Arial", 12, "bold"))
            self.radio_frame_client.place(relx=0.015, rely=0.015, width=110, height=128)

            self.radio_exsen = Radiobutton(self.radio_frame_client, variable=self.client_id, value='59', command=self.check_submit_state,
                                        text="Exsen",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))           
            self.radio_exsen.pack(anchor='w')

            self.radio_rede_brasil = Radiobutton(self.radio_frame_client, variable=self.client_id, value='66', command=self.check_submit_state,
                                        text="Rede Brasil",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))  
            self.radio_rede_brasil.pack(anchor='w')

            self.radio_setra_bpo = Radiobutton(self.radio_frame_client, variable=self.client_id, value='81', command=self.check_submit_state,
                                        text="Setra",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))  
            self.radio_setra_bpo.pack(anchor='w') 

            self.radio_cls = Radiobutton(self.radio_frame_client, variable=self.client_id, value='60', command=self.check_submit_state,
                                        text="CLS",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_cls.pack(anchor='w')

            # RADIO PROCESSOS
            self.process_type = StringVar(value=" ")

            self.radio_frame_process = LabelFrame(self.frame_1, 
                                        text="Processo",
                                        bg=self.frame_1['bg'], 
                                        fg="darkblue", 
                                        font=("Arial", 12, "bold"))
            self.radio_frame_process.place(relx=0.35, rely=0.015, width=110, height=128)

            self.radio_registry = Radiobutton(self.radio_frame_process, variable=self.process_type, value='Registry', command=self.check_submit_state,
                                        text="Registro",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_registry.pack(anchor='w')

            self.radio_return = Radiobutton(self.radio_frame_process, variable=self.process_type, value='Return', command=self.check_submit_state,
                                        text="Retorno",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_return.pack(anchor='w')

            self.radio_sep = Radiobutton(self.radio_frame_process, state=DISABLED, variable=self.process_type, value='Separations', command=self.check_submit_state,
                                        text="Separação",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_sep.pack(anchor='w')

            # RADIO PROCEDIMENTO
            self.procedure_type = StringVar(value=" ")

            self.radio_frame_procedure = LabelFrame(self.frame_1,
                                        text="Procedimento",
                                        bg=self.frame_1['bg'], 
                                        fg="darkblue", 
                                        font=("Arial", 12, "bold"))
            self.radio_frame_procedure.place(relx=0.68, rely=0.015, width=120, height=128)

            self.radio_leopoldina = Radiobutton(self.radio_frame_procedure, variable=self.procedure_type, value='leopoldina', command=self.check_submit_state,
                                        text="Leopoldina",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_leopoldina.pack(anchor='w')

            self.radio_carta_simples = Radiobutton(self.radio_frame_procedure, state=DISABLED, variable=self.procedure_type, value='carta_simples', command=self.check_submit_state,
                                        text="C. Simples",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_carta_simples.pack(anchor='w')

            self.radio_email = Radiobutton(self.radio_frame_procedure, state=DISABLED, variable=self.procedure_type, value='email', command=self.check_submit_state,
                                        text="E-mail",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_email.pack(anchor='w')

            self.radio_carta_registrada = Radiobutton(self.radio_frame_procedure, state=DISABLED, variable=self.procedure_type, value='carta_registrada', command=self.check_submit_state,
                                        text="C. Registrada",
                                        bg=self.frame_1['bg'], 
                                        font=("Arial", 10, "bold"))
            self.radio_carta_registrada.pack(anchor='w')

            # BOTÕES
            self.file_selected_client = False
            self.file_selected_return = False
            self.send_email = False

            self.file_client_btn = Button(self.frame_1, command=self.select_base_client,
                                        text="Base Cliente",
                                        bg=self.frame_1['bg'],
                                        fg="darkblue", 
                                        font=("Arial", 11, "bold"),
                                        borderwidth=5, 
                                        highlightthickness=0)
            self.file_client_btn.place(relx=0.015, rely=0.60, width=110, height=40)

            self.file_return_btn = Button(self.frame_1, state=DISABLED, command=self.select_base_return,
                                        text="Base Retorno",
                                        bg=self.frame_1['bg'],
                                        fg="darkblue", 
                                        font=("Arial", 11, "bold"),
                                        borderwidth=5, 
                                        highlightthickness=0)
            self.file_return_btn.place(relx=0.35, rely=0.60, width=110, height=40)

            self.send_email_btn = Button(self.frame_1, state=DISABLED, command=self.email_send,
                                        text="Enviar E-mail",
                                        bg=self.frame_1['bg'],
                                        fg="darkblue", 
                                        font=("Arial", 11, "bold"),
                                        borderwidth=5, 
                                        highlightthickness=0)
            self.send_email_btn.place(relx=0.70, rely=0.60, width=110, height=40)

            self.submit_btn = Button(self.frame_1, state=DISABLED, command=self.submit,
                                        text="Processar",
                                        bg=self.frame_1['bg'],
                                        fg="darkblue", 
                                        font=("Arial", 11, "bold"),
                                        borderwidth=5, 
                                        highlightthickness=0)
            self.submit_btn.place(relx=0.015, rely=0.82, width=110, height=40)

            self.new_btn = Button(self.frame_1, state=DISABLED, command=self.reset,
                                        text="Novo",
                                        bg=self.frame_1['bg'],
                                        fg="darkblue", 
                                        font=("Arial", 11, "bold"),
                                        borderwidth=5, 
                                        highlightthickness=0)
            self.new_btn.place(relx=0.70, rely=0.82, width=110, height=40)

            self.save_btn = Button(self.frame_1, state=DISABLED, command=self.save_etl_file,
                                        text="Salvar",
                                        bg=self.frame_1['bg'],
                                        fg="darkblue", 
                                        font=("Arial", 11, "bold"),
                                        borderwidth=5, 
                                        highlightthickness=0)
            self.save_btn.place(relx=0.35, rely=0.82, width=110, height=40)
        
        # WIDGETS PAINEL 3
        def widgets_frame_3(self):
            # Área de texto para logs e exibição de erros
            self.log_area = Text(self.frame_3, state=DISABLED, 
                                bg=self.frame_3['bg'], 
                                relief='flat', 
                                highlightthickness=0)
            self.log_area.place(relwidth=1.0, relheight=1.0)

        # FUNÇÕES
        def reset(self):
            self.frame_1.destroy()
            self.frame_3.destroy()
            self.screen_frames()  # Recria os frames
            self.widgets_frame_1()  # Recria os widgets
            self.widgets_frame_3()

        def data_view(self):
            client_table = Table(self.frame_2, dataframe=self.base_client, showtoolbar=False, showstatusbar=False)
            client_table.show()
            client_table.redraw()# Atualizar a exibição da tabela
            etl_table = Table(self.frame_4, dataframe=self.etl_file, showtoolbar=False, showstatusbar=False)
            etl_table.show()
            etl_table.redraw()# Atualizar a exibição da tabela
     
        def check_submit_state(self):
            if self.client_id.get()=="60": # Se o cliente for CLS
                self.radio_sep.config(state=NORMAL) # Habilita processo Separação
                if self.process_type.get()=="Separations": # Se o tipo do processo for separação
                    if self.procedure_type.get()=="leopoldina":
                        self.procedure_type.set(" ")
                    self.file_client_btn.config(state=NORMAL) # Habilita botão Base Cliente
                    self.file_return_btn.config(state=DISABLED)# Desabilita o botão Base Retorno
                    self.radio_leopoldina.config(state=DISABLED)
                    self.radio_carta_simples.config(state=NORMAL) # Habilita procedimento Carta Simples
                    self.radio_carta_registrada.config(state=NORMAL) # Habilita o procedimento Carta Registrada
                    self.radio_email.config(state=NORMAL) # Habilita procedimento E-mail
                elif self.process_type.get()=="Return": # Se o tipo do processo for retorno
                        if self.procedure_type.get()=="carta_simples" or self.procedure_type.get()=="email" or self.procedure_type.get()=="carta_registrada":
                            self.procedure_type.set(" ")
                        self.file_client_btn.config(state=DISABLED) # Desabilita botão Base Cliente
                        self.file_return_btn.config(state=NORMAL) # Habilita o botão Base Retorno
                        self.radio_leopoldina.config(state=NORMAL) # Habilita procedimento Leopoldina
                        self.radio_carta_simples.config(state=DISABLED) # Desabilita procedimento Carta Simples
                        self.radio_carta_registrada.config(state=DISABLED) # Desabilita o procedimento Carta Registrada
                        self.radio_email.config(state=DISABLED) # Desabilita procedimento E-mail
                else: # Se o tipo do processo for registro
                    if self.procedure_type.get()=="carta_simples" or self.procedure_type.get()=="email" or self.procedure_type.get()=="carta_registrada":
                            self.procedure_type.set(" ")
                    self.file_client_btn.config(state=NORMAL) # Habilita botão Base Cliente
                    self.file_return_btn.config(state=DISABLED) # Desabilita o botão Base Retorno
                    self.radio_leopoldina.config(state=NORMAL)
                    self.radio_carta_simples.config(state=DISABLED) # Desabilita procedimento Carta Simples
                    self.radio_carta_registrada.config(state=DISABLED) # Desabilita o procedimento Carta Registrada
                    self.radio_email.config(state=DISABLED) # Desabilita procedimento E-mail
            else: # Se o cliente não for CLS
                if self.procedure_type.get()=="carta_simples" or self.procedure_type.get()=="email" or self.procedure_type.get()=="carta_registrada":
                    self.procedure_type.set(" ")
                self.radio_sep.config(state=DISABLED) # Desabilita processo Separação
                self.file_client_btn.config(state=NORMAL) # Habilita o botão Base Cliente
                self.radio_leopoldina.config(state=NORMAL)
                self.radio_carta_simples.config(state=DISABLED) # Desabilita procedimento Carta Simples
                self.radio_carta_registrada.config(state=DISABLED) # Desabilita o procedimento Carta Registrada
                self.radio_email.config(state=DISABLED) # Desabilita procedimento Email

                if self.process_type.get()=="Separations":
                    self.process_type.set(" ")   
                elif self.process_type.get() == "Return": 
                    self.file_return_btn.config(state=NORMAL)
                else:   
                    self.file_return_btn.config(state=DISABLED)    
                     
            if ((not self.client_id.get()==" " and not self.process_type.get()==" "  
                and not self.procedure_type.get()==" ") 
                and (self.file_selected_client or self.file_client_btn.cget("state")==DISABLED)
                and (self.file_selected_return if self.process_type.get() == "Return" else True)):
                self.submit_btn.config(state=NORMAL)
            else:
                self.submit_btn.config(state=DISABLED)

        def select_base_client(self):
            self.file_path_client = filedialog.askopenfilename(
                filetypes=[("CSV and Excel files", "*.csv *.xlsx")]
            )
            if self.file_path_client:
                self.file_selected_client = True
                self.check_submit_state()

        def select_base_return(self):
            self.file_path_return = filedialog.askopenfilename(
                filetypes=[("CSV and TXT", "*.csv *.txt")]
            )
            if self.file_path_return:
                self.file_selected_return = True
                self.check_submit_state()

        def email_send(self):
            self.notebook.select(self.email_tab)

        def finalize_process(self):
            # Lista dos widgets que devem ser desabilitados
            widgets_to_disable = [
            self.submit_btn, self.radio_exsen, self.radio_rede_brasil, self.radio_cls, self.radio_setra_bpo,
            self.radio_registry, self.radio_return, self.radio_sep, 
            self.radio_leopoldina, self.radio_carta_simples, 
            self.radio_carta_registrada, self.radio_email, 
            self.file_client_btn, self.file_return_btn
            ]
        
            # Desabilita todos os widgets da lista
            for widget in widgets_to_disable:
                widget.config(state=DISABLED)
            
            # Habilita o botão 'Novo'
            self.new_btn.config(state=NORMAL)
            self.save_btn.config(state=NORMAL)

        def submit(self):
            self.dataframes = None
            self.registers = None  # Evita erro caso a variável não seja definida antes da exceção
            
            try:
                # ETL para o processo de registro
                if self.process_type.get() == 'Registry':  
                    self.file_path = self.file_path_client
                    base_std = Loaders.base_std_loader()
                    self.base_client = Loaders.base_client_loader(file_path_client=self.file_path)
                    self.etl_file, self.registers = processes(base_std=base_std, base_client=self.base_client,   
                                                            client_name=clients(self.client_id.get()), 
                                                            process_type=self.process_type.get(), 
                                                            procedure_type=self.procedure_type.get())
                # ETL para o processo de retorno                                                    
                elif self.process_type.get() == 'Return':
                    if clients(self.client_id.get()) != "CLS_DOCUMENTOS":
                        self.file_path = self.file_path_client
                        self.base_client = Loaders.base_client_loader(file_path_client=self.file_path)
                        base_client_copy = self.base_client.copy() 
                        self.base_return = Loaders.base_return_loader(file_path_return=self.file_path_return)
                        self.etl_file, self.registers = processes(base_client=base_client_copy, 
                                                                base_return=self.base_return, 
                                                                client_name=clients(self.client_id.get()), 
                                                                process_type=self.process_type.get(),
                                                                procedure_type=self.procedure_type.get())
                    else:
                        self.file_path = self.file_path_return
                        self.base_return = Loaders.base_return_loader(file_path_return=self.file_path)
                        self.base_client = self.base_return.copy()
                        self.etl_file, self.registers = processes(client_name=clients(self.client_id.get()), 
                                                                process_type=self.process_type.get(), 
                                                                base_return=self.base_client,
                                                                procedure_type=self.procedure_type.get())
                # ETL para o processo de separação        
                elif self.process_type.get() == 'Separations':
                    self.file_path = self.file_path_client
                    self.base_client = Loaders.base_client_loader(file_path_client=self.file_path) 
                    base_client_copy = self.base_client.copy()    
                    self.etl_file, self.dataframes, self.registers = processes(base_client=base_client_copy, 
                                                client_name=clients(self.client_id.get()), 
                                                process_type=self.process_type.get(), 
                                                procedure_type=self.procedure_type.get())

                # Mostra as bases nos painéis    
                self.data_view()

                # Finaliza o processo desabilitando opções e botões
                self.finalize_process()

                # Cria e atualiza o Logger
                self.logger = Logger(
                    log_area=self.log_area,
                    client_id=self.client_id.get(),
                    client_name=clients(self.client_id.get()),
                    process_type=self.process_type.get(),
                    procedure_type=self.procedure_type.get(),
                    registers=self.registers    
                )   
                self.logger.processes_log()
                
            except Exception as e:
                error_trace = traceback.format_exc()  # Captura traceback completo para facilitar a depuração

                if not hasattr(self, 'logger'):  # Evita erro caso self.logger ainda não tenha sido inicializado
                    self.logger = Logger(
                        log_area=self.log_area,
                        client_id=self.client_id.get(),
                        client_name=clients(self.client_id.get()),
                        process_type=self.process_type.get(),
                        procedure_type=self.procedure_type.get(),
                        registers=self.registers    
                    ) 
                
                self.logger.log_error(message=f"Erro durante o processo: {str(e)}")
                self.logger.log_error(message=f"Detalhes do erro:\n{error_trace}")

        def save_etl_file(self):
            object = SaveFile(
                file_path=self.file_path,
                client_id=self.client_id.get(),
                client_name=clients(self.client_id.get()),
                process_type=self.process_type.get(),
                procedure_type=self.procedure_type.get(),
                etl_file=self.etl_file,
                dataframes=self.dataframes,
                return_file=self.base_return if self.process_type.get() == "Return" else None
            )
            full_path = object.save_processes()
    
            self.logger.save_log(full_path=full_path)

            self.save_btn.config(state=DISABLED)
            self.send_email_btn.config(state=NORMAL)

    app = App()         

if __name__ == "__main__":
    run_interface()