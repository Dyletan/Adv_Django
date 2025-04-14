<template>
    <div class="container mx-auto px-4 py-8">
      <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
        {{ error }}
      </div>
      <div v-if="success" class="bg-green-100 text-green-700 p-4 rounded mb-4">
        {{ success }}
        <div v-if="match_score !== null" class="mt-2">
          <p><strong>Match Score:</strong> {{ match_score }}/10</p>
          <p><strong>Feedback:</strong> {{ feedback_text }}</p>
        </div>
      </div>
      <div v-if="job" class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-3xl font-bold mb-4">{{ job.title }}</h1>
        <p class="text-gray-700 mb-2"><strong>Company:</strong> {{ job.company_name }}</p>
        <p class="text-gray-700 mb-2"><strong>Location:</strong> {{ job.location }}</p>
        <p class="text-gray-700 mb-2"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
        <p class="text-gray-700 mb-2"><strong>Experience:</strong> {{ job.required_experience }} years</p>
        <p class="text-gray-700 mb-2">
          <strong>Skills:</strong> {{ job.required_skills_data.map(s => s.name).join(', ') }}
        </p>
        <p class="text-gray-600 mb-4 whitespace-pre-wrap">{{ job.description }}</p>
        <p class="text-gray-500 text-sm mb-4">Posted on {{ formatDate(job.created_at) }}</p>
        <button
          v-if="isJobSeeker"
          @click="applyJob"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors duration-200"
          :disabled="applying"
        >
          {{ applying ? 'Applying...' : 'Apply Now' }}
        </button>
      </div>
      <div v-else class="text-gray-600">
        Loading job details...
      </div>
    </div>
  </template>
  
  <script>
  import apiClient from '../api'
  
  export default {
    name: 'JobDetailPage',
    data() {
      return {
        job: null,
        error: null,
        success: null,
        applying: false,
        match_score: null,
        feedback_text: null
      }
    },
    computed: {
      isJobSeeker() {
        return localStorage.getItem('user_role') === 'job_seeker'
      }
    },
    async created() {
      await this.fetchJob()
    },
    methods: {
      async fetchJob() {
        try {
          this.error = null
          const jobId = this.$route.params.id
          this.job = (await apiClient.get(`/jobs/${jobId}/`)).data
        } catch (err) {
          this.error = 'Failed to load job details.'
        }
      },
      async applyJob() {
        if (this.applying) return
        this.applying = true
        try {
          this.error = null
          this.success = null
          const jobId = this.$route.params.id
          const response = await apiClient.post(`/jobs/${jobId}/apply/`)
          this.success = 'Application submitted successfully!'
          this.match_score = response.data.match_score
          this.feedback_text = response.data.feedback_text
        } catch (err) {
          this.error = err.response?.data?.error || 'Failed to apply.'
        } finally {
          this.applying = false
        }
      },
      capitalize(value) {
        if (!value) return ''
        return value.charAt(0).toUpperCase() + value.slice(1)
      },
      formatDate(value) {
        if (!value) return ''
        return new Date(value).toLocaleDateString()
      }
    }
  }
  </script>