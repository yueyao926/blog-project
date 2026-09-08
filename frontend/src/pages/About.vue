<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue"
import { profile, moodOptions, currentMood, saveProfile, setTodayMood } from "../services/profile"

const isAdmin = computed(() => localStorage.getItem("is_admin") === "true")
const editing = ref(false)
const draft = ref({ ...profile })
const selectedMood = ref(currentMood())
const now = new Date()
const calendarMonth = ref(new Date(now.getFullYear(), now.getMonth(), 1))
const monthTitle = computed(() => calendarMonth.value.toLocaleDateString("zh-CN", { year: "numeric", month: "long" }))
const calendarDays = computed(() => {
  const year = calendarMonth.value.getFullYear(), month = calendarMonth.value.getMonth()
  return [...Array(new Date(year, month, 1).getDay()).fill(null), ...Array.from({ length: new Date(year, month + 1, 0).getDate() }, (_, i) => i + 1)]
})
const moodMap = Object.fromEntries(moodOptions.map((mood) => [mood.value, mood]))
const moodGroups = computed(() => [...new Set(moodOptions.map((mood) => mood.group))])
const currentMoodOption = computed(() => moodMap[selectedMood.value] || { emoji: "○", label: "今日暂未设置" })
const dateKeyForDay = (day) => day ? `${calendarMonth.value.getFullYear()}-${String(calendarMonth.value.getMonth() + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}` : ""
const moodForDay = (day) => moodMap[profile.moods[dateKeyForDay(day)]]
const monthMoodCount = computed(() => calendarDays.value.filter((day) => moodForDay(day)).length)
const changeMonth = (delta) => { calendarMonth.value = new Date(calendarMonth.value.getFullYear(), calendarMonth.value.getMonth() + delta, 1) }
const chooseMood = (value) => { selectedMood.value = value; setTodayMood(value) }
const fileToDataUrl = (event, field) => {
  const file = event.target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => { draft.value[field] = reader.result }
  reader.readAsDataURL(file)
}
const startEditing = () => { draft.value = { ...profile }; editing.value = true }
const submit = () => { saveProfile({ ...draft.value, moods: profile.moods }); editing.value = false }

const profileCover = ref(null)
let motionFrame = 0
let lastMotionTime = 0
let coverHeight = 1
const motion = { x: 0, y: 0, scroll: 0, targetX: 0, targetY: 0, targetScroll: 0 }
const clamp = (value, min, max) => Math.min(Math.max(value, min), max)

const renderCoverMotion = (time) => {
  const follow = 1 - Math.exp(-7 * Math.min((time - lastMotionTime) / 1000 || 0, 1 / 30))
  lastMotionTime = time
  motion.x += (motion.targetX - motion.x) * follow
  motion.y += (motion.targetY - motion.y) * follow
  motion.scroll += (motion.targetScroll - motion.scroll) * follow

  const cover = profileCover.value
  if (!cover) return
  cover.style.setProperty("--profile-bg-x", `${motion.x * -14}px`)
  cover.style.setProperty("--profile-bg-y", `${motion.y * -10 + motion.scroll * 34}px`)
  cover.style.setProperty("--profile-copy-x", `${motion.x * 4.5}px`)
  cover.style.setProperty("--profile-copy-y", `${motion.y * 2.2 - motion.scroll * 58}px`)
  cover.style.setProperty("--profile-index-y", `${motion.scroll * -18}px`)
  cover.style.setProperty("--profile-scale", String(1.07 + motion.scroll * .035))
  cover.style.setProperty("--profile-opacity", String(1 - motion.scroll * .58))
  cover.style.setProperty("--profile-light-x", `${50 + motion.x * 20}%`)
  cover.style.setProperty("--profile-light-y", `${45 + motion.y * 16}%`)

  const unsettled = Math.abs(motion.targetX - motion.x) + Math.abs(motion.targetY - motion.y) + Math.abs(motion.targetScroll - motion.scroll) > .002
  motionFrame = unsettled ? requestAnimationFrame(renderCoverMotion) : 0
}

const requestCoverMotion = () => {
  if (!motionFrame && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    lastMotionTime = performance.now()
    motionFrame = requestAnimationFrame(renderCoverMotion)
  }
}

const onCoverPointerMove = (event) => {
  if (event.pointerType !== "mouse") return
  const rect = profileCover.value?.getBoundingClientRect()
  if (!rect) return
  motion.targetX = clamp((event.clientX - rect.left) / rect.width * 2 - 1, -1, 1)
  motion.targetY = clamp((event.clientY - rect.top) / rect.height * 2 - 1, -1, 1)
  requestCoverMotion()
}

const resetCoverPointer = () => { motion.targetX = 0; motion.targetY = 0; requestCoverMotion() }
const onPageScroll = () => { motion.targetScroll = clamp(window.scrollY / coverHeight, 0, 1); requestCoverMotion() }
const updateCoverMetrics = () => { coverHeight = profileCover.value?.offsetHeight || 1; onPageScroll() }

onMounted(() => {
  window.addEventListener("scroll", onPageScroll, { passive: true })
  window.addEventListener("resize", updateCoverMetrics)
  updateCoverMetrics()
})

onUnmounted(() => {
  window.removeEventListener("scroll", onPageScroll)
  window.removeEventListener("resize", updateCoverMetrics)
  cancelAnimationFrame(motionFrame)
})
</script>

<template>
  <main class="profile-page">
    <section ref="profileCover" class="profile-cover" @pointermove="onCoverPointerMove" @pointerleave="resetCoverPointer">
      <div class="profile-cover-bg" :style="{ backgroundImage: `url('${profile.cover}')` }"></div>
      <div class="profile-cover-shade"></div>
      <div class="profile-cover-light" aria-hidden="true"></div>
      <div class="profile-cover-index" aria-hidden="true"><span>PORTRAIT / 01</span><span>SCROLL TO KNOW ME</span></div>
      <div class="profile-cover-copy"><span>ABOUT YUEYAO</span><h1>在好奇心里，<br />慢慢生长。</h1><p>{{ profile.tagline }}</p></div>
    </section>
    <div class="profile-layout">
      <aside class="profile-side">
        <section class="profile-panel identity-panel"><img :src="profile.avatar" :alt="profile.name" class="profile-avatar" /><h2>{{ profile.name }}</h2><p>{{ profile.location }}</p><a :href="profile.github" target="_blank" rel="noreferrer">GitHub ↗</a></section>
        <section class="profile-panel mood-panel">
          <div class="panel-heading"><span>今日状态</span><small>{{ isAdmin ? "仅管理员可设置" : "Yueyao 的今日状态" }}</small></div>
          <div class="current-mood"><b>{{ currentMoodOption.emoji }}</b><div><strong>{{ currentMoodOption.label }}</strong><small>{{ isAdmin ? "选择状态后会记录到日历" : "状态由 Yueyao 更新" }}</small></div></div>
          <div v-if="isAdmin" class="mood-picker">
            <div v-for="group in moodGroups" :key="group" class="mood-group">
              <p>{{ group }}</p>
              <div class="mood-grid"><button v-for="mood in moodOptions.filter((item) => item.group === group)" :key="mood.value" :class="{ active: selectedMood === mood.value }" @click="chooseMood(mood.value)"><span>{{ mood.emoji }}</span>{{ mood.label }}</button></div>
            </div>
          </div>
        </section>
        <section class="profile-panel calendar-panel status-calendar-panel">
          <div class="calendar-head"><button @click="changeMonth(-1)" aria-label="上个月">‹</button><div><strong>{{ monthTitle }}</strong><small>{{ monthMoodCount ? `留下了 ${monthMoodCount} 个状态` : "还没有状态足迹" }}</small></div><button @click="changeMonth(1)" aria-label="下个月">›</button></div>
          <div class="calendar-grid weekdays"><span v-for="day in ['日','一','二','三','四','五','六']" :key="day">{{ day }}</span></div>
          <div class="calendar-grid status-calendar-grid"><span v-for="(day, index) in calendarDays" :key="index" class="status-day" :class="{ today: day === now.getDate() && calendarMonth.getMonth() === now.getMonth() && calendarMonth.getFullYear() === now.getFullYear(), recorded: moodForDay(day) }" :title="moodForDay(day)?.label || ''"><small>{{ day }}</small><b v-if="moodForDay(day)" :data-mood="moodForDay(day).value">{{ moodForDay(day).emoji }}</b></span></div>
        </section>
      </aside>
      <section class="profile-main profile-panel profile-story">
        <div class="profile-title-row"><div><span class="eyebrow">HELLO, NICE TO MEET YOU</span><h2>关于我</h2></div><button v-if="isAdmin && !editing" class="profile-edit-btn" @click="startEditing">编辑资料</button></div>
        <template v-if="!editing"><p class="profile-intro">{{ profile.intro }}</p><div class="profile-note"><span>最近感兴趣</span><strong>{{ profile.interests }}</strong></div><blockquote>“保持敏锐，也允许自己偶尔慢下来。”</blockquote></template>
        <form v-else class="profile-form" @submit.prevent="submit">
          <label>名字<input v-model="draft.name" /></label><label>所在地<input v-model="draft.location" /></label><label>个人签名<input v-model="draft.tagline" /></label>
          <label>个人介绍<textarea v-model="draft.intro" rows="5"></textarea></label><label>兴趣关键词<input v-model="draft.interests" /></label><label>GitHub 链接<input v-model="draft.github" /></label>
          <label>头像图片<input type="file" accept="image/*" @change="fileToDataUrl($event, 'avatar')" /></label><label>封面图片<input type="file" accept="image/*" @change="fileToDataUrl($event, 'cover')" /></label>
          <div class="profile-form-actions"><button type="button" @click="editing = false">取消</button><button type="submit">保存更改</button></div>
        </form>
      </section>
    </div>
  </main>
</template>
