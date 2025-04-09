import sys
from PyQt6.QtWidgets import QApplication
from interface import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1280, 720)  # Tamanho inicial da janela (Pode ser modificado pelo usuário)
    window.show()
    sys.exit(app.exec())