<template>
    <header class="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <nav class="container mx-auto px-6 py-4 flex items-center justify-between">
        <!-- Logo/Brand -->
        <router-link to="/" class="text-2xl font-bold tracking-tight hover:text-blue-200 transition-colors duration-200">
          Resume Analyzer
        </router-link>
  
        <!-- Desktop Navigation -->
        <div class="hidden md:flex space-x-8 items-center">
          <!-- Links for authenticated users -->
          <template v-if="isAuthenticated">
            <router-link to="/jobs" class="text-lg font-medium hover:text-blue-200 hover:scale-105 transform transition-all duration-200">
              Job Listings
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
  
        <!-- Mobile Menu Button -->
        <button @click="toggleMenu" class="md:hidden focus:outline-none">
          <svg class="h-6 w-6 hover:text-blue-200 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="isMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'"></path>
          </svg>
        </button>
      </nav>
  
      <!-- Mobile Menu -->
      <div v-if="isMenuOpen" class="md:hidden bg-blue-700 transition-all duration-300">
        <div class="container mx-auto px-6 py-4 flex flex-col space-y-4">
          <template v-if="isAuthenticated">
            <router-link to="/jobs" @click="toggleMenu" class="text-lg font-medium hover:text-blue-200 hover:bg-blue-600 py-2 px-4 rounded-md transition-all duration-200">
              Job Listings
            </router-link>
            <router-link v-if="userRole?.toLowerCase() === 'job_seeker'" to="/upload-resume" @click="toggleMenu" class="text-lg font-medium hover:text-blue-200 hover:bg-blue-600 py-2 px-4 rounded-md transition-all duration-200">
              Upload Resume
            </router-link>
            <router-link v-if="userRole?.toLowerCase() === 'recruiter'" to="/create-job" @click="toggleMenu" class="text-lg font-medium hover:text-blue-200 hover:bg-blue-600 py-2 px-4 rounded-md transition-all duration-200">
              Create Listing
            </router-link>
            <button @click="logout" class="text-lg font-medium text-left hover:text-blue-200 hover:bg-blue-600 py-2 px-4 rounded-md transition-all duration-200">
              Logout
            </button>
          </template>
          <template v-else>
            <router-link to="/login" @click="toggleMenu" class="text-lg font-medium hover:text-blue-200 hover:bg-blue-600 py-2 px-4 rounded-md transition-all duration-200">
              Login
            </router-link>
            <router-link to="/register" @click="toggleMenu" class="text-lg font-medium hover:text-blue-200 hover:bg-blue-600 py-2 px-4 rounded-md transition-all duration-200">
              Register
            </router-link>
          </template>
        </div>
      </div>
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