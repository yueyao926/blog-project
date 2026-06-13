<script setup>
import { computed, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"
import { getCategories } from "../api/category"
import Sidebar from "../components/Sidebar.vue"

const removeMarkdown = (text) => {
  return text
    .replace(/[#_*`>-]/g, "")
    .replace(/\n/g, " ")
}

const router = useRouter()

const articles = ref([])

const categories = ref([])

const categoryMap = ref({})

const isAdmin = ref(false)

const keyword = ref("")

const filteredArticles = computed(() => {
  const keywords = keyword.value
    .toLowerCase()
    .trim()
    .split(/\s+/)
    .filter(Boolean)

  if (keywords.length === 0) {
    return articles.value
  }

  return articles.value.filter((article) => {
    const searchableText = [
      article.title || "",
      article.summary || "",
      article.content || "",
    ]
      .join(" ")
      .toLowerCase()

    return keywords.some((item) => searchableText.includes(item))
  })
})

const particles = Array.from({ length: 12 }, (_, i) => ({
  id: i,
  left: `${Math.random() * 100}%`,
  size: `${Math.random() * 5 + 3}px`,
  duration: `${Math.random() * 8 + 10}s`,
  delay: `${Math.random() * 10}s`,
}))

const fetchArticles = async () => {

  const response = await api.get("/articles")

  articles.value = response.data
}

const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = Array.isArray(response.data) ? response.data : []

    categoryMap.value = Object.fromEntries(
      categories.value.map((cat) => [String(cat.id), cat.name])
    )
  } catch (error) {
    console.error(error)
  }
}

const getCategoryName = (article) => {
  if (article.category?.name) {
    return article.category.name
  }

  const categoryId = article.category_id ?? article.category?.id

  if (categoryId != null && categoryMap.value[String(categoryId)]) {
    return categoryMap.value[String(categoryId)]
  }

  return null
}

onMounted(async () => {

  await Promise.all([
    fetchArticles(),
    fetchCategories(),
  ])

  isAdmin.value =
    localStorage.getItem("is_admin") === "true"
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
      <Sidebar
        :article-count="articles.length"
        :category-count="categories.length"
      />

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
            placeholder="搜索文章标题、摘要或内容..."
            class="input-field shadow-sm"
          />
        </div>

        <div
          v-for="(article, index) in filteredArticles"
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
            <div class="text-sm text-[#c4b498] flex flex-wrap gap-x-4 gap-y-1">
              <span>
                作者：
                {{ article.author?.username }}
              </span>

              <span v-if="getCategoryName(article)">
                分类：
                {{ getCategoryName(article) }}
              </span>
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
