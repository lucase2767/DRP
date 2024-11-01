import tkinter as tk
from tkinter import ttk, messagebox
from Banco_BackEnd import BancoDados, ErroBanco
#separação do front e back end

class JanelaAdicionarAluno:
    def __init__(self, parent, db, callback):
        self.janela = tk.Toplevel(parent)
        self.janela.title("Adicionar Novo Aluno")
        self.janela.geometry("500x450")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        self.db = db
        self.callback = callback
        
        self._configurar_janela()
        
    def _configurar_janela(self):
        frame_principal = ttk.Frame(self.janela, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        titulo_label = ttk.Label(
            frame_principal, 
            text="Adicionar Novo Aluno", 
            style="Cabecalho.TLabel"
        )
        titulo_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        self.campos_entrada = {}
        labels = [
            ('Nome:', str), 
            ('Matrícula:', int),
            ('Turma:', str),
            ('Nota AV1:', float),
            ('Nota AV2:', float)
        ]
        
        for i, (label, _) in enumerate(labels, start=1):
            ttk.Label(frame_principal, text=label).grid(
                row=i, column=0, padx=5, pady=5, sticky=tk.W
            )
            entrada = ttk.Entry(frame_principal, width=40)
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
            self.campos_entrada[label] = entrada
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.grid(row=len(labels)+1, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            frame_botoes,
            text="Adicionar Aluno",
            style="Acao.TButton",
            command=self._adicionar_aluno
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            frame_botoes,
            text="Cancelar",
            style="Acao.TButton",
            command=self.janela.destroy
        ).grid(row=0, column=1, padx=5)
        
        frame_principal.columnconfigure(1, weight=1)
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)
        
        #centralizar janela
        self.janela.update_idletasks()
        x = self.janela.master.winfo_x() + (self.janela.master.winfo_width() - self.janela.winfo_width()) // 2
        y = self.janela.master.winfo_y() + (self.janela.master.winfo_height() - self.janela.winfo_height()) // 2
        self.janela.geometry(f"+{x}+{y}")

    def _adicionar_aluno(self):
        try:
            nome = self.campos_entrada['Nome:'].get().strip()
            matricula = self.campos_entrada['Matrícula:'].get().strip()
            turma = self.campos_entrada['Turma:'].get().strip()
            av1 = self.campos_entrada['Nota AV1:'].get().strip()
            av2 = self.campos_entrada['Nota AV2:'].get().strip()
            
            if not all([nome, matricula, turma, av1, av2]):
                raise ValueError("Todos os campos são obrigatórios")
            
            matricula = int(matricula)
            av1 = float(av1)
            av2 = float(av2)
            
            if not (0 <= av1 <= 10 and 0 <= av2 <= 10):
                raise ValueError("As notas devem estar entre 0 e 10")
            
            self.db.adicionar_aluno(nome, matricula, turma, av1, av2)
            messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso")
            
            self.callback()
            self.janela.destroy()
                
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))
        except ErroBanco as e:
            messagebox.showerror("Erro do Banco", str(e))

class JanelaAtualizarAluno:
    def __init__(self, parent, db, aluno_dados, callback):
        self.janela = tk.Toplevel(parent)
        self.janela.title("Atualizar Aluno")
        self.janela.geometry("500x450")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        self.db = db
        self.aluno_dados = aluno_dados
        self.callback = callback
        
        self._configurar_janela()
        
    def _configurar_janela(self):
        frame_principal = ttk.Frame(self.janela, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        titulo_label = ttk.Label(
            frame_principal, 
            text="Atualizar Aluno", 
            style="Cabecalho.TLabel"
        )
        titulo_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        self.campos_entrada = {}
        labels = [
            ('Nome:', str, 1), 
            ('Matrícula:', int, 2),
            ('Turma:', str, 3),
            ('Nota AV1:', float, 4),
            ('Nota AV2:', float, 5)
        ]
        
        #separação das variaveis dadas para uso
        dados_atuais = {
            'Nome:': self.aluno_dados[1],
            'Matrícula:': self.aluno_dados[2],
            'Turma:': self.aluno_dados[3],
            'Nota AV1:': self.aluno_dados[4],
            'Nota AV2:': self.aluno_dados[5]
        }
        
        for label, _, idx in labels:
            ttk.Label(frame_principal, text=label).grid(
                row=idx, column=0, padx=5, pady=5, sticky=tk.W
            )
            entrada = ttk.Entry(frame_principal, width=40)
            entrada.insert(0, str(dados_atuais[label]))
            entrada.grid(row=idx, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
            self.campos_entrada[label] = entrada
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.grid(row=len(labels)+1, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            frame_botoes,
            text="Atualizar",
            style="Acao.TButton",
            command=self._atualizar_aluno
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            frame_botoes,
            text="Cancelar",
            style="Acao.TButton",
            command=self.janela.destroy
        ).grid(row=0, column=1, padx=5)
        
        frame_principal.columnconfigure(1, weight=1)
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)
        
        #centralizar janela
        self.janela.update_idletasks()
        x = self.janela.master.winfo_x() + (self.janela.master.winfo_width() - self.janela.winfo_width()) // 2
        y = self.janela.master.winfo_y() + (self.janela.master.winfo_height() - self.janela.winfo_height()) // 2
        self.janela.geometry(f"+{x}+{y}")

    def _atualizar_aluno(self):
        try:
            nome = self.campos_entrada['Nome:'].get().strip()
            matricula = self.campos_entrada['Matrícula:'].get().strip()
            turma = self.campos_entrada['Turma:'].get().strip()
            av1 = self.campos_entrada['Nota AV1:'].get().strip()
            av2 = self.campos_entrada['Nota AV2:'].get().strip()
            
            if not all([nome, matricula, turma, av1, av2]):
                raise ValueError("Todos os campos são obrigatórios")
            
            matricula = int(matricula)
            av1 = float(av1)
            av2 = float(av2)
            
            if not (0 <= av1 <= 10 and 0 <= av2 <= 10):
                raise ValueError("As notas devem estar entre 0 e 10")
            
            self.db.atualizar_aluno(self.aluno_dados[0], nome, matricula, turma, av1, av2)
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso")
            
            self.callback()
            self.janela.destroy()
                
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))
        except ErroBanco as e:
            messagebox.showerror("Erro do Banco", str(e))

class SistemaGerenciamentoAlunos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Alunos")
        self.root.geometry("1000x700")
        
        try:
            self.db = BancoDados()
        except ErroBanco as e:
            messagebox.showerror("Erro do Banco", str(e))
            raise

        #inicialização da interface principal
        self._configurar_estilos()
        self._configurar_interface_principal()
        self._criar_menu_contexto()
        
    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure("Acao.TButton", padding=5)
        style.configure("Cabecalho.TLabel", font=('Helvetica', 12, 'bold'))
        style.configure("Custom.Treeview", rowheight=25)

    def _criar_menu_contexto(self):
        self.menu_contexto = tk.Menu(self.root, tearoff=0)
        self.menu_contexto.add_command(
            label="Editar",
            command=lambda: self._abrir_janela_atualizar(self.aluno_selecionado_id)
        )
        self.menu_contexto.add_command(
            label="Excluir",
            command=lambda: self._confirmar_exclusao(self.aluno_selecionado_id)
        )

    def _configurar_interface_principal(self):
        self.container_principal = ttk.Frame(self.root, padding="10")
        self.container_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        #barra de ações superior
        barra_acoes = ttk.Frame(self.container_principal)
        barra_acoes.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        frame_busca = ttk.Frame(barra_acoes)
        frame_busca.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(
            frame_busca,
            text="Buscar:",
            style="Cabecalho.TLabel"
        ).pack(side=tk.LEFT, padx=5)
        
        self.var_busca = tk.StringVar()
        self.var_busca.trace('w', self._ao_mudar_busca)
        
        self.entrada_busca = ttk.Entry(
            frame_busca, 
            width=40,
            textvariable=self.var_busca
        )
        self.entrada_busca.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            frame_busca,
            text="Limpar",
            command=self._limpar_busca,
            style="Acao.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            barra_acoes,
            text="Adicionar Novo Aluno",
            style="Acao.TButton",
            command=self._abrir_janela_adicionar
        ).pack(side=tk.RIGHT, padx=5)
        
        #contador do db
        frame_stats = ttk.Frame(self.container_principal)
        frame_stats.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.label_stats = ttk.Label(
            frame_stats,
            text="Total de Alunos: 0",
            style="Cabecalho.TLabel"
        )
        self.label_stats.pack(side=tk.LEFT)
        
        self.arvore_lista = self._criar_treeview_alunos(self.container_principal)
        self.arvore_lista.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.arvore_lista.bind("<Button-3>", self._mostrar_menu_contexto)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.container_principal.columnconfigure(0, weight=1)
        self.container_principal.rowconfigure(2, weight=1)

    def _criar_treeview_alunos(self, parent):
        colunas = ('ID', 'Nome', 'Matrícula', 'Turma', 'AV1', 'AV2', 'Média')  # Removed 'Ações' column
        arvore = ttk.Treeview(
            parent, 
            columns=colunas,
            show='headings',
            style="Custom.Treeview"
        )
        
        larguras = [50, 200, 100, 100, 80, 80, 80]  # Adjusted widths
        for col, largura in zip(colunas, larguras):
            arvore.heading(col, text=col, command=lambda c=col: self._ordenar_treeview(arvore, c))
            arvore.column(col, width=largura, minwidth=50)
        
        #barra de rolagem
        y_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=arvore.yview)
        y_scroll.grid(row=2, column=1, sticky=(tk.N, tk.S))
        
        x_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=arvore.xview)
        x_scroll.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        arvore.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        return arvore

    def _mostrar_menu_contexto(self, event):
        item = self.arvore_lista.identify_row(event.y)
        if item:
            self.arvore_lista.selection_set(item)
            self.aluno_selecionado_id = self.arvore_lista.item(item)['values'][0]
            self.menu_contexto.post(event.x_root, event.y_root)

    def _ordenar_treeview(self, tree, col):
        items = [(tree.set(item, col), item) for item in tree.get_children('')]
        
        try:
            items.sort(key=lambda x: float(x[0]) if x[0].replace('.', '').isdigit() else x[0].lower())
        except ValueError:
            items.sort(key=lambda x: x[0].lower())
        
        for index, (_, item) in enumerate(items):
            tree.move(item, '', index)

    def _atualizar_treeview(self, dados):
        for item in self.arvore_lista.get_children():
            self.arvore_lista.delete(item)
        
        for row in dados:
            self.arvore_lista.insert('', tk.END, values=row)
        
        self.label_stats.config(text=f"Total de Alunos: {len(dados)}")


    def _abrir_janela_adicionar(self):
        JanelaAdicionarAluno(self.root, self.db, self._atualizar_lista)

    def _abrir_janela_atualizar(self, aluno_id):
        for item in self.arvore_lista.get_children():
            if self.arvore_lista.item(item)['values'][0] == aluno_id:
                aluno_dados = self.arvore_lista.item(item)['values']
                JanelaAtualizarAluno(self.root, self.db, aluno_dados, self._atualizar_lista)
                break

    def _confirmar_exclusao(self, aluno_id):
        if messagebox.askyesno("Confirmar Exclusão", 
                              "Tem certeza que deseja excluir este aluno?"):
            try:
                self.db.excluir_aluno(aluno_id)
                self._atualizar_lista()
                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso")
            except ErroBanco as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno: {e}")

    def _ordenar_treeview(self, tree, col):
        items = [(tree.set(item, col), item) for item in tree.get_children('')]
        
        if col not in ['Ações']:
            try:
                items.sort(key=lambda x: float(x[0]) if x[0].replace('.', '').isdigit() else x[0].lower())
            except ValueError:
                items.sort(key=lambda x: x[0].lower())
            
            for index, (_, item) in enumerate(items):
                tree.move(item, '', index)


    def _ao_mudar_busca(self, *args):
        termo_busca = self.var_busca.get().strip()
        try:
            if termo_busca:
                resultados = self.db.procurar_aluno(termo_busca)
            else:
                resultados = self.db.listar_alunos()
            self._atualizar_treeview(resultados)
        except ErroBanco as e:
            messagebox.showerror("Erro na Busca", str(e))

    def _limpar_busca(self):
        self.var_busca.set('')
        self._atualizar_lista()

    def _atualizar_lista(self):
        try:
            resultados = self.db.listar_alunos()
            self._atualizar_treeview(resultados)
        except ErroBanco as e:
            messagebox.showerror("Erro", str(e))

    def _atualizar_treeview(self, dados):
        for item in self.arvore_lista.get_children():
            self.arvore_lista.delete(item)
        
        for row in dados:
            item = self.arvore_lista.insert('', tk.END, values=row)      
        self.label_stats.config(text=f"Total de Alunos: {len(dados)}")

    def executar(self):
        self._atualizar_lista()
        self.root.mainloop()

    def limpar(self):
        if hasattr(self, 'db'):
            self.db.fechar()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGerenciamentoAlunos(root)
    try:
        app.executar()
    finally:
        app.limpar()