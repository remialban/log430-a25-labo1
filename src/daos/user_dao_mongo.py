from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
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
