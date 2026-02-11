<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

const handleLogin = async () => {
  error.value = null
  loading.value = true

  try {
    await authStore.login(username.value, password.value)
    router.push('/tasks')
  } catch (err: any) {
    error.value = 'Nieprawidłowe dane logowania'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-md">
      
      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-xl p-8">
        
        <!-- Header -->
        <div class="mb-8 text-center">
          <h1 class="text-3xl font-bold text-gray-800">
            System Zarządzania
          </h1>
          <p class="text-gray-500 mt-2">
            Zaloguj się do swojego konta
          </p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-5">

          <!-- Username -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Login
            </label>
            <input
              v-model="username"
              type="text"
              required
              class="w-full rounded-xl border border-gray-300 px-4 py-2.5 
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                     outline-none transition"
              placeholder="Wpisz login"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Hasło
            </label>
            <input
              v-model="password"
              type="password"
              required
              class="w-full rounded-xl border border-gray-300 px-4 py-2.5 
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                     outline-none transition"
              placeholder="Wpisz hasło"
            />
          </div>

          <!-- Error -->
          <div v-if="error" class="text-sm text-red-600 bg-red-50 p-3 rounded-lg">
            {{ error }}
          </div>

          <!-- Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white 
                   font-semibold py-2.5 rounded-xl transition 
                   disabled:opacity-60 disabled:cursor-not-allowed
                   flex items-center justify-center"
          >
            <span v-if="!loading">Zaloguj się</span>

            <svg
              v-else
              class="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8H4z"
              />
            </svg>
          </button>

        </form>
      </div>

      <!-- Footer -->
      <p class="text-center text-xs text-gray-400 mt-6">
        © 2026 System Zarządzania Zadaniami Technicznymi
      </p>

    </div>
  </div>
</template>
