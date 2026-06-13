<script setup>
import { computed, ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import PandaPet from "./components/PandaPet.vue"

const router = useRouter()

const isLoggedIn = computed(() => {
  return !!localStorage.getItem("token")
})

const isAdmin = computed(() => {
  return localStorage.getItem("is_admin") === "true"
})

const navScrolled = ref(false)

const onScroll = () => {
  navScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener("scroll", onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener("scroll", onScroll)
})

const logout = () => {
  localStorage.removeItem("token")
  localStorage.removeItem("is_admin")

  alert("已退出登录")

  router.push("/login")

  location.reload()
}
</script>

<template>
  <div>
    <!-- 导航 -->
    <nav class="nav-bar" :class="{ scrolled: navScrolled }">
      <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

        <div class="nav-logo" @click="router.push('/')">
          Yueyao <span>Blog</span>
        </div>

        <div class="flex items-center gap-6">
          <router-link to="/" class="nav-link">首页</router-link>

          <router-link v-if="isAdmin" to="/admin" class="nav-link">
            后台管理
          </router-link>

          <template v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link">登录</router-link>
            <router-link to="/register" class="btn-primary">注册</router-link>
          </template>

          <button v-if="isLoggedIn" @click="logout" class="btn-danger">
            退出登录
          </button>
        </div>

      </div>
    </nav>

    <!-- 页面内容（只保留一个！） -->
    <div class="pt-16">
      <router-view />
    </div>

    <!-- ⭐ 全局悬浮组件（放这里） -->
    <PandaPet />
  </div>
</template>