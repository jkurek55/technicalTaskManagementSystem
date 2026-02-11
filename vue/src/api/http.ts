import axios from 'axios'
import { useAuthStore } from '@/stores/auth.store'


export const http = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 10000,
})

http.interceptors.request.use((config) => {
    const authStore = useAuthStore()
    if (authStore.accessToken) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    return config
})

http.interceptors.request.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore()

        if (error.response?.status === 401 && authStore.refreshToken){
            try {
                await authStore.refresh()

                error.config.headers.Authorization = `Bearer ${authStore.accessToken}`
                return http(error.config)
            } catch ( refreshError){
                authStore.logout()
            }
        }
        return Promise.reject(error)
    }
)
