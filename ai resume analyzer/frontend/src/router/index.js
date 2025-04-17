import { createRouter, createWebHistory } from 'vue-router'
import RegisterPage from '../views/Register.vue'
import LoginPage from '../views/Login.vue'
import JobListPage from '../views/JobList.vue'
import UploadResumePage from '../views/UploadResume.vue'
import JobCreatePage from '../views/JobCreate.vue'
import JobDetailPage from '../views/JobDetail.vue'
import RecruiterApplications from '../views/RecruiterApplication.vue'
import MyListingsPage from '../views/MyListings.vue'

const routes = [
  {
    path: '/',
    redirect: () => {
      const token = localStorage.getItem('access_token')
      const userRole = localStorage.getItem('user_role')?.toLowerCase()
      if (token) {
        return userRole === 'recruiter' ? '/my-listings' : '/jobs'
      }
      return '/login'
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
  },
  {
    path: '/my-listings',
    name: 'MyListings',
    component: MyListingsPage,
    meta: { requiresAuth: true, requiresRecruiter: true }
  },
  {
    path: '/recruiter-applications/:job_id',
    name: 'RecruiterApplications',
    component: RecruiterApplications,
    meta: { requiresAuth: true, requiresRecruiter: true },
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && to.meta.role !== userRole) {
    next('/jobs')
  } else {
    next()
  }
})

export default router