<template>
  <div class="bg-gradient-to-br from-blue-100 to-blue-300 min-h-screen">
    <div class="container mx-auto px-6 py-12" style="max-width: 1800px;">
      <section class="mb-12">
        <div class="bg-white shadow-lg rounded-xl p-6 border-t-4 border-blue-500">
          <h1 class="text-3xl font-bold text-gray-800 text-center">Job Listings</h1>
        </div>
      </section>

      <div v-if="error" class="mb-12">
        <div class="bg-red-100 text-red-700 p-4 rounded-xl shadow-lg border-l-4 border-red-500">
          {{ error }}
        </div>
      </div>

      <section class="mb-12">
        <div class="bg-white shadow-lg rounded-xl p-6 border-t-4 border-teal-500">
          <h2 class="text-2xl font-semibold text-gray-900 mb-6 text-left">Filter & Sort</h2>
          <div class="flex flex-wrap gap-4">
            <input
              v-model="filters.location"
              type="text"
              placeholder="Filter by location"
              class="flex-grow min-w-[200px] p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-blue-50 transition text-gray-700 bg-white"
            />
            <select
              v-model="filters.employment_type"
              class="flex-grow min-w-[200px] p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-blue-50 transition text-gray-700 bg-white"
            >
              <option value="">All Types</option>
              <option value="remote">Remote</option>
              <option value="hybrid">Hybrid</option>
              <option value="onsite">Onsite</option>
            </select>
            <input
              v-model="filters.skill"
              type="text"
              placeholder="Filter by skill"
              class="flex-grow min-w-[200px] p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-blue-50 transition text-gray-700 bg-white"
            />
            <select
              v-model="sortBy"
              class="flex-grow min-w-[200px] p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-blue-50 transition text-gray-700 bg-white"
            >
              <option value="created_at">Newest First</option>
              <option value="required_experience">Experience (Low to High)</option>
            </select>
          </div>
        </div>
      </section>

      <section>
        <div v-if="filteredJobs.length === 0" class="bg-white shadow-lg rounded-xl p-6 text-gray-600 text-center border-t-4 border-gray-400">
          No jobs match your filters.
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="job in filteredJobs" :key="job.id" class="job-card">
            <router-link
              :to="'/jobs/' + job.id"
              class="block p-6 rounded-xl transition-all duration-300 border-l-4 border-blue-400 h-full flex flex-col justify-between"
            >
              <div class="job-content">
                <h2 class="text-xl font-semibold text-blue-600 mb-2">{{ job.title }}</h2>
                <p class="text-teal-600 mb-1"><strong>Company:</strong> {{ job.company_name }}</p>
                <p class="text-teal-600 mb-1"><strong>Location:</strong> {{ job.location }}</p>
                <p class="text-teal-600 mb-1"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
                <p class="text-teal-600 mb-1"><strong>Experience:</strong> {{ job.required_experience }} years</p>
                <p class="text-teal-600 mb-1">
                  <strong>Skills:</strong> {{ job.required_skills_data.map(s => s.name).join(', ') }}
                </p>
                <p class="text-gray-600 mt-2 leading-relaxed">{{ truncate(job.description, 150) }}</p>
              </div>
            </router-link>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'JobListPage',
  data() {
    return {
      jobs: [],
      filters: {
        location: '',
        employment_type: '',
        skill: ''
      },
      sortBy: 'created_at',
      error: null
    }
  },
  computed: {
    filteredJobs() {
      let filtered = this.jobs
      if (this.filters.location) {
        filtered = filtered.filter(job =>
          job.location.toLowerCase().includes(this.filters.location.toLowerCase())
        )
      }
      if (this.filters.employment_type) {
        filtered = filtered.filter(job => job.employment_type === this.filters.employment_type)
      }
      if (this.filters.skill) {
        const skillLower = this.filters.skill.toLowerCase()
        filtered = filtered.filter(job =>
          job.required_skills_data.some(skill => skill.name.toLowerCase().includes(skillLower))
        )
      }
      if (this.sortBy === 'required_experience') {
        filtered = [...filtered].sort((a, b) => a.required_experience - b.required_experience)
      } else {
        filtered = [...filtered].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      }
      return filtered
    }
  },
  async created() {
    await this.fetchJobs()
  },
  methods: {
    async fetchJobs() {
      try {
        this.error = null
        const response = await apiClient.get('/jobs/')
        this.jobs = response.data
      } catch (err) {
        this.error = 'Failed to load jobs.'
      }
    },
    capitalize(value) {
      if (!value) return ''
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
    truncate(value, length) {
      if (!value) return ''
      return value.length > length ? value.substring(0, length) + '...' : value
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
