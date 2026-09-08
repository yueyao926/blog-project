<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()
const route = useRoute()
const sessionExpired = route.query.expired === "1"

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
  <div class="page-bg auth-page">
    <main class="auth-stage">
      <section class="auth-intro" aria-hidden="true">
        <span>WELCOME BACK</span>
        <p>Dream</p><p>Act</p><p>Succeed</p>
        <small>继续你的阅读与记录。</small>
      </section>

      <section class="auth-card glass-card">
      <p class="auth-kicker">MEMBER ACCESS · 01</p>
      <h1>欢迎回来</h1>

      <p v-if="sessionExpired" class="auth-session-notice">
        登录状态已过期，请重新登录。
      </p>

      <div class="form-group">
        <label>邮箱</label>
        <input
          v-model="email"
          placeholder="请输入邮箱"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <label>密码</label>
        <input
          v-model="password"
          type="password"
          placeholder="请输入密码"
          class="input-field"
        />
      </div>

      <button
        @click="login"
        class="btn-primary w-full py-3 mt-2"
      >
        登录
      </button>

      <p class="text-center text-sm text-[#c4b498] mt-6">
        还没有账号？
        <router-link
          to="/register"
          class="link-accent"
        >
          立即注册
        </router-link>
      </p>
      </section>
    </main>
  </div>
</template>
