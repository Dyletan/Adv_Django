from rest_framework.test import APITestCase
from rest_framework import status
from core.models import User, Task, Project, Category, Priority
from rest_framework_simplejwt.tokens import RefreshToken

class RoleBasedAccessTest(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name='New Project', description='Test Project', start_date='2025-01-01', end_date='2025-12-31')
        self.category = Category.objects.create(name='Development')
        self.priority = Priority.objects.create(level='High')
        self.employee = User.objects.create(username='employee', email='employee@gmail.com', role='employee', password='123')
        self.admin = User.objects.create_user(username='admin', role='admin', password='123')
        self.manager = User.objects.create_user(username='manager', role='manager', password='123')
        self.task = Task.objects.create(title='Test Task', description='Test Description', project=self.project, category=self.category, priority=self.priority, assignee=self.employee, due_date='2025-02-01')

    def get_jwt_token(self, user):
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_admin_access(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_access(self):
        token = self.get_jwt_token(self.manager)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_access(self):
        token = self.get_jwt_token(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)