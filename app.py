from PyQt5.QtWidgets import (
    QApplication,
    QWidget
)


class CRUDWindow(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication([])
    win = CRUDWindow()

    win.show()
    app.exec()
