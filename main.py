import crawler_app.crawler
import crawler_app.scrapper
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit
import mysql.connector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Модели лаптопи")

        # Връзката с базата данни
        self.setup_database_connection()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Поле за филтриране по име на модела
        self.model_filter = QLineEdit(self)
        self.model_filter.setPlaceholderText("Филтър по име на модела")
        self.model_filter.setFixedSize(200, 20)  
        self.layout.addWidget(self.model_filter)

        # Бутон за филтриране
        self.filter_button = QPushButton("Филтрирай", self)
        self.filter_button.clicked.connect(self.filter_data)
        self.filter_button.setFixedSize(100, 30)  
        self.layout.addWidget(self.filter_button)

        # Бутони за сортиране
        self.sort_asc_button = QPushButton("Сортирай по цена (възходящ ред)", self)
        self.sort_asc_button.clicked.connect(lambda: self.sort_data("ASC"))
        self.sort_asc_button.setFixedSize(200, 30)  # Задаване на размери
        self.layout.addWidget(self.sort_asc_button)

        self.sort_desc_button = QPushButton("Сортирай по цена (низходящ ред)", self)
        self.sort_desc_button.clicked.connect(lambda: self.sort_data("DESC"))
        self.sort_desc_button.setFixedSize(200, 30)  # Задаване на размери
        self.layout.addWidget(self.sort_desc_button)

        # Таблица за визуализация на данните
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Извличане на данните от базата данни и визуализация в таблицата
        self.display_data()

    def setup_database_connection(self):
        # Данни за свързване с базата данни
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "Julia132293@"
        self.db_name = "laptop_base_final_3"

        # Създаване на връзка с базата данни
        self.connection = mysql.connector.connect(
            host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name
        )

    def display_data(self):
        cursor = self.connection.cursor()

        # Извличане на данните от базата данни
        cursor.execute("SELECT * FROM products_final_3")
        data = cursor.fetchall()

        # Затваряне на курсора
        cursor.close()

        # Показване на данните в таблицата
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

    def filter_data(self):
        # Филтриране на данните според въведеното име на модела
        model_name = self.model_filter.text()

        cursor = self.connection.cursor()

        # Филтриране на данните от базата данни
        query = "SELECT * FROM products_final_3 WHERE model LIKE %s"
        cursor.execute(query, (f"%{model_name}%",))
        filtered_data = cursor.fetchall()

        # Затваряне на курсора
        cursor.close()

        # Показване на филтрираните данни в таблицата
        self.table.setRowCount(len(filtered_data))
        self.table.setColumnCount(len(filtered_data[0]))
        for i, row in enumerate(filtered_data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

    def sort_data(self, order):
        cursor = self.connection.cursor()

        # Сортиране на данните от базата данни
        query = f"SELECT * FROM products_final_3 ORDER BY price {order}"
        cursor.execute(query)
        sorted_data = cursor.fetchall()

        # Затваряне на курсора
        cursor.close()

        # Показване на сортираните данни в таблицата
        self.table.setRowCount(len(sorted_data))
        self.table.setColumnCount(len(sorted_data[0]))
        for i, row in enumerate(sorted_data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

    def closeEvent(self, event):
        # Затваряне на връзката с базата данни при затваряне на приложението
        self.connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
