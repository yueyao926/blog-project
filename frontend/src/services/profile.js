import { reactive } from "vue"

const STORAGE_KEY = "yueyao-profile-v1"
const todayKey = () => new Date().toISOString().slice(0, 10)

export const moodOptions = [
  { value: "work", emoji: "💻", label: "工作中", group: "工作学习" },
  { value: "meeting", emoji: "🗣️", label: "开会中", group: "工作学习" },
  { value: "study", emoji: "📚", label: "学习中", group: "工作学习" },
  { value: "creating", emoji: "✍️", label: "创作中", group: "工作学习" },
  { value: "busy", emoji: "⏳", label: "忙碌中", group: "工作学习" },
  { value: "rest", emoji: "☕", label: "休息中", group: "生活休闲" },
  { value: "sleep", emoji: "😴", label: "睡觉中", group: "生活休闲" },
  { value: "music", emoji: "🎧", label: "听音乐", group: "生活休闲" },
  { value: "movie", emoji: "🎬", label: "看电影", group: "生活休闲" },
  { value: "gaming", emoji: "🎮", label: "玩游戏", group: "生活休闲" },
  { value: "reading", emoji: "📖", label: "阅读中", group: "生活休闲" },
  { value: "travel", emoji: "✈️", label: "旅行中", group: "出行运动" },
  { value: "walking", emoji: "🚶", label: "散步中", group: "出行运动" },
  { value: "exercise", emoji: "🏃", label: "运动中", group: "出行运动" },
  { value: "eating", emoji: "🍜", label: "干饭中", group: "出行运动" },
  { value: "happy", emoji: "😊", label: "开心", group: "今日心情" },
  { value: "excited", emoji: "🥳", label: "兴奋", group: "今日心情" },
  { value: "calm", emoji: "🌿", label: "平静", group: "今日心情" },
  { value: "tired", emoji: "🥱", label: "有点累", group: "今日心情" },
  { value: "sad", emoji: "😔", label: "有点难过", group: "今日心情" },
  { value: "stressed", emoji: "😵‍💫", label: "压力山大", group: "今日心情" },
  { value: "healing", emoji: "🌷", label: "治愈中", group: "今日心情" },
]

const defaults = {
  name: "Yueyao",
  avatar: "/meng-er-avatar.png",
  cover: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=85",
  tagline: "And miles to go before I sleep.",
  location: "Hangzhou, China",
  intro: "你好呀，我是 Yueyao。这里收藏我的学习笔记、技术实践，以及生活里值得记住的小小瞬间。",
  interests: "人工智能 · 全栈开发 · 摄影 · 旅行",
  github: "https://github.com/yueyao926",
  moods: {},
}

const readProfile = () => {
  try { return { ...defaults, ...JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}") } }
  catch { return { ...defaults } }
}

export const profile = reactive(readProfile())
export const currentMood = () => profile.moods[todayKey()] || ""
export const saveProfile = (value = profile) => {
  Object.assign(profile, value)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(profile))
  window.dispatchEvent(new CustomEvent("profile-updated"))
}
export const setTodayMood = (mood) => {
  profile.moods = { ...profile.moods, [todayKey()]: mood }
  saveProfile()
}
