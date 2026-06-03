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
  <div class="page-bg py-10 px-4">
    <div
      v-if="article"
      class="
        relative
        z-10
        max-w-4xl
        mx-auto
        glass-card
        p-10
        animate-fade-up
      "
    >
      <h1
        class="
          font-display
          text-5xl
          font-bold
          text-[#6b5d4d]
          leading-tight
        "
      >
        {{ article.title }}
      </h1>

      <div class="mt-5 flex items-center gap-4">
        <button
          @click="toggleLike"
          class="like-btn btn-like"
        >
          👍 {{ likeCount }}
        </button>
      </div>

      <div
        class="
          mt-6
          text-[#c4b498]
          flex
          gap-6
          text-sm
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

      <div class="section-divider"></div>

      <div
        class="
          prose
          prose-lg
          max-w-none
        "
        v-html="renderMarkdown(article.content)"
      ></div>

      <div class="mt-16">
        <h2
          class="
            font-display
            text-3xl
            font-bold
            mb-6
            text-[#6b5d4d]
          "
        >
          评论区
        </h2>

        <textarea
          v-model="commentContent"
          placeholder="写点什么..."
          class="input-field mb-4 resize-none"
          rows="4"
        />

        <button
          @click="createComment"
          class="btn-dark px-6 py-3"
        >
          发表评论
        </button>
      </div>

      <div
        v-for="(comment, index) in comments"
        :key="comment.id"
        class="comment-card mt-4"
        :style="{ animationDelay: `${index * 0.06}s` }"
      >
        <div class="font-bold text-[#6b5d4d]">
          {{ comment.user.username }}
        </div>

        <div class="text-[#a89478] mt-2 leading-relaxed">
          {{ comment.content }}
        </div>
      </div>
    </div>
  </div>
</template>
