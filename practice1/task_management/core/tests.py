from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Task, Project, Category, Priority
class RoleBasedAccessTest(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name='New Project', description='Test Project', start_date='2025-01-01', end_date='2025-12-31')
        self.category = Category.objects.create(name='Development')
        self.priority = Priority.objects.create(level='High')
        self.employee = User.objects.create(username='employee', email='employee@gmail.com', role='employee', password='123')
        self.admin = User.objects.create_user(username='admin', role='admin', password='123')
        self.manager = User.objects.create_user(username='manager', role='manager', password='123')
        self.task = Task.objects.create(title='Test Task', description='Test Description', project=self.project, category=self.category, priority=self.priority, assignee=self.employee, due_date='2025-02-01')

    def test_admin_access(self):
        self.client.login(username='admin', password='123')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_access(self):
        self.client.login(username='manager', password='123')
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_access(self):
        self.client.login(username='employee', password='123')
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)