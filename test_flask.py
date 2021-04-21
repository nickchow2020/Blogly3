from unittest import TestCase

from app import app
from models import db,User,Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_user_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Pets"""

    def setUp(self):
        db.drop_all()
        db.create_all()

        test_1 = User(first_name="shumin",last_name="zhou",image_url="www.google.com")
        test_2 = User(first_name="nick",last_name="zhou",image_url="www.google.com")
        test_3 = User(first_name="stephen",last_name="zhou",image_url="www.google.com")

        post_1 = Post(title="Inspiring 1",content="If you want something you never had,you have to do something you've never done",user_id=1)
        post_2 = Post(title="Inspiring 2",content="If you can dream it,you can do it",user_id=2)
        post_3 = Post(title="Inspiring 3",content="Difficult Roads lead to beautiful destinations",user_id=3)

        db.session.add(test_1)
        db.session.add(test_2)
        db.session.add(test_3)
        db.session.commit()

        db.session.add(post_1)
        db.session.add(post_2)
        db.session.add(post_3)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_redirect(self):
        with app.test_client() as client: 
            res = client.get("/",follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn('<a href="/users/1">shumin</a>',html)

    def test_add_new_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn("<h1>Create a user</h1>",html)

    def test_add_user_form(self):
        with app.test_client() as client:
            res = client.post('/users/new',data={'first_name':'hello','last_name':'world','user_url':'www.google.com'},follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<li><a href="/users/4">hello</a></li>',html)

    def test_user_detail(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn("<h2>shumin zhou</h2>",html)

    def test_user_post_form(self):
        with app.test_client() as client:
            res = client.get('/users/1/post/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn("<h2>Add Post For shumin</h2>",html)

    def test_user_form_post(self):
        with app.test_client() as client: 
            res = client.post('/users/2/post/new',data={"title":"inspiring_1",
                                                        "content":"The best view comes after the hardest climb",
                                                        "user_id":2},
                                                    follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn("<h2>nick zhou</h2>",html)
            self.assertIn('<a href="/posts/4">inspiring_1</a>',html)


    
