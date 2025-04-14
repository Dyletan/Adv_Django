import { createRouter, createWebHistory } from 'vue-router'
import RegisterPage from '../views/Register.vue'
import LoginPage from '../views/Login.vue'
import JobListPage from '../views/JobList.vue'
import UploadResumePage from '../views/UploadResume.vue'
import JobCreatePage from '../views/JobCreate.vue'
import JobDetailPage from '../views/JobDetail.vue'


const routes = [
  {
    path: '/',
    redirect: () => {
      const token = localStorage.getItem('access_token')
      return token ? '/jobs' : '/login'
    },
  },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/login', name: 'Login', component: LoginPage },
  { 
    path: '/jobs', 
    name: 'JobList', 
    component: JobListPage,
    meta: { requiresAuth: true },
  },
  { 
    path: '/upload-resume', 
    name: 'UploadResume', 
    component: UploadResumePage,
    meta: { requiresAuth: true, role: 'job_seeker' },
  },
  { 
    path: '/create-job', 
    name: 'JobCreate', 
    component: JobCreatePage,
    meta: { requiresAuth: true, role: 'recruiter' },
  },
  {
    path: '/jobs/:id',
    name: 'JobDetail',
    component: JobDetailPage,
    meta: { requiresAuth: true },
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !token) {
    // Redirect to login if the route requires auth and user is not logged in
    next('/login')
  } else if (to.meta.role && to.meta.role !== userRole) {
    // Redirect to /jobs if the user doesn't have the required role
    next('/jobs')
  } else {
    next()
  }
})

export default router