<template>
  <div class="npc" @click="handleClick">
    <img
      :src="currentImg"
      class="npc-img"
      :style="{
        transform: `translate(${offsetX}px, ${offsetY}px)`
      }"
    />

    <div v-if="message" class="bubble">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"

// ================= 图片 =================
import idle from "../assets/panda_idle.png"
import happy from "../assets/panda_happy.png"
import angry from "../assets/panda_angry.png"
import sleepy from "../assets/panda_sleepy.png"

const images = { idle, happy, angry, sleepy }

// ================= 状态 =================
const currentImg = ref(idle)
const message = ref("")
const mood = ref("idle")

// ================= 情绪值 =================
const emotion = ref(50)

// ================= 动画 =================
const offsetX = ref(0)
const offsetY = ref(0)

let targetX = 0
let targetY = 0

// ================= 控制 =================
const canClick = ref(true)

// ================= 连点检测（生气触发核心） =================
const clickCount = ref(0)
let clickTimer = null

// ================= 文案 =================
const messages = {
  idle: "好好学习，天天向上！",
  happy: "嘿嘿！是找我玩吗？",
  angry: "别戳我！！",
  sleepy: "我困了…"
}

// ================= 设置状态（唯一入口） =================
function setMood(m) {
  mood.value = m
  currentImg.value = images[m]
}

// ================= 点击交互（触发型设计） =================
function handleClick() {
  if (!canClick.value) return
  canClick.value = false

  // ===== 连点计数 =====
  clickCount.value++

  clearTimeout(clickTimer)
  clickTimer = setTimeout(() => {
    clickCount.value = 0
  }, 1500)

  // ===== 生气触发条件 =====
  if (clickCount.value >= 5) {
    emotion.value = 0
    setMood("angry")
    message.value = "你别一直戳我！！"

    setTimeout(() => {
      message.value = ""
      canClick.value = true
    }, 1200)

    return
  }

  // ===== 普通点击 =====
  emotion.value += 10

  setMood("happy")
  message.value = messages.happy

  // 轻微弹跳反馈
  offsetY.value -= 10
  setTimeout(() => {
    offsetY.value = 0
  }, 150)

  setTimeout(() => {
    message.value = ""
    canClick.value = true
  }, 800)
}

// ================= 鼠标跟随 =================
function handleMouseMove(e) {
  const cx = window.innerWidth / 2
  const cy = window.innerHeight / 2

  targetX = (e.clientX - cx) * 0.08
  targetY = (e.clientY - cy) * 0.08

  // ===== 距离检测（靠太近会紧张）=====
  const dx = window.innerWidth - e.clientX
  const dy = window.innerHeight - e.clientY
  const dist = Math.sqrt(dx * dx + dy * dy)

  if (dist < 150 && emotion.value < 40) {
    setMood("angry")
    message.value = "别吵我睡觉！"
    setTimeout(() => {
      message.value = ""
    }, 1200)
  }
}

// ================= 平滑动画 =================
function animate() {
  offsetX.value += (targetX - offsetX.value) * 0.12
  offsetY.value += (targetY - offsetY.value) * 0.12

  requestAnimationFrame(animate)
}

// ================= 情绪衰减（只改变状态，不说话） =================
let timer = null

onMounted(() => {
  window.addEventListener("mousemove", handleMouseMove)
  animate()

  timer = setInterval(() => {
    emotion.value -= 3

    if (emotion.value < 30) {
      setMood("sleepy")
    } else if (emotion.value > 70) {
      setMood("happy")
    } else {
      setMood("idle")
    }
  }, 4000)
})

onUnmounted(() => {
  window.removeEventListener("mousemove", handleMouseMove)
  clearInterval(timer)
})
</script>

<style scoped>
.npc {
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: 999999;
  filter: drop-shadow(0 10px 14px rgba(0,0,0,0.2));
}

.npc-img {
  width: 150px;
  cursor: pointer;
  animation: breathe 2.5s ease-in-out infinite;
  transition: transform 0.15s ease;
}

.npc-img:hover {
  transform: scale(1.08);
}

.bubble {
  position: absolute;
  bottom: 110px;
  right: 0;

  background: white;
  padding: 6px 10px;
  border-radius: 10px;
  font-size: 13px;

  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  white-space: nowrap;
}

/* 呼吸感 */
@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@media (max-width: 768px) {
  .npc {
    right: 12px;
    bottom: 12px;
  }

  .npc-img {
    width: 90px;
  }

  .bubble {
    bottom: 72px;
    max-width: 70vw;
    white-space: normal;
  }
}
</style>
