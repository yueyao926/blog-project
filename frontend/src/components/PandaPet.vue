<template>
  <div
    class="npc"
    :class="{ 'is-ready': isReady }"
    @click="handleClick"
    @mouseenter="handleMouseEnter"
  >
    <div ref="positionLayer" class="panda-position">
      <Transition name="bubble">
        <div v-if="message" class="bubble" role="status">
          {{ message }}
        </div>
      </Transition>

      <div class="panda-interaction" :class="{ 'is-bouncing': isBouncing }">
        <Transition name="panda-swap">
          <img
            :key="mood"
            :src="images[mood]"
            class="npc-img"
            alt="小熊猫萌二"
            draggable="false"
          />
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue"

import angry from "../assets/panda_angry.png"
import happy from "../assets/panda_happy.png"
import hello from "../assets/panda_hello.png"
import idle from "../assets/panda_idle.png"
import sad from "../assets/panda_sad.png"
import sleepy from "../assets/panda_sleepy.png"

const images = { idle, happy, angry, sleepy, sad, hello }

const isReady = ref(false)
const isBouncing = ref(false)
const message = ref("")
const mood = ref("idle")
const positionLayer = ref(null)

let emotion = 50
let isInteracting = false
let clickCount = 0
let targetX = 0
let targetY = 0
let currentX = 0
let currentY = 0
let animationFrame = 0
let bounceTimer = 0
let clickTimer = 0
let moodTimer = 0
let sceneTimer = 0
let helloCooldownUntil = 0

function setScene(nextMood, nextMessage = "", duration = 0) {
  window.clearTimeout(sceneTimer)
  mood.value = nextMood
  message.value = nextMessage
  isInteracting = duration > 0

  if (duration) {
    sceneTimer = window.setTimeout(() => {
      isInteracting = false
      message.value = ""
      applyAmbientMood()
    }, duration)
  }
}

function applyAmbientMood() {
  if (isInteracting) return
  mood.value = emotion < 18 ? "sleepy" : "idle"
}

function bounce() {
  window.clearTimeout(bounceTimer)
  isBouncing.value = false
  requestAnimationFrame(() => {
    isBouncing.value = true
    bounceTimer = window.setTimeout(() => {
      isBouncing.value = false
    }, 320)
  })
}

function handleClick() {
  clickCount += 1
  window.clearTimeout(clickTimer)
  clickTimer = window.setTimeout(() => {
    clickCount = 0
  }, 900)

  if (clickCount >= 5) {
    emotion = 0
    setScene("angry", "你别一直戳我！！", 3000)
    return
  }

  emotion = Math.min(100, emotion + 10)
  bounce()
  setScene("happy", "嘿嘿！是找我玩吗？", 3000)
}

function handleMouseEnter() {
  if (isInteracting || Date.now() < helloCooldownUntil) return
  helloCooldownUntil = Date.now() + 12000
  setScene("hello", "嗨，你来啦！", 3000)
}

function handleMouseMove(event) {
  targetX = (event.clientX / window.innerWidth - 0.5) * 18
  targetY = (event.clientY / window.innerHeight - 0.5) * 12

  const distanceFromPet = Math.hypot(
    window.innerWidth - event.clientX,
    window.innerHeight - event.clientY
  )

  if (distanceFromPet < 150 && emotion < 35 && !isInteracting) {
    setScene("sad", "陪陪我嘛……", 3000)
  }
}

function animatePosition() {
  currentX += (targetX - currentX) * 0.1
  currentY += (targetY - currentY) * 0.1

  if (positionLayer.value) {
    positionLayer.value.style.transform =
      `translate3d(${currentX.toFixed(2)}px, ${currentY.toFixed(2)}px, 0)`
  }

  animationFrame = requestAnimationFrame(animatePosition)
}

function preloadImages() {
  return Promise.allSettled(
    Object.values(images).map((src) => new Promise((resolve) => {
      const image = new Image()
      image.onload = resolve
      image.onerror = resolve
      image.src = src
    }))
  )
}

onMounted(async () => {
  window.addEventListener("mousemove", handleMouseMove, { passive: true })
  animationFrame = requestAnimationFrame(animatePosition)

  await preloadImages()
  isReady.value = true

  moodTimer = window.setInterval(() => {
    emotion = Math.max(0, emotion - 3)
    applyAmbientMood()
  }, 5000)
})

onUnmounted(() => {
  window.removeEventListener("mousemove", handleMouseMove)
  cancelAnimationFrame(animationFrame)
  window.clearInterval(moodTimer)
  window.clearTimeout(bounceTimer)
  window.clearTimeout(clickTimer)
  window.clearTimeout(sceneTimer)
})
</script>

<style scoped>
.npc {
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: 999999;
  opacity: 0;
  pointer-events: none;
  filter: drop-shadow(0 10px 14px rgba(0, 0, 0, 0.2));
  transition: opacity 180ms ease;
}

.npc.is-ready {
  opacity: 1;
  pointer-events: auto;
}

.panda-position {
  position: relative;
  will-change: transform;
}

.panda-interaction {
  position: relative;
  cursor: pointer;
  transition: transform 160ms ease;
}

.panda-interaction:hover {
  transform: scale(1.04);
}

.panda-interaction.is-bouncing {
  animation: bounce 320ms ease-out;
}

.npc-img {
  display: block;
  width: 150px;
  height: 150px;
  object-fit: contain;
  user-select: none;
  animation: breathe 2.6s ease-in-out infinite;
}

.bubble {
  position: absolute;
  right: 8px;
  bottom: 138px;
  padding: 7px 11px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  color: #312b27;
  font-size: 13px;
  line-height: 1.4;
  white-space: nowrap;
}

.bubble::after {
  position: absolute;
  right: 22px;
  bottom: -6px;
  width: 12px;
  height: 12px;
  background: white;
  content: "";
  transform: rotate(45deg);
}

.bubble-enter-active,
.bubble-leave-active,
.panda-swap-enter-active,
.panda-swap-leave-active {
  transition: opacity 120ms ease;
}

.bubble-enter-from,
.bubble-leave-to {
  opacity: 0;
  transform: translateY(5px) scale(0.96);
}

.panda-swap-enter-from,
.panda-swap-leave-to {
  opacity: 0;
}

.panda-swap-leave-active {
  position: absolute;
  inset: 0;
}

@keyframes breathe {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-3px) scale(1.025); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0) scale(1); }
  40% { transform: translateY(-12px) scale(1.04, 0.97); }
  70% { transform: translateY(2px) scale(0.99, 1.02); }
}

@media (max-width: 768px) {
  .npc {
    right: 12px;
    bottom: 12px;
  }

  .npc-img {
    width: 104px;
    height: 104px;
  }

  .bubble {
    right: 0;
    bottom: 96px;
    max-width: 70vw;
    white-space: normal;
  }
}

@media (prefers-reduced-motion: reduce) {
  .npc,
  .panda-interaction,
  .npc-img,
  .bubble-enter-active,
  .bubble-leave-active,
  .panda-swap-enter-active,
  .panda-swap-leave-active {
    animation: none;
    transition: none;
  }
}
</style>
