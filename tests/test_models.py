import pytest
from app import create_app, db, login
from app.models import User, Contact, Password
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='function')
def new_user(test_client):
    app = test_client.application
    with app.app_context():
        user = User(username='testuser', bithdate=2000, gender='M')
        user.password = Password(password_hash=generate_password_hash('password'))
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture(scope='function')
def new_contact(test_client, new_user):
    app = test_client.application
    with app.app_context():
        contact = Contact(user_id=new_user.id, mobile='123456789012', whatsapp='123456789012', email='test@example.com')
        db.session.add(contact)
        db.session.commit()
        return contact

@pytest.fixture(scope='function')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.metadata.clear()
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_new_user(new_user):
    assert new_user.username == 'testuser'
    assert new_user.bithdate == 2000
    assert new_user.gender == 'M'
    assert new_user.password.password_hash is not None

def test_new_contact(new_contact):
    assert new_contact.mobile == '123456789012'
    assert new_contact.whatsapp == '123456789012'
    assert new_contact.email == 'test@example.com'

def test_user_contact_relationship(test_client, new_user, new_contact):
    app = test_client.application
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        new_contact.user_id = new_user.id # Ensure contact is linked to the user in the session
        db.session.add(new_contact)
        db.session.commit()

        retrieved_user = db.session.get(User, new_user.id)
        assert retrieved_user.contact.email == 'test@example.com'

