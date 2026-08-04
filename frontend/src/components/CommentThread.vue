<script setup>
import { ref } from "vue"

defineProps({ comment: Object, depth: { type: Number, default: 0 } })
const emit = defineEmits(["reply", "like", "remove"])
const collapsed = ref(false)
</script>

<template>
  <article class="comment-node" :style="{ '--depth': Math.min(depth, 5) }">
    <div class="comment-head">
      <span class="comment-avatar">{{ comment.user.username.slice(0, 1).toUpperCase() }}</span>
      <div class="min-w-0 flex-1">
        <div class="comment-author">{{ comment.user.username }}</div>
        <time>{{ new Date(comment.created_at).toLocaleString('zh-CN') }}</time>
      </div>
    </div>
    <p>{{ comment.content }}</p>
    <div class="comment-actions">
      <button @click="emit('reply', comment)">回复</button>
      <button class="heart-action" @click="emit('like', comment)" aria-label="点赞评论">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.7-7.5 1.1-1.1a5.5 5.5 0 0 0 0-7.8Z"/></svg>
        {{ comment.like_count || 0 }}
      </button>
      <button v-if="comment.children?.length" @click="collapsed = !collapsed">
        {{ collapsed ? `展开 ${comment.children.length} 条回复` : '收起回复' }}
      </button>
      <button class="comment-delete" @click="emit('remove', comment)">删除</button>
    </div>
    <div v-if="!collapsed" class="comment-children">
      <CommentThread
        v-for="child in comment.children"
        :key="child.id"
        :comment="child"
        :depth="depth + 1"
        @reply="emit('reply', $event)"
        @like="emit('like', $event)"
        @remove="emit('remove', $event)"
      />
    </div>
  </article>
</template>
