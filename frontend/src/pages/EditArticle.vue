<script setup>
import { ref, onMounted, computed } from "vue"
import { useRoute, useRouter } from "vue-router"

import { MdEditor } from "md-editor-v3"
import "md-editor-v3/lib/style.css"

import api from "../services/api"
import { getCategories } from "../api/category"

const route = useRoute()
const router = useRouter()

const title = ref("")
const summary = ref("")
const cover_image = ref("")
const content = ref("")
const category_id = ref("")
const categories = ref([])

const isCreate = computed(() => route.params.id === "new")

onMounted(async () => {
  const token = localStorage.getItem("token")

  if (!token) {
    alert("请先登录")

    router.push("/login")

    return
  }

  await fetchCategories()

  if (!isCreate.value) {
    await fetchArticle()
  }
})

const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error(error)
  }
}

const fetchArticle = async () => {
  try {

    const response = await api.get(
      `/articles/${route.params.id}`
    )

    title.value = response.data.title

    summary.value = response.data.summary

    cover_image.value = response.data.cover_image

    content.value = response.data.content

    category_id.value =
      response.data.category_id != null
        ? String(response.data.category_id)
        : response.data.category?.id != null
          ? String(response.data.category.id)
          : ""

  } catch (error) {

    console.error(error)

    alert("获取文章失败")
  }
}

const uploadImage = async (event) => {

  const file = event.target.files[0]

  if (!file) return

  const formData = new FormData()

  formData.append("file", file)

  try {

    const response = await api.post(
      "/upload",
      formData
    )

    cover_image.value = response.data.url

    alert("图片上传成功")

  } catch (error) {

    console.error(error)

    alert("上传失败")
  }
}

const onUploadImg = async (
  files,
  callback
) => {

  const res = await Promise.all(

    files.map(async (file) => {

      const formData = new FormData()

      formData.append("file", file)

      const response = await api.post(
        "/upload",
        formData
      )

      return response.data.url
    })
  )

  callback(res)
}

const buildPayload = () => ({
  title: title.value,
  summary: summary.value,
  cover_image: cover_image.value,
  content: content.value,
  category_id: category_id.value === "" ? null : Number(category_id.value),
})

const createArticle = async () => {
  try {
    await api.post("/articles", buildPayload())

    alert("文章发布成功")

    router.push("/")
  } catch (error) {
    console.error(error)

    alert("发布失败")
  }
}

const updateArticle = async () => {

  try {

    await api.put(
      `/articles/${route.params.id}`,
      buildPayload()
    )

    alert("修改成功")

    router.push("/")

  } catch (error) {

    console.error(error)

    alert("修改失败")
  }
}
</script>

<template>
  <div class="page-bg">
    <div class="admin-page relative z-10">
      <div class="glass-card admin-form p-8">
        <h1>{{ isCreate ? "发布文章" : "编辑文章" }}</h1>

        <div class="space-y-5">
          <div>
            <label class="admin-label">文章标题</label>
            <input
              v-model="title"
              placeholder="文章标题"
              class="input-field"
            />
          </div>

          <div>
            <label class="admin-label">文章摘要</label>
            <textarea
              v-model="summary"
              placeholder="文章摘要"
              rows="3"
              class="input-field resize-none"
            />
          </div>

          <div>
            <label class="admin-label">分类</label>
            <select
              v-model="category_id"
              class="input-field"
            >
              <option value="">未分类</option>
              <option
                v-for="cat in categories"
                :key="cat.id"
                :value="String(cat.id)"
              >
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="admin-label">封面图片 URL</label>
            <input
              v-model="cover_image"
              placeholder="封面图片URL"
              class="input-field"
            />
          </div>

          <div>
            <label class="admin-label">上传封面</label>
            <input
              type="file"
              @change="uploadImage"
              class="file-input"
            />
          </div>

          <div>
            <label class="admin-label">正文内容</label>
            <MdEditor
              v-model="content"
              height="500px"
              @onUploadImg="onUploadImg"
            />
          </div>

          <button
            @click="isCreate ? createArticle() : updateArticle()"
            class="btn-dark px-8 py-3"
          >
            {{ isCreate ? "发布文章" : "保存修改" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
