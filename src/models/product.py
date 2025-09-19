"""
Product model
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
        