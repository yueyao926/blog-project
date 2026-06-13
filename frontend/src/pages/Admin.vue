<script setup>

import { ref, onMounted } from "vue"

import { useRouter } from "vue-router"



import { MdEditor } from "md-editor-v3"

import "md-editor-v3/lib/style.css"



import api from "../services/api"



const router = useRouter()

const title = ref("")

const cover_image = ref("")

const selectedFile = ref(null)

const content = ref("")

const summary = ref("")



onMounted(async () => {

  const token = localStorage.getItem("token")



  if (!token) {

    alert("请先登录")



    router.push("/login")



    return

  }



  try {

    const response = await api.get("/me")



    if (!response.data.is_admin) {

      alert("你不是管理员")



      router.push("/")

    }



  } catch (error) {

    console.log(error)



    router.push("/login")

  }

})



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



const createArticle = async () => {

  try {

    const response = await api.post("/articles", {

      title: title.value,

      summary: summary.value,

      content: content.value,

      cover_image: cover_image.value,

    })



    console.log(response.data)



    alert("文章发布成功")



    title.value = ""

    summary.value = ""

    content.value = ""

    cover_image.value = ""

  } catch (error) {

    console.error(error)



    alert("发布失败")

  }

}

</script>



<template>

  <div class="page-bg">

    <div class="admin-page relative z-10">

      <div class="glass-card admin-form p-8">

        <h1>后台管理</h1>



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

            @click="createArticle"

            class="btn-dark px-8 py-3"

          >

            发布文章

          </button>

        </div>

      </div>

    </div>

  </div>

</template>

