<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue"

const root = ref(null)
const scroll = ref(0)
const vh = ref(1)
const scene = computed(() => scroll.value < vh.value * .72 ? 0 : scroll.value < vh.value * 1.85 ? 1 : 2)

const update = () => {
  scroll.value = window.scrollY
  vh.value = window.innerHeight || 1
  root.value?.style.setProperty("--sy", `${scroll.value}px`)
}

const point = (event) => {
  root.value?.style.setProperty("--px", `${(event.clientX / innerWidth - .5).toFixed(3)}`)
  root.value?.style.setProperty("--py", `${(event.clientY / innerHeight - .5).toFixed(3)}`)
}

onMounted(() => {
  update()
  addEventListener("scroll", update, { passive: true })
  addEventListener("resize", update)
})
onUnmounted(() => {
  removeEventListener("scroll", update)
  removeEventListener("resize", update)
})
</script>

<template>
  <main ref="root" class="cinema-home" :class="`cinema-scene-${scene}`" @pointermove="point">
    <section class="cinema-hero">
      <div class="cinema-sky"></div>
      <div class="cinema-hills far"></div>
      <div class="cinema-hills near"></div>
      <div class="cinema-light"></div>
      <div class="cinema-leaves leaves-left"></div>
      <div class="cinema-leaves leaves-right"></div>

      <nav class="cinema-nav">
        <router-link class="cinema-brand" to="/"><i>◆</i> Yueyao Blog</router-link>
        <div><router-link to="/">首页</router-link><router-link to="/articles">文章</router-link><router-link to="/projects">项目</router-link><router-link to="/about">关于</router-link></div>
      </nav>

      <div class="cinema-copy">
        <p>WRITING · MAKING · WANDERING</p>
        <h1>聚沙成塔，<br>做纯粹的争冠者</h1>
        <blockquote>And miles to go before I sleep.</blockquote>
        <router-link to="/articles">开始漫游 <span>→</span></router-link>
      </div>

      <div class="cinema-panda hero-panda-real">
        <img src="../assets/panda-traveler-hd.png" alt="熊猫旅行者">
        <div class="gaze-dot"></div>
      </div>
      <div class="cinema-sign"><span>Good</span><span>Things</span><span>Ahead ♡</span></div>
      <div class="cinema-scroll"><i></i>SCROLL TO WANDER</div>
      <div class="torn torn-bottom"></div>
    </section>

    <section class="cinema-story">
      <header><h2>最近在写</h2><i></i></header>
      <router-link to="/articles" class="cinema-paper-card">
        <b class="paperclip">⌇</b>
        <div class="cinema-photo"><span></span></div>
        <div><h3>学习与创造</h3><span>→</span></div>
      </router-link>
      <div class="peek-stage"><img src="../assets/panda-peek-hd.png" alt="熊猫正在看向文章卡片"><i></i></div>
      <div class="rock-note">Notes<br>Ideas<br>A Kinder Me</div>
      <div class="cinema-now"><img src="../assets/panda-peek-hd.png" alt=""><span>NOW · 正在探索</span></div>
      <div class="torn torn-bottom"></div>
    </section>

    <section class="cinema-portals">
      <div class="portal-landscape"></div>
      <div class="real-portal-grid">
        <router-link to="/articles" class="real-portal"><img class="portal-illustration" src="../assets/portal-books-watercolor.png" alt="手绘书本"><h3>文章</h3><p>FIELD NOTES</p><span>→</span></router-link>
        <router-link to="/projects" class="real-portal"><img class="portal-illustration" src="../assets/portal-camera-watercolor.png" alt="手绘相机"><h3>项目</h3><p>MADE BY HAND</p><span>→</span></router-link>
        <router-link to="/about" class="real-portal"><img class="portal-illustration" src="../assets/portal-panda-watercolor.png" alt="手绘萌二"><h3>关于我</h3><p>THIS IS YUEYAO</p><span>→</span></router-link>
      </div>
      <footer>YUEYAO'S PERSONAL ARCHIVE</footer>
    </section>
  </main>
</template>
