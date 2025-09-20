from daos.user_dao_mongo import UserDAOMongo
from models.user import User


def test_user_select():
    dao = UserDAOMongo()

    user_list = dao.select_all()
    assert len(user_list) >= 0

def test_user_insert():
    dao = UserDAOMongo()

    user = User(None, 'Margaret Hamilton', 'hamilton@example.com')
    dao.insert(user)
    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert user.email in emails

def test_user_update():
    dao = UserDAOMongo()

    user = User(None, 'Charles Babbage', 'babage@example.com')
    assigned_id = dao.insert(user)

    corrected_email = 'babbage@example.com'
    user.id = assigned_id
    user.email = corrected_email

    dao.update(user)

    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert corrected_email in emails

def test_user_delete():
    dao = UserDAOMongo()

    user = User(None, 'Douglas Engelbart', 'engelbart@example.com')
    assigned_id = dao.insert(user)
    dao.delete(assigned_id)

    user_list = dao.select_all()
    emails = [u.email for u in user_list]
    assert user.email not in emails
    