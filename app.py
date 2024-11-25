import customtkinter as ctk
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")  # Outros modos: "light", "system"
ctk.set_default_color_theme("dark-blue")  # Outros temas: "green", "dark-blue"

class GraphTheoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Teoria dos Grafos")
        self.geometry("1200x800")
        self.graph = nx.Graph()  # Inicializa o grafo vazio

        # Configurações básicas
        self.weighted = True  # Sempre considerado como grafo valorizado (não há mais a opção não valorizado)
        self.directed = False  # Grafo direcionado inicialmente desativado

        # Criando os frames principais
        self.sidebar_frame = ctk.CTkFrame(self, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Widgets da barra lateral
        arial_bold_font = ("Arial", 35, "bold")
        ctk.CTkLabel(self.sidebar_frame, text="GRAPHIN", font=arial_bold_font).pack(pady=35)

        # Entrada de vértices/arestas
        self.input_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Insira os vértices ou arestas...", width=300, height=30)
        self.input_entry.pack(pady=20, padx=20)
        
        ctk.CTkButton(self.sidebar_frame, text="Adicionar", command=self.add_vertex_or_edge, width=300).pack(pady=5)

        # Upload de arquivo para inserção em lote
        ctk.CTkButton(self.sidebar_frame, text="Inserir em Lote", command=self.load_from_file, width=300).pack(pady=5)

        # Botão para alternar o tipo de grafo
        self.toggle_button = ctk.CTkButton(self.sidebar_frame, text="Tornar Grafo Direcionado", command=self.toggle_directed, width=300)
        self.toggle_button.pack(pady=5)

        # Label indicando o tipo de grafo
        self.graph_type_label = ctk.CTkLabel(self.sidebar_frame, text="Tipo de Grafo: Não Direcionado", font=("Arial", 14))
        self.graph_type_label.pack(pady=5)

        # Labels para Ordem e Tamanho do Grafo
        self.order_label = ctk.CTkLabel(self.sidebar_frame, text="Ordem: 0", font=("Arial", 14))
        self.order_label.pack(pady=5)
        self.size_label = ctk.CTkLabel(self.sidebar_frame, text="Tamanho: 0", font=("Arial", 14))
        self.size_label.pack(pady=5)

        # Botões para funcionalidades principais
        ctk.CTkButton(self.sidebar_frame, text="Limpar", command=self.clear_graph, width=300, fg_color="red", hover_color="darkred").pack(pady=5)
        ctk.CTkButton(self.sidebar_frame, text="Visualizar Grafo", command=self.display_graph, width=300, fg_color="green", hover_color="darkgreen").pack(pady=5)

        # Entrada e botão para verificar vértices adjacentes
        self.vertex_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Insira o vértice", width=300, height=30)
        self.vertex_entry.pack(pady=20, padx=20)
        ctk.CTkButton(self.sidebar_frame, text="Ver Adjacentes", command=self.show_adjacent_vertices, width=300).pack(pady=5)

        # Label para exibir os vértices adjacentes
        self.adjacency_label = ctk.CTkLabel(self.sidebar_frame, text="Vértices adjacentes: Nenhum", font=("Arial", 12))
        self.adjacency_label.pack(pady=5)

        # Widgets do frame principal (canvas para desenhar o grafo)
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def log_message(self, message):
        print(message)  # Por enquanto, apenas imprime no console

    def toggle_directed(self):
        if self.graph.number_of_nodes() > 0 or self.graph.number_of_edges() > 0:
            messagebox.showerror("Erro", "Não é possível alterar o tipo de grafo com vértices ou arestas presentes.")
        else:
            self.directed = not self.directed
            self.graph = nx.DiGraph() if self.directed else nx.Graph()
            # Atualiza o texto do botão e do label
            self.toggle_button.configure(text="Tornar Grafo Não Direcionado" if self.directed else "Tornar Grafo Direcionado")
            self.graph_type_label.configure(text=f"Tipo de Grafo: {'Direcionado' if self.directed else 'Não Direcionado'}")
            messagebox.showinfo("Configuração Alterada", f"Grafo {'Direcionado' if self.directed else 'Não Direcionado'}")
    

    def process_vertex_or_edge(self, data):
        if "-" in data:  # Verifica se é uma aresta
            parts = data.split("-")
            if len(parts) == 2:  # Aresta sem peso (v1-v2)
                try:
                    u = int(parts[0].strip())  # Primeiro vértice
                    v = int(parts[1].strip())  # Segundo vértice
                    self.graph.add_edge(u, v)  # Adiciona aresta com peso padrão 1
                    self.log_message(f"Aresta sem peso adicionada entre {u} e {v}")
                except ValueError:
                    messagebox.showerror("Erro", "Formato inválido. Certifique-se de que os vértices são números inteiros.")
            elif len(parts) == 3:  # Aresta com peso (v1-(peso)-v2)
                try:
                    u = int(parts[0].strip())  # Primeiro vértice
                    weight_part = parts[1].strip()  # Parte do peso
                    v = int(parts[2].strip())  # Segundo vértice
                    
                    # Verifica se o peso está entre parênteses
                    if weight_part.startswith("(") and weight_part.endswith(")"):
                        weight = int(weight_part[1:-1])  # Extrai o número entre parênteses
                        self.graph.add_edge(u, v, weight=weight)  # Adiciona aresta com peso
                        self.log_message(f"Aresta com peso {weight} adicionada entre {u} e {v}")
                    else:
                        messagebox.showerror("Erro", "Formato de peso inválido. Use '(peso)'.")
                except ValueError:
                    messagebox.showerror("Erro", "Formato inválido. Certifique-se de que os vértices e peso são números inteiros.")
            else:
                messagebox.showerror("Erro", "Formato de aresta inválido. Use 'v1-(peso)-v2' ou 'v1-v2'.")
        else:  # Caso contrário, trata como vértice único
            try:
                vertex = int(data)
                self.graph.add_node(vertex)
                self.log_message(f"Vértice adicionado: {vertex}")
            except ValueError:
                messagebox.showerror("Erro", "Vértice inválido. Insira um número inteiro.")

    def add_vertex_or_edge(self):
        data = self.input_entry.get().strip()
        if "," in data:
            datas = data.split(",")
            for i in range (len(datas)): 
                datas[i] = datas[i].strip()
                self.process_vertex_or_edge(datas[i])
        else:
            self.process_vertex_or_edge(data)
        self.input_entry.delete(0, tk.END)
        self.update_graph_info()

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    edges = line.split()  # Separa as arestas por espaços

                    for edge in edges:
                        parts = edge.split("-")  # Divide a aresta
                        if len(parts) == 2:  # Caso sem peso
                            try:
                                u = int(parts[0].strip())  # Primeiro vértice
                                v = int(parts[1].strip())  # Segundo vértice
                                self.graph.add_edge(u, v)  # Adiciona aresta sem peso
                                self.log_message(f"Aresta sem peso adicionada entre {u} e {v}")
                            except ValueError:
                                messagebox.showerror("Erro", "Formato inválido. Certifique-se de que os vértices são números inteiros.")
                        elif len(parts) == 3:  # Caso com peso
                            try:
                                u = int(parts[0].strip())  # Primeiro vértice
                                weight_part = parts[1].strip()  # Parte do peso
                                v = int(parts[2].strip())  # Segundo vértice
                                
                                # Verifica se o peso está entre parênteses
                                if weight_part.startswith("(") and weight_part.endswith(")"):
                                    weight = int(weight_part[1:-1])  # Extrai o número entre parênteses
                                    self.graph.add_edge(u, v, weight=weight)  # Adiciona aresta com peso
                                    self.log_message(f"Aresta com peso {weight} adicionada entre {u} e {v}")
                                else:
                                    messagebox.showerror("Erro", "Formato de peso inválido. Use '(peso)'.")
                            except ValueError:
                                messagebox.showerror("Erro", "Formato inválido. Certifique-se de que os vértices e peso são números inteiros.")
                        else:
                            messagebox.showerror("Erro", "Formato de aresta inválido. Use 'v1-(peso)-v2' ou 'v1-v2'.")


    def display_graph(self):
        if self.graph.number_of_nodes() == 0:
            messagebox.showerror("Erro", "O grafo está vazio. Adicione vértices ou arestas antes de visualizar.")
            return

        # Limpa o canvas removendo o gráfico atual antes de desenhar um novo
        for widget in self.canvas.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title("Visualização do Grafo")

        # Desenha o grafo
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, ax=ax)

        # Exibe os pesos das arestas, se houver
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        if edge_labels:  # Se houver pesos
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def update_graph_info(self):
        self.order_label.configure(text=f"Ordem: {self.graph.number_of_nodes()}")
        self.size_label.configure(text=f"Tamanho: {self.graph.number_of_edges()}")

    def clear_graph(self):
        self.graph.clear()
        self.update_graph_info()
        self.canvas.delete("all")
        messagebox.showinfo("Grafo Limpo", "O grafo foi limpo com sucesso.")

    def show_adjacent_vertices(self):
        vertex = self.vertex_entry.get().strip()
        if vertex.isdigit():
            vertex = int(vertex)
            if vertex in self.graph.nodes:
                # Se o grafo for direcionado, mostra tanto os predecessores (entrada) quanto os sucessores (saída)
                if self.directed:
                    # Predecessores (vértices de entrada)
                    predecessors = list(self.graph.predecessors(vertex))
                    # Sucessores (vértices de saída)
                    successors = list(self.graph.successors(vertex))
                    
                    self.adjacency_label.configure(
                        text=f"Vértices de Entrada: {', '.join(map(str, predecessors)) if predecessors else 'Nenhum'}\n"
                            f"Vértices de Saída: {', '.join(map(str, successors)) if successors else 'Nenhum'}"
                    )
                else:
                    # Para grafos não direcionados, basta pegar os adjacentes
                    adjacents = list(self.graph.adj[vertex])
                    self.adjacency_label.configure(
                        text=f"Vértices adjacentes: {', '.join(map(str, adjacents)) if adjacents else 'Nenhum'}"
                    )
            else:
                messagebox.showerror("Erro", "O vértice inserido não existe no grafo.")
        else:
            messagebox.showerror("Erro", "Insira um vértice válido.")


if __name__ == "__main__":
    app = GraphTheoryApp()
    app.mainloop()
