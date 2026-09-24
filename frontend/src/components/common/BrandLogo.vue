<template>
  <svg
    class="brand-logo"
    :class="{ animated: animated }"
    :width="size"
    :height="size"
    viewBox="0 0 32 32"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M16 3L4 9.5L16 16L28 9.5L16 3Z"
      fill="currentColor"
      fill-opacity="0.15"
      stroke="currentColor"
      stroke-width="2"
      stroke-linejoin="round"
    />

    <path
      d="M4 15.5L16 22L28 15.5"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    />

    <path
      d="M4 21.5L16 28L28 21.5"
      stroke="#F97316"
      stroke-width="2.5"
      stroke-linecap="round"
      stroke-linejoin="round"
      style="stroke: rgb(var(--v-theme-primary, 249, 115, 22))"
    />

    <circle cx="16" cy="9.5" r="2.5" fill="#F97316" style="fill: rgb(var(--v-theme-primary, 249, 115, 22))" />
  </svg>
</template>

<script setup>
defineProps({
  size: {
    type: Number,
    default: 40,
  },
  animated: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.brand-logo.animated {
  animation: logoPulse 3s cubic-bezier(0.45, 0.05, 0.55, 0.95) forwards;
  transform-origin: center;
  will-change: transform, filter;
}

@keyframes logoPulse {
  0% {
    transform: translateY(0) scale(1);
    filter: drop-shadow(0 0 0px rgba(var(--v-theme-primary), 0));
  }
  50% {
    transform: translateY(-3px) scale(1.04);
    filter: drop-shadow(0 6px 12px rgba(var(--v-theme-primary), 0.55));
  }
  100% {
    transform: translateY(0) scale(1);
    filter: drop-shadow(0 0 0px rgba(var(--v-theme-primary), 0));
  }
}
</style>
