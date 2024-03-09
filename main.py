import crawler_app.crawler
import crawler_app.scrapper
import mysql.connector


# Информация за свързване
db_host = "localhost"
db_user = "root"
db_password = "Julia132293@"

# Проверка за съществуване на база данни
try:
    connection = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database="laptop_base"
    )
    print("Базата данни 'laptop_base' съществува.")
    # Изпълнете код, който използва базата данни

except mysql.connector.Error as err:
    if err.errno == 1049:  # Database doesn't exist
        print("Базата данни 'laptop_base' не съществува.")
        # Създайте базата данни и таблицата
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS laptop_base")
        cursor.execute("USE laptop_base")
        cursor.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                model VARCHAR(255) NOT NULL,
                screen_size DECIMAL(5,2) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            );
        """)
        cursor.close()
        connection.close()

        # Свързване с новосъздадената база данни
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database="laptop_base"
        )
        print("Създадена е базата данни 'laptop_base'.")

    else:
        print(f"Грешка при свързване: {err}")

# Затваряне на връзката
finally:
    if connection is not None:
        connection.close()

if __name__=='__main__':
    url = 'https://www.jarcomputers.com/Laptopi_cat_2.html?ref=c_1'

