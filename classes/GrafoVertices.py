from PyQt6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt6.QtGui import QBrush, QPen, QColor, QPainter
from PyQt6.QtCore import Qt

'''
CLASSE DE VÉRTICES

Essa classe herda de 'QGraphicsEllipseItem', um componente que desenha círculos
com propriedades que podem ser modificadas de qualquer forma. Cada vértice tem as 
seguintes propriedades:
- Um ID.
- raio.
- Posição atual.
- Cor da borda e fundo.
- Um 'QGraphicsTextItem' filho, que exibe seu ID no centro do vértice.
'''

class GrafoVertices(QGraphicsEllipseItem):
    def __init__(self, vertice_id, x, y, raio = 20, cor = QColor(128, 128, 128)):
        super().__init__(-raio, -raio, 2*raio, 2*raio) # (posição x, posição y, largura, altura)

        self.vertice_id = vertice_id
        self.rotulo = vertice_id
        self.setPos(x, y)
        self.raio = raio

        self.cor_atual = cor
        self.cor_alvo = cor

        self.update()

        self.vx = 0.0
        self.vy = 0.0

        self.fixo = False

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        ) # Flags que permitem que os vértices sejam selecionados e movidos.
        self.setAcceptHoverEvents(True)

        # Texto no centro do vértice
        self.texto = QGraphicsTextItem(str(self.rotulo), self)
        self.texto.setDefaultTextColor(Qt.GlobalColor.white)
        limite = self.texto.boundingRect()
        self.texto.setPos(-limite.width()/2, -limite.height()/2)

    def paint(self, painter: QPainter, opcao, widget = None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) # Ativar suavização dos cantos dos objetos.

        # Cor dos cantos do vértice.
        pen = QPen(Qt.GlobalColor.black)
        painter.setPen(pen)

        # Cor de fundo do vértice.
        brush = QBrush(self.cor_atual)
        painter.setBrush(brush)

        # Desenhar o vértice.
        painter.drawEllipse(self.rect())
    
    def alterar_rotulo(self, novo_rotulo):
        self.rotulo = novo_rotulo
        self.texto.setPlainText(str(self.rotulo))
        limite = self.texto.boundingRect()
        self.texto.setPos(-limite.width()/2, -limite.height()/2)