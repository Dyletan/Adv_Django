<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Job Listings</h1>
    <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
      {{ error }}
    </div>
    <div class="mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <input
          v-model="filters.location"
          type="text"
          placeholder="Filter by location"
          class="border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select v-model="filters.employment_type" class="border border-gray-300 rounded py-2 px-3">
          <option value="">All Types</option>
          <option value="remote">Remote</option>
          <option value="hybrid">Hybrid</option>
          <option value="onsite">Onsite</option>
        </select>
        <input
          v-model="filters.skill"
          type="text"
          placeholder="Filter by skill"
          class="border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select v-model="sortBy" class="border border-gray-300 rounded py-2 px-3">
          <option value="created_at">Newest First</option>
          <option value="required_experience">Experience (Low to High)</option>
        </select>
      </div>
    </div>
    <div v-if="filteredJobs.length === 0" class="text-gray-600">
      No jobs match your filters.
    </div>
    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="job in filteredJobs"
        :key="job.id"
        :to="'/jobs/' + job.id"
        class="bg-white shadow-md rounded-lg p-6 hover:shadow-lg transition-shadow"
      >
        <h2 class="text-xl font-semibold mb-2">{{ job.title }}</h2>
        <p class="text-gray-700 mb-1"><strong>Company:</strong> {{ job.company_name }}</p>
        <p class="text-gray-700 mb-1"><strong>Location:</strong> {{ job.location }}</p>
        <p class="text-gray-700 mb-1"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
        <p class="text-gray-700 mb-1"><strong>Experience:</strong> {{ job.required_experience }} years</p>
        <p class="text-gray-700 mb-1">
          <strong>Skills:</strong> {{ job.required_skills_data.map(s => s.name).join(', ') }}
        </p>
        <p class="text-gray-600 mt-2">{{ truncate(job.description, 200) }}</p>
      </router-link>
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