<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-6">Applications for Your Jobs</h1>
      <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
        {{ error }}
      </div>
      <div class="mb-4">
        <label for="jobFilter" class="block text-gray-700 font-medium mb-2">Filter by Job</label>
        <select
          id="jobFilter"
          v-model="selectedJobId"
          @change="fetchApplications"
          class="block w-full max-w-xs border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Jobs</option>
          <option v-for="job in jobs" :key="job.id" :value="job.id">{{ job.title }}</option>
        </select>
      </div>
      <div v-if="applications.length" class="space-y-6">
        <div v-for="app in applications" :key="app.created_at" class="bg-white shadow-md rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-2">{{ app.job_title }}</h2>
          <p class="text-gray-700 mb-2"><strong>Applicant:</strong> {{ app.user_email }}</p>
          <p class="text-gray-700 mb-2"><strong>Match Score:</strong> {{ app.match_score }}/10</p>
          <p class="text-gray-700 mb-2"><strong>Feedback:</strong> {{ app.feedback_text }}</p>
          <div class="text-gray-600 mb-2">
            <strong>Resume:</strong>
            <pre class="bg-gray-100 p-4 rounded mt-2 max-h-64 overflow-auto">{{ app.resume_text }}</pre>
          </div>
          <p class="text-gray-500 text-sm">Applied on {{ formatDate(app.created_at) }}</p>
        </div>
      </div>
      <div v-else class="text-gray-600">
        No applications found.
      </div>
    </div>
  </template>
  
  <script>
  import apiClient from '../api'
  
  export default {
    name: 'RecruiterApplicationsPage',
    data() {
      return {
        applications: [],
        jobs: [],
        selectedJobId: '',
        error: null
      }
    },
    async created() {
      await this.fetchJobs()
      await this.fetchApplications()
    },
    methods: {
      async fetchJobs() {
        try {
          this.error = null
          const response = await apiClient.get('/jobs/list/')
          this.jobs = response.data.filter(job => job.recruiter === localStorage.getItem('user_id'))
        } catch (err) {
          this.error = 'Failed to load jobs.'
        }
      },
      async fetchApplications() {
        try {
          this.error = null
          const url = this.selectedJobId ? `/jobs/applications/?job_id=${this.selectedJobId}` : '/jobs/applications/'
          const response = await apiClient.get(url)
          this.applications = response.data
        } catch (err) {
          this.error = 'Failed to load applications.'
        }
      },
      formatDate(value) {
        if (!value) return ''
        return new Date(value).toLocaleString()
      }
    }
  }
  </script>