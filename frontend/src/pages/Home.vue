<script setup>
import { ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const removeMarkdown = (text) => {
  return text
    .replace(/[#_*`>-]/g, "")
    .replace(/\n/g, " ")
}

const router = useRouter()

const articles = ref([])

const isAdmin = ref(false)

const keyword = ref("")

const particles = Array.from({ length: 12 }, (_, i) => ({
  id: i,
  left: `${Math.random() * 100}%`,
  size: `${Math.random() * 5 + 3}px`,
  duration: `${Math.random() * 8 + 10}s`,
  delay: `${Math.random() * 10}s`,
}))

const fetchArticles = async () => {

  const response = await api.get(
    "/articles",
    {
      params: {
        keyword: keyword.value
      }
    }
  )

  articles.value = response.data
}

onMounted(async () => {

  await fetchArticles()

  isAdmin.value =
    localStorage.getItem("is_admin") === "true"
})

watch(keyword, () => {
  fetchArticles()
})

const deleteArticle = async (id) => {
  const confirmDelete = confirm(
    "确定删除这篇文章吗？"
  )

  if (!confirmDelete) return

  try {
    await api.delete(`/articles/${id}`)

    articles.value = articles.value.filter(
      article => article.id !== id
    )

    alert("删除成功")
  } catch (error) {
    console.error(error)

    alert("删除失败")
  }
}
</script>

<template>
  <div class="page-bg">
    <!-- 顶部大图 -->
    <div class="hero-banner">
      <div
        class="hero-bg"
        style="
          background-image:
          url('https://images.unsplash.com/photo-1501854140801-50d01698950b');
        "
      ></div>

      <div class="hero-overlay"></div>

      <div class="particles">
        <span
          v-for="p in particles"
          :key="p.id"
          class="particle"
          :style="{
            left: p.left,
            width: p.size,
            height: p.size,
            animationDuration: p.duration,
            animationDelay: p.delay,
          }"
        ></span>
      </div>

      <div class="hero-content">
        <h1 class="hero-title">
          Welcome to Yueyao's Blog
        </h1>

        <p class="hero-subtitle">
          And miles to go before I sleep
        </p>
      </div>

      <div class="hero-scroll-hint">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14M5 12l7 7 7-7"/>
        </svg>
      </div>
    </div>

    <!-- 内容区域 -->
    <div
      class="
        relative
        z-10
        max-w-7xl
        mx-auto
        px-6
        py-10
        grid
        grid-cols-12
        gap-8
      "
    >
      <!-- 左侧个人信息 -->
      <div class="col-span-3">
        <div
          class="
            glass-card
            sidebar-card
            p-6
            sticky
            top-24
            animate-fade-up
          "
        >
          <span class="meng-deco meng-deco-1">✿</span>
          <span class="meng-deco meng-deco-2">+</span>
          <span class="meng-deco meng-deco-3">+</span>
          <span class="meng-deco meng-deco-4">✿</span>

          <div class="avatar-frame">
            <img
              src="/meng-er-avatar.png"
              alt="Yueyao"
            />
          </div>

          <h2
            class="
              font-display
              text-2xl
              font-bold
              text-center
              mt-5
              text-[#6b5d4d]
            "
          >
            Yueyao
          </h2>

          <p
            class="
              text-[#a89478]
              text-center
              mt-3
              leading-7
              text-sm
            "
          >
            你好呀，欢迎来到我的空间~
          </p>

          <div
            class="
              mt-6
              flex
              justify-center
              gap-3
            "
          >
            <a
              href="https://github.com"
              target="_blank"
              class="btn-dark"
            >
              GitHub
            </a>

            <a
              href="#"
              class="btn-primary"
            >
              关于我
            </a>
          </div>

          <div class="section-divider"></div>

          <div class="space-y-1 text-[#a89478] text-sm">
            <div class="stat-item">
              <span><span class="stat-icon">✿</span>文章</span>
              <span class="stat-value">{{ articles.length }}</span>
            </div>

            <div class="stat-item">
              <span><span class="stat-icon">+</span>分类</span>
              <span class="stat-value">1</span>
            </div>

            <div class="stat-item">
              <span><span class="stat-icon">✿</span>标签</span>
              <span class="stat-value">3</span>
            </div>
          </div>

          <p class="sidebar-footer">
            学会放松 · 奇迹自会悄悄发生
          </p>
        </div>
      </div>

      <!-- 右侧文章 -->
      <div class="col-span-9 space-y-8">
        <div class="search-box">
          <svg
            class="search-icon"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>

          <input
            v-model="keyword"
            placeholder="搜索文章标题..."
            class="input-field shadow-sm"
          />
        </div>

        <div
          v-for="(article, index) in articles"
          :key="article.id"
          class="glass-card article-card p-8"
          :style="{ animationDelay: `${index * 0.08}s` }"
        >
          <div
            v-if="article.cover_image"
            class="overflow-hidden cover-wrap mb-6"
          >
            <img
              :src="article.cover_image"
              class="cover-img w-full h-64 object-cover"
            />
          </div>

          <h2
            @click="router.push(`/articles/${article.id}`)"
            class="
              article-title
              font-display
              text-3xl
              font-bold
              text-[#6b5d4d]
            "
          >
            {{ article.title }}
          </h2>

          <p
            class="
              mt-4
              text-[#a89478]
              leading-8
            "
          >
            {{ article.summary }}
          </p>

          <div
            class="
              mt-6
              flex
              justify-between
              items-center
            "
          >
            <div class="text-sm text-[#c4b498]">
              作者：
              {{ article.author?.username }}
            </div>

            <div
              v-if="isAdmin"
              class="flex gap-3"
            >
              <button
                @click="
                  router.push(
                    `/edit/${article.id}`
                  )
                "
                class="btn-primary"
              >
                编辑
              </button>

              <button
                @click="deleteArticle(article.id)"
                class="btn-danger"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
