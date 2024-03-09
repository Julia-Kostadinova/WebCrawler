import crawler_app.crawler
import crawler_app.scrapper
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit
import mysql.connector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Модели лаптопи")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Поле за филтриране по име на модела
        self.model_filter = QLineEdit(self)
        self.model_filter.setPlaceholderText("Филтър по име на модела")
        self.layout.addWidget(self.model_filter)

        # Бутон за филтриране
        self.filter_button = QPushButton("Филтрирай", self)
        self.filter_button.clicked.connect(self.filter_data)
        self.layout.addWidget(self.filter_button)

        # Таблица за визуализация на данните
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Извличане на данните от базата данни и визуализация в таблицата
        self.display_data()

    def display_data(self):
        # Данни за свързване с базата данни
        db_host = "localhost"
        db_user = "root"
        db_password = "Julia132293@"
        db_name = "laptop_base_final_3"

        # Свързване с базата данни
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )
        cursor = connection.cursor()

        # Извличане на данните от базата данни
        cursor.execute("SELECT * FROM products_final_3")
        data = cursor.fetchall()

        # Затваряне на връзката с базата данни
        cursor.close()
        connection.close()

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

        # Данни за свързване с базата данни
        db_host = "localhost"
        db_user = "root"
        db_password = "Julia132293@"
        db_name = "laptop_base_final_3"

        # Свързване с базата данни
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )
        cursor = connection.cursor()

        # Филтриране на данните от базата данни
        query = "SELECT * FROM products_final_3 WHERE model LIKE %s"
        cursor.execute(query, (f"%{model_name}%",))
        filtered_data = cursor.fetchall()

        # Затваряне на връзката с базата данни
        cursor.close()
        connection.close()

        # Показване на филтрираните данни в таблицата
        self.table.setRowCount(len(filtered_data))
        self.table.setColumnCount(len(filtered_data[0]))
        for i, row in enumerate(filtered_data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
