from rest_framework.test import APITestCase
from rest_framework import status
from core.models import User, Task, Project, Category, Priority
from rest_framework_simplejwt.tokens import RefreshToken

class RoleBasedAccessTest(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name='New Project', description='Test Project', start_date='2025-01-01', end_date='2025-12-31')
        self.category = Category.objects.create(name='Development')
        self.priority = Priority.objects.create(level='High')
        # create necessary users
        self.employee = User.objects.create_user(username='employee', email='employee@gmail.com', role='employee', password='123')
        self.other_employee = User.objects.create_user(username='other_employee', email='other_employee@gmail.com', role='employee', password='123')
        self.admin = User.objects.create_user(username='admin', role='admin', password='123')
        self.manager = User.objects.create_user(username='manager', role='manager', password='123')
        
        self.task = Task.objects.create(
            title='Test Task', description='Test Description', project=self.project,
            category=self.category, priority=self.priority, assignee=self.employee, due_date='2025-02-01'
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_admin_manage_users(self):
        # Admin can access user management
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Manager cannot access user management
        token = self.get_jwt_token(self.manager)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_manage_projects(self):
        # Manager can access project management
        token = self.get_jwt_token(self.manager)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(
            '/api/projects/', {'name': 'New Project 2', 'description': 'Another Project', 'start_date': '2025-02-01', 'end_date': '2025-12-31'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Employee cannot access project management
        token = self.get_jwt_token(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(
            '/api/projects/', {'name': 'Invalid Project', 'description': 'Should fail', 'start_date': '2025-02-01', 'end_date': '2025-12-31'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_manage_own_tasks(self):
        token = self.get_jwt_token(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Employee can view their assigned task
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Employee cannot view another employee's task
        other_task = Task.objects.create(
            title='Other Task', description='Not yours', project=self.project, category=self.category,
            priority=self.priority, assignee=self.other_employee, due_date='2025-03-01'
        )
        response = self.client.get(f'/api/tasks/{other_task.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_update_own_task(self):
        token = self.get_jwt_token(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Employee can update their assigned task
        response = self.client.patch(f'/api/tasks/{self.task.id}/', {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        # Employee cannot update another employee's task
        other_task = Task.objects.create(
            title='Other Task', description='Not yours', project=self.project, category=self.category,
            priority=self.priority, assignee=self.other_employee, due_date='2025-03-01'
        )
        response = self.client.patch(f'/api/tasks/{other_task.id}/', {'title': 'Invalid Update'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_has_full_access(self):
        # Admin can perform any action on tasks, projects, and users
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Admin can update a task
        response = self.client.patch(f'/api/tasks/{self.task.id}/', {'title': 'Admin Updated Task'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin can create a project
        response = self.client.post(
            '/api/projects/', {'name': 'Admin Project', 'description': 'Created by Admin', 'start_date': '2025-02-01', 'end_date': '2025-12-31'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)