import api from "../services/api"

export const getCategories = () => {
  return api.get("/categories")
}

export const createCategory = (name, parentId = null) => {
  return api.post("/categories", {
    name,
    parent_id: parentId,
  })
}

export const updateCategory = (id, name, parentId = null) => {
  return api.put(`/categories/${id}`, {
    name,
    parent_id: parentId,
  })
}

export const deleteCategory = (id) => {
  return api.delete(`/categories/${id}`)
}
