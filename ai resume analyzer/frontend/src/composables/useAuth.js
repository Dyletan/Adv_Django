import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api'

export function useAuth() {
  const router = useRouter()

  const loginForm = reactive({
    email: '',
    password: '',
  })

  const registerForm = reactive({
    email: '',
    password: '',
    role: 'job_seeker',
  })

  const error = ref(null)

  const resetForms = () => {
    loginForm.email = ''
    loginForm.password = ''
    registerForm.email = ''
    registerForm.password = ''
    registerForm.role = 'job_seeker'
    error.value = null
  }

  const login = async () => {
    try {
      error.value = null
      console.log('Login attempt:', loginForm)
      const response = await apiClient.post('/auth/login/', loginForm)
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      localStorage.setItem('user_role', loginForm.email.includes('recruiter') ? 'recruiter' : 'job_seeker')
      router.push('/jobs')
    } catch (err) {
      console.error('Login error:', err.response?.data)
      error.value = err.response?.data?.error || 'Login failed'
    }
  }

  const register = async () => {
    try {
      error.value = null
      console.log('Register attempt:', registerForm)
      await apiClient.post('/auth/register/', registerForm)
      error.value = 'Registration successful! Please verify your email.'
      router.push('/login')
    } catch (err) {
      console.error('Register error:', err.response?.data)
      const emailError = err.response?.data?.email?.[0]
      if (emailError && emailError.includes('user with this email already exists')) {
        error.value = 'This email is already registered. Please use a different email or log in.'
      } else {
        error.value = emailError || JSON.stringify(err.response?.data) || 'Registration failed'
      }
    }
  }

  return { loginForm, registerForm, error, login, register, resetForms }
}