```vue
<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"

import api from "../services/api"

import { marked } from "marked"

import hljs from "highlight.js"

import "highlight.js/styles/github.css"

const route = useRoute()
const article = ref(null)
const comments = ref([])
const commentContent = ref("")
const likeCount = ref(0)

onMounted(async () => {

  const response = await api.get(
    `/articles/${route.params.id}`
  )

  article.value = response.data

  await fetchComments()

  await fetchLikes()

  marked.setOptions({
    highlight: function(code, lang) {
      return hljs.highlightAuto(code).value
    }
  })
})

const fetchComments = async () => {

  const response = await api.get(
    `/comments/article/${route.params.id}`
  )

  comments.value = response.data
}

const fetchLikes = async () => {

  const response = await api.get(
    `/likes/${route.params.id}`
  )

  likeCount.value = response.data.count
}

const createComment = async () => {

  if (!commentContent.value.trim()) {
    return
  }

  try {

    await api.post(
      `/comments/article/${route.params.id}`,
      {
        content: commentContent.value
      }
    )

    commentContent.value = ""

    await fetchComments()

  } catch (error) {

    alert("请先登录")
  }
}

const toggleLike = async () => {
  try {

    const response = await api.post(
      `/likes/${route.params.id}`
    )

    console.log("点赞成功")

    console.log(response.data)

    await fetchLikes()

  } catch (error) {

    console.log("点赞失败")

    console.log(error)

    console.log(error.response)

    alert("点赞失败")
  }
}

const renderMarkdown = (content) => {
  if (!content) return ""

  // 替换所有图片URL中的空格
  const fixedContent = content.replace(
    /!\[([^\]]*)\]\(([^)]+)\)/g,
    (_, alt, url) => {
      const newUrl = url.replace(/ /g, "%20")
      return `![${alt}](${newUrl})`
    }
  )

  return marked(fixedContent)
}

</script>

<template>
  <div
    class="
      min-h-screen
      bg-gradient-to-br
      from-slate-100
      to-blue-100
      py-10
      px-4
    "
  >
    <div
      v-if="article"
      class="
        max-w-4xl
        mx-auto
        bg-white/70
        backdrop-blur-md
        rounded-3xl
        shadow-xl
        p-10
      "
    >
      <!-- 标题 -->
      <h1
        class="
          text-5xl
          font-bold
          text-gray-800
          leading-tight
        "
      >
        {{ article.title }}
      </h1>

      <div
        class="
            mt-4
            flex
            items-center
            gap-4
        "
        >

        <button
            @click="toggleLike"
            class="
            px-4
            py-2
            rounded-xl
            bg-pink-500
            text-white
            hover:bg-pink-600
            "
        >
            👍 {{ likeCount }}
        </button>

    </div>

      <!-- 作者 -->
      <div
        class="
          mt-6
          text-gray-500
          flex
          gap-6
        "
      >
        <span>
          作者：
          {{ article.author?.username }}
        </span>

        <span>
          文章ID：
          {{ article.id }}
        </span>
      </div>

      <!-- 分割线 -->
      <div
        class="
          border-t
          my-8
        "
      ></div>

      <!-- markdown 内容 -->
      <div
        class="
          prose
          prose-lg
          max-w-none
        "
        v-html="renderMarkdown(article.content)"
      ></div>

      <div class="mt-16">

        <h2 class="text-3xl font-bold mb-6">
            评论区
        </h2>

        <textarea
            v-model="commentContent"
            placeholder="写点什么..."
            class="
            w-full
            border
            rounded-xl
            p-4
            mb-4
            "
        />

        <button
            @click="createComment"
            class="
            bg-black
            text-white
            px-6
            py-3
            rounded-xl
            "
        >
            发表评论
        </button>

      </div>

      <div
        v-for="comment in comments"
        :key="comment.id"
        class="
            mt-6
            border-b
            pb-4
        "
        >

        <div
            class="
            font-bold
            text-gray-800
            "
        >
            {{ comment.user.username }}
        </div>

        <div
            class="
            text-gray-600
            mt-2
            "
        >
            {{ comment.content }}
        </div>

      </div>
    </div>
  </div>
</template>
```
