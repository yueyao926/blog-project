<script setup>

import { ref, onMounted } from "vue"

import { useRouter } from "vue-router"



import { MdEditor } from "md-editor-v3"

import "md-editor-v3/lib/style.css"



import api from "../services/api"
import { getCategories } from "../api/category"



const router = useRouter()

const title = ref("")

const cover_image = ref("")

const selectedFile = ref(null)

const content = ref("")

const summary = ref("")

const category_id = ref("")

const categories = ref([])

const users = ref([])

const usersError = ref("")

const showUsers = ref(false)



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

      return

    }

    const categoriesResponse = await getCategories()

    categories.value = Array.isArray(categoriesResponse.data)
      ? categoriesResponse.data
      : []

    try {
      const usersResponse = await api.get("/admin/users")
      users.value = Array.isArray(usersResponse.data)
        ? usersResponse.data
        : []
    } catch (error) {
      console.error(error)
      usersError.value =
        error.response?.data?.detail || "获取用户列表失败"
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

      category_id:
        category_id.value === ""
          ? null
          : Number(category_id.value),

    })



    console.log(response.data)



    alert("文章发布成功")



    title.value = ""

    summary.value = ""

    content.value = ""

    cover_image.value = ""

    category_id.value = ""

  } catch (error) {

    console.error(error)



    alert("发布失败")

  }

}

</script>



<template>

  <div class="page-bg">

    <div class="admin-page relative z-10 max-w-full px-4 md:px-0">

      <div class="glass-card admin-form w-full max-w-full overflow-hidden p-4 md:p-8">

        <h1>后台管理</h1>

        <div class="space-y-5">

          <div>

            <label class="admin-label">文章标题</label>

            <input

              v-model="title"

              placeholder="文章标题"

              class="input-field w-full"

            />

          </div>



          <div>

            <label class="admin-label">文章摘要</label>

            <textarea

              v-model="summary"

              placeholder="文章摘要"

              rows="3"

              class="input-field w-full resize-none"

            />

          </div>



          <div>

            <label class="admin-label">分类</label>

            <select

              v-model="category_id"

              class="input-field w-full"

            >

              <option value="">未分类</option>

              <option

                v-for="category in categories"

                :key="category.id"

                :value="String(category.id)"

              >

                {{ category.name }}

              </option>

            </select>

          </div>



          <div>

            <label class="admin-label">封面图片 URL</label>

            <input

              v-model="cover_image"

              placeholder="封面图片URL"

              class="input-field w-full"

            />

          </div>



          <div class="max-w-full overflow-x-auto">

            <label class="admin-label">上传封面</label>

            <input

              type="file"

              @change="uploadImage"

              class="file-input w-full max-w-full"

            />

          </div>



          <div class="max-w-full overflow-x-auto">

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

        <div class="glass-card mt-8 p-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <h2 class="text-xl font-bold text-[#6b5d4d]">
              用户管理（共 {{ users.length }} 人）
            </h2>

            <button
              type="button"
              class="btn-primary"
              @click="showUsers = !showUsers"
            >
              {{ showUsers ? "收起用户列表" : "展开用户列表" }}
            </button>
          </div>

          <div v-if="showUsers">
            <p
              v-if="usersError"
              class="mt-3 text-red-500"
            >
              {{ usersError }}
            </p>

            <div v-else class="mt-4 overflow-x-auto">
              <table class="w-full text-left">
                <thead>
                  <tr>
                    <th class="p-2">ID</th>
                    <th class="p-2">用户名</th>
                    <th class="p-2">邮箱</th>
                    <th class="p-2">是否管理员</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="user in users"
                    :key="user.id"
                  >
                    <td class="p-2">{{ user.id }}</td>
                    <td class="p-2">{{ user.username }}</td>
                    <td class="p-2">{{ user.email }}</td>
                    <td class="p-2">
                      {{ user.is_admin ? "是" : "否" }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

    </div>

  </div>

</template>

