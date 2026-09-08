<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")

const register = async () => {
  if (!username.value.trim()) {
    alert("用户名不能为空")
    return
  }

  if (!email.value.trim()) {
    alert("邮箱不能为空")
    return
  }

  if (!password.value) {
    alert("密码不能为空")
    return
  }

  try {
    await api.post("/register", {
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
    })

    alert("注册成功")

    router.push("/login")
  } catch (error) {
    console.error(error)

    const detail = error.response?.data?.detail
    const message = Array.isArray(detail)
      ? detail[0]?.msg
      : detail

    alert(message || "注册失败")
  }
}
</script>

<template>
  <div class="page-bg auth-page">
    <main class="auth-stage auth-stage-register">
      <section class="auth-intro" aria-hidden="true">
        <span>NEW CHAPTER</span>
        <p>Courage</p><p>Strength</p><p>Victory</p>
        <small>从这里开始留下你的足迹。</small>
      </section>

      <section class="auth-card glass-card">
      <p class="auth-kicker">CREATE ACCOUNT · 02</p>
      <h1>加入这里</h1>

      <div class="form-group">
        <label>用户名</label>
        <input
          v-model="username"
          placeholder="请输入用户名"
          class="input-field"
        />
      </div>

      <div class="form-group">
        <label>邮箱</label>
        <input
          v-model="email"
          type="email"
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
        @click="register"
        class="btn-primary w-full py-3 mt-2"
      >
        注册
      </button>

      <p class="text-center text-sm text-[#c4b498] mt-6">
        已有账号？
        <router-link
          to="/login"
          class="link-accent"
        >
          去登录
        </router-link>
      </p>
      </section>
    </main>
  </div>
</template>
