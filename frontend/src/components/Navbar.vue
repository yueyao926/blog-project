<script setup>
import { ref, onMounted } from "vue"

const isLoggedIn = ref(false)

const isAdmin = ref(false)

onMounted(() => {
  isLoggedIn.value =
    !!localStorage.getItem("token")

  isAdmin.value =
    localStorage.getItem("is_admin") === "true"

  console.log("管理员状态:", isAdmin.value)
})

const logout = () => {
  localStorage.clear()

  alert("已退出登录")

  window.location.href = "/login"
}
</script>

<template>
  <nav
    class="
      bg-white
      border-b
      shadow-sm
      px-8
      py-4
      flex
      justify-between
      items-center
    "
  >
    <!-- 左侧 -->
    <div class="flex items-center gap-6">

      <RouterLink
        to="/"
        class="
          text-2xl
          font-bold
          text-blue-600
        "
      >
        Yueyao Blog
      </RouterLink>

      <RouterLink
        to="/"
        class="
          text-gray-700
          hover:text-blue-500
        "
      >
        首页
      </RouterLink>

      <RouterLink
        v-if="isAdmin"
        to="/admin"
        class="
          text-gray-700
          hover:text-blue-500
        "
      >
        后台管理
      </RouterLink>

    </div>

    <!-- 右侧 -->
    <div class="flex items-center gap-4">

      <RouterLink
        v-if="!isLoggedIn"
        to="/login"
      >
        <button
          class="
            px-4
            py-2
            rounded-lg
            border
            hover:bg-gray-100
          "
        >
          登录
        </button>
      </RouterLink>

      <RouterLink
        v-if="!isLoggedIn"
        to="/register"
      >
        <button
          class="
            bg-blue-500
            text-white
            px-4
            py-2
            rounded-lg
            hover:bg-blue-600
          "
        >
          注册
        </button>
      </RouterLink>

      <button
        v-if="isLoggedIn"
        @click="logout"
        class="
          bg-red-500
          text-white
          px-4
          py-2
          rounded-lg
          hover:bg-red-600
        "
      >
        退出登录
      </button>

    </div>
  </nav>
</template>