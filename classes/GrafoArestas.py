from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen, QColor
from classes import GrafoVertices

'''
CLASSE DE ARESTAS

Essa classe herda de 'QGraphicsLineItem', um componente que desenha linhas e suas propriedades:
- Vértices que ela está ligando
- Cor atual
- Cor alvo
'''
class GrafoArestas(QGraphicsLineItem):
    def __init__(self, vertice1: GrafoVertices, vertice2: GrafoVertices, cor = QColor(128, 128, 128)):
        super().__init__()

        self.vertice1 = vertice1
        self.vertice2 = vertice2

        self.cor_atual = cor
        self.cor_alvo = cor

        pen = QPen(self.cor_atual)
        pen.setWidth(2)

        self.setPen(pen)
        self.setZValue(-1) # Garante que as arestas fiquem por trás dos vértices

        self.atualizar_posicao()

    # Função que ajusta as arestas conforme os vértices se movem
    def atualizar_posicao(self):
        p1 = self.vertice1.pos()
        p2 = self.vertice2.pos()

        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def atualizar_cor(self):
        pen = self.pen()
        pen.setColor(self.cor_atual)
        self.setPen(pen)

    def get_vertices(self):
        return [self.vertice1.vertice_id, self.vertice2.vertice_id]