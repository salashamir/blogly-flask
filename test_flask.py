from unittest import TestCase

from app import app
from models import db, User, Post

# use test db and dont clutter tests with sql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make flask errors be real errors, rather than html pages w error info
app.config['TESTING'] = True

# dont use flaks debugtoolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users"""
    def setUp(self):
        """Add a sample user"""
        Post.query.delete()
        User.query.delete()
        user = User(first_name="TestUserFirst", last_name="TestUserLast")
        db.session.add(user)
        db.session.commit()
        post = Post(title="TestUserFirst Post", content="Content for this user's post.", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up any foiled transsaction"""
        db.session.rollback()
        db.session.rollback()

    def test_root(self):
        """Test that slash root leads to recent posts"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("TestUserFirst Post", html)

    def test_list_users(self):
        """Test that users route displays list of users from db"""
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestUserFirst', html)

    def test_user_details(self):
        """Test that details page for a speicific user id displays info for that user"""
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>TestUserFirst TestUserLast</h1',html)
            self.assertIn('<form>', html)

    def test_add_user(self):
          """Test that user is added to db from form"""
          with app.test_client() as client:
              u = {"first_name": "TestUser2First", "last_name": "TestUser2Last", "image_url": ""}
              res = client.post("/users/new", data=u, follow_redirects=True)
              html = res.get_data(as_text=True)

              self.assertEqual(res.status_code, 200)
              self.assertIn("TestUser2First",html)

    def test_error_route(self):
        """Test that error route leads to 404 page"""
        with app.test_client() as client:
            res = client.get('/users/90000')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 404)
            self.assertIn("Looks like the page your looking for was not found!", html)

    def test_add_post(self):
        """Test that post is added from form"""
        with app.test_client() as client:
              p = {"title": "TEST POST TITLE", "content": "TEST POST CONTENT.", "user_id": self.user_id}
              res = client.post(f"/users/{self.user_id}/posts/new", data=p, follow_redirects=True)
              html = res.get_data(as_text=True)

              self.assertEqual(res.status_code, 200)
              self.assertIn("TEST POST TITLE",html)
            
