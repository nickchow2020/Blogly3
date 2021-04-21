from unittest import TestCase

from app import app
from models import db,User,Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_user_db'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all() 

class UserModelTestCase(TestCase):

    def setUp(self):
        user1 = User(first_name='shumin',last_name='zhou',image_url='www.google.com')
        user2 = User(first_name='nick',last_name='zhou',image_url='www.googlesss.com')
        db.session.add(user1)
        db.session.add(user2)

    def tearDown(self):
        db.session.rollback()

    def test_greeting(self):
        user = User.query.get(1)
        self.assertEqual(user.greeting(),"Hi,my name is shumin zhou!")

    def test_add_new_user(self):
        user = User(first_name='stephen',last_name='zhou',image_url='www.google.com')
        db.session.add(user)
        db.session.commit()

        shumin = User.query.get(3)
        self.assertEqual(shumin,user)

    def test_new_post(self):
        post = Post(title="inspiring_1",content="The best view comes after hardest climb",user_id=1)
        db.session.add(post)
        db.session.commit()

        nick = User.query.get(2)
        new_post = Post.query.get(1)

        self.assertEqual(nick.first_name,"nick")
        self.assertEqual(new_post,post)


