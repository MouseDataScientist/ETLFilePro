from tkinter import *

def create_email_tab(tab):
    """Função para criar a aba de e-mail dentro do frame fornecido"""
    
    # Painel 1
    tab.frame_1 = Frame(tab, bd=4, bg="#70ebca", 
                            highlightbackground="black", highlightthickness=2)
    tab.frame_1.place(relx=0.006, rely=0.01, relwidth=0.340, relheight=0.7)

    # Painel 2
    tab.frame_2 = Frame(tab, bd=4, bg="#d5eaf4", 
                            highlightbackground="black", highlightthickness=2)
    tab.frame_2.place(relx=0.35, rely=0.01, relwidth=0.645, relheight=0.5)

    # Painel 3
    tab.frame_3 = Frame(tab, bd=4, bg="#8ec6e4", 
                            highlightbackground="black", highlightthickness=2)
    tab.frame_3.place(relx=0.006, rely=0.716, relwidth=0.340, relheight=0.278)

    # Painel 4
    tab.frame_4 = Frame(tab, bd=4, bg="#d5eaf4", 
                            highlightbackground="black", highlightthickness=2)
    tab.frame_4.place(relx=0.35, rely=0.516, relwidth=0.645, relheight=0.478)