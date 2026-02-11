import { http } from './http'

export const getTasks = () => {
  return http.get('/ping')
}
