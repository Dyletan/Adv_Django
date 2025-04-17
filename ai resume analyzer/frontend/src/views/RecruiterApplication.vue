<template>
  <div class="bg-gradient-to-br from-blue-100 to-blue-300 min-h-screen">
    <div class="container mx-auto" style="padding-left: 24px; padding-right: 24px; padding-top: 48px; padding-bottom: 48px;">
      <section class="mb-12" style="padding-left: 24px; padding-right: 24px;">
        <h1 class="text-3xl font-bold text-gray-800 text-center">Applicants for {{ jobTitle }}</h1>
      </section>
      <div v-if="error" class="mb-12" style="padding-left: 24px; padding-right: 24px;">
        <div class="bg-red-100 text-red-700 p-4 rounded-xl shadow-lg border-l-4 border-red-500">
          {{ error }}
        </div>
      </div>
      <section v-if="applications.length" class="space-y-6" style="padding-left: 24px; padding-right: 24px;">
        <div v-for="(app, index) in applications" :key="app.created_at" class="bg-white shadow-lg rounded-xl p-6 transition-all duration-300 border-t-4 border-blue-400">
          <div class="space-y-4">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold">
                {{ app.user_email.charAt(0).toUpperCase() }}
              </div>
              <div>
                <p class="text-lg font-semibold text-blue-700">Applicant: <span class="text-gray-800">{{ app.user_email }}</span></p>
                <p class="text-gray-600">Applied on: <span class="text-teal-600">{{ formatDate(app.created_at) }}</span></p>
              </div>
            </div>
            <p class="text-teal-600"><strong>Match Score:</strong> <span class="text-gray-800">{{ app.match_score }}/10</span></p>
            <p class="text-teal-600"><strong>Feedback:</strong> <span class="text-gray-800">{{ app.feedback_text }}</span></p>
            <div class="text-gray-700">
              <strong class="block mb-2">Resume:</strong>
              <pre class="bg-gray-100 p-4 rounded mt-2 max-h-64 overflow-auto">{{ app.resume_text }}</pre>
            </div>
          </div>
          <hr v-if="index < applications.length - 1" style="margin-top: 24px; margin-bottom: 24px; border-color: #d1d5db;">
        </div>
      </section>
      <section v-else class="bg-white shadow-lg rounded-xl p-6 text-gray-600 text-center border-t-4 border-gray-400" style="padding-left: 24px; padding-right: 24px;">
        No applicants found for this job.
      </section>
      <div class="mt-8 flex justify-center" style="padding-left: 24px; padding-right: 24px;">
        <router-link to="/my-listings" class="inline-flex items-center text-blue-600 hover:text-blue-800 hover:underline transition-colors duration-200 font-medium">
          Back to My Listings
        </router-link>
      </div>
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
      jobTitle: '',
      error: null
    }
  },
  async created() {
    await this.fetchApplications()
  },
  methods: {
    async fetchApplications() {
      try {
        this.error = null
        const jobId = this.$route.params.job_id
        const response = await apiClient.get(`/jobs/applications/${jobId}/`)
        this.applications = response.data
        this.jobTitle = response.data.length ? response.data[0].job_title : 'Job'
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load applicants.'
      }
    },
    formatDate(value) {
      if (!value) return ''
      return new Date(value).toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit'
      });
    }
  }
}
</script>