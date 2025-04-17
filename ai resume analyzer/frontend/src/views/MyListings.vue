<template>
  <div class="bg-gradient-to-br from-blue-100 to-blue-300 min-h-screen">
    <div class="container mx-auto px-6 py-12" style="max-width: 1800px;">
      <section class="mb-12">
        <div class="bg-white shadow-lg rounded-xl p-6 border-t-4 border-blue-500">
          <h1 class="text-3xl font-bold text-gray-800 text-center">My Listings</h1>
        </div>
      </section>

      <div v-if="error" class="mb-12">
        <div class="bg-red-100 text-red-700 p-4 rounded-xl shadow-lg border-l-4 border-red-500">
          {{ error }}
        </div>
      </div>

      <section>
        <div v-if="jobs.length === 0" class="bg-white shadow-lg rounded-xl p-6 text-gray-600 text-center border-t-4 border-gray-400">
          No job listings created.
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="job in jobs" :key="job.id" class="job-card">
            <router-link
              :to="`/recruiter-applications/${job.id}`"
              class="block p-6 rounded-xl transition-all duration-300 border-l-4 border-blue-400 h-full flex flex-col justify-between"
            >
              <div class="job-content">
                <h2 class="text-xl font-semibold text-blue-600 mb-2">{{ job.title }}</h2>
                <p class="text-teal-600 mb-1"><strong>Company:</strong> {{ job.company_name }}</p>
                <p class="text-teal-600 mb-1"><strong>Location:</strong> {{ job.location }}</p>
                <p class="text-teal-600 mb-1"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
                <p class="text-gray-600 mb-4 leading-relaxed">{{ truncate(job.description, 100) }}</p>
              </div>
            </router-link>
          </div>
        </div>
      </section>
      <div class="mt-8 flex justify-center">
        <router-link
          to="/create-job"
          style="
            background-color: #3b82f6;
            border-radius: 9999px;
            color: #fff;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            transition-duration: 300ms;
            transition-property: all;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            &:hover {
              background-color: #2563eb;
              box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.12);
              transform: translateY(-2px);
            }
          "
        >
          Create New Listing
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'MyListingsPage',
  data() {
    return {
      jobs: [],
      error: null
    }
  },
  async created() {
    await this.fetchJobs()
  },
  methods: {
    async fetchJobs() {
      try {
        this.error = null
        const response = await apiClient.get('/jobs/my-listings/')
        this.jobs = response.data
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load listings.'
      }
    },
    capitalize(value) {
      if (!value) return ''
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
    truncate(text, length) {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }
  }
}
</script>

<style scoped>
.job-card {
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 0.75rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 1.5rem;
}

.job-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  background-color: #f0f4f8;
}

.job-card a {
  display: flex;
  flex-direction: column;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.job-content {
  padding: 1.5rem;
}
</style>