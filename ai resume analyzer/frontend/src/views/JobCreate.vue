<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Create Job Listing</h1>
    <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
      {{ error }}
    </div>
    <div v-if="success" class="bg-green-100 text-green-700 p-4 rounded mb-4">
      {{ success }}
    </div>
    <form @submit.prevent="createJob" class="max-w-lg">
      <div class="mb-4">
        <label for="title" class="block text-gray-700 font-medium mb-2">Job Title</label>
        <input
          v-model="form.title"
          type="text"
          id="title"
          class="block w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
          maxlength="100"
        />
      </div>
      <div class="mb-4">
        <label for="company_name" class="block text-gray-700 font-medium mb-2">Company Name</label>
        <input
          v-model="form.company_name"
          type="text"
          id="company_name"
          class="block w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
          maxlength="100"
        />
      </div>
      <div class="mb-4">
        <label for="location" class="block text-gray-700 font-medium mb-2">Location</label>
        <input
          v-model="form.location"
          type="text"
          id="location"
          class="block w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
          maxlength="100"
        />
      </div>
      <div class="mb-4">
        <label for="employment_type" class="block text-gray-700 font-medium mb-2">Employment Type</label>
        <select
          v-model="form.employment_type"
          id="employment_type"
          class="block w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
          <option value="remote">Remote</option>
          <option value="hybrid">Hybrid</option>
          <option value="onsite">Onsite</option>
        </select>
      </div>
      <div class="mb-4">
        <label for="required_experience" class="block text-gray-700 font-medium mb-2">Required Experience (Years)</label>
        <input
          v-model.number="form.required_experience"
          type="number"
          id="required_experience"
          class="block w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
          min="0"
        />
      </div>
      <div class="mb-4">
        <label for="required_skills" class="block text-gray-700 font-medium mb-2">Required Skills</label>
        <div class="flex flex-wrap gap-2 mb-2">
          <span
            v-for="skill in form.required_skills"
            :key="skill"
            class="bg-blue-100 text-blue-700 px-2 py-1 rounded flex items-center"
          >
            {{ skill }}
            <button
              type="button"
              @click="removeSkill(skill)"
              class="ml-2 text-red-500 hover:text-red-700"
            >
              &times;
            </button>
          </span>
        </div>
        <input
          v-model="newSkill"
          type="text"
          id="required_skills"
          class="block w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type a skill and press Enter"
          @keydown.enter.prevent="addSkill"
          maxlength="50"
        />
      </div>
      <div class="mb-4">
        <label for="description" class="block text-gray-700 font-medium mb-2">Description</label>
        <textarea
          v-model="form.description"
          id="description"
          class="block w-full border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        ></textarea>
      </div>
      <button
        type="submit"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors duration-200"
      >
        Create Job
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
        company_name: '',
        location: '',
        employment_type: 'remote',
        required_experience: 0,
        required_skills: [],
        description: ''
      },
      newSkill: '',
      error: null,
      success: null
    }
  },
  methods: {
    addSkill() {
      const skill = this.newSkill.trim()
      if (skill && !this.form.required_skills.includes(skill) && skill.length <= 50) {
        this.form.required_skills.push(skill)
        this.newSkill = ''
      }
    },
    removeSkill(skill) {
      this.form.required_skills = this.form.required_skills.filter(s => s !== skill)
    },
    async createJob() {
      try {
        this.error = null
        this.success = null
        const response = await apiClient.post('/jobs/create/', {
          title: this.form.title,
          company_name: this.form.company_name,
          location: this.form.location,
          employment_type: this.form.employment_type,
          required_experience: this.form.required_experience,
          required_skills: this.form.required_skills,
          description: this.form.description
        })
        this.success = response.data.message
        this.form = {
          title: '',
          company_name: '',
          location: '',
          employment_type: 'remote',
          required_experience: 0,
          required_skills: [],
          description: ''
        }
        this.$router.push('/jobs')
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create job.'
      }
    }
  }
}
</script>