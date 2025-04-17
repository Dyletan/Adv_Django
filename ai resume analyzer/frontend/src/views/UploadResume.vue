<template>
  <div class="bg-gradient-to-br from-blue-100 to-blue-300 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-6">
      <div>
        <h1 class="text-center text-3xl font-extrabold text-gray-900">
          Upload Resume
        </h1>
        <p class="mt-2 text-center text-sm text-gray-600 mb-4">
          Upload your resume in PDF or DOCX format.
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
      <form @submit.prevent="uploadResume" class="mt-8 space-y-4">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="resume" class="sr-only">Select Resume</label>
            <input
              type="file"
              id="resume"
              accept=".pdf,.docx"
              @change="handleFileChange"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
            />
          </div>
        </div>

        <div class="flex items-center justify-center">
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 max-w-[200px]"
            :disabled="!file"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="h-5 w-5 text-blue-500 group-hover:text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 010 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L7 10.586V3a1 1 0 112 0v7.586l2.293-2.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </span>
            Upload Resume
          </button>
        </div>
      </form>
    </div>
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
      if (selectedFile && ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(selectedFile.type)) {
        this.file = selectedFile
        this.error = null
      } else {
        this.file = null
        this.error = 'Please select a PDF or DOCX file.'
      }
       if (selectedFile && selectedFile.size > 2 * 1024 * 1024) { // 2MB limit
        this.file = null;
        this.error = 'File size exceeds 2MB limit.';
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
        await apiClient.post('/resumes/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.success = 'Resume uploaded successfully!'
        this.file = null
        document.getElementById('resume').value = '' // Reset file input
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to upload resume.'
      }
    },
  },
}
</script>