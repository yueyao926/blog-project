<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")

const register = async () => {
  try {
    await api.post("/register", {
      username: username.value,
      email: email.value,
      password: password.value,
    })

    alert("注册成功")

    router.push("/login")
  } catch (error) {
    console.error(error)

    alert("注册失败")
  }
}
</script>

<template>
  <div>
    <h1>注册</h1>

    <input
      v-model="username"
      placeholder="用户名"
    />

    <br /><br />

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

    <button @click="register">
      注册
    </button>
  </div>
</template>