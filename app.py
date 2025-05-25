from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMenu,
    QAction,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QTableWidget
)


class CRUDWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(720, 480)
        self.setWindowTitle("Manajemen Buku")

        self.menubarInit_()
        self.menubarCallbacks_()

        self.widgetInit_()

    def menubarInit_(self):
        menubar = self.menuBar()

        # Buat aksi untuk menu file
        self.file_save_action_ = QAction("Simpan", self)
        self.file_export_action_ = QAction("Expor ke CSV", self)
        self.file_exit_action_ = QAction("Keluar", self)

        # Tambah aksi ke menu file
        file_menu = QMenu("File", self)
        file_menu.addAction(self.file_save_action_)
        file_menu.addAction(self.file_export_action_)
        file_menu.addAction(self.file_exit_action_)

        # Buat aksi untuk menu edit
        self.edit_search_action_ = QAction("Cari Judul", self)
        self.edit_delete_action_ = QAction("Hapus Data", self)

        # Tambah aksi ke menu edit
        edit_menu = QMenu("Edit", self)
        edit_menu.addAction(self.edit_search_action_)
        edit_menu.addAction(self.edit_delete_action_)

        # Tambah menu ke menubar
        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)

    def menubarCallbacks_(self):
        # Callback/Signal untuk menu file
        self.file_save_action_.triggered.connect(self.fileSaved_)
        self.file_export_action_.triggered.connect(self.fileExported_)
        self.file_exit_action_.triggered.connect(self.fileExited_)

        # Callback/Signal untuk menu file
        self.edit_search_action_.triggered.connect(self.editSearched_)
        self.edit_delete_action_.triggered.connect(self.editDeleted_)

    def widgetInit_(self):
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Cari judul...")

        self.record_title = QLineEdit()
        self.record_author = QLineEdit()
        self.record_year = QLineEdit()

        self.table = QTableWidget()
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Pengarang", "Tahun"])

        save_button = QPushButton("Simpan")
        delete_button = QPushButton("Hapus Data")

        widget = QWidget()
        root = QVBoxLayout()
        form = QFormLayout()

        form.addRow(QLabel("Judul"), self.record_title)
        form.addRow(QLabel("Pengarang"), self.record_author)
        form.addRow(QLabel("Tahun"), self.record_year)

        root.addLayout(form)
        root.addWidget(save_button)
        root.addWidget(self.search_line)
        root.addWidget(self.table)
        root.addWidget(delete_button)
        widget.setLayout(root)

        self.setCentralWidget(widget)

    def fileSaved_(self):
        pass

    def fileExported_(self):
        pass

    def fileExited_(self):
        self.close()

    def editSearched_(self):
        pass

    def editDeleted_(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    win = CRUDWindow()

    win.show()
    app.exec()
