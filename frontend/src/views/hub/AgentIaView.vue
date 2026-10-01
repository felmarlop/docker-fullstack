<template>
  <v-container class="py-10 py-md-14" fluid>
    <div class="mx-auto hub-content">
      <div class="text-md-headline-large text-headline-small font-weight-bold tracking-tight text-high-emphasis mb-8">
        Lia Agent
      </div>

      <v-card variant="outlined" class="hub-card d-flex flex-column">
        <v-card-text ref="chatContainer" class="chat-messages pa-6 grow overflow-y-auto d-flex flex-column">
          <div v-if="listingMessages" class="text-center text-muted ma-auto">
            <v-progress-circular indeterminate color="primary" size="32" class="mb-3" />
            <p>Loading conversation...</p>
          </div>
          <div v-else-if="!messages.length" class="text-center text-muted ma-auto">
            <v-icon size="48" class="mb-2">mdi-robot-outline</v-icon>
            <p>Ask anything about your system!</p>
          </div>
          <div
            v-for="(msg, index) in messages"
            v-else
            :key="index"
            class="d-flex mb-4 w-100"
            :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div
              class="message-bubble pa-3 rounded-lg max-w-75"
              :class="msg.role === 'user' ? 'bg-primary text-white' : 'bg-grey-darken-3 text-high-emphasis'"
            >
              <div class="text-caption font-weight-bold mb-1 opacity-70">
                {{ msg.role === 'user' ? 'You' : 'Assistant' }}
              </div>
              <div class="text-body-1 whitespace-pre-wrap">{{ msg.content }}</div>
            </div>
          </div>
          <div v-if="loading && !listingMessages" class="d-flex justify-start mb-4 w-100">
            <div class="message-bubble pa-3 rounded-lg bg-grey-darken-3 text-high-emphasis d-flex align-center">
              <v-icon size="18" color="primary" class="mr-2 loading-icon">mdi-creation</v-icon>
              <span class="text-body-2 font-italic opacity-80">Thinking...</span>
            </div>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4 bg-surface">
          <v-textarea
            v-model="prompt"
            placeholder="Ask Lia"
            rows="1"
            max-rows="3"
            auto-grow
            hide-details
            variant="outlined"
            class="rounded-xl"
            @keydown.enter.exact.prevent="runAgent(prompt)"
          >
            <template #prepend-inner>
              <v-icon class="mr-1 text-medium-emphasis" size="18">mdi-creation</v-icon>
            </template>

            <template #append-inner>
              <v-btn
                icon="mdi-send"
                color="primary"
                size="small"
                :disabled="!prompt.trim()"
                @click="runAgent(prompt)"
              />
            </template>
          </v-textarea>
        </v-card-actions>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import { nextTick, ref, watch } from 'vue'
import * as aiApi from '@/core/api/modules/agentia'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

const PAGE_SIZE = 6
const AGENT_ERROR_MSG = 'An error occurred connecting to the agent. Please try again later.'

let messages = ref([])
const prompt = ref('')
const loading = ref(false)
const chatContainer = ref(null)

async function listMessages() {
  try {
    loading.value = true
    const { data } = await aiApi.listMessages({ page_size: PAGE_SIZE })
    messages.value = data.results
    messages.value.reverse()
  } catch {
    ui.showError(AGENT_ERROR_MSG)
  } finally {
    loading.value = false
    listingMessages.value = false
  }
}

async function runAgent(msg) {
  if (!msg) return
  try {
    loading.value = true
    prompt.value = ''

    addMessage(formatUserPrompt(msg))

    const { data } = await aiApi.runAgent(msg)
    if (data.answer) {
      addMessage(data.answer)
    } else {
      listMessages()
    }
  } catch {
    ui.showError(AGENT_ERROR_MSG)
  } finally {
    loading.value = false
  }
}

const addMessage = (msg) => {
  messages.value.push(msg)
  messages.value = messages.value.splice(-PAGE_SIZE)
}

const formatUserPrompt = (msg) => {
  return { role: 'user', content: msg }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    const el = chatContainer.value.$el || chatContainer.value
    el.scrollTo({ top: el.scrollHeight })
  }
}

const listingMessages = ref(true)
listMessages()

// Watch both messages array and loading state to auto-scroll
watch(
  [messages, loading],
  () => {
    scrollToBottom()
  },
  { deep: true },
)
</script>

<style scoped>
.chat-messages {
  max-height: 540px;
}

.max-w-75 {
  max-width: 75%;
}

.whitespace-pre-wrap {
  white-space: pre-wrap;
}

.w-100 {
  width: 100%;
}

.loading-icon {
  animation: aiPulse 1s infinite ease-in-out;
  will-change: transform, filter, opacity;
}

@keyframes aiPulse {
  0% {
    transform: scale(1);
    filter: drop-shadow(0 0 0px rgba(var(--v-theme-primary), 0));
    opacity: 0.6;
  }
  50% {
    transform: scale(1.1);
    filter: drop-shadow(0 0 8px rgba(var(--v-theme-primary), 0.8));
    opacity: 1;
  }
  100% {
    transform: scale(1);
    filter: drop-shadow(0 0 0px rgba(var(--v-theme-primary), 0));
    opacity: 0.6;
  }
}
</style>
