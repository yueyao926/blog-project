<script setup>
import { computed, ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"
import { profile } from "../services/profile"
import {
  createCategory,
  deleteCategory,
  getCategories,
  updateCategory,
} from "../api/category"

const removeMarkdown = (text) => {
  return (text || "")
    .replace(/[#_*`>-]/g, "")
    .replace(/\n/g, " ")
}

const router = useRouter()

const formatDate = (value) => value
  ? new Date(value).toLocaleDateString("zh-CN", { year: "numeric", month: "short", day: "numeric" })
  : ""

const articles = ref([])
const categories = ref([])
const categoryMap = ref({})

const isAdmin = ref(false)
const keyword = ref("")
const DEFAULT_HERO_IMAGE = "https://images.unsplash.com/photo-1501854140801-50d01698950b"
const heroImage = ref(DEFAULT_HERO_IMAGE)
const heroFileInput = ref(null)
const heroBanner = ref(null)
const isUpdatingHeroImage = ref(false)

const selectedCategoryId = ref("")
const isCategoryDrawerOpen = ref(false)

const newCategoryName = ref("")
const newCategoryParentId = ref("")
const isCreatingCategory = ref(false)

const activeCategoryParentId = ref(null)
const categoryNavigationStack = ref([])
const editingCategoryId = ref(null)
const editingCategoryName = ref("")
const editingCategoryParentId = ref("")
const isSavingCategory = ref(false)

const buildCategoryTree = (items) => {
  const nodes = new Map(
    items.map((item) => [
      item.id,
      { ...item, children: [] },
    ])
  )

  const roots = []

  nodes.forEach((node) => {
    const parent = nodes.get(node.parent_id)

    if (parent) {
      parent.children.push(node)
    } else {
      roots.push(node)
    }
  })

  return roots
}

const flattenCategoryTree = (nodes, depth = 0) => {
  return nodes.flatMap((node) => {
    const row = { ...node, depth }
    return [
      row,
      ...flattenCategoryTree(node.children, depth + 1),
    ]
  })
}

const categoryTree = computed(() => buildCategoryTree(categories.value))

const categoryRows = computed(() =>
  flattenCategoryTree(categoryTree.value)
)

const visibleCategories = computed(() => {
  const parentId = activeCategoryParentId.value

  return categories.value
    .filter((category) => String(category.parent_id ?? "") === String(parentId ?? ""))
    .map((category) => ({
      ...category,
      children: categories.value.filter(
        (child) => String(child.parent_id ?? "") === String(category.id)
      ),
    }))
})

const activeParentCategory = computed(() =>
  categories.value.find(
    (category) => String(category.id) === String(activeCategoryParentId.value)
  ) || null
)

const editableParentRows = computed(() => {
  if (editingCategoryId.value == null) return categoryRows.value

  const excludedIds = new Set([
    String(editingCategoryId.value),
    ...getDescendantCategoryIds(editingCategoryId.value),
  ])

  return categoryRows.value.filter(
    (category) => !excludedIds.has(String(category.id))
  )
})

const getDescendantCategoryIds = (categoryId) => {
  const result = []
  const targetId = String(categoryId)

  const collect = (parentId) => {
    categories.value.forEach((category) => {
      if (String(category.parent_id ?? "") === String(parentId)) {
        result.push(String(category.id))
        collect(category.id)
      }
    })
  }

  collect(targetId)
  return result
}

const filteredArticles = computed(() => {
  const keywords = keyword.value
    .toLowerCase()
    .trim()
    .split(/\s+/)
    .filter(Boolean)

  const allowedCategoryIds =
    selectedCategoryId.value === ""
      ? null
      : new Set([
          selectedCategoryId.value,
          ...getDescendantCategoryIds(selectedCategoryId.value),
        ])

  return articles.value.filter((article) => {
    const articleCategoryId = String(
      article.category_id ?? article.category?.id ?? ""
    )

    const matchesCategory =
      allowedCategoryIds === null ||
      allowedCategoryIds.has(articleCategoryId)

    if (!matchesCategory) {
      return false
    }

    if (keywords.length === 0) {
      return true
    }

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

let motionFrame = 0
let lastMotionTime = 0
let heroHeight = 1
const motion = {
  x: 0,
  y: 0,
  scroll: 0,
  targetX: 0,
  targetY: 0,
  targetScroll: 0,
}

const clamp = (value, min, max) => Math.min(Math.max(value, min), max)

const renderHeroMotion = (time) => {
  const dt = Math.min((time - lastMotionTime) / 1000 || 0, 1 / 30)
  const follow = 1 - Math.exp(-7 * dt)
  lastMotionTime = time

  motion.x += (motion.targetX - motion.x) * follow
  motion.y += (motion.targetY - motion.y) * follow
  motion.scroll += (motion.targetScroll - motion.scroll) * follow

  const hero = heroBanner.value
  if (!hero) return

  hero.style.setProperty("--hero-bg-x", `${motion.x * -14}px`)
  hero.style.setProperty("--hero-bg-y", `${motion.y * -10 + motion.scroll * 34}px`)
  hero.style.setProperty("--hero-copy-x", `${motion.x * 4.5}px`)
  hero.style.setProperty("--hero-copy-y", `${motion.y * 2.2 - motion.scroll * 58}px`)
  hero.style.setProperty("--hero-index-y", `${motion.scroll * -18}px`)
  hero.style.setProperty("--hero-scale", String(1.07 + motion.scroll * .035))
  hero.style.setProperty("--hero-opacity", String(1 - motion.scroll * .58))
  hero.style.setProperty("--light-x", `${50 + motion.x * 20}%`)
  hero.style.setProperty("--light-y", `${45 + motion.y * 16}%`)
  const unsettled = Math.abs(motion.targetX - motion.x)
    + Math.abs(motion.targetY - motion.y)
    + Math.abs(motion.targetScroll - motion.scroll) > 0.002

  motionFrame = unsettled ? requestAnimationFrame(renderHeroMotion) : 0
}

const requestHeroMotion = () => {
  if (!motionFrame && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    lastMotionTime = performance.now()
    motionFrame = requestAnimationFrame(renderHeroMotion)
  }
}

const onHeroPointerMove = (event) => {
  if (event.pointerType !== "mouse") return

  const rect = heroBanner.value?.getBoundingClientRect()
  if (!rect) return

  motion.targetX = clamp((event.clientX - rect.left) / rect.width * 2 - 1, -1, 1)
  motion.targetY = clamp((event.clientY - rect.top) / rect.height * 2 - 1, -1, 1)
  requestHeroMotion()
}

const resetHeroPointer = () => {
  motion.targetX = 0
  motion.targetY = 0
  requestHeroMotion()
}

const onPageScroll = () => {
  motion.targetScroll = clamp(window.scrollY / heroHeight, 0, 1)
  requestHeroMotion()
}

const updateHeroMetrics = () => {
  heroHeight = heroBanner.value?.offsetHeight || 1
  onPageScroll()
}

const fetchArticles = async () => {
  try {
    const response = await api.get("/articles")
    articles.value = response.data
  } catch (error) {
    articles.value = []
    console.warn("文章列表暂时不可用", error)
  }
}

const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = Array.isArray(response.data) ? response.data : []

    categoryMap.value = Object.fromEntries(
      categories.value.map((cat) => [String(cat.id), cat.name])
    )

  } catch (error) {
    console.warn("分类列表暂时不可用", error)
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

  return "未分类"
}

const selectCategory = (categoryId) => {
  selectedCategoryId.value = categoryId
  isCategoryDrawerOpen.value = false
}

const openCategoryLevel = (category) => {
  if (!category.children.length) {
    selectCategory(String(category.id))
    return
  }

  categoryNavigationStack.value.push(category.id)
  activeCategoryParentId.value = category.id
  cancelEditCategory()
}

const fetchSiteSettings = async () => {
  try {
    const response = await api.get("/site-settings")
    heroImage.value = response.data.hero_image || DEFAULT_HERO_IMAGE
  } catch (error) {
    console.warn("首页图暂时不可用，已使用默认图片", error)
  }
}

const chooseHeroImage = () => {
  if (!isUpdatingHeroImage.value) {
    heroFileInput.value?.click()
  }
}

const uploadHeroImage = async (event) => {
  const input = event.target
  const file = input.files?.[0]
  if (!file || isUpdatingHeroImage.value) return

  if (!file.type.startsWith("image/")) {
    alert("请选择图片文件")
    input.value = ""
    return
  }

  if (file.size > 10 * 1024 * 1024) {
    alert("图片大小不能超过 10 MB")
    input.value = ""
    return
  }

  isUpdatingHeroImage.value = true

  try {
    const formData = new FormData()
    formData.append("file", file)
    const response = await api.put("/site-settings/hero-image", formData)
    heroImage.value = response.data.hero_image || DEFAULT_HERO_IMAGE
  } catch (error) {
    console.error(error)
    alert(error.response?.data?.detail || "首页图更换失败")
  } finally {
    isUpdatingHeroImage.value = false
    input.value = ""
  }
}

const goBackCategoryLevel = () => {
  categoryNavigationStack.value.pop()
  activeCategoryParentId.value = categoryNavigationStack.value.at(-1) ?? null
  cancelEditCategory()
}

const addCategory = async () => {
  const name = newCategoryName.value.trim()

  if (!name || isCreatingCategory.value) return

  isCreatingCategory.value = true

  try {
    const parentId =
      newCategoryParentId.value === ""
        ? null
        : Number(newCategoryParentId.value)

    await createCategory(name, parentId)

    newCategoryName.value = ""
    newCategoryParentId.value = ""

    await fetchCategories()
  } catch (error) {
    console.error(error)
    alert("分类创建失败")
  } finally {
    isCreatingCategory.value = false
  }
}

const startEditCategory = (category) => {
  editingCategoryId.value = category.id
  editingCategoryName.value = category.name
  editingCategoryParentId.value = category.parent_id == null
    ? ""
    : String(category.parent_id)
}

const cancelEditCategory = () => {
  editingCategoryId.value = null
  editingCategoryName.value = ""
  editingCategoryParentId.value = ""
}

const saveCategory = async () => {
  const name = editingCategoryName.value.trim()
  if (!name || editingCategoryId.value == null || isSavingCategory.value) return

  isSavingCategory.value = true

  try {
    const parentId = editingCategoryParentId.value === ""
      ? null
      : Number(editingCategoryParentId.value)

    await updateCategory(editingCategoryId.value, name, parentId)
    await fetchCategories()
    cancelEditCategory()
  } catch (error) {
    console.error(error)
    alert(error.response?.data?.detail || "分类保存失败")
  } finally {
    isSavingCategory.value = false
  }
}

const removeCategory = async (category) => {
  const confirmed = confirm(
    "删除该分类后，子分类会上移一级，直接属于该分类的文章会变为未分类。确定删除吗？"
  )

  if (!confirmed) return

  try {
    await deleteCategory(category.id)

    if (selectedCategoryId.value === String(category.id)) {
      selectedCategoryId.value = ""
    }

    if (editingCategoryId.value === category.id) {
      cancelEditCategory()
    }

    await Promise.all([
      fetchCategories(),
      fetchArticles(),
    ])
  } catch (error) {
    console.error(error)

    alert(
      error.response?.data?.detail || "分类删除失败"
    )
  }
}

const openCategoryDrawer = () => {
  activeCategoryParentId.value = null
  categoryNavigationStack.value = []
  cancelEditCategory()
  isCategoryDrawerOpen.value = true
}

onMounted(async () => {
  window.addEventListener("open-category-drawer", openCategoryDrawer)
  window.addEventListener("scroll", onPageScroll, { passive: true })
  window.addEventListener("resize", updateHeroMetrics)
  updateHeroMetrics()

  await Promise.all([
    fetchArticles(),
    fetchCategories(),
    fetchSiteSettings(),
  ])

  isAdmin.value =
    localStorage.getItem("is_admin") === "true"
})

onUnmounted(() => {
  window.removeEventListener("open-category-drawer", openCategoryDrawer)
  window.removeEventListener("scroll", onPageScroll)
  window.removeEventListener("resize", updateHeroMetrics)
  cancelAnimationFrame(motionFrame)
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
    <div
      ref="heroBanner"
      class="hero-banner"
      @pointermove="onHeroPointerMove"
      @pointerleave="resetHeroPointer"
    >
      <div
        class="hero-bg"
        :style="{ backgroundImage: `url('${heroImage}')` }"
      ></div>

      <div class="hero-overlay"></div>

      <div class="hero-light" aria-hidden="true"></div>

      <div class="hero-index" aria-hidden="true">
        <span>FIELD NOTES</span>
        <span>PERSONAL ARCHIVE</span>
      </div>

      <div class="hero-content">
        <p class="hero-kicker">Writing · Making · Wandering</p>
        <h1 class="hero-title">
          <span>Yueyao's</span>
          <span>Field Notes</span>
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

      <input
        ref="heroFileInput"
        type="file"
        accept="image/jpeg,image/png,image/webp,image/gif"
        class="sr-only"
        @change="uploadHeroImage"
      />

      <button
        v-if="isAdmin"
        type="button"
        class="hero-image-edit"
        :disabled="isUpdatingHeroImage"
        :aria-label="isUpdatingHeroImage ? '正在更换首页图' : '更换首页图'"
        title="更换首页图"
        @click="chooseHeroImage"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 16.5V20h3.5L18 9.5 14.5 6 4 16.5Z"/>
          <path d="m13 7.5 3.5 3.5"/>
        </svg>
        <span>{{ isUpdatingHeroImage ? "上传中" : "更换背景" }}</span>
      </button>
    </div>

    <button
      v-if="isCategoryDrawerOpen"
      type="button"
      aria-label="关闭分类栏"
      class="fixed inset-0 z-40 bg-black/20"
      @click="isCategoryDrawerOpen = false"
    ></button>

    <aside
      class="category-drawer fixed left-0 top-0 z-50 h-screen w-80 max-w-[85vw] overflow-y-auto transition-transform duration-300"
      :class="isCategoryDrawerOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="category-drawer-header">
        <button
          v-if="activeParentCategory"
          type="button"
          class="category-icon-button"
          aria-label="返回上一级分类"
          @click="goBackCategoryLevel"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>
        </button>

        <div class="category-heading">
          <span>{{ activeParentCategory ? "子分类" : "文章分类" }}</span>
          <h2>{{ activeParentCategory?.name || "全部分类" }}</h2>
        </div>

        <button
          type="button"
          class="category-icon-button"
          aria-label="关闭分类栏"
          @click="isCategoryDrawerOpen = false"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>
        </button>
      </div>

      <div class="category-list">
        <button
          type="button"
          class="category-list-row category-all-row"
          @click="selectCategory(activeParentCategory ? String(activeParentCategory.id) : '')"
        >
          <span>{{ activeParentCategory ? `查看「${activeParentCategory.name}」的全部文章` : "查看全部文章" }}</span>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>
        </button>

        <div
          v-for="category in visibleCategories"
          :key="category.id"
          class="category-list-row"
        >
          <button
            type="button"
            class="category-row-main"
            @click="openCategoryLevel(category)"
          >
            <span>{{ category.name }}</span>
            <small v-if="category.children.length">{{ category.children.length }} 个子分类</small>
            <svg v-if="category.children.length" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>
          </button>

          <div v-if="isAdmin" class="category-row-actions">
            <button type="button" class="category-edit" @click="startEditCategory(category)">编辑</button>
            <button type="button" class="category-delete" @click="removeCategory(category)">删除</button>
          </div>
        </div>

        <p v-if="!visibleCategories.length" class="category-empty">这里还没有子分类</p>
      </div>

      <div v-if="isAdmin && editingCategoryId != null" class="category-admin-panel">
        <div class="category-form-heading">
          <div>
            <span>编辑分类</span>
            <strong>{{ editingCategoryName }}</strong>
          </div>
          <button type="button" @click="cancelEditCategory">取消</button>
        </div>

        <input
          v-model="editingCategoryName"
          placeholder="分类名称"
          class="input-field"
          @keyup.enter="saveCategory"
        />

        <select v-model="editingCategoryParentId" class="input-field mt-3">
          <option value="">无父分类（一级分类）</option>
          <option
            v-for="category in editableParentRows"
            :key="category.id"
            :value="String(category.id)"
          >
            {{ "　".repeat(category.depth) }}{{ category.name }}
          </option>
        </select>

        <button
          type="button"
          class="category-save-button"
          :disabled="isSavingCategory"
          @click="saveCategory"
        >
          {{ isSavingCategory ? "保存中..." : "保存修改" }}
        </button>
      </div>

      <div v-if="isAdmin && editingCategoryId == null" class="category-admin-panel">

        <div class="category-form-heading">
          <div>
            <span>管理分类</span>
            <strong>新建分类</strong>
          </div>
        </div>

        <input
          v-model="newCategoryName"
          placeholder="分类名称"
          class="input-field"
          @keyup.enter="addCategory"
        />

        <select
          v-model="newCategoryParentId"
          class="input-field mt-3"
        >
          <option value="">无父分类（一级分类）</option>
          <option
            v-for="category in categoryRows"
            :key="category.id"
            :value="String(category.id)"
          >
            {{ "　".repeat(category.depth) }}{{ category.name }}
          </option>
        </select>

        <button
          type="button"
          class="category-save-button"
          :disabled="isCreatingCategory"
          @click="addCategory"
        >
          {{ isCreatingCategory ? "创建中..." : "新建分类" }}
        </button>
      </div>
    </aside>

    <div
      class="
        relative
        z-10
        max-w-7xl
        mx-auto
        px-4
        md:px-6
        py-10
        grid
        grid-cols-1
        lg:grid-cols-12
        gap-6
        lg:gap-8
      "
    >
      <div class="col-span-1 lg:col-span-3">
        <div
          class="
            glass-card
            sidebar-card
            p-5
            md:p-6
            lg:sticky
            lg:top-24
            animate-fade-up
          "
        >
          <span class="meng-deco meng-deco-1">✿</span>
          <span class="meng-deco meng-deco-2">+</span>
          <span class="meng-deco meng-deco-3">+</span>
          <span class="meng-deco meng-deco-4">✿</span>

          <router-link to="/about" class="avatar-frame profile-home-link" aria-label="前往 Yueyao 的个人页面">
            <img
              :src="profile.avatar"
              alt="Yueyao"
            />
          </router-link>

          <router-link to="/about"><h2
            class="
              font-display
              text-2xl
              font-bold
              text-center
              mt-5
              text-[#6b5d4d]
            "
          >
            {{ profile.name }}
          </h2></router-link>

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
              href="https://github.com/yueyao926"
              target="_blank"
              rel="noopener noreferrer"
              class="btn-dark"
            >
              GitHub
            </a>

            <router-link
              to="/about"
              class="btn-primary"
            >
              关于我
            </router-link>
          </div>

          <div class="section-divider"></div>

          <div class="space-y-1 text-[#a89478] text-sm">
            <div class="stat-item">
              <span><span class="stat-icon">✿</span>文章</span>
              <span class="stat-value">{{ articles.length }}</span>
            </div>

            <div class="stat-item">
              <span><span class="stat-icon">+</span>分类</span>
              <span class="stat-value">{{ categories.length }}</span>
            </div>
          </div>

          <p class="sidebar-footer">
            学会放松 · 奇迹自会悄悄发生
          </p>
        </div>
      </div>

      <div class="col-span-1 lg:col-span-9 min-w-0 space-y-8">
        <div class="article-index-heading">
          <div>
            <span>01 / NOTES</span>
            <h2>最近写下的事</h2>
          </div>
          <p>{{ filteredArticles.length }} 篇文章</p>
        </div>

        <div class="search-box w-full max-w-full">
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
          class="glass-card article-card article-card-side max-w-full overflow-hidden"
          :class="{ 'article-card-reverse': index % 2 === 1 }"
          :style="{ animationDelay: `${index * 0.08}s` }"
        >
          <div
            v-if="article.cover_image"
            class="overflow-hidden cover-wrap article-cover-side"
          >
            <img
              :src="article.cover_image"
              class="cover-img"
            />
          </div>

          <div class="article-card-body">
          <h2
            @click="router.push(`/articles/${article.id}`)"
            class="
              article-title
              font-display
              text-2xl
              md:text-3xl
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
              flex-col
              sm:flex-row
              justify-between
              items-start
              sm:items-center
              gap-4
            "
          >
            <div class="text-sm text-[#c4b498] flex flex-wrap gap-x-4 gap-y-1">
              <span>{{ formatDate(article.created_at) }}</span>
              <span>{{ article.view_count || 0 }} 次阅读</span>
              <span>
                作者：
                {{ article.author?.username }}
              </span>

              <span>
                分类：
                {{ getCategoryName(article) }}
              </span>
            </div>

            <div
              v-if="isAdmin"
              class="article-admin-actions"
            >
              <button
                @click="
                  router.push(
                    `/edit/${article.id}`
                  )
                "
                class="article-admin-action"
              >
                编辑
              </button>

              <button
                @click="deleteArticle(article.id)"
                class="article-admin-action danger"
              >
                删除
              </button>
            </div>
          </div>
          </div>
        </div>

        <div v-if="!filteredArticles.length" class="article-empty-state">
          <span>NO NOTES FOUND</span>
          <p>{{ keyword ? "没有找到匹配的文章，换个关键词试试。" : "新的文字正在路上，先去别处逛逛吧。" }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
