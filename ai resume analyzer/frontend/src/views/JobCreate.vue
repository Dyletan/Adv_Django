<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-6">Create Job Listing</h1>
      <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
        {{ error }}
      </div>
      <div v-if="success" class="bg-green-100 text-green-700 p-4 rounded mb-4">
        {{ success }}
      </div>
      <form @submit.prevent="createJob" class="max-w-md">
        <div class="mb-4">
          <label for="title" class="block text-gray-700 font-medium mb-2">Job Title</label>
          <input
            type="text"
            id="title"
            v-model="form.title"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div class="mb-4">
          <label for="description" class="block text-gray-700 font-medium mb-2">Job Description</label>
          <textarea
            id="description"
            v-model="form.description"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="5"
            required
          ></textarea>
        </div>
        <div class="mb-4">
          <label for="company" class="block text-gray-700 font-medium mb-2">Company</label>
          <input
            type="text"
            id="company"
            v-model="form.company"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div class="mb-4">
          <label for="location" class="block text-gray-700 font-medium mb-2">Location</label>
          <input
            type="text"
            id="location"
            v-model="form.location"
            class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors duration-200"
        >
          Create Listing
        </button>
      </form>
    </div>
  </template>
  
  <script>
  import apiClient from '../api'
  
  export default {
    name: 'JobCreatePage',
    data() {
      return {
        form: {
          title: '',
          description: '',
          company: '',
          location: '',
        },
        error: null,
        success: null,
      }
    },
    methods: {
      async createJob() {
        try {
          this.error = null
          this.success = null
          await apiClient.post('/jobs/create/', this.form) // Removed unused 'response' variable
          this.success = 'Job listing created successfully!'
          this.resetForm()
          setTimeout(() => {
            this.$router.push('/jobs')
          }, 2000) // Redirect to job listings after 2 seconds
        } catch (err) {
          this.error = err.response?.data?.error || 'Failed to create job listing.'
        }
      },
      resetForm() {
        this.form.title = ''
        this.form.description = ''
        this.form.company = ''
        this.form.location = ''
      },
    },
  }
  </script>