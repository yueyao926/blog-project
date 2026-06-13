import api from "../services/api"

export const getCategories = () => {
  return api.get("/categories")
}

export const createCategory = (name) => {
  return api.post("/categories", {
    name,
    parent_id: null,
  })
}
