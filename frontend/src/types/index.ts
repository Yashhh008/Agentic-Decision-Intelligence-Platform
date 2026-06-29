// ADIP — Shared TypeScript Types
// Keep in sync with backend Pydantic models

export interface Customer {
  customer_id: string
  company_name: string
  industry: string
  health_score: number
  renewal_date: string
  active_users: number
  licensed_users: number
  contract_value: number
  champion_status: string
  months_active: number
}

export interface Session {
  session_id: string
  customer_id: string
  interaction_type: string
  status: string
  planner_summary: string | null
  created_at: string | null
}

export interface PlannerDecision {
  session_id: string
  detected_signals: string[]
  selected_capabilities: string[]
  selected_agents: string[]
  skipped_agents: string[]
  planner_reasoning: string
  execution_mode: string
  execution_time_ms: number | null
}

export interface KnowledgeChunk {
  content: string
  source: string
  document_type: string
  similarity_score: number
}

export interface Recommendation {
  recommendation_id: string
  session_id: string
  action: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  confidence: number
  reasoning: string
  evidence_source: string[]
  business_rule: string
  decision: 'pending' | 'approved' | 'rejected' | 'overridden'
  created_at: string | null
}

export interface MemoryRecord {
  memory_id: string
  customer_id: string
  recommendation: string
  decision: string
  outcome: string | null
  health_score_before: number | null
  health_score_after: number | null
  signals: string[]
  timestamp: string | null
}

export interface AnalyticsDashboard {
  total_customers: number
  average_health_score: number
  total_recommendations: number
  average_confidence: number
  total_decisions: number
  approved_count: number
  rejected_count: number
  overridden_count: number
  approval_rate: number
  memory_records: number
}

export type InteractionType = 'meeting_transcript' | 'crm_update' | 'email' | 'support_ticket'

export type ViewMode = 'dashboard' | 'workspace' | 'insights'
