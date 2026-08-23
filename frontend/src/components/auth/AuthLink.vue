<template>
  <div class="text-body-2 text-medium-emphasis text-center mt-4 auth-link">
    {{ text }}

    <RouterLink :to="to" class="text-primary font-weight-medium ms-1">
      {{ action }}
    </RouterLink>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '',
  },

  action: {
    type: String,
    required: true,
  },

  to: {
    type: String,
    required: true,
  },
})
</script>
