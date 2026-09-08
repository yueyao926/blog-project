<script setup>
import { computed, nextTick, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { marked } from "marked"
import hljs from "highlight.js"
import "highlight.js/styles/github.css"
import api from "../services/api"
import { getCategories } from "../api/category"
import CommentThread from "../components/CommentThread.vue"

const route = useRoute()
const article = ref(null)
const categoryMap = ref({})
const comments = ref([])
const commentContent = ref("")
const replyingTo = ref(null)
const likeCount = ref(0)
const headings = ref([])

marked.setOptions({ highlight: (code) => hljs.highlightAuto(code).value })

const formatDate = (value) => value ? new Date(value).toLocaleDateString("zh-CN", { year: "numeric", month: "long", day: "numeric" }) : ""
const categoryName = computed(() => article.value?.category?.name || categoryMap.value[String(article.value?.category_id)] || "未分类")
const commentTree = computed(() => {
  const map = new Map(comments.value.map(item => [item.id, { ...item, children: [] }]))
  const roots = []
  map.forEach(item => map.has(item.parent_id) ? map.get(item.parent_id).children.push(item) : roots.push(item))
  return roots
})

const renderMarkdown = (content) => marked((content || "").replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt, url) => `![${alt}](${url.replace(/ /g, "%20")})`))

const buildToc = async () => {
  await nextTick()
  const nodes = [...document.querySelectorAll(".article-prose h1, .article-prose h2, .article-prose h3")]
  headings.value = nodes.map((node, index) => {
    node.id = `heading-${index}`
    return { id: node.id, text: node.textContent, level: Number(node.tagName.slice(1)) }
  })
}

const fetchComments = async () => { comments.value = (await api.get(`/comments/article/${route.params.id}`)).data }
const fetchLikes = async () => { likeCount.value = (await api.get(`/likes/${route.params.id}`)).data.count }

const submitComment = async () => {
  if (!commentContent.value.trim()) return
  try {
    await api.post(`/comments/article/${route.params.id}`, { content: commentContent.value, parent_id: replyingTo.value?.id || null })
    commentContent.value = ""; replyingTo.value = null; await fetchComments()
  } catch { alert("请先登录后再评论") }
}
const replyTo = (comment) => { replyingTo.value = comment; document.querySelector(".comment-compose textarea")?.focus() }
const likeComment = async (comment) => {
  try { comment.like_count = (await api.post(`/comments/${comment.id}/like`)).data.count; await fetchComments() }
  catch { alert("请先登录后再点赞") }
}
const removeComment = async (comment) => {
  if (!confirm("删除这条评论及其全部回复？")) return
  try { await api.delete(`/comments/${comment.id}`); await fetchComments() }
  catch (error) { alert(error.response?.data?.detail || "只能删除自己的评论") }
}
const toggleArticleLike = async () => {
  try { await api.post(`/likes/${route.params.id}`); await fetchLikes() }
  catch { alert("请先登录后再点赞") }
}

onMounted(async () => {
  const [categories, articleResponse] = await Promise.all([getCategories(), api.get(`/articles/${route.params.id}`)])
  categoryMap.value = Object.fromEntries((categories.data || []).map(item => [String(item.id), item.name]))
  article.value = articleResponse.data
  await Promise.all([fetchComments(), fetchLikes()])
  await buildToc()
})
</script>

<template>
  <main class="reading-page">
    <span class="reading-marker" aria-hidden="true">JOURNAL</span>
    <div v-if="article" class="reading-shell">
      <article class="article-sheet">
        <header class="article-header">
          <p class="article-kicker">JOURNAL · {{ categoryName }}</p>
          <h1>{{ article.title }}</h1>
          <div class="article-meta top-meta">
            <span>{{ formatDate(article.created_at) }}</span><span>{{ article.view_count }} 次阅读</span><span>作者 {{ article.author?.username }}</span>
          </div>
        </header>
        <div class="article-prose prose" v-html="renderMarkdown(article.content)"></div>
        <footer class="article-footer">
          <div class="article-meta"><span>{{ formatDate(article.created_at) }}</span><span>{{ article.view_count }} 次阅读</span><span>{{ categoryName }}</span></div>
          <button class="article-heart" @click="toggleArticleLike" aria-label="点赞文章">
            <svg viewBox="0 0 24 24"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.7-7.5 1.1-1.1a5.5 5.5 0 0 0 0-7.8Z"/></svg>
            {{ likeCount }}
          </button>
        </footer>
      </article>

      <aside class="reading-sidebar">
        <router-link to="/about" class="author-panel side-panel" aria-label="前往个人主页">
          <img src="/meng-er-avatar.png" alt="Yueyao 的头像" />
          <div><strong>Yueyao</strong><span>记录生活，也记录思考</span></div>
          <span class="author-arrow">↗</span>
        </router-link>
        <nav v-if="headings.length" class="toc-panel side-panel">
          <p class="side-title">目录</p>
          <a v-for="heading in headings" :key="heading.id" :href="`#${heading.id}`" :class="`toc-level-${heading.level}`">{{ heading.text }}</a>
        </nav>
        <section class="comments-panel side-panel">
          <div class="comments-title"><div><p class="side-title">评论</p><span>{{ comments.length }} 条交流</span></div></div>
          <div class="comment-compose">
            <div v-if="replyingTo" class="replying-label">回复 @{{ replyingTo.user.username }} <button @click="replyingTo = null">取消</button></div>
            <textarea v-model="commentContent" rows="3" placeholder="写下你的想法…" @keydown.ctrl.enter="submitComment"></textarea>
            <button class="comment-submit" @click="submitComment">发布评论</button>
          </div>
          <div v-if="commentTree.length" class="comment-list">
            <CommentThread v-for="comment in commentTree" :key="comment.id" :comment="comment" @reply="replyTo" @like="likeComment" @remove="removeComment" />
          </div>
          <p v-else class="comments-empty">还没有评论，来留下第一条吧。</p>
        </section>
      </aside>
    </div>
    <div v-else class="reading-loading" role="status"><span>LOADING JOURNAL</span><p>正在翻开这篇文章…</p></div>
  </main>
</template>
