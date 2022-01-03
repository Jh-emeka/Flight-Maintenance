from unittest import TestCase
from app import app


# for testing this application, one of the already added admins will be used("username: Hashed, Password:Hashed123.")


class Test(TestCase):
    def test_login(self):
        self.client = app.test_client()
        response = self.client.post(
            '/login',
            data=dict(username="Hashed", password="Hashed123."),
            follow_redirects=True
        )
        self.assertIn(b'Welcome Hashed', response.data)

    def test_incorrect_login(self):
        self.client = app.test_client()
        response = self.client.post(  # Attempt Login
            '/login',
            data=dict(username="Hashed", password="Hashed234."),  # Login details provided are wrong
            follow_redirects=True
        )
        self.assertIn(b'Login failed, Incorrect username or password', response.data)  # statement should be found in
        # response data should include

    def test_unauthorised_user(self):
        self.client = app.test_client()
        self.client = app.test_client()
        self.client.post(
            '/login',
            data=dict(username="Hashed", password="Hashed234."),  # Login details provided are wrong
            follow_redirects=True
        )
        user = self.client.get('/newAdmin')  # Route to this page after attempting login
        self.assertIn(b'Please log in to access this page', user.data)  # statement should be found in response data

    def test_authorised_user(self):
        self.client = app.test_client()
        self.client.post(
            '/login',
            data=dict(username="Hashed", password="Hashed123."),  # Login details provided are correct
            follow_redirects=True
        )
        user = self.client.get('/newAdmin')  # Route to this page after attempting login
        self.assertIn(b'New Admin', user.data)  # statement should be found in response data

    def test_new_admin(self):
        self.client = app.test_client()
        self.client.post(
            '/login',
            data=dict(username="Hashed", password="Hashed123."),
            follow_redirects=True
        )
        user = self.client.post('/addAdmin', data=dict(username="Azeez", Pwd="Fakeadmin1.", Pwd2="Fakeadmin1."),
                                follow_redirects=True)
        self.assertIn(b'username already exists, please choose a different username', user.data)

    def test_pass_not_match(self):
        self.client = app.test_client()

        response = self.client.post(
            '/addAdmin',
            data=dict(username="John", Pwd="Fakeadmin1.", Pwd2="Fakeadmin2."),
            follow_redirects=True
        )
        self.assertIn(b'Passwords do not match', response.data)

    def test_username_exists(self):
        self.client = app.test_client()

        response = self.client.post(
            '/addAdmin',
            data=dict(username="Hashed", Pwd="Fakeadmin1.", Pwd2="Fakeadmin1."),
            follow_redirects=True
        )
        self.assertIn(b'username already exists, please choose a different username', response.data)

    def test_invalid_details(self):
        self.client = app.test_client()
        response = self.client.post(
            '/login',
            data=dict(username="", password=""),  # Log into the system with no details provided
            follow_redirects=True
        )
        self.assertIn(b'Invalid details', response.data)  # system should handle this error and not crash

    def test_logout(self):
        self.client = app.test_client()
        self.client.post(
            '/login',
            data=dict(username="Hashed", password="Hashed123."),  # Log into the system, details
            follow_redirects=True
        )
        self.client.get('/logout')  # Then log out
        user = self.client.get('/newAdmin')  # Attempt to route to the new admin page

        self.assertIn(b'Please log in to access this page', user.data)  # access is denied since user is logged out
