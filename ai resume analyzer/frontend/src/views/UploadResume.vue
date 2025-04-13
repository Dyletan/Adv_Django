<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Upload Resume</h1>
    <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded mb-4">
      {{ error }}
    </div>
    <div v-if="success" class="bg-green-100 text-green-700 p-4 rounded mb-4">
      {{ success }}
    </div>
    <form @submit.prevent="uploadResume" class="max-w-md">
      <div class="mb-4">
        <label for="resume" class="block text-gray-700 font-medium mb-2">Select Resume (PDF only)</label>
        <input
          type="file"
          id="resume"
          accept=".pdf"
          @change="handleFileChange"
          class="block w-full text-gray-700 border border-gray-300 rounded py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button
        type="submit"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors duration-200"
        :disabled="!file"
      >
        Upload Resume
      </button>
    </form>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'UploadResumePage',
  data() {
    return {
      file: null,
      error: null,
      success: null,
    }
  },
  methods: {
    handleFileChange(event) {
      const selectedFile = event.target.files[0]
      if (selectedFile && selectedFile.type === 'application/pdf') {
        this.file = selectedFile
        this.error = null
      } else {
        this.file = null
        this.error = 'Please select a PDF file.'
      }
    },
    async uploadResume() {
      if (!this.file) {
        this.error = 'Please select a file to upload.'
        return
      }

      const formData = new FormData()
      formData.append('resume', this.file)

      try {
        this.error = null
        this.success = null
        const response = await apiClient.post('/auth/upload-resume/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.success = response.data.message
        this.file = null
        document.getElementById('resume').value = '' // Reset file input
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to upload resume.'
      }
    },
  },
}
</script>