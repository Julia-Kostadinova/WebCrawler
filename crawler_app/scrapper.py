from bs4 import BeautifulSoup
import mysql.connector

# Отваряне на HTML файла
with open("output.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Създаване на BeautifulSoup обект
soup = BeautifulSoup(html_code, "html.parser")

# Намиране на всички елементи с продукти
products = soup.select(".sProduct")

# Информация за свързване
db_host = "localhost"
db_user = "root"
db_password = "Julia132293@"

# Проверка за съществуване на база данни
try:
    connection = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database="laptop_base_final_3"
    )
    print("Базата данни 'laptop_base_final_3' съществува.")
    # Изпълнете код, който използва базата данни

except mysql.connector.Error as err:
    if err.errno == 1049:  # Database doesn't exist
        print("Базата данни 'laptop_base_final_3' не съществува.")
        # Създайте базата данни и таблицата
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS laptop_base_final_3")
        cursor.execute("USE laptop_base_final_3")
        cursor.execute("""
            CREATE TABLE products_final_3 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                model VARCHAR(255) NOT NULL,
                screen_size VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            );
        """)

# Свързване с базата данни
connection = mysql.connector.connect(
    host=db_host, user=db_user, password=db_password, database="laptop_base_final_3"
)

# Итерация през продуктите
for product in products:
    model_element = product.select_one(".short_title.fn a")
    model = model_element.text.split(" ")[1] if model_element else "Няма информация"
    
    screen_size_element = product.select_one(".pprop li:nth-child(3) span")
    screen_size = float(screen_size_element.text) if (screen_size_element and screen_size_element.text.isdigit()) else 0
    
    price_element = product.select_one(".row-price .price")
    price = float(price_element.text.replace(" лв", "").replace(",", ".")) if (price_element and price_element.text.replace(" лв", "").replace(",", ".").replace(".", "", 1).isdigit()) else 0

    # Вмъкване на данните в базата данни
    cursor = connection.cursor()
    sql = "INSERT INTO products_final_3 (model, screen_size, price) VALUES (%s, %s, %s)"
    values = (model, screen_size, price)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()

# Затваряне на връзката с базата данни
connection.close()
