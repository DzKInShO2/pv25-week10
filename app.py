from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlQuery
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMenu,
    QAction,
    QVBoxLayout,
    QFormLayout,
    QMessageBox,
    QLineEdit,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)


class CRUDWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(720, 480)
        self.setWindowTitle("Manajemen Buku")

        self.setupDatabase_()

        self.menubarInit_()
        self.menubarCallbacks_()

        self.widgetInit_()

        print(self.sql_conn.tables())

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
        self.table.setHorizontalHeaderLabels(
            ["ID", "Judul", "Pengarang", "Tahun"]
        )

        self.table_active_cell = -1
        self.table.cellChanged.connect(self.tableCellChanged_)
        self.table.cellActivated.connect(self.tableCellActivated_)

        save_button = QPushButton("Simpan")
        delete_button = QPushButton("Hapus Data")

        save_button.clicked.connect(self.fileSaved_)
        delete_button.clicked.connect(self.editDeleted_)

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

    def setupDatabase_(self):
        self.sql_conn = QSqlDatabase.addDatabase("QSQLITE")
        self.sql_conn.setDatabaseName("perpustakaan.sqlite")

        self.sql_conn.open()

        QSqlQuery().exec(
            """
            CREATE TABLE IF NOT EXISTS Buku (
                id INTEGER PRIMARY KEY NOT NULL,
                judul TEXT NOT NULL,
                pengarang TEXT NOT NULL,
                tahun INTEGER NOT NULL
            );
            """
        )

        self.sql_insert_book_query = QSqlQuery()
        self.sql_insert_book_query.prepare(
            """
            INSERT INTO Buku (judul, pengarang, tahun) VALUES (?, ?, ?);
            """
        )

        self.sql_delete_book_query = QSqlQuery()
        self.sql_delete_book_query.prepare(
            """
            DELETE FROM Buku WHERE id = ?;
            """
        )

        self.sql_retrieve_all_book_query = QSqlQuery()
        self.sql_retrieve_all_book_query.prepare(
            """
            SELECT * FROM Buku;
            """
        )

        self.sql_retrieve_by_title_query = QSqlQuery()
        self.sql_retrieve_by_title_query.prepare(
            """
            SELECT * FROM Buku WHERE id = ?;
            """
        )

    def tableUpdateView_(self):
        if self.sql_retrieve_all_book_query.exec():
            row = 0
            while self.sql_retrieve_all_book_query.next():
                id = int(self.sql_retrieve_all_book_query.value(0))
                title = str(self.sql_retrieve_all_book_query.value(1))
                publisher = str(self.sql_retrieve_all_book_query.value(2))
                year = int(self.sql_retrieve_all_book_query.value(3))

                self.table.setItem(row, 1, QTableWidgetItem(id))
                self.table.setItem(row, 2, QTableWidgetItem(title))
                self.table.setItem(row, 3, QTableWidgetItem(publisher))
                self.table.setItem(row, 4, QTableWidgetItem(year))

                row += 1

    def fileSaved_(self):
        title = self.record_title.text()
        publisher = self.record_author.text()
        year = self.record_year.text()

        if title == "":
            QMessageBox.warning(None,
                                "Insert Error",
                                "Judul dari buku belum terisi mohon diisi.")
            return

        if publisher == "":
            QMessageBox.warning(None,
                                "Insert Error",
                                "Pengarang dari buku belum terisi mohon diisi.")
            return

        if year == "":
            QMessageBox.warning(None,
                                "Insert Error",
                                "Tahun dari buku belum terisi mohon diisi.")
            return

        if not year.isnumeric():
            QMessageBox.warning(None,
                                "Insert Error",
                                "Tahun harus dalam bentuk angka.")
            return

        self.sql_insert_book_query.addBindValue(title)
        self.sql_insert_book_query.addBindValue(publisher)
        self.sql_insert_book_query.addBindValue(year)
        self.sql_insert_book_query.exec()

        self.tableUpdateView_()

    def fileExported_(self):
        pass

    def fileExited_(self):
        self.close()

    def editSearched_(self):
        pass

    def editDeleted_(self):
        self.tableUpdateView_()

    def tableCellChanged_(self, row, column):
        _ = row
        _ = column

    def tableCellActivated_(self, row, column):
        _ = row
        _ = column


if __name__ == "__main__":
    app = QApplication([])
    win = CRUDWindow()

    win.show()
    app.exec()
