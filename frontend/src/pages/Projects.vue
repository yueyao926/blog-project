<script setup>
import { computed, onMounted, ref } from "vue"

import api from "../services/api"

const projects = ref([])
const keyword = ref("")
const loading = ref(true)
const loadError = ref("")
const showForm = ref(false)
const saving = ref(false)
const formError = ref("")
const form = ref({ name: "", description: "", github_url: "", tags: "" })
const editingProjectId = ref(null)

const isAdmin = computed(() => localStorage.getItem("is_admin") === "true")
const filteredProjects = computed(() => {
  const query = keyword.value.trim().toLocaleLowerCase()
  if (!query) return projects.value
  return projects.value.filter((project) =>
    [project.name, project.description, project.tags]
      .join(" ")
      .toLocaleLowerCase()
      .includes(query)
  )
})

const tagsFor = (project) =>
  (project.tags || "")
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean)

const loadProjects = async () => {
  loading.value = true
  loadError.value = ""
  try {
    const response = await api.get("/projects")
    projects.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error(error)
    loadError.value = "项目列表暂时无法加载，请稍后重试。"
  } finally {
    loading.value = false
  }
}

const openAddForm = () => {
  editingProjectId.value = null
  form.value = { name: "", description: "", github_url: "", tags: "" }
  formError.value = ""
  showForm.value = !showForm.value
}

const editProject = (project) => {
  editingProjectId.value = project.id
  form.value = { name: project.name, description: project.description, github_url: project.github_url, tags: project.tags || "" }
  formError.value = ""
  showForm.value = true
  window.scrollTo({ top: 0, behavior: "smooth" })
}

const saveProject = async () => {
  saving.value = true
  formError.value = ""
  try {
    const response = editingProjectId.value
      ? await api.put(`/projects/${editingProjectId.value}`, form.value)
      : await api.post("/projects", form.value)
    if (editingProjectId.value) {
      projects.value = projects.value.map((item) => item.id === editingProjectId.value ? response.data : item)
    } else {
      projects.value.unshift(response.data)
    }
    form.value = { name: "", description: "", github_url: "", tags: "" }
    showForm.value = false
    editingProjectId.value = null
  } catch (error) {
    console.error(error)
    if (error.response?.status === 401) {
      formError.value = "登录状态已过期，请重新登录后再添加项目。"
    } else if (error.response?.status === 403) {
      formError.value = "当前账号没有管理员权限。"
    } else {
      formError.value = error.response?.data?.detail?.[0]?.msg || error.response?.data?.detail || "添加失败，请检查填写内容。"
    }
  } finally {
    saving.value = false
  }
}

const deleteProject = async (project) => {
  if (!window.confirm(`确定删除「${project.name}」吗？`)) return
  try {
    await api.delete(`/projects/${project.id}`)
    projects.value = projects.value.filter((item) => item.id !== project.id)
  } catch (error) {
    console.error(error)
    window.alert("删除失败，请稍后重试。")
  }
}

onMounted(loadProjects)
</script>

<template>
  <main class="projects-page">
    <section class="projects-shell">
      <header class="projects-header">
        <div>
          <p class="projects-eyebrow">OPEN SOURCE · 精选收藏</p>
          <h1>优质开源项目</h1>
          <p class="projects-intro">收集值得关注的工具、框架与灵感，让好项目更容易被发现。</p>
        </div>
        <button v-if="isAdmin" type="button" class="project-add-button" @click="openAddForm">
          <span aria-hidden="true">{{ showForm ? "×" : "+" }}</span>
          {{ showForm ? "取消添加" : "添加项目" }}
        </button>
      </header>

      <form v-if="isAdmin && showForm" class="project-admin-form" @submit.prevent="saveProject">
        <div class="project-form-title">
          <div class="project-folder small">+</div>
          <div><strong>{{ editingProjectId ? "编辑开源项目" : "添加开源项目" }}</strong><p>{{ editingProjectId ? "修改后会立即更新项目卡片" : "保存后会立即出现在项目列表中" }}</p></div>
        </div>
        <div class="project-form-grid">
          <label>项目名称<input v-model.trim="form.name" required maxlength="120" placeholder="例如：vLLM"></label>
          <label>GitHub 仓库<input v-model.trim="form.github_url" required type="url" placeholder="https://github.com/owner/repo"></label>
          <label class="full">项目简介<textarea v-model.trim="form.description" required maxlength="1000" rows="3" placeholder="简要介绍项目的用途和亮点"></textarea></label>
          <label class="full">标签<input v-model.trim="form.tags" maxlength="300" placeholder="AI, RAG, Python（用逗号分隔）"></label>
        </div>
        <p v-if="formError" class="project-form-error">{{ formError }}</p>
        <button class="project-submit" :disabled="saving">{{ saving ? "正在保存…" : editingProjectId ? "保存修改" : "保存项目" }}</button>
      </form>

      <div class="project-search-wrap">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m16.5 16.5 4 4"/></svg>
        <input v-model="keyword" type="search" aria-label="搜索开源项目" placeholder="搜索项目名称、描述或标签…">
        <span v-if="keyword">{{ filteredProjects.length }} 个结果</span>
      </div>

      <div v-if="loading" class="project-state">正在整理项目清单…</div>
      <div v-else-if="loadError" class="project-state error">{{ loadError }}</div>
      <div v-else-if="!filteredProjects.length" class="project-state">
        <strong>{{ keyword ? "没有找到匹配的项目" : "还没有开源项目" }}</strong>
        <span>{{ keyword ? "换个关键词试试吧。" : "管理员可以点击右上角添加第一个项目。" }}</span>
      </div>

      <div v-else class="projects-grid">
        <article v-for="(project, index) in filteredProjects" :key="project.id" class="project-card" :style="{ '--delay': `${index * 55}ms` }">
          <a :href="project.github_url" target="_blank" rel="noopener noreferrer" :aria-label="`在 GitHub 查看 ${project.name}`">
            <div class="project-folder" aria-hidden="true"><span /></div>
            <div class="project-content">
              <div class="project-title-row"><h2>{{ project.name }}</h2><span class="github-arrow">↗</span></div>
              <p>{{ project.description }}</p>
              <div v-if="tagsFor(project).length" class="project-tags"><span v-for="tag in tagsFor(project)" :key="tag">{{ tag }}</span></div>
            </div>
          </a>
          <div v-if="isAdmin" class="project-card-actions"><button type="button" class="project-edit" title="编辑项目" @click="editProject(project)">编辑</button><button type="button" class="project-delete" title="删除项目" @click="deleteProject(project)">删除</button></div>
        </article>
      </div>
    </section>
  </main>
</template>
