<template>
  <div class="bg-gradient-to-br from-blue-100 to-blue-300 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl w-full space-y-8 bg-white rounded-xl shadow-lg p-8">
      <div>
        <h1 class="text-center text-3xl font-extrabold text-gray-900">
          Create Job Listing
        </h1>
        <p class="mt-2 text-center text-sm text-gray-600">
          Fill out the form below to create a new job listing.
        </p>
      </div>
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">Error:</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>
      <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">Success:</strong>
        <span class="block sm:inline">{{ success }}</span>
      </div>
      <form @submit.prevent="createJob" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="title" class="sr-only">Job Title</label>
            <input
              v-model="form.title"
              type="text"
              id="title"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Job Title (Max 100 characters)"
              required
              maxlength="100"
            />
          </div>
          <div>
            <label for="company_name" class="sr-only">Company Name</label>
            <input
              v-model="form.company_name"
              type="text"
              id="company_name"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Company Name (Max 100 characters)"
              required
              maxlength="100"
            />
          </div>
          <div>
            <label for="location" class="sr-only">Location</label>
            <input
              v-model="form.location"
              type="text"
              id="location"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Location (Max 100 characters)"
              required
              maxlength="100"
            />
          </div>
          <div>
            <label for="employment_type" class="sr-only">Employment Type</label>
            <select
              v-model="form.employment_type"
              id="employment_type"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              required
            >
              <option value="remote">Remote</option>
              <option value="hybrid">Hybrid</option>
              <option value="onsite">Onsite</option>
            </select>
          </div>
          <div>
            <label for="required_experience" class="sr-only">Required Experience (Years)</label>
            <input
              v-model.number="form.required_experience"
              type="number"
              id="required_experience"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Required Experience (Years)"
              required
              min="0"
            />
          </div>
          <div>
            <label for="required_skills" class="sr-only">Required Skills</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="skill in form.required_skills"
                :key="skill"
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                {{ skill }}
                <button
                  type="button"
                  @click="removeSkill(skill)"
                  class="inline-flex items-center justify-center h-4 w-4 rounded-full ml-2 text-blue-400 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <span class="sr-only">x</span>
                </button>
              </span>
            </div>
            <input
              v-model="newSkill"
              type="text"
              id="required_skills"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Add a skill and press Enter (Max 50 characters)"
              @keydown.enter.prevent="addSkill"
              maxlength="50"
            />
          </div>
          <div class="mb-6">
            <label for="description" class="sr-only">Description</label>
            <textarea
              v-model="form.description"
              id="description"
              rows="4"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Job Description"
              required
            ></textarea>
          </div>
        </div>

        <div class="flex items-center justify-center">
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 max-w-[200px]"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
            </span>
            Create Job
          </button>
        </div>
      </form>
    </div>
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