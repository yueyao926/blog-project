<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const isLoggedIn = computed(() => {
  return !!localStorage.getItem("token")
})

const isAdmin = computed(() => {
  return localStorage.getItem("is_admin") === "true"
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
    <!-- 顶部导航栏 -->
    <nav
      class="
        fixed
        top-0
        left-0
        w-full
        z-50
        bg-white/30
        backdrop-blur-lg
        border-b
        border-white/20
        shadow-sm
      "
    >
      <div
        class="
          max-w-7xl
          mx-auto
          px-6
          h-16
          flex
          items-center
          justify-between
        "
      >
        <!-- 左侧 Logo -->
        <div
          class="
            text-2xl
            font-bold
            text-gray-800
            cursor-pointer
          "
          @click="router.push('/')"
        >
          Yueyao Blog
        </div>

        <!-- 右侧菜单 -->
        <div
          class="
            flex
            items-center
            gap-6
          "
        >
          <router-link
            to="/"
            class="
              text-gray-700
              hover:text-blue-500
              transition
            "
          >
            首页
          </router-link>

          <!-- 管理员 -->
          <router-link
            v-if="isAdmin"
            to="/admin"
            class="
              text-gray-700
              hover:text-blue-500
              transition
            "
          >
            后台管理
          </router-link>

          <!-- 未登录 -->
          <template v-if="!isLoggedIn">
            <router-link
              to="/login"
              class="
                text-gray-700
                hover:text-blue-500
                transition
              "
            >
              登录
            </router-link>

            <router-link
              to="/register"
              class="
                px-4
                py-2
                rounded-xl
                bg-gradient-to-r
                from-blue-500
                to-indigo-500
                text-white
                shadow-md
                hover:scale-105
                transition
              "
            >
              注册
            </router-link>
          </template>

          <!-- 已登录 -->
          <button
            v-if="isLoggedIn"
            @click="logout"
            class="
              px-4
              py-2
              rounded-xl
              bg-red-500
              text-white
              hover:bg-red-600
              transition
            "
          >
            退出登录
          </button>
        </div>
      </div>
    </nav>

    <!-- 页面内容 -->
    <div class="pt-16">
      <router-view />
    </div>
  </div>
</template>