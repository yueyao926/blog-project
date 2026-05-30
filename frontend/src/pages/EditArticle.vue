```vue
<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"

import { MdEditor } from "md-editor-v3"
import "md-editor-v3/lib/style.css"

import api from "../services/api"

const route = useRoute()
const router = useRouter()

const title = ref("")
const summary = ref("")
const cover_image = ref("")
const content = ref("")

onMounted(() => {
  const token = localStorage.getItem("token")

  if (!token) {
    alert("请先登录")

    router.push("/login")

    return
  }

  fetchArticle()
})

const fetchArticle = async () => {
  try {

    const response = await api.get(
      `/articles/${route.params.id}`
    )

    title.value = response.data.title

    summary.value = response.data.summary

    cover_image.value = response.data.cover_image

    content.value = response.data.content

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

const updateArticle = async () => {

  try {

    await api.put(
      `/articles/${route.params.id}`,
      {
        title: title.value,
        summary: summary.value,
        cover_image: cover_image.value,
        content: content.value,
      }
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
  <div class="max-w-5xl mx-auto p-6">

    <h1 class="text-3xl font-bold mb-6">
      编辑文章
    </h1>

    <!-- 标题 -->
    <input
      v-model="title"
      placeholder="文章标题"
      class="
        w-full
        p-3
        rounded-xl
        border
        mb-4
      "
    />

    <!-- 摘要 -->
    <textarea
      v-model="summary"
      placeholder="文章摘要"
      rows="3"
      class="
        w-full
        p-3
        rounded-xl
        border
        mb-4
      "
    />

    <!-- 封面图 -->
    <input
      v-model="cover_image"
      placeholder="封面图片URL"
      class="
        w-full
        p-3
        rounded-xl
        border
        mb-4
      "
    />

    <!-- 上传图片 -->
    <input
      type="file"
      @change="uploadImage"
      class="mb-6"
    />

    <!-- Markdown 编辑器 -->
    <MdEditor
      v-model="content"
      height="500px"
      @onUploadImg="onUploadImg"
    />

    <!-- 保存按钮 -->
    <button
      @click="updateArticle"
      class="
        mt-6
        bg-black
        text-white
        px-6
        py-3
        rounded-xl
      "
    >
      保存修改
    </button>
  </div>
</template>
```
