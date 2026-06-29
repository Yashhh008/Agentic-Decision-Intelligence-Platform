// ADIP — API Client
// All API communication goes through this module.

import axios from 'axios'
import type {
  Customer, Session, PlannerDecision, KnowledgeChunk,
  Recommendation, MemoryRecord, AnalyticsDashboard, InteractionType,
} from '../types'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// ── Response unwrapper ────────────────────────────────────────────────────
const unwrap = <T>(response: { data: { data: T } }): T => response.data.data

// ── Customers ─────────────────────────────────────────────────────────────
export const getCustomers = () =>
  api.get<{ data: Customer[] }>('/customers').then(unwrap)

export const getCustomer = (id: string) =>
  api.get<{ data: Customer }>(`/customers/${id}`).then(unwrap)

export const getCustomerHistory = (id: string) =>
  api.get<{ data: any[] }>(`/customers/${id}/history`).then(unwrap)

export const getCustomerMemory = (id: string) =>
  api.get<{ data: MemoryRecord[] }>(`/customers/${id}/memory`).then(unwrap)

// ── Sessions ──────────────────────────────────────────────────────────────
export const createSession = (params: {
  customer_id: string
  interaction_type: InteractionType
  interaction_text: string
}) => api.post<{ data: { session_id: string; status: string } }>('/sessions', params).then(unwrap)

export const getSession = (id: string) =>
  api.get<{ data: Session }>(`/sessions/${id}`).then(unwrap)

export const analyzeSession = (id: string) =>
  api.post<{ data: { status: string } }>(`/sessions/${id}/analyze`).then(unwrap)

// ── Planner ───────────────────────────────────────────────────────────────
export const getPlannerDecision = (sessionId: string) =>
  api.get<{ data: PlannerDecision }>(`/sessions/${sessionId}/planner`).then(unwrap)

// ── Knowledge ─────────────────────────────────────────────────────────────
export const getSessionKnowledge = (sessionId: string) =>
  api.get<{ data: { chunks: KnowledgeChunk[] } }>(`/sessions/${sessionId}/knowledge`).then(unwrap)

// ── Recommendations ───────────────────────────────────────────────────────
export const getRecommendations = (sessionId: string) =>
  api.get<{ data: Recommendation[] }>(`/sessions/${sessionId}/recommendations`).then(unwrap)

export const updateRecommendation = (
  recId: string,
  decision: 'approved' | 'rejected' | 'overridden',
  customAction?: string
) =>
  api.patch<{ data: any }>(`/recommendations/${recId}`, {
    decision,
    custom_action: customAction,
  }).then(unwrap)

// ── Analytics ─────────────────────────────────────────────────────────────
export const getDashboardAnalytics = () =>
  api.get<{ data: AnalyticsDashboard }>('/analytics/dashboard').then(unwrap)
