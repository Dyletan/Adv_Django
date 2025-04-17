<template>
  <div class="bg-gradient-to-br from-blue-100 to-blue-300 min-h-screen">
    <div class="container mx-auto px-6 py-12">
      <div v-if="error" class="bg-red-100 text-red-700 p-6 rounded-xl shadow-lg border-l-4 border-red-500 mb-6">
        {{ error }}
      </div>
      <div v-if="success" class="bg-green-100 text-green-700 p-6 rounded-xl shadow-lg border-l-4 border-green-500 mb-6">
        {{ success }}
        <div v-if="match_score !== null" class="mt-4 p-4 bg-green-50 rounded-lg border border-green-300">
          <p class="text-green-700"><strong>Match Score:</strong> <span class="font-semibold">{{ match_score }}/10</span></p>
          <p class="text-green-700"><strong>Feedback:</strong> <span class="font-medium">{{ feedback_text }}</span></p>
        </div>
      </div>
      <div v-if="job" class="bg-white shadow-lg rounded-xl p-8">
        <h1 class="text-3xl font-bold text-blue-700 mb-4">{{ job.title }}</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <p class="text-gray-600 mb-1"><strong class="text-gray-700">Company:</strong> {{ job.company_name }}</p>
            <p class="text-gray-600 mb-1"><strong class="text-gray-700">Location:</strong> {{ job.location }}</p>
            <p class="text-gray-600 mb-1"><strong class="text-gray-700">Type:</strong> {{ capitalize(job.employment_type) }}</p>
            <p class="text-gray-600 mb-1"><strong class="text-gray-700">Experience:</strong> {{ job.required_experience }} years</p>
          </div>
          <div>
            <p class="text-gray-600 mb-1"><strong class="text-gray-700">Skills:</strong>
              <span v-for="(skill, index) in job.required_skills_data" :key="skill.id" class="inline-block">
                {{ skill.name }}<span v-if="index < job.required_skills_data.length - 1">, </span>
              </span>
            </p>
            <p class="text-gray-500 text-sm">Posted on {{ formatDate(job.created_at) }}</p>
          </div>
        </div>
        <p class="text-gray-700 mb-6 whitespace-pre-wrap leading-relaxed">{{ job.description }}</p>

        <div v-if="isJobSeeker">
          <form @submit.prevent="applyJob" class="mt-8 flex flex-col items-start">
            <div class="mb-6">
              <label for="resume" class="block text-gray-700 text-lg font-semibold mb-3">Select Resume:</label>
              <select
                v-model="selectedResume"
                id="resume"
                class="border rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-700"
                required
              >
                <option value="" disabled>Select a resume</option>
                <option v-for="resume in resumes" :key="resume.id" :value="resume.id">
                  {{ formatFileName(resume.file_name) }}
                </option>
              </select>
            </div>
            <p v-if="resumes.length === 0" class="text-red-600 mb-4 p-3 bg-red-50 rounded-md border border-red-300">
              No resumes available. Please upload a resume first.
            </p>
            <button
              type="submit"
              class="bg-blue-600 text-white px-8 py-2 rounded-full hover:bg-blue-700 transition-all duration-300 shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
              :disabled="applying || !selectedResume"
            >
              <span v-if="applying">Applying...</span>
              <span v-else>Apply Now</span>
            </button>
          </form>
        </div>
      </div>
      <div v-else class="text-gray-600 text-center py-8">
        Loading job details...
      </div>
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
      resumes: [],
      selectedResume: '',
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
    if (this.isJobSeeker) {
      await this.fetchResumes()
    }
  },
  methods: {
    async fetchJob() {
      try {
        this.error = null
        const jobId = this.$route.params.id
        const token = localStorage.getItem('access_token')
        this.job = (await apiClient.get(`/jobs/${jobId}/`, {
          headers: {
            'Authorization': token ? `Bearer ${token}` : undefined
          }
        })).data
      } catch (err) {
        this.error = 'Failed to load job details.'
        console.error('Fetch job error:', err.response?.data, err.response?.status)
      }
    },
    async fetchResumes() {
      try {
        this.error = null
        const token = localStorage.getItem('access_token')
        this.resumes = (await apiClient.get('/jobs/resumes/', {
          headers: {
            'Authorization': token ? `Bearer ${token}` : undefined
          }
        })).data
        console.log('Fetched resumes:', this.resumes)
        if (this.resumes.length === 0) {
          this.error = 'No resumes found. Please upload a resume at /upload-resume.'
        }
      } catch (err) {
        this.error = 'Failed to load resumes.'
        console.error('Resume fetch error:', err.response?.data, err.response?.status)
      }
    },
    async applyJob() {
      if (this.applying) return
      this.applying = true
      try {
        this.error = null
        this.success = null
        const jobId = this.$route.params.id
        const token = localStorage.getItem('access_token')

        // Debug: Log the request details
        console.log('Applying to job ID:', jobId)
        console.log('Selected resume ID:', this.selectedResume)
        console.log('Access token:', token)

        const response = await apiClient.post(`/jobs/${jobId}/apply/`, {
          resume_id: this.selectedResume
        }, {
          headers: {
            'Authorization': token ? `Bearer ${token}` : undefined
          }
        })

        console.log('Apply response:', response.data)
        this.success = 'Application submitted successfully!'
        this.match_score = response.data.match_score
        this.feedback_text = response.data.feedback_text
      } catch (err) {
        console.error('Apply error:', err.response?.data, err.response?.status)
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
    },
    formatFileName(fileName) {
      return fileName.replace(/\.(pdf|docx)$/i, '')
    }
  }
}
</script>