from cProfile import label
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import filedialog as fd
from analisador import lexer, parser, saidas



class Application():
    def __init__(self):
        self.root = tk.Tk()
        # self.saidas = []
        self.tela()
        self.frames_da_tela()
        self.botoes()
        self.Menus()
        self.root.mainloop()


    def limpa_telaentrada(self, delete_input=True):
        if delete_input:
            self.codigo_entry.delete(1.0, END)
        for i in self.saida.get_children():
            self.saida.delete(i)
        saidas.clear()
        self.frame_1.update()
        self.frame_2.update()
        self.root.update()

    def tela(self):
        self.root.title("Compilador")
        self.root.configure(background="white")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.minsize(width=550, height=350)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#DCDCDC",highlightbackground="grey", highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.07, relwidth=0.96, relheight=0.55)
        self.frame_2 = Frame(self.root, bd=4, bg="#DCDCDC",highlightbackground="grey", highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.70, relwidth=0.96, relheight=0.20)

        self.saida = ttk.Treeview(self.frame_2, height=5, columns=('token', 'lexema', 'linha', 'posicao'), show='headings')
        self.saida.column('token', width=200)
        self.saida.heading('#1', text="Token") 
        self.saida.column('lexema', width=200)
        self.saida.heading('#2', text="Lexema") 
        self.saida.column('linha', width=50)
        self.saida.heading('#3', text="Linha") 
        self.saida.column('posicao', width=50)
        self.saida.heading('#4', text="Posição")
        self.saida.place(relx=0.001, rely=0.01, relwidth=0.999, relheight=0.95)
        # self.saida.place_forget()  # Oculta inicialmente

        # Text (para Sintático)
        self.saida_texto = tk.Text(self.frame_2, wrap="word", font=('', 10))
        self.saida_texto.place_forget()

    def add_lista_saida(self, t):
        saidas.append((t.type, t.value, t.lineno, t.lexpos))
    
    def chama_analisador(self):
        if self.tipo_analise.get() == "lexica":
            # columns = ('token', 'lexema', 'linha', 'posicao')
            # self.saida = ttk.Treeview(self.frame_2, height=5, columns=columns, show='headings')
            # self.saida.column('token', width=200)
            # self.saida.heading('#1', text="Token") 

            # self.saida.column('lexema', width=200)
            # self.saida.heading('#2', text="Lexema") 

            # self.saida.column('linha', width=50)
            # self.saida.heading('#3', text="Linha") 

            # self.saida.column('posicao', width=50)
            # self.saida.heading('#4', text="Posição")

            data = self.codigo_entry.get(1.0, "end-1c")
            linhas = data.strip().split('\n')
            saidas.clear()
            self.limpa_telaentrada(delete_input=False)
            for i, linha in enumerate(linhas, start=1):
                lexer.input(linha)

                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    saidas.append((tok.type, tok.value, i, tok.lexpos))
            
            for retorno in saidas:
                self.saida.insert('', tk.END, values=retorno)
                self.saida.place(relx=0.001, rely=0.01, relwidth=0.999, relheight=0.95)

                self.scrollAnalise = ttk.Scrollbar(self.frame_2, orient='vertical',command=self.saida.yview)
                self.scrollAnalise.place(relx=0.979, rely=0.0192, relwidth=0.02, relheight=0.92)
                self.saida['yscrollcommand'] = self.scrollAnalise

        # 🧠 Aqui executamos a análise sintática
        else:
            # columns = ('linha')
            # self.saida = ttk.Treeview(self.frame_2, height=5, columns=columns, show='headings')
            # self.saida.column('token', width=200)
            # self.saida.heading('#1', text="Excel") 

            data = self.codigo_entry.get(1.0, "end-1c")
            linhas = data.strip().split('\n')
            saidas.clear()
            self.saida_texto.delete(1.0, END)
            try:
                parser.parse(data)
                # saidas.append(("Sintático", "Análise realizada com sucesso", "-", "-"))
                for data in saidas:
                    self.saida_texto.insert(END, f'{data}\n\n')
            except Exception as e:
                print(f"[ERRO NA ANÁLISE SINTÁTICA] {e}")
                erro_msg = f"Erro sintático: {e}"
                saidas.append(("Erro", erro_msg, "-", "-"))
             

        

    def exibir_lexico(self):
        self.lb_analise.config(text="Análise Léxica")
        self.saida_texto.place_forget()
        self.saida.place(relx=0.001, rely=0.01, relwidth=0.999, relheight=0.95)

    def exibir_sintatico(self):
        self.lb_analise.config(text="Análise Sintática")
        self.saida.place_forget()
        self.saida_texto.place(relx=0.001, rely=0.01, relwidth=0.999, relheight=0.95)

    def botoes(self):
        # botao limpar
        self.bt_limpar = Button(text="Limpar", bd=2, bg="#FF6347", font=('', 11), command=self.limpa_telaentrada)
        self.bt_limpar.place(relx=0.74, rely=0.92, relwidth=0.1, relheight=0.05)

        # botao executar
        self.bt_executar = Button(text="Executar", bd=2, bg="lightgreen", font=('', 11), command=self.chama_analisador)
        self.bt_executar.place(relx=0.85, rely=0.92, relwidth=0.1, relheight=0.05)

        # criação da label e entrada do código
        self.lb_codigo = Label(text="Código Fonte", bg="white", font=('', 12))
        self.lb_codigo.place(relx=0.001, rely=-0.001, relwidth=0.2, relheight=0.07)
        
        self.tipo_analise = tk.StringVar(value="lexica")
        self.radio_lexica = tk.Radiobutton(text="Léxica", variable=self.tipo_analise, value="lexica", bg="white", command=self.exibir_lexico)
        self.radio_lexica.place(relx=0.35, rely=0.62)
        
        self.radio_sintatica = tk.Radiobutton(text="Sintática", variable=self.tipo_analise, value="sintatica", bg="white", command=self.exibir_sintatico)
        self.radio_sintatica.place(relx=0.45, rely=0.62)


        # criação da label da analise lexica
        self.lb_analise = Label(text="Análise Léxica", bg="white", font=('', 12))
        self.lb_analise.place(relx=0.001, rely=0.62, relwidth=0.2, relheight=0.07)

        self.msg_resultado = tk.Label(self.root, text="", fg="blue", bg="white", font=('', 10))
        self.msg_resultado.place(relx=0.02, rely=0.92, relwidth=0.30, relheight=0.05)

        self.codigo_entry = tk.Text(self.frame_1)
        self.codigo_entry.place(relx=0.001, rely=0.001, relwidth=0.995, relheight=0.995)

        self.scroll_bar = ttk.Scrollbar(self.frame_1, orient='vertical', command=self.codigo_entry.yview)
        self.scroll_bar.place(relx=0.982, rely=0.0019, relwidth=0.015, relheight=0.99)
        self.codigo_entry['yscrollcommand'] = self.scroll_bar

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)

        def Quit(): self.root.destroy()

        def onOpen():
            tf = fd.askopenfilename(
                initialdir="C:/Users/MainFrame/Desktop/",
                title="Open Text file",
                filetypes=(("Text Files", "*.txt"),)
            )
            tf = open(tf, 'r')
            entrada = tf.read()
            self.codigo_entry.insert(END, entrada)
            tf.close()

        def onSave():
            files = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
            t = self.codigo_entry.get(0.0, END)
            files.write(t.rstrip())

        

        menubar.add_cascade(label="Arquivo", menu=filemenu)
        filemenu.add_command(label="Abrir Script", command=onOpen)
        filemenu.add_command(label="Salvar Como", command=onSave)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=Quit)


Application()