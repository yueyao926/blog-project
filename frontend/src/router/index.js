import { createRouter, createWebHistory } from "vue-router"

import Home from "../pages/Home.vue"
import Login from "../pages/Login.vue"
import Register from "../pages/Register.vue"
import Admin from "../pages/Admin.vue"
import ArticleDetail from "../pages/ArticleDetail.vue"
import EditArticle from "../pages/EditArticle.vue"
import About from "../pages/About.vue"

const routes = [
  {
    path: "/",
    component: Home
  },
  {
    path: "/about",
    component: About
  },
  {
    path: "/login",
    component: Login
  },
  {
    path: "/register",
    component: Register
  },
  {
    path: "/admin",
    component: Admin
  },
  {
    path: "/articles/:id",
    component: ArticleDetail
  },
  {
    path: "/edit/:id",
    component: EditArticle
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
