<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const email = ref("")
const password = ref("")

const login = async () => {
  try {
    const formData = new FormData()

    formData.append("username", email.value)

    formData.append("password", password.value)

    const response = await api.post(
      "/login",
      formData
    )

    localStorage.setItem(
      "token",
      response.data.access_token
    )

    // 给后续请求带 token
    api.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${response.data.access_token}`

    const meResponse = await api.get("/me")

    localStorage.setItem(
      "is_admin",
      meResponse.data.is_admin
    )

    alert("登录成功")

    window.location.href = "/"
  } catch (error) {
    console.error(error)

    alert("登录失败")
  }
}
</script>

<template>
  <div>
    <h1>登录</h1>

    <input
      v-model="email"
      placeholder="邮箱"
    />

    <br /><br />

    <input
      v-model="password"
      type="password"
      placeholder="密码"
    />

    <br /><br />

    <button @click="login">
      登录
    </button>
  </div>
</template>