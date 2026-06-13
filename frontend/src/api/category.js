import api from "../services/api"

export const getCategories = () => {
  return api.get("/categories")
}
