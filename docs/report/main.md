# Rapport Lab1 LOG430 Automne 2025 - Rémi ALBAN (ALBR 9237 0401)

## Question 1 :

Pour implémenter le UserDAO j'ai utilisé du code Python et des requêtes SQL pour communiquer avec la BD Mysql. J'ai également utilisé la méthode execute de l'objet cursor pour faire appel à la base de donnée.
```python
def update(self, user):
    """ Update given user in MySQL """
    self.cursor.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        (user.name, user.email, user.id)
    )
    self.conn.commit()

def delete(self, user_id):
    """ Delete user from MySQL with given user ID """
    self.cursor.execute(
        "DELETE FROM users WHERE id = %s",
        (user_id,)
    )
    self.conn.commit()
```

## Question 2

Je n'ai pas utilisé de SQL étant donné que MongoDB est une base de donnée NoSQL. J'ai utilisé uniquement du Python avec le module pymongo. On utilise à la place du SQL des dictionnaires pour stocker les données. Les collections sont l'équivalent des tables en SQL.

- **Sélectionner tous les utilisateurs** : utilisation de la commande `find`.  
- **Insérer un utilisateur** : utilisation de la commande `insertOne`.  
- **Mettre à jour un utilisateur** : utilisation de la commande `updateOne` avec l’opérateur `$set`.  
- **Supprimer un utilisateur** : utilisation de la commande `deleteOne`.  
- **Supprimer tous les utilisateurs** : utilisation de la commande `deleteMany`.  


```python
from models.user import User

class UserDAOMongo:
    def __init__(self):
        try:
            load_dotenv()

            db_host = os.getenv("MONGODB_HOST")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD")

            self.client = MongoClient(f"mongodb://{db_user}:{db_pass}@{db_host}:27017/")


            self.db = self.client[db_name]
            self.collection = self.db["users"]
        except FileNotFoundError:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur lors de la connexion à MongoDB :", str(e))

    def select_all(self):
        rows = self.collection.find()
        return [User(str(row["_id"]), row["name"], row["email"]) for row in rows]

    def insert(self, user):
        data = {
            "name": user.name,
            "email": user.email
        }
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, user):
        self.collection.update_one(
            {
                "_id": ObjectId(user.id)
            },
            {
                "$set": {
                    "name": user.name,
                    "email": user.email
                }
            }
        )

    def delete(self, user_id):
        self.collection.delete_one({"_id": ObjectId(user_id)})

    def delete_all(self):
        self.collection.delete_many({})
```

## Question 3

Le product_view.py a un code similaire au user_view.py. La vue n'appelle pas directement le DAO. Elle appelle le controlleur ProductController. C'est ProductController qui appelle le DAO de Product.


Voici le code de ProductView :

```python
"""
Product view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from models.product import Product
from controllers.product_controller import ProductController

class ProductView:
    @staticmethod
    def show_options():
        """ Show menu with operation options which can be selected by the product """
        controller = ProductController()
        while True:
            print("\n1. Montrer la liste de produits\n2. Ajouter un produit\n3. Quitter l'appli")
            choice = input("Choisissez une option: ")

            if choice == '1':
                products = controller.list_products()
                ProductView.show_products(products)
            elif choice == '2':
                name, brand, price = ProductView.get_inputs()
                product = Product(None, name, brand, price)
                controller.create_product(product)
            elif choice == '3':
                controller.shutdown()
                break
            else:
                print("Cette option n'existe pas.")

    @staticmethod
    def show_products(products):
        """ List products """
        print("\n".join(f"{product.id}: {product.name} ({product.brand}) - {product.price}€" for product in products))

    @staticmethod
    def get_inputs():
        """ Prompt product for inputs necessary to add a new product """
        name = input("Nom du produit : ").strip()
        brand = input("Marque du produit : ").strip()
        price = float(input("Prix du produit : ").strip())
        return name, brand, price
```

Voici le code du controlleur ProductController :

```python
from daos.product_dao import ProductDAO

class ProductController:
    def __init__(self):
        self.dao = ProductDAO()

    def list_products(self):
        """ List all products """
        return self.dao.select_all()
        
    def create_product(self, product):
        """ Create a new product based on product inputs """
        self.dao.insert(product)

    def shutdown(self):
        """ Close database connection """
        self.dao.close()
```

## Question 4


On suppose qu'on a affaire à une relation "plusieurs à plusieurs". Un produits peut être associés à plusieurs utilisateurs et un utilisateurs peut être associé à plusieurs produits. On aurait une table Achat qui va permettre de réaliser la jointure entre la table User et la table Product. Elle va avoir deux champs :
- user_id: clé étrangère pour lier l'utilisateur
- product_id: clé étrangère pour lier le produit


Elle peut contenir d'autre champs, comme la quantité acheté, la date, ...



Dans Mongodb, c'est assez différent. On va plutot stocké de cette manière là dans la collection utilisateur :

```json
[
    {
        id: 1,
        name: "John Doe",
        email: "john.doe@lorem.fr"
        products: [
            {id: 1, name: "Produit X", brand: "Super brand", price: 10.10},
            {id: 2, name: "Produit Y", brand: "Super brand2", price: 42.10},

        ]
    }
]

```

