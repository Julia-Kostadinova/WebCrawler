from bs4 import BeautifulSoup
import requests
import logging

class Scraper:

# Отваряне на HTML файла
    with open("output.html", "r", encoding="utf-8") as f:
     html_code = f.read()

# Създаване на BeautifulSoup обект
    soup = BeautifulSoup(html_code, "html.parser")

# Намиране на всички елементи с продукти
    products = soup.select(".sProduct")

# Итерация през продуктите
    for product in products:

    # Извличане на модела
        model_element = product.select_one(".short_title.fn a")
    if model_element:
        model = model_element.text.split(" ")[1]
    else:
        # Обработка на липсващ елемент
        model = "Няма информация"

    # Извличане на размера на екрана
    screen_size_element = product.select_one(".pprop li:nth-child(3) span")
    if screen_size_element:
        screen_size = screen_size_element.text
    else:
        # Обработка на липсващ елемент
        screen_size = "Няма информация"

    # Извличане на цената
    price_element = product.select_one(".row-price .price")
    if price_element:
        price = price_element.text
    else:
        # Обработка на липсващ елемент
        price = "Няма информация"

    # Принтиране на резултатите
    print(f"**Модел:** {model}")
    print(f"**Размер на екрана:** {screen_size}")
    print(f"**Цена:** {price}")
    print("-" * 20)