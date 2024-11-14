import customtkinter as ctk
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode("dark")  # Outros modos: "light", "system"
ctk.set_default_color_theme("dark-blue")  # Outros temas: "green", "dark-blue"

class GraphTheoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Teoria dos Grafos")
        self.geometry("800x600")


        # Criando os frames principais
        self.sidebar_frame = ctk.CTkFrame(self, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Definindo a fonte Arial em negrito
        arial_bold_font = ("Arial", 35, "bold")

        # Exemplo de uso no CTkLabel
        ctk.CTkLabel(self.sidebar_frame, text="GRAPHIN", font=arial_bold_font).pack(pady=35)

        ctk.CTkEntry(self.sidebar_frame, placeholder_text="Insira os vértices... (Ex.: 1 2 3 4 ou 1, 2, 3, 4)", width=300, height=30).pack(pady=20, padx=20)

        self.algorithm_option = ctk.StringVar(value="Selecione um algoritmo")
        self.algorithm_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dijkstra", "Bellman-Ford", "Kruskal", "Prim", "Busca em Largura", "Busca em Profundidade"],
                                            variable=self.algorithm_option, width=300)
        self.algorithm_menu.pack(pady=5)

        ctk.CTkButton(self.sidebar_frame, text="Executar", command=self.run_algorithm, width=300).pack(pady=5)
        ctk.CTkButton(self.sidebar_frame, text="Limpar", command=self.run_clear_screen, width=300).pack(pady=5)

        # Widgets do frame principal (canvas para desenhar o grafo)
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Criando o canvas
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_algorithm(self):
        selected_algorithm = self.algorithm_option.get()
        print(f"Executando: {selected_algorithm}")
        # Lógica para executar o algoritmo selecionado
        self.display_graph()
  

    def run_clear_screen(self):
        print("Deve limpar a tela")

    def display_graph(self):
        # Exemplo de criação de um grafo simples usando networkx
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

        # Cria uma figura do matplotlib
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Desenha o grafo usando networkx
        nx.draw(G, ax=ax, with_labels=True, node_size=500, node_color='skyblue')

        # Embarca a figura do matplotlib no Canvas do tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas)  
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = GraphTheoryApp()
    app.mainloop()
