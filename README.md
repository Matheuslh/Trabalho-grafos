# GRAPHIN - Sistema de Visualização e Manipulação de Grafos

Projeto feito para disciplina de Teoria dos Grafos, cadeira ministrada <br/>
pelo professor Breno Alencar na C.E.S.A.R. School

## Funcionalidades
- **Adicionar vértices e arestas**: Manual ou em lote.
- **Grafo direcionado ou não-direcionado**: Configurável.
- **Grafo valorizado**: Arestas com pesos.
- **Visualização gráfica**: Exibição do grafo.
- **Propriedades**: Ordem, tamanho, e vizinhança de vértices.
- **Carregar grafo em lote**: A partir de arquivo `.txt`.
- **Limpar grafo**: Restaura o sistema.

## Requisitos
- **Python 3.8+**
- Bibliotecas:
  - `customtkinter`
  - `networkx`
  - `matplotlib`
    
## Instruções Execução
Faça clone do respositório e navegue até o projeto:

```bash
git clone https://github.com/Matheuslh/graphin.git
cd graphin
```
Instale as dependências:

```bash
pip install -r requirements.txt
```

## Instruções de Uso

### Adicionar Elementos
1. Para adicionar um vértice ou aresta, insira os dados no campo de entrada:
   - **Vértices**: Digite apenas o número do vértice e clique em **Adicionar**.
   - **Arestas**: Digite a conexão entre dois vértices no formato `v1-v2` (sem peso) ou `v1-(peso)-v2` (com peso) e clique em **Adicionar**.

### Upload em Lote
1. Clique em **Inserir em Lote**.
2. Selecione um arquivo `.txt` com os dados dos vértices e arestas separados por vírgulas.
3. O sistema processará o arquivo e construirá o grafo automaticamente.

### Alterar Tipo de Grafo
1. Use o botão **Tornar Grafo Direcionado/Não Direcionado** para alternar o tipo do grafo.
2. Observação: Essa ação só pode ser feita antes de adicionar vértices ou arestas.

### Visualizar Grafo
1. Clique em **Visualizar Grafo** para exibir o grafo no painel principal.

### Verificar Eulerianidade
1. Clique em **Verificar Euleriano** para checar se o grafo atende às condições de um grafo Euleriano.

### Vizinhança de um Vértice
1. Insira o número do vértice no campo apropriado.
2. Clique em **Ver Adjacentes** para visualizar os vértices conectados ao vértice selecionado.

---

## Formatos de Entrada

### Inserção Manual
- **Vértices**:
  - Exemplo: `1`, `2`, `3`.
- **Arestas**:
  - Sem peso: `1-2`
  - Com peso: `1-(10)-2`

### Arquivo para Inserção em Lote
- O arquivo deve ser `.txt`, com vértices e arestas separados por vírgulas.
