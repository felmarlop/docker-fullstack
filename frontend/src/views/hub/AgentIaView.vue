<template>
  <v-container class="py-10 py-md-14" fluid>
    <div class="mx-auto hub-content">
      <div class="text-md-headline-large text-headline-small font-weight-bold tracking-tight text-high-emphasis mb-8">
        Agent
      </div>

      <v-card variant="outlined" class="hub-card d-flex flex-column">
        <div class="ps-4 pe-3 border-b d-flex align-center justify-space-between bg-surface" style="min-height: 50px">
          <v-icon icon="mdi-robot-outline" color="primary" size="24" class="mr-1" />
          <v-spacer />
          <v-btn
            icon
            variant="text"
            color="error"
            size="small"
            class="mx-0"
            :disabled="!conversation || listingMessages"
            @click="confirmDeleteDialog = true"
          >
            <v-icon icon="mdi-trash-can-outline font-weight-bold" size="18" />
          </v-btn>
        </div>

        <v-card-text ref="chatContainer" class="chat-messages pa-6 grow overflow-y-auto d-flex flex-column">
          <div v-if="listingMessages || deleting" class="text-center text-muted ma-auto">
            <v-progress-circular indeterminate color="primary" size="32" class="mb-3" />
            <p>{{ deleting ? 'Deleting conversation...' : 'Loading conversation...' }}</p>
          </div>

          <div v-else-if="!messages.length" class="text-center text-muted ma-auto">
            <v-icon size="48" class="mb-2">mdi-robot-outline</v-icon>
            <p class="typewritten-reveal">Hello! I'm <b>LIA</b>, ask anything about your system!</p>
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
                {{ msg.role === 'user' ? 'You' : 'LIA' }}
              </div>
              <div class="text-body-medium whitespace-pre-wrap">{{ msg.content }}</div>
            </div>
          </div>

          <div v-if="loading && !listingMessages" class="d-flex justify-start mb-4 w-100">
            <div class="message-bubble pa-3 rounded-lg bg-grey-darken-3 text-high-emphasis d-flex align-center">
              <v-icon size="18" color="primary" class="mr-2 loading-icon">mdi-creation</v-icon>
              <span class="text-body-medium font-italic opacity-90">Thinking...</span>
            </div>
          </div>
        </v-card-text>
        <v-card-actions class="pa-4 bg-surface">
          <v-textarea
            v-model="prompt"
            placeholder="Ask LIA"
            rows="1"
            max-rows="3"
            auto-grow
            hide-details
            variant="outlined"
            class="rounded-xl"
            :disabled="loading"
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
                :disabled="!prompt.trim() || loading"
                @click="runAgent(prompt)"
              />
            </template>
          </v-textarea>
        </v-card-actions>
      </v-card>
    </div>

    <v-dialog v-model="confirmDeleteDialog" max-width="500">
      <v-card variant="outlined" class="danger-card bg-surface">
        <v-card-item class="pa-6 border-b">
          <template #prepend>
            <v-avatar color="error-lighten-5" size="44" class="mr-2">
              <v-icon icon="mdi-alert-octagon-outline" color="error" size="32" />
            </v-avatar>
          </template>
          <v-card-title class="font-weight-bold text-error"> Clear Conversation? </v-card-title>
        </v-card-item>

        <v-card-text class="pa-6 text-body-large text-medium-emphasis">
          Are you sure you want to delete all messages in this conversation?
        </v-card-text>

        <div class="pa-6 pt-0 d-flex justify-end ga-3">
          <v-btn
            variant="text"
            color="default"
            size="large"
            class="px-6 font-weight-bold"
            :disabled="deleting"
            @click="confirmDeleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            elevation="0"
            size="large"
            prepend-icon="mdi-trash-can-outline"
            :loading="deleting"
            class="px-6 font-weight-bold"
            @click="clearConversation()"
          >
            Clear
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { nextTick, ref, watch } from 'vue'
import * as aiApi from '@/core/api/modules/agentia'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

const MSG_SIZE = 6
const CONVERSATION_SIZE = 1
const AGENT_ERROR_MSG = 'An error occurred connecting to Lia. Please try again later.'

const conversation = ref(null)
const messages = ref([])
const prompt = ref('')
const loading = ref(false)
const deleting = ref(false)
const confirmDeleteDialog = ref(false)
const chatContainer = ref(null)
const listingMessages = ref(true)

async function listMessages() {
  try {
    loading.value = true
    const { data: conv } = await aiApi.listConversations({ page_size: CONVERSATION_SIZE })

    if (conv.results.length) {
      conversation.value = conv.results[0].id

      const { data: msg } = await aiApi.listMessages({ page_size: MSG_SIZE, conversation: conversation.value })
      messages.value = msg.results
      messages.value.reverse()
    }
  } catch {
    ui.showError(AGENT_ERROR_MSG)
  } finally {
    loading.value = false
    listingMessages.value = false
  }
}

async function runAgent(msg) {
  if (!msg) return

  let run = false
  try {
    loading.value = true
    prompt.value = ''

    addMessage(formatUserPrompt(msg))

    const { data } = await aiApi.runAgent(msg.trim())
    if (data.prompt && data.answer) {
      conversation.value = data.prompt.conversation

      messages.value.pop()
      addMessage(data.prompt)
      addMessage(data.answer)
      run = true
    }
  } catch {
    ui.showError(AGENT_ERROR_MSG)
  } finally {
    if (!run) await listMessages()
    loading.value = false
  }
}

async function clearConversation() {
  if (!conversation.value) return false

  try {
    deleting.value = true
    await aiApi.deleteConversation(conversation.value)
    conversation.value = null
    messages.value = []
    confirmDeleteDialog.value = false
  } catch {
    ui.showError('Could not clear conversation. Please try again.')
  } finally {
    deleting.value = false
  }
}

const addMessage = (msg) => {
  messages.value.push(msg)
  messages.value = messages.value.slice(-MSG_SIZE)
}

const formatUserPrompt = (msg) => {
  return { role: 'user', content: msg }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    const el = chatContainer.value.$el || chatContainer.value
    el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })
  }
}

listMessages()

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

.typewritten-reveal {
  font-family: 'Roboto Mono', Courier, monospace;
  overflow: hidden;
  white-space: nowrap;
  margin: 0 auto;
  letter-spacing: 0.01em;
  animation: typing 1.5s steps(55, end) forwards;
}

/* 3. The 'Reveal' Animation */
@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 100%;
  } /* Animates width from 0 to full line length */
}

/* 4. Optional Cursor Blink */
@keyframes blink-caret {
  from,
  to {
    border-color: transparent;
  }
  50% {
    border-color: rgb(var(--v-theme-primary));
  }
}
</style>
