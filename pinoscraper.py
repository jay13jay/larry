import requests
from bs4 import BeautifulSoup
import json

class MenuItem:
    def __init__(self, name, description, ingredients, price):
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "price": self.price
        }

def scrape_menu(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    menu_items = []

    for item in soup.select('div[data-hook="restaurants.menu.item-view-6de34876-b456-4f1d-bd40-84ae3c9237b3"]'):
        name = item.select_one('button[data-hook="restaurants.menu.item-view.title"] span').text.strip()
        description = item.select_one('div[data-hook="restaurants.menu.item-view.labels"]').text.strip() if item.select_one('div[data-hook="restaurants.menu.item-view.labels"]') else ""
        ingredients = ""  # Assuming ingredients are not available in the provided HTML structure
        price = item.select_one('span[data-hook="price-view.price"]').text.strip()

        menu_item = MenuItem(name, description, ingredients, price)
        menu_items.append(menu_item)

    return menu_items

if __name__ == "__main__":
    url = "https://www.pinosrva.com/order-online/"
    menu_items = scrape_menu(url)
    
    menu_items_dict = [item.to_dict() for item in menu_items]
    
    with open('files/pino_menu.json', 'w') as file:
        json.dump(menu_items_dict, file, indent=4)
