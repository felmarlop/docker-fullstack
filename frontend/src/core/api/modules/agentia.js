import api from '../index'

export function runAgent(prompt) {
  return api.post(`ai/agent/`, { prompt: prompt })
}

export function listConversations(params = {}) {
  return api.get(`conversations/`, params)
}

export function getConversation(conversationId) {
  return api.get(`conversations/${conversationId}/`)
}

export function listMessages(params = {}) {
  return api.get(`conversation/messages/`, { params })
}

export function getMessage(messageId) {
  return api.get(`conversation/messages/${messageId}/`)
}
