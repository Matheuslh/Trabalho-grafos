import customtkinter as ctk
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox
import csv

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

        # Widgets do frame principal (canvas para desenhar o grafo)
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Novo frame para funcionalidades adicionais no lado direito
        self.right_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Widgets da barra lateral
        arial_bold_font = ("Arial", 35, "bold")
        ctk.CTkLabel(self.right_frame, text="FUNÇÕES", font=arial_bold_font).pack(pady=35)

        # Funcionalidades adicionais no right_frame
        ctk.CTkButton(self.right_frame, text="Verificar Euleriano", command=self.check_eulerian, width=300).pack(pady=5)

        # Entrada e botão para verificar vértices adjacentes
        self.vertex_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Insira o vértice", width=300, height=30)
        self.vertex_entry.pack(pady=20, padx=20)
        ctk.CTkButton(self.right_frame, text="Ver Adjacentes", command=self.show_adjacent_vertices, width=300).pack(pady=5)
        
        # Label para exibir os vértices adjacentes
        self.adjacency_label = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 14))
        self.adjacency_label.pack(pady=3)

        ctk.CTkLabel(self.right_frame, text="Ver menor caminho", font=("Arial", 16)).pack(pady=2)

        # Entrada para o vértice de origem
        self.start_vertex_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Vértice de origem", width=300, height=30)
        self.start_vertex_entry.pack(pady=5, padx=20)

        # Entrada para o vértice de destino
        self.end_vertex_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Vértice de destino", width=300, height=30)
        self.end_vertex_entry.pack(pady=5, padx=20)

        # Botão para encontrar o caminho mais curto
        ctk.CTkButton(self.right_frame, text="Caminho Mais Curto", command=self.find_shortest_path, width=300).pack(pady=20)


        
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
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
        if file_path:
            if file_path.endswith(".csv"):
                with open(file_path, "r") as file:
                    reader = csv.reader(file)
                    next(reader)  # Ignora a primeira linha (título)
                    for row in reader:
                        if len(row) >= 3:  # Verifica se a linha tem pelo menos 3 colunas
                            # Formato: [coluna 1]-([coluna 3])-[coluna 2]
                            processed_item = f"{row[0].strip()}-({row[2].strip()})-{row[1].strip()}"
                            self.process_vertex_or_edge(processed_item)  # Chama a função de processamento existente
            else:  # Caso seja um arquivo .txt
                with open(file_path, "r") as file:
                    for line in file:
                        line = line.strip()
                        items = line.split(",")  
                        for item in items:
                            self.process_vertex_or_edge(item.strip())  # Chama a função de processamento existente
            self.update_graph_info()
            messagebox.showinfo("Sucesso", "Dados carregados com sucesso do arquivo.")



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
            
    def find_shortest_path(self):
        # Obtém os valores de entrada dos vértices de origem e destino
        start_vertex = self.start_vertex_entry.get().strip()
        target_vertex = self.end_vertex_entry.get().strip()
        
        # Verifica se os valores são números válidos
        if not start_vertex.isdigit() or not target_vertex.isdigit():
            messagebox.showerror("Erro", "Por favor, insira vértices válidos (números inteiros).")
            return

        start_vertex = int(start_vertex)
        target_vertex = int(target_vertex)

        # Verifica se os vértices existem no grafo
        if start_vertex not in self.graph.nodes or target_vertex not in self.graph.nodes:
            messagebox.showerror("Erro", "Os vértices fornecidos não existem no grafo.")
            return

        try:
            # Usa o algoritmo de Dijkstra para encontrar o menor caminho
            path = nx.shortest_path(self.graph, source=start_vertex, target=target_vertex, weight="weight")
            cost = nx.shortest_path_length(self.graph, source=start_vertex, target=target_vertex, weight="weight")
            
            # Exibe o custo e o caminho encontrado
            messagebox.showinfo(
                "Caminho Mais Curto",
                f"Custo do menor caminho: {cost}\nSequência de vértices: {', '.join(map(str, path))}"
            )
        except nx.NetworkXNoPath:
            messagebox.showerror("Erro", "Não há caminho entre os vértices fornecidos.")

    def check_eulerian(self):
        if self.graph.number_of_nodes() == 0:
            messagebox.showerror("Erro", "O grafo está vazio. Adicione vértices ou arestas antes de verificar se é Euleriano.")
            return
        if self.directed:
            if nx.is_strongly_connected(self.graph) and all(self.graph.in_degree(n) == self.graph.out_degree(n) for n in self.graph.nodes):
                messagebox.showinfo("Grafo Euleriano", "O grafo é um Circuito Euleriano (Direcionado).")
            else:
                messagebox.showinfo("Grafo Não Euleriano", "O grafo não é um Circuito Euleriano.")
        else:
            if nx.is_connected(self.graph) and all(deg % 2 == 0 for _, deg in self.graph.degree()):
                messagebox.showinfo("Grafo Euleriano", "O grafo é Euleriano.")
            else:
                messagebox.showinfo("Grafo Não Euleriano", "O grafo não é Euleriano.")



if __name__ == "__main__":
    app = GraphTheoryApp()
    app.mainloop()
