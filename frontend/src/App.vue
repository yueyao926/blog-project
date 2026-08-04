<script setup>
import { computed, ref, onMounted, onUnmounted, nextTick } from "vue"
import { useRouter } from "vue-router"
import PandaPet from "./components/PandaPet.vue";
import api from "./services/api"

const router = useRouter()

const isLoggedIn = ref(!!localStorage.getItem("token"))
const isAdmin = ref(localStorage.getItem("is_admin") === "true")

const syncAuthState = () => {
  isLoggedIn.value = !!localStorage.getItem("token")
  isAdmin.value = localStorage.getItem("is_admin") === "true"
}

const navScrolled = ref(false)

const onScroll = () => {
  navScrolled.value = window.scrollY > 20
}

onMounted(async () => {
  window.addEventListener("scroll", onScroll, { passive: true })
  window.addEventListener("auth-changed", syncAuthState)

  if (isLoggedIn.value) {
    try {
      const response = await api.get("/me")
      localStorage.setItem("is_admin", String(response.data.is_admin))
      syncAuthState()
    } catch (error) {
      console.error("登录状态校验失败", error)
    }
  }
})

onUnmounted(() => {
  window.removeEventListener("scroll", onScroll)
  window.removeEventListener("auth-changed", syncAuthState)
})

const logout = () => {
  localStorage.removeItem("token")
  localStorage.removeItem("is_admin")

  alert("已退出登录")

  router.push("/login")

  location.reload()
}

const openCategories = async () => {
  if (router.currentRoute.value.path !== "/") {
    await router.push("/")
    await nextTick()
  }

  window.dispatchEvent(new Event("open-category-drawer"))
}
</script>

<template>
  <div>
    <nav
      class="nav-bar"
      :class="{ scrolled: navScrolled }"
    >
      <div
        class="
          max-w-7xl
          mx-auto
          px-3
          md:px-6
          py-2
          min-h-16
          flex
          flex-wrap
          items-center
          justify-between
          gap-2
        "
      >
        <div
          class="nav-logo text-sm sm:text-base md:text-lg"
          @click="router.push('/')"
        >
          Yueyao <span>Blog</span>
        </div>

        <div
          class="
            flex
            flex-wrap
            items-center
            justify-end
            gap-2
            md:gap-6
            text-sm
            md:text-base
          "
        >
          <router-link
            to="/"
            class="nav-link"
          >
            首页
          </router-link>

          <button
            type="button"
            class="nav-link"
            @click="openCategories"
          >
            分类
          </button>

          <router-link
            to="/projects"
            class="nav-link"
          >
            开源项目
          </router-link>

          <router-link
            v-if="isAdmin"
            to="/admin"
            class="nav-link"
          >
            后台管理
          </router-link>

          <template v-if="!isLoggedIn">
            <router-link
              to="/login"
              class="nav-link"
            >
              登录
            </router-link>

            <router-link
              to="/register"
              class="btn-primary"
            >
              注册
            </router-link>
          </template>

          <button
            v-if="isLoggedIn"
            @click="logout"
            class="btn-danger"
          >
            退出登录
          </button>
        </div>
      </div>
    </nav>

    <div class="pt-24 sm:pt-16">
      <router-view />
    </div>

    <PandaPet />
  </div>
</template>
