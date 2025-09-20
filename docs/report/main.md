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