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
  <div
    class="
      min-h-screen
      bg-gradient-to-br
      from-slate-100
      to-blue-100
    "
  >
    <!-- 顶部大图 -->
    <div
      class="
        h-[320px]
        bg-cover
        bg-center
        relative
      "
      style="
        background-image:
        url('https://images.unsplash.com/photo-1506744038136-46273834b3fb');
      "
    >
      <!-- 黑色遮罩 -->
      <div
        class="
          absolute
          inset-0
          bg-black/40
        "
      ></div>

      <!-- 标题 -->
      <div
        class="
          relative
          z-10
          h-full
          flex
          flex-col
          justify-center
          items-center
          text-white
        "
      >
        <h1
          class="
            text-6xl
            font-bold
            drop-shadow-lg
          "
        >
          Welcome to Yueyao's Blog
        </h1>

        <p class="mt-4 text-xl">
          And miles to go before I sleep
        </p>
      </div>
    </div>

    <!-- 内容区域 -->
    <div
      class="
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
      <div
        class="
          col-span-3
        "
      >
        <div
          class="
            bg-white/70
            backdrop-blur-md
            rounded-3xl
            p-6
            shadow-lg
            sticky
            top-6
          "
        >
          <!-- 头像 -->
          <img
            src="https://i.pravatar.cc/300"
            class="
              w-32
              h-32
              rounded-full
              mx-auto
              object-cover
              border-4
              border-white
              shadow-lg
            "
          />

          <!-- 名字 -->
          <h2
            class="
              text-2xl
              font-bold
              text-center
              mt-4
            "
          >
            Yueyao
          </h2>

          <!-- 简介 -->
          <p
            class="
              text-gray-600
              text-center
              mt-3
              leading-7
            "
          >
            你好呀，欢迎来到我的空间~
          </p>

          <!-- 按钮 -->
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
              class="
                px-4
                py-2
                rounded-xl
                bg-black
                text-white
                hover:scale-105
                transition
              "
            >
              GitHub
            </a>

            <a
              href="#"
              class="
                px-4
                py-2
                rounded-xl
                bg-blue-500
                text-white
                hover:scale-105
                transition
              "
            >
              关于我
            </a>
          </div>

          <!-- 统计 -->
          <div
            class="
              mt-8
              border-t
              pt-6
              space-y-4
              text-gray-700
            "
          >
            <div class="flex justify-between">
              <span>文章</span>
              <span>{{ articles.length }}</span>
            </div>

            <div class="flex justify-between">
              <span>分类</span>
              <span>1</span>
            </div>

            <div class="flex justify-between">
              <span>标签</span>
              <span>3</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧文章 -->
      <div
        class="
          col-span-9
          space-y-8
        "
      >

        <input
          v-model="keyword"
          placeholder="搜索文章标题..."
          class="
            w-full
            p-4
            rounded-2xl
            border
            bg-white
            shadow
          "
        />

        <div
          v-for="article in articles"
          :key="article.id"
          class="
            bg-white/70
            backdrop-blur-md
            rounded-3xl
            p-8
            shadow-lg
            hover:shadow-2xl
            transition
            duration-300
          "
          >
            <!-- 封面图 -->
            <img
              v-if="article.cover_image"
              :src="article.cover_image"
              class="
                w-full
                h-64
                object-cover
                rounded-2xl
                mb-6
              "
            />

            <!-- 标题 -->
            <h2
              @click="router.push(`/articles/${article.id}`)"
              class="
                text-3xl
                font-bold
                text-gray-800
                cursor-pointer
                hover:text-blue-600
                transition
              "
            >
              {{ article.title }}
            </h2>

          <!-- 内容 -->
          <p
            class="
              mt-4
              text-gray-600
              leading-8
            "
          >
            {{ article.summary }}
          </p>

          <!-- 底部 -->
          <div
            class="
              mt-6
              flex
              justify-between
              items-center
            "
          >
            <!-- 作者 -->
            <div
              class="
                text-sm
                text-gray-500
              "
            >
              作者：
              {{ article.author?.username }}
            </div>

            <!-- 管理员按钮 -->
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
                class="
                  px-4
                  py-2
                  rounded-xl
                  bg-blue-500
                  text-white
                  hover:bg-blue-600
                  transition
                "
              >
                编辑
              </button>

              <button
                @click="deleteArticle(article.id)"
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
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>