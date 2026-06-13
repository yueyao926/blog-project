<script setup>
defineProps({
  articleCount: {
    type: Number,
    default: 0,
  },
})
</script>

<template>
  <div class="col-span-3">
    <div
      class="
        glass-card
        sidebar-card
        p-6
        sticky
        top-24
        animate-fade-up
      "
    >
      <span class="meng-deco meng-deco-1">✿</span>
      <span class="meng-deco meng-deco-2">+</span>
      <span class="meng-deco meng-deco-3">+</span>
      <span class="meng-deco meng-deco-4">✿</span>

      <div class="avatar-frame">
        <img
          src="/meng-er-avatar.png"
          alt="Yueyao"
        />
      </div>

      <h2
        class="
          font-display
          text-2xl
          font-bold
          text-center
          mt-5
          text-[#6b5d4d]
        "
      >
        Yueyao
      </h2>

      <p
        class="
          text-[#a89478]
          text-center
          mt-3
          leading-7
          text-sm
        "
      >
        你好呀，欢迎来到我的空间~
      </p>

      <div
        class="
          mt-6
          flex
          justify-center
          gap-3
        "
      >
        <a
          href="https://github.com/yueyao926"
          target="_blank"
          rel="noopener noreferrer"
          class="btn-dark"
        >
          GitHub
        </a>

        <a
          href="#"
          class="btn-primary"
        >
          关于我
        </a>
      </div>

      <div class="section-divider"></div>

      <div class="space-y-1 text-[#a89478] text-sm">
        <div class="stat-item">
          <span><span class="stat-icon">✿</span>文章</span>
          <span class="stat-value">{{ articleCount }}</span>
        </div>

        <div class="stat-item">
          <span><span class="stat-icon">+</span>分类</span>
          <span class="stat-value">1</span>
        </div>

        <div class="stat-item">
          <span><span class="stat-icon">✿</span>标签</span>
          <span class="stat-value">3</span>
        </div>
      </div>

      <p class="sidebar-footer">
        学会放松 · 奇迹自会悄悄发生
      </p>
    </div>
  </div>
</template>
