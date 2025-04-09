from PyQt6.QtWidgets import QMainWindow, QToolBar
from PyQt6.QtGui import QAction
from classes import GrafoWidget

'''
CLASSE DA JANELA PRINCIPAL

Essa classe herda do componente 'QMainWindow' e integra a classe GrafoWidget como seu conteúdo principal. Além disso, ela cria uma barra de ferramentas para ações globais, como:
- Adicionar vértices.
- Adicionar arestas.
- Resetar o grafo.
'''
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grafla") # Nome da janela

        self.grafoWidget = GrafoWidget()
        self.setCentralWidget(self.grafoWidget)

        toolbar = QToolBar('Barra de Ferramentas')
        self.addToolBar(toolbar)

        botao_adicionar_vertice = QAction('Adicionar vertice', self)
        botao_adicionar_vertice.triggered.connect(lambda: self.grafoWidget.adicionar_vertice())
        toolbar.addAction(botao_adicionar_vertice)

        botao_adicionar_aresta = QAction('Adicionar aresta', self)
        botao_adicionar_aresta.triggered.connect(self.comecar_aresta)
        toolbar.addAction(botao_adicionar_aresta)

        botao_resetar = QAction('Resetar', self)
        botao_resetar.triggered.connect(lambda: self.grafoWidget.resetar_grafo())
        toolbar.addAction(botao_resetar)

    def comecar_aresta(self):
        if self.grafoWidget.vertice_selecionado:
            self.grafoWidget.comeco_aresta = self.grafoWidget.vertice_selecionado