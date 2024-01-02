import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from server import app, db, Task

class TestAppWithOAuth(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, this is your local server!')

    def test_callback_authorization(self):
        # Redirect to TickTick OAuth authorization
        response = self.client.get('/callback')
        expected_location = 'https://ticktick.com/oauth/authorize'
        # self.assertIn(expected_location, response.location)

    def test_oauth_authorization(self):
        # Redirect to TickTick OAuth authorization
        response = self.client.get('/login')
        expected_location = 'https://ticktick.com/oauth/authorize'
        # self.assertIn(expected_location, response.location)


    # def test_oauth_callback(self):
    #     # Simulate TickTick OAuth callback
    #     response = self.client.get('/callback?state=test_state&code=test_code')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Your Expected Content', response.data)  # Adjust based on your expected content

    # def test_tasks_with_oauth(self):
    #     # Ensure OAuth token is available in the session (replace with actual token)
    #     with self.client.session_transaction() as sess:
    #         sess['oauth_token'] = {'access_token': 'your_access_token', 'token_type': 'Bearer'}

    #     # Access tasks endpoint with OAuth token
    #     response = self.client.get('/tasks')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'your_expected_task_data', response.data)  # Adjust based on your expected data

    # def test_ticktick_callback(self):
    #     data = {'title': 'Test Task', 'description': 'This is a test task'}
    #     response = self.client.post('/ticktick-callback', json=data)
    #     self.assertEqual(response.status_code, 200)

    #     # Check if the task is stored in the database
    #     task = Task.query.first()
    #     self.assertIsNotNone(task)
    #     self.assertEqual(task.title, 'Test Task')
    #     self.assertEqual(task.description, 'This is a test task')

if __name__ == '__main__':
    unittest.main()
