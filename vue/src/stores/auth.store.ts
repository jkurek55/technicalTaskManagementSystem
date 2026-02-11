import { defineStore } from 'pinia'
import { getToken, refreshToken } from '@/api/auth.api'

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: localStorage.getItem('accessToken'),
    refreshToken: localStorage.getItem('refreshToken'),
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(username: string, password: string) {
      const response = await getToken(username, password)

      this.accessToken = response.data.access
      this.refreshToken = response.data.refresh

      localStorage.setItem('accessToken', this.accessToken!)
      localStorage.setItem('refreshToken', this.refreshToken!)
    },

    async refresh() {
      if (!this.refreshToken) throw new Error('No refresh token')

      const response = await refreshToken(this.refreshToken)

      this.accessToken = response.data.access
      localStorage.setItem('accessToken', this.accessToken!)
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null

      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },
  },
})
