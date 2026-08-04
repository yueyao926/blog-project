import axios from "axios"

const api = axios.create({
  baseURL: "/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const isLoginRequest = error.config?.url === "/login"

    if (error.response?.status === 401 && !isLoginRequest) {
      localStorage.removeItem("token")
      localStorage.removeItem("is_admin")
      window.dispatchEvent(new Event("auth-changed"))

      if (window.location.pathname !== "/login") {
        window.location.href = "/login?expired=1"
      }
    }

    return Promise.reject(error)
  }
)


export default api
