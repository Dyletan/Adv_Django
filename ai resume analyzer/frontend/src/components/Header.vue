<template>
  <header class="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
    <nav class="container mx-auto px-6 py-4 flex items-center justify-between">
      <!-- Logo/Brand -->
      <router-link to="/" class="text-2xl font-bold tracking-tight hover:text-blue-200 transition-colors duration-200">
        Resume Analyzer
      </router-link>

      <div class="hidden md:flex space-x-8 items-center">
        <!-- Links for authenticated users -->
        <template v-if="isAuthenticated">
          <router-link v-if="userRole?.toLowerCase() === 'job_seeker'" to="/jobs" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
            Job Listings
          </router-link>
          <router-link v-if="userRole?.toLowerCase() === 'recruiter'" to="/my-listings" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
            My Listings
          </router-link>
          <!-- Job Seeker links -->
          <router-link v-if="userRole?.toLowerCase() === 'job_seeker'" to="/upload-resume" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
            Upload Resume
          </router-link>
          <!-- Recruiter links -->
          <router-link v-if="userRole?.toLowerCase() === 'recruiter'" to="/create-job" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
            Create Listing
          </router-link>
          <!-- Logout -->
          <button @click="logout" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
            Logout
          </button>
        </template>

        <!-- Links for unauthenticated users -->
        <template v-else>
          <router-link to="/login" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
            Login
          </router-link>
          <router-link to="/register" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
            Register
          </router-link>
        </template>
      </div>
    </nav>
  </header>
</template>

<script>
import { useAuth } from '../composables/useAuth'

export default {
name: 'Header',
data() {
  return {
    isMenuOpen: false,
    isAuthenticated: false,
    userRole: null,
  }
},
setup() {
  const { resetForms } = useAuth()
  return { resetForms }
},
methods: {
  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen
  },
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_role')
    this.isAuthenticated = false
    this.userRole = null
    this.resetForms()
    this.$router.push('/login')
  },
  checkAuth() {
    const token = localStorage.getItem('access_token')
    this.isAuthenticated = !!token
    this.userRole = localStorage.getItem('user_role')
    console.log('User Role:', this.userRole)
  },
},
created() {
  this.checkAuth()
  this.$router.afterEach(() => {
    this.checkAuth()
  })
},
}
</script>