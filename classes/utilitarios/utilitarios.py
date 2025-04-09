from PyQt6.QtGui import QColor

def interpolar_cor(c1: QColor, c2: QColor, alpha: float) -> QColor:
    r = int(c1.red() + alpha * (c2.red() - c1.red()))
    g = int(c1.green() + alpha * (c2.green() - c1.green()))
    b = int(c1.blue() + alpha * (c2.blue() - c1.blue()))
    return QColor(r, g, b)