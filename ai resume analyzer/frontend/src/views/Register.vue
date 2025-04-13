<template>
  <div class="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-8">
      <!-- Logo/Icon Placeholder -->
      <div class="flex justify-center mb-6">
        <div class="w-12 h-12 flex items-center justify-center">
          <svg class="h-full w-full text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
      </div>
      <h2 class="text-3xl font-bold text-gray-800 text-center mb-6">Create an Account</h2>
      <div v-if="error" class="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
        {{ error }}
      </div>
      <form @submit.prevent="register">
        <div class="mb-5">
          <label class="block text-gray-700 font-medium mb-2" for="email">Email</label>
          <input
            v-model="registerForm.email"
            type="email"
            id="email"
            class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="mb-5">
          <label class="block text-gray-700 font-medium mb-2" for="password">Password</label>
          <input
            v-model="registerForm.password"
            type="password"
            id="password"
            class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="Enter your password"
            required
          />
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 font-medium mb-2" for="role">Role</label>
          <select
            v-model="registerForm.role"
            id="role"
            class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            required
          >
            <option value="job_seeker">Job Seeker</option>
            <option value="recruiter">Recruiter</option>
          </select>
        </div>
        <button
          type="submit"
          class="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition font-semibold"
        >
          Register
        </button>
      </form>
      <p class="mt-6 text-center text-gray-600">
        Already have an account?
        <router-link to="/login" class="text-blue-600 hover:underline font-medium">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { useAuth } from '../composables/useAuth'

export default {
  name: 'RegisterPage',
  setup() {
    const { registerForm, error, register } = useAuth()
    return { registerForm, error, register }
  },
}
</script>