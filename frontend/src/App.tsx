import { useState, useEffect, useCallback, useRef } from 'react'
import { QueryClient, QueryClientProvider, useQuery, useMutation } from '@tanstack/react-query'
import {
  Brain, Users, Activity, BarChart2, Zap, Shield,
  CheckCircle, XCircle, AlertTriangle, Database,
  BookOpen, TrendingUp, Star, Target, Loader2,
  Building2, Calendar, Eye, MessageSquare, ChevronRight,
  Cpu, Network, GitBranch, Layers, ArrowRight, Sparkles,
  Clock, UserCheck, Award, FileText, RefreshCw, Hash,
  Search, Filter, BrainCircuit, Workflow, Bot, FlaskConical
} from 'lucide-react'
import * as api from './api/client'
import type {
  Customer, Recommendation, PlannerDecision,
  KnowledgeChunk, MemoryRecord, ViewMode, InteractionType
} from './types'

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 30000 } }
})

// ── Utility helpers ───────────────────────────────────────────────────────
const healthColor = (s: number) => s >= 70 ? '#10b981' : s >= 40 ? '#f59e0b' : '#f43f5e'
const healthLabel = (s: number) => s >= 70 ? 'Healthy' : s >= 40 ? 'At Risk' : 'Critical'
const confidencePct = (c: number) => Math.round(c * 100)

const SIGNALS: Record<string, { color: string; label: string; icon: string }> = {
  churn_risk:          { color: '#f43f5e', label: 'Churn Risk',          icon: '⚠' },
  renewal_risk:        { color: '#f59e0b', label: 'Renewal Risk',        icon: '⏰' },
  upsell_opportunity:  { color: '#10b981', label: 'Upsell Opportunity',  icon: '📈' },
  onboarding_friction: { color: '#a855f7', label: 'Onboarding Friction', icon: '🔧' },
  dissatisfaction:     { color: '#f43f5e', label: 'Dissatisfaction',     icon: '😞' },
  feature_confusion:   { color: '#6366f1', label: 'Feature Confusion',   icon: '❓' },
  cancellation_intent: { color: '#ef4444', label: 'Cancel Intent',       icon: '🚫' },
  champion_resigned:   { color: '#f97316', label: 'Champion Resigned',   icon: '👤' },
  low_adoption:        { color: '#eab308', label: 'Low Adoption',        icon: '📉' },
  expansion_interest:  { color: '#10b981', label: 'Expansion Interest',  icon: '🚀' },
}

const AGENT_META: Record<string, { icon: any; color: string; desc: string }> = {
  ContextAgent:        { icon: BrainCircuit, color: '#22d3ee', desc: 'Signal Extraction'   },
  RetrievalAgent:      { icon: Search,       color: '#6366f1', desc: 'Knowledge Retrieval' },
  RiskAgent:           { icon: Shield,       color: '#f43f5e', desc: 'Risk Assessment'     },
  OpportunityAgent:    { icon: TrendingUp,   color: '#10b981', desc: 'Opportunity Detect'  },
  RenewalAgent:        { icon: Calendar,     color: '#f59e0b', desc: 'Renewal Analysis'    },
  RecommendationAgent: { icon: Sparkles,     color: '#a855f7', desc: 'Action Generation'  },
}

// ── Log generator for analysis stages ─────────────────────────────────────
const STAGE_LOGS: Record<string, { text: string; type: 'info' | 'success' | 'warn' | 'muted' }[]> = {
  'Creating session...':                 [{ text: '> Initializing analysis session', type: 'muted' }],
  'Extracting context...':              [{ text: '> ContextAgent: Parsing interaction text...', type: 'info' }, { text: '> Detecting business signals...', type: 'muted' }],
  'Retrieving organizational memory...': [{ text: '> MemoryService: Querying historical decisions', type: 'info' }],
  'Planning agent execution...':         [{ text: '> Planner: Analyzing signal matrix...', type: 'info' }, { text: '> Building dynamic execution plan', type: 'muted' }],
  'Generating recommendations...':       [{ text: '> ExecutionEngine: Running parallel agents', type: 'info' }, { text: '> BusinessRulesEngine: Evaluating thresholds', type: 'muted' }],
  'Complete':                            [{ text: '> Analysis complete. Recommendations generated.', type: 'success' }],
}

// ══════════════════════════════════════════════════════════════════════════
// ROOT
// ══════════════════════════════════════════════════════════════════════════
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="neural-bg" />
      <div className="grid-overlay" />
      <Dashboard />
    </QueryClientProvider>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// DASHBOARD (root layout)
// ══════════════════════════════════════════════════════════════════════════
function Dashboard() {
  const [view, setView] = useState<ViewMode>('dashboard')
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [analysisStage, setAnalysisStage] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [interactionText, setInteractionText] = useState('')
  const [interactionType, setInteractionType] = useState<InteractionType>('meeting_transcript')
  const [overrideText, setOverrideText] = useState('')
  const [overridingRecId, setOverridingRecId] = useState<string | null>(null)
  const [logs, setLogs] = useState<{ text: string; type: string }[]>([])

  const { data: customers = [], isLoading: customersLoading } = useQuery({
    queryKey: ['customers'],
    queryFn: api.getCustomers,
  })
  const { data: analytics, refetch: refetchAnalytics } = useQuery({
    queryKey: ['analytics'],
    queryFn: api.getDashboardAnalytics,
  })
  const { data: planner } = useQuery({
    queryKey: ['planner', sessionId],
    queryFn: () => api.getPlannerDecision(sessionId!),
    enabled: !!sessionId, retry: false, throwOnError: false,
  })
  const { data: knowledge } = useQuery({
    queryKey: ['knowledge', sessionId],
    queryFn: () => api.getSessionKnowledge(sessionId!),
    enabled: !!sessionId, retry: false, throwOnError: false,
  })
  const { data: recommendations = [], refetch: refetchRecs } = useQuery({
    queryKey: ['recommendations', sessionId],
    queryFn: () => api.getRecommendations(sessionId!),
    enabled: !!sessionId, retry: false, throwOnError: false,
  })
  const { data: memory = [], refetch: refetchMemory } = useQuery({
    queryKey: ['memory', selectedCustomer?.customer_id],
    queryFn: () => api.getCustomerMemory(selectedCustomer!.customer_id),
    enabled: !!selectedCustomer,
  })

  const approveMutation = useMutation({
    mutationFn: ({ id, decision, customAction }: {
      id: string; decision: 'approved' | 'rejected' | 'overridden'; customAction?: string
    }) => api.updateRecommendation(id, decision, customAction),
    onSuccess: () => {
      refetchRecs()
      refetchMemory()
      refetchAnalytics()
      queryClient.invalidateQueries({ queryKey: ['memory'] })
      queryClient.invalidateQueries({ queryKey: ['analytics'] })
    },
  })

  const addLog = useCallback((entries: { text: string; type: string }[]) => {
    setLogs(prev => [...prev.slice(-30), ...entries])
  }, [])

  const handleAnalyze = useCallback(async () => {
    if (!selectedCustomer || !interactionText.trim()) return
    setIsAnalyzing(true)
    setSessionId(null)
    setLogs([])
    let currentSessionId = ''
    const stages = [
      'Creating session...', 'Extracting context...',
      'Retrieving organizational memory...', 'Planning agent execution...',
      'Generating recommendations...', 'Complete',
    ]
    try {
      for (const stage of stages) {
        setAnalysisStage(stage)
        addLog(STAGE_LOGS[stage] || [])
        if (stage === 'Creating session...') {
          const sess = await api.createSession({
            customer_id: selectedCustomer.customer_id,
            interaction_type: interactionType,
            interaction_text: interactionText,
          })
          currentSessionId = sess.session_id
          setSessionId(currentSessionId)
          await new Promise(r => setTimeout(r, 400))
        } else if (stage === 'Generating recommendations...') {
          await api.analyzeSession(currentSessionId)
          await new Promise(r => setTimeout(r, 500))
        } else if (stage === 'Complete') {
          queryClient.invalidateQueries({ queryKey: ['planner', currentSessionId] })
          queryClient.invalidateQueries({ queryKey: ['knowledge', currentSessionId] })
          queryClient.invalidateQueries({ queryKey: ['recommendations', currentSessionId] })
        } else {
          await new Promise(r => setTimeout(r, 350))
        }
      }
    } catch {
      setAnalysisStage('Analysis failed.')
      addLog([{ text: '> ERROR: Analysis pipeline failed. Check backend.', type: 'warn' }])
    } finally {
      setIsAnalyzing(false)
    }
  }, [selectedCustomer, interactionText, interactionType, addLog])

  const handleSelectCustomer = (c: Customer) => {
    setSelectedCustomer(c)
    setSessionId(null)
    setAnalysisStage('')
    setLogs([])
    setInteractionText('')
    setView('workspace')
  }

  useEffect(() => {
    if (selectedCustomer?.customer_id === 'acme_corp' && !interactionText) {
      setInteractionText("We're struggling with onboarding, adoption is very low and our operations team has gone back to spreadsheets. We have two support tickets open for over two weeks with no resolution. Honestly, we're unsure whether we'll renew unless things improve significantly.")
    }
  }, [selectedCustomer])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', position: 'relative', zIndex: 1 }}>
      {/* ── HEADER ────────────────────────────────────────────────────────── */}
      <header style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 24px', height: 58, flexShrink: 0,
        borderBottom: '1px solid var(--border)',
        background: 'rgba(6,11,24,0.9)',
        backdropFilter: 'blur(20px)',
        position: 'relative', zIndex: 10,
      }}>
        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 20px rgba(99,102,241,0.4)',
          }}>
            <Brain size={18} color="white" />
          </div>
          <div>
            <span className="font-display gradient-text" style={{ fontWeight: 800, fontSize: 16, letterSpacing: '-0.5px' }}>ADIP</span>
            <span style={{ color: 'var(--text-muted)', fontWeight: 400, fontSize: 12, marginLeft: 8 }}>
              Agentic Decision Intelligence Platform
            </span>
          </div>
        </div>

        {/* Nav */}
        <nav style={{ display: 'flex', gap: 6 }}>
          {([
            ['dashboard', 'Dashboard', Users],
            ['workspace', 'Decision Workspace', Workflow],
            ['insights', 'Platform Insights', BarChart2],
          ] as [ViewMode, string, any][]).map(([v, label, Icon]) => (
            <button key={v} className={`nav-tab ${view === v ? 'active' : 'inactive'}`} onClick={() => setView(v)}>
              <Icon size={14} />
              {label}
            </button>
          ))}
        </nav>

        {/* Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          {analytics && (
            <div style={{ display: 'flex', gap: 16 }}>
              <QuickStat label="Avg Health" value={`${analytics.average_health_score}%`} color={healthColor(analytics.average_health_score)} />
              <QuickStat label="Approval Rate" value={`${analytics.approval_rate}%`} color="#10b981" />
            </div>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '5px 12px', borderRadius: 20, background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.25)' }}>
            <div className="live-dot" />
            <span style={{ fontSize: 11, color: '#10b981', fontWeight: 600 }}>NimbusCRM</span>
          </div>
        </div>
      </header>

      {/* ── BODY ──────────────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>

        {/* ── SIDEBAR ─────────────────────────────────────────────────────── */}
        <aside style={{
          width: 268, flexShrink: 0,
          borderRight: '1px solid var(--border)',
          background: 'rgba(8,14,31,0.8)',
          backdropFilter: 'blur(10px)',
          display: 'flex', flexDirection: 'column', overflow: 'hidden',
        }}>
          <div style={{ padding: '14px 16px 6px', display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontSize: 10, fontWeight: 700, color: 'var(--text-muted)', letterSpacing: 1.2, textTransform: 'uppercase' }}>
              Customer Portfolio
            </span>
            <span style={{ fontSize: 10, padding: '2px 7px', borderRadius: 10, background: 'var(--electric-dim)', color: 'var(--text-accent)', fontWeight: 700 }}>
              {customers.length}
            </span>
          </div>

          <div style={{ flex: 1, overflowY: 'auto', padding: '4px 10px 10px' }}>
            {customersLoading ? (
              [1, 2, 3, 4].map(i => (
                <div key={i} style={{ padding: '10px 12px', marginBottom: 4 }}>
                  <div className="skeleton" style={{ height: 12, width: '70%', marginBottom: 8 }} />
                  <div className="skeleton" style={{ height: 8, width: '50%' }} />
                </div>
              ))
            ) : customers.map(c => (
              <CustomerSidebarItem
                key={c.customer_id}
                customer={c}
                selected={selectedCustomer?.customer_id === c.customer_id}
                onClick={() => handleSelectCustomer(c)}
              />
            ))}
          </div>

          {/* Platform Stats */}
          {analytics && (
            <div style={{ padding: '14px 16px', borderTop: '1px solid var(--border)' }}>
              <div style={{ fontSize: 9, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: 1.2, marginBottom: 10, fontWeight: 700 }}>Platform Stats</div>
              <SidebarStat label="Recommendations" value={String(analytics.total_recommendations)} icon={Star} />
              <SidebarStat label="Memory Records" value={String(analytics.memory_records)} icon={Database} />
              <SidebarStat label="Decisions Made" value={String(analytics.total_decisions)} icon={CheckCircle} />
            </div>
          )}
        </aside>

        {/* ── MAIN CONTENT ─────────────────────────────────────────────────── */}
        <main style={{ flex: 1, overflowY: 'auto', padding: '24px', position: 'relative' }}>
          {view === 'dashboard' && (
            <DashboardView customers={customers} analytics={analytics} onSelectCustomer={handleSelectCustomer} />
          )}
          {view === 'workspace' && (
            <WorkspaceView
              customer={selectedCustomer}
              interactionText={interactionText}
              setInteractionText={setInteractionText}
              interactionType={interactionType}
              setInteractionType={setInteractionType}
              isAnalyzing={isAnalyzing}
              analysisStage={analysisStage}
              logs={logs}
              planner={planner}
              knowledge={knowledge?.chunks || []}
              recommendations={recommendations}
              memory={memory}
              onAnalyze={handleAnalyze}
              onApprove={(id: string) => approveMutation.mutate({ id, decision: 'approved' })}
              onReject={(id: string) => approveMutation.mutate({ id, decision: 'rejected' })}
              onOverride={(id: string) => setOverridingRecId(id)}
              overridingRecId={overridingRecId}
              overrideText={overrideText}
              setOverrideText={setOverrideText}
              onSubmitOverride={(id: string) => {
                approveMutation.mutate({ id, decision: 'overridden', customAction: overrideText })
                setOverridingRecId(null)
                setOverrideText('')
              }}
              isPendingMutation={approveMutation.isPending}
              sessionId={sessionId}
            />
          )}
          {view === 'insights' && (
            <InsightsView analytics={analytics} customers={customers} />
          )}
        </main>
      </div>
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// DASHBOARD VIEW
// ══════════════════════════════════════════════════════════════════════════
function DashboardView({ customers, analytics, onSelectCustomer }: {
  customers: Customer[]; analytics: any; onSelectCustomer: (c: Customer) => void
}) {
  return (
    <div style={{ maxWidth: 1200 }}>
      {/* Hero */}
      <div className="animate-fade-in-up" style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
          <div style={{ padding: '4px 12px', borderRadius: 20, background: 'var(--electric-dim)', border: '1px solid rgba(99,102,241,0.3)', fontSize: 12, color: 'var(--text-accent)', fontWeight: 600 }}>
            ⚡ AI-Powered · Multi-Agent · Real-Time
          </div>
        </div>
        <h1 className="font-display" style={{ fontSize: 30, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 8 }}>
          Customer Intelligence{' '}
          <span className="gradient-text">Dashboard</span>
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: 14, maxWidth: 520 }}>
          Monitor portfolio health, detect churn signals early, and deploy evidence-backed AI recommendations — all with human oversight.
        </p>
      </div>

      {/* Analytics KPIs */}
      {analytics && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 28 }}>
          <KpiCard label="Avg Health Score" value={`${analytics.average_health_score}`} unit="%" icon={Activity} color="#10b981" glow="rgba(16,185,129,0.25)" delay={0} />
          <KpiCard label="AI Recommendations" value={String(analytics.total_recommendations)} icon={Sparkles} color="#6366f1" glow="rgba(99,102,241,0.25)" delay={80} />
          <KpiCard label="Approval Rate" value={`${analytics.approval_rate}`} unit="%" icon={CheckCircle} color="#22d3ee" glow="rgba(34,211,238,0.2)" delay={160} />
          <KpiCard label="Memory Records" value={String(analytics.memory_records)} icon={Database} color="#a855f7" glow="rgba(168,85,247,0.25)" delay={240} />
        </div>
      )}

      {/* Customer Table */}
      <div className="glass" style={{ overflow: 'hidden', animation: 'fade-in-up 0.5s ease 0.2s both' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <Network size={16} color="var(--text-accent)" />
            <span style={{ fontWeight: 700, fontSize: 15 }}>Customer Portfolio</span>
            <span style={{ fontSize: 11, padding: '2px 8px', borderRadius: 10, background: 'var(--electric-dim)', color: 'var(--text-accent)', fontWeight: 700 }}>
              {customers.length} accounts
            </span>
          </div>
          <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>Click to open Decision Workspace →</div>
        </div>
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                {['Company', 'Industry', 'Health', 'Renewal Date', 'Adoption', 'ARR', 'Champion', 'Action'].map(h => (
                  <th key={h}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {customers.map((c, idx) => {
                const color = healthColor(c.health_score)
                const adoption = c.licensed_users > 0 ? Math.round(c.active_users / c.licensed_users * 100) : 0
                return (
                  <tr key={c.customer_id} style={{ animationDelay: `${idx * 60}ms` }} className="animate-fade-in">
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <div style={{ width: 32, height: 32, borderRadius: 8, background: `${color}18`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                          <Building2 size={15} color={color} />
                        </div>
                        <span style={{ fontWeight: 600, fontSize: 14 }}>{c.company_name}</span>
                      </div>
                    </td>
                    <td style={{ color: 'var(--text-secondary)', fontSize: 13 }}>{c.industry}</td>
                    <td>
                      <HealthPill score={c.health_score} />
                    </td>
                    <td style={{ color: 'var(--text-secondary)', fontSize: 13, whiteSpace: 'nowrap' }}>
                      <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
                        <Calendar size={12} color="var(--text-muted)" /> {c.renewal_date}
                      </span>
                    </td>
                    <td>
                      <AdoptionBar value={adoption} />
                    </td>
                    <td style={{ color: 'var(--text-primary)', fontSize: 13, fontWeight: 600 }}>${(c.contract_value / 1000).toFixed(0)}k</td>
                    <td>
                      <span style={{
                        fontSize: 11, padding: '3px 9px', borderRadius: 20, fontWeight: 600,
                        background: c.champion_status === 'resigned' ? 'rgba(244,63,94,0.12)' : c.champion_status === 'strong' ? 'rgba(16,185,129,0.12)' : 'rgba(245,158,11,0.12)',
                        color: c.champion_status === 'resigned' ? '#f43f5e' : c.champion_status === 'strong' ? '#10b981' : '#f59e0b',
                        border: `1px solid ${c.champion_status === 'resigned' ? 'rgba(244,63,94,0.25)' : c.champion_status === 'strong' ? 'rgba(16,185,129,0.25)' : 'rgba(245,158,11,0.25)'}`,
                      }}>{c.champion_status}</span>
                    </td>
                    <td>
                      <button className="btn-ghost" onClick={() => onSelectCustomer(c)} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12 }}>
                        Analyze <ArrowRight size={12} />
                      </button>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// WORKSPACE VIEW — Heart of the Demo
// ══════════════════════════════════════════════════════════════════════════
function WorkspaceView({
  customer, interactionText, setInteractionText, interactionType, setInteractionType,
  isAnalyzing, analysisStage, logs, planner, knowledge, recommendations, memory,
  onAnalyze, onApprove, onReject, onOverride, overridingRecId, overrideText, setOverrideText,
  onSubmitOverride, isPendingMutation, sessionId
}: any) {
  if (!customer) {
    return (
      <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '70vh', gap: 20 }}>
        <div className="animate-float">
          <div style={{ width: 80, height: 80, borderRadius: 24, background: 'var(--electric-dim)', border: '1px solid rgba(99,102,241,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Workflow size={36} color="var(--text-accent)" />
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <h2 className="font-display" style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>Select a Customer</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Choose an account from the sidebar to open the AI Decision Workspace</p>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', justifyContent: 'center' }}>
          {['Multi-Agent Orchestration', 'RAG Evidence', 'HITL Approval', 'Memory Learning'].map(f => (
            <span key={f} className="badge badge-electric">{f}</span>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 1200 }}>
      {/* Customer Header */}
      <CustomerHeader customer={customer} />

      {/* Agent Pipeline Visualization */}
      <div className="glass animate-fade-in-up" style={{ padding: '18px 20px', margin: '20px 0', overflow: 'hidden' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
          <GitBranch size={15} color="var(--text-accent)" />
          <span style={{ fontWeight: 700, fontSize: 13 }}>Agent Execution Pipeline</span>
          <span className="badge badge-electric" style={{ fontSize: 10 }}>LangGraph Orchestration</span>
          {isAnalyzing && (
            <span style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--cyan)' }}>
              <Loader2 size={12} className="animate-spin" /> {analysisStage}
            </span>
          )}
          {analysisStage === 'Complete' && !isAnalyzing && (
            <span style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--emerald)' }}>
              <CheckCircle size={12} /> Pipeline complete
            </span>
          )}
        </div>
        <AgentPipeline planner={planner} isAnalyzing={isAnalyzing} analysisStage={analysisStage} />
      </div>

      {/* Main Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 20 }}>
        {/* LEFT */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

          {/* Interaction Input */}
          <div className="glass glass-glow" style={{ padding: 22 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
              <MessageSquare size={15} color="var(--text-accent)" />
              <span style={{ fontWeight: 700, fontSize: 14 }}>Customer Interaction Input</span>
            </div>
            <div style={{ display: 'flex', gap: 6, marginBottom: 14, flexWrap: 'wrap' }}>
              {(['meeting_transcript', 'crm_update', 'email', 'support_ticket'] as InteractionType[]).map(t => (
                <button key={t} className={`int-type-btn ${interactionType === t ? 'active' : ''}`} onClick={() => setInteractionType(t)}>
                  {t.replace('_', ' ')}
                </button>
              ))}
            </div>
            <textarea
              className="interaction-textarea"
              value={interactionText}
              onChange={e => setInteractionText(e.target.value)}
              placeholder="Paste meeting transcript, email, CRM update, or support ticket text here..."
              style={{ minHeight: 120 }}
            />

            {/* Log stream */}
            {logs.length > 0 && (
              <div className="log-stream" style={{ marginTop: 12 }}>
                {logs.map((l, i) => (
                  <div key={i} className={`log-line ${l.type}`} style={{ animationDelay: `${i * 30}ms` }}>
                    {l.text}
                  </div>
                ))}
                {isAnalyzing && (
                  <div className="log-line info animate-glow-pulse">
                    {'>'} <span className="animate-status-blink">█</span>
                  </div>
                )}
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 14 }}>
              <button
                className="btn-primary"
                onClick={onAnalyze}
                disabled={isAnalyzing || !interactionText.trim()}
                style={{ padding: '11px 28px', fontSize: 14 }}
              >
                {isAnalyzing
                  ? <><Loader2 size={15} className="animate-spin" /> {analysisStage}</>
                  : <><Brain size={15} /> Run AI Analysis</>
                }
              </button>
            </div>
          </div>

          {/* Planner Decision Panel */}
          {planner && (
            <PlannerPanel planner={planner} />
          )}

          {/* Recommendations */}
          {recommendations.length > 0 && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
                <Sparkles size={15} color="var(--violet)" />
                <span style={{ fontWeight: 700, fontSize: 14 }}>AI Recommendations</span>
                <span className="badge badge-info" style={{ fontSize: 10 }}>{recommendations.length} actions</span>
                <span style={{ fontSize: 12, color: 'var(--text-muted)', marginLeft: 4 }}>
                  Human approval required
                </span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                {recommendations.map((rec: Recommendation, i: number) => (
                  <RecommendationCard
                    key={rec.recommendation_id}
                    rec={rec}
                    index={i}
                    onApprove={() => onApprove(rec.recommendation_id)}
                    onReject={() => onReject(rec.recommendation_id)}
                    onOverride={() => onOverride(rec.recommendation_id)}
                    isOverriding={overridingRecId === rec.recommendation_id}
                    overrideText={overrideText}
                    setOverrideText={setOverrideText}
                    onSubmitOverride={() => onSubmitOverride(rec.recommendation_id)}
                    isPendingMutation={isPendingMutation && rec.decision === 'pending'}
                    delay={i * 100}
                  />
                ))}
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>

          {/* Retrieved Knowledge */}
          {knowledge.length > 0 && (
            <div className="glass" style={{ padding: 18 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
                <BookOpen size={14} color="var(--text-accent)" />
                <span style={{ fontWeight: 700, fontSize: 13 }}>Retrieved Knowledge</span>
                <span className="badge badge-electric" style={{ fontSize: 10 }}>{knowledge.length} chunks</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {knowledge.slice(0, 5).map((chunk: KnowledgeChunk, i: number) => (
                  <div key={i} className="knowledge-chunk" style={{ animationDelay: `${i * 80}ms` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                      <span style={{
                        fontSize: 9, fontWeight: 700, color: '#818cf8',
                        background: 'var(--electric-dim)', padding: '2px 7px', borderRadius: 20, textTransform: 'uppercase', letterSpacing: 0.5,
                      }}>
                        {chunk.document_type?.replace('_', ' ')}
                      </span>
                      <span style={{
                        fontSize: 11, color: Math.round(chunk.similarity_score * 100) > 60 ? '#10b981' : '#f59e0b',
                        fontWeight: 700,
                      }}>
                        {Math.round(chunk.similarity_score * 100)}% match
                      </span>
                    </div>
                    <div style={{ fontSize: 10, color: '#a855f7', marginBottom: 5, fontWeight: 600 }}>
                      📄 {chunk.source}
                    </div>
                    <p style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                      {chunk.content?.slice(0, 150)}...
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Memory Timeline */}
          <div className="glass" style={{ padding: 18 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
              <Database size={14} color="var(--text-accent)" />
              <span style={{ fontWeight: 700, fontSize: 13 }}>Organizational Memory</span>
              {memory.length > 0 && <span className="badge badge-electric" style={{ fontSize: 10 }}>{memory.length} records</span>}
            </div>
            {memory.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '24px 0' }}>
                <Database size={28} color="var(--text-muted)" style={{ marginBottom: 8 }} />
                <p style={{ fontSize: 12, color: 'var(--text-muted)' }}>No previous decisions on record</p>
                <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
                  Approved recommendations will appear here
                </p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
                {memory.slice(0, 6).map((m: MemoryRecord, i: number) => (
                  <div key={m.memory_id} className={`memory-item ${m.decision}`} style={{ paddingBottom: 14, animationDelay: `${i * 60}ms` }}>
                    <div style={{ padding: '10px 12px', background: 'var(--bg-elevated)', borderRadius: 10, marginBottom: 2 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5 }}>
                        <span style={{
                          fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5,
                          color: m.decision === 'approved' ? '#10b981' : m.decision === 'rejected' ? '#f43f5e' : '#f59e0b',
                        }}>
                          {m.decision === 'approved' ? '✓' : m.decision === 'rejected' ? '✗' : '~'} {m.decision}
                        </span>
                        <span style={{ fontSize: 10, color: 'var(--text-muted)' }}>
                          {m.timestamp ? new Date(m.timestamp).toLocaleDateString() : ''}
                        </span>
                      </div>
                      <p style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                        {m.recommendation?.slice(0, 90)}...
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// AGENT PIPELINE VISUALIZATION
// ══════════════════════════════════════════════════════════════════════════
function AgentPipeline({ planner, isAnalyzing, analysisStage }: {
  planner: PlannerDecision | undefined; isAnalyzing: boolean; analysisStage: string
}) {
  const ALL_AGENTS = ['ContextAgent', 'RetrievalAgent', 'RiskAgent', 'OpportunityAgent', 'RenewalAgent', 'RecommendationAgent']

  const getStatus = (name: string): 'idle' | 'running' | 'complete' | 'skipped' | 'pending' => {
    if (!isAnalyzing && !planner) return 'idle'
    if (isAnalyzing) {
      const stageIndex = ['Creating session...', 'Extracting context...', 'Retrieving organizational memory...', 'Planning agent execution...', 'Generating recommendations...', 'Complete'].indexOf(analysisStage)
      const agentIndex = ALL_AGENTS.indexOf(name)
      if (agentIndex < stageIndex - 1) return 'complete'
      if (agentIndex === stageIndex - 1) return 'running'
      return 'pending'
    }
    if (planner) {
      if (planner.skipped_agents.includes(name)) return 'skipped'
      if (planner.selected_agents.includes(name) || name === 'ContextAgent') return 'complete'
    }
    return 'idle'
  }

  const isActive = (name: string) => {
    if (!planner && !isAnalyzing) return false
    if (isAnalyzing) return true
    return planner?.selected_agents.includes(name) || name === 'ContextAgent'
  }

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '4px 0', overflowX: 'auto' }}>
      {ALL_AGENTS.map((name, idx) => {
        const status = getStatus(name)
        const meta = AGENT_META[name] || { icon: Bot, color: '#6366f1', desc: 'Agent' }
        const Icon = meta.icon
        const active = isActive(name)
        return (
          <div key={name} style={{ display: 'flex', alignItems: 'center', flex: idx < ALL_AGENTS.length - 1 ? '1' : 'none', minWidth: idx < ALL_AGENTS.length - 1 ? 'auto' : undefined }}>
            <div className="agent-node">
              <div className={`agent-node-box ${status}`}>
                <Icon size={20} color={status === 'idle' || status === 'skipped' ? 'var(--text-muted)' : meta.color} />
                <span style={{ fontSize: 9, color: status === 'idle' || status === 'skipped' ? 'var(--text-muted)' : 'var(--text-secondary)', fontWeight: 600, textAlign: 'center', lineHeight: 1.2, paddingInline: 4 }}>
                  {name.replace('Agent', '')}
                </span>
                {status === 'running' && (
                  <div style={{ position: 'absolute', top: 4, right: 4, width: 7, height: 7, borderRadius: '50%', background: 'var(--cyan)', boxShadow: '0 0 8px var(--cyan-glow)', animation: 'status-blink 1s ease-in-out infinite' }} />
                )}
                {status === 'complete' && (
                  <div style={{ position: 'absolute', top: 4, right: 4, width: 14, height: 14, borderRadius: '50%', background: 'rgba(16,185,129,0.2)', border: '1px solid rgba(16,185,129,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <CheckCircle size={8} color="#10b981" />
                  </div>
                )}
                {status === 'skipped' && (
                  <div style={{ position: 'absolute', top: 4, right: 4 }}>
                    <XCircle size={10} color="var(--text-muted)" />
                  </div>
                )}
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 9, color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>{meta.desc}</div>
                {status === 'skipped' && <div style={{ fontSize: 9, color: '#f43f5e', fontWeight: 700 }}>SKIPPED</div>}
              </div>
            </div>
            {idx < ALL_AGENTS.length - 1 && (
              <div className={`connector ${active ? 'active' : ''}`} style={{ minWidth: 24 }} />
            )}
          </div>
        )
      })}
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// PLANNER DECISION PANEL
// ══════════════════════════════════════════════════════════════════════════
function PlannerPanel({ planner }: { planner: PlannerDecision }) {
  return (
    <div className="glass animate-fade-in-up" style={{ padding: 22 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 18 }}>
        <Target size={15} color="var(--text-accent)" />
        <span style={{ fontWeight: 700, fontSize: 14 }}>Planner Decision Panel</span>
        <span className="badge badge-electric" style={{ fontSize: 10 }}>AI Orchestration</span>
        {planner.execution_mode && (
          <span className="badge badge-info" style={{ fontSize: 10, marginLeft: 'auto' }}>{planner.execution_mode}</span>
        )}
      </div>

      {/* Detected Signals */}
      <div style={{ marginBottom: 16 }}>
        <div style={{ fontSize: 10, color: 'var(--text-muted)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.8, fontWeight: 700 }}>
          ⚡ Detected Business Signals
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7 }}>
          {planner.detected_signals.map((s: string, i: number) => {
            const sig = SIGNALS[s] || { color: '#94a3b8', label: s, icon: '•' }
            return (
              <span key={s} className="signal-chip" style={{
                background: `${sig.color}18`, color: sig.color,
                border: `1px solid ${sig.color}35`,
                animationDelay: `${i * 60}ms`,
              }}>
                {sig.icon} {sig.label}
              </span>
            )
          })}
        </div>
      </div>

      {/* Agent Selection */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
        <div style={{ background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.2)', borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 10, color: '#10b981', fontWeight: 700, marginBottom: 10, textTransform: 'uppercase', letterSpacing: 0.8 }}>✓ Agents Activated</div>
          {planner.selected_agents.map((a: string) => {
            const meta = AGENT_META[a]
            const Icon = meta?.icon || Bot
            return (
              <div key={a} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 7 }}>
                <div style={{ width: 22, height: 22, borderRadius: 6, background: `${meta?.color || '#6366f1'}18`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon size={12} color={meta?.color || '#6366f1'} />
                </div>
                <span style={{ fontSize: 12, color: 'var(--text-secondary)', fontWeight: 500 }}>{a}</span>
                <CheckCircle size={11} color="#10b981" style={{ marginLeft: 'auto' }} />
              </div>
            )
          })}
        </div>
        <div style={{ background: 'rgba(244,63,94,0.05)', border: '1px solid rgba(244,63,94,0.15)', borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 10, color: '#f43f5e', fontWeight: 700, marginBottom: 10, textTransform: 'uppercase', letterSpacing: 0.8 }}>✗ Agents Skipped</div>
          {planner.skipped_agents.length > 0 ? planner.skipped_agents.map((a: string) => {
            const meta = AGENT_META[a]
            const Icon = meta?.icon || Bot
            return (
              <div key={a} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 7 }}>
                <div style={{ width: 22, height: 22, borderRadius: 6, background: 'rgba(244,63,94,0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon size={12} color="#f43f5e" />
                </div>
                <span style={{ fontSize: 12, color: 'var(--text-muted)', textDecoration: 'line-through' }}>{a}</span>
                <XCircle size={11} color="#f43f5e" style={{ marginLeft: 'auto' }} />
              </div>
            )
          }) : (
            <div style={{ fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>All agents selected</div>
          )}
        </div>
      </div>

      {/* Planner Reasoning */}
      {planner.planner_reasoning && (
        <div style={{ background: 'rgba(99,102,241,0.06)', border: '1px solid rgba(99,102,241,0.18)', borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 10, color: 'var(--text-accent)', fontWeight: 700, marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.8 }}>
            🧠 Planner Reasoning
          </div>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.65 }}>{planner.planner_reasoning}</p>
        </div>
      )}
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// RECOMMENDATION CARD
// ══════════════════════════════════════════════════════════════════════════
function RecommendationCard({ rec, index, onApprove, onReject, onOverride, isOverriding, overrideText, setOverrideText, onSubmitOverride, isPendingMutation, delay }: any) {
  const [expanded, setExpanded] = useState(false)
  const confidence = confidencePct(rec.confidence)
  const isPending = rec.decision === 'pending'

  return (
    <div
      className={`rec-card ${rec.priority} ${rec.decision !== 'pending' ? rec.decision : ''}`}
      style={{ padding: '18px 20px', animationDelay: `${delay}ms` }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
          <span style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 700 }}>#{index + 1}</span>
          <span className={`badge badge-${rec.priority}`}>{rec.priority.toUpperCase()}</span>
          {rec.decision !== 'pending' && (
            <span style={{
              fontSize: 11, fontWeight: 700, padding: '3px 10px', borderRadius: 20,
              background: rec.decision === 'approved' ? 'rgba(16,185,129,0.15)' : rec.decision === 'rejected' ? 'rgba(244,63,94,0.15)' : 'rgba(245,158,11,0.15)',
              color: rec.decision === 'approved' ? '#10b981' : rec.decision === 'rejected' ? '#f43f5e' : '#f59e0b',
              border: `1px solid ${rec.decision === 'approved' ? 'rgba(16,185,129,0.3)' : rec.decision === 'rejected' ? 'rgba(244,63,94,0.3)' : 'rgba(245,158,11,0.3)'}`,
            }}>
              {rec.decision === 'approved' ? '✓' : rec.decision === 'rejected' ? '✗' : '~'} {rec.decision.toUpperCase()}
            </span>
          )}
        </div>
        <div style={{ textAlign: 'right', flexShrink: 0 }}>
          <div style={{
            fontSize: 22, fontWeight: 800, lineHeight: 1,
            color: confidence >= 75 ? '#10b981' : confidence >= 50 ? '#f59e0b' : '#f43f5e',
          }}>
            {confidence}%
          </div>
          <div style={{ fontSize: 9, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: 0.5 }}>confidence</div>
        </div>
      </div>

      {/* Action */}
      <p style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)', lineHeight: 1.55, marginBottom: 12 }}>
        {rec.action}
      </p>

      {/* Confidence bar */}
      <div style={{ marginBottom: 12 }}>
        <div className="conf-bar">
          <div className="conf-fill" style={{ width: `${confidence}%` }} />
        </div>
      </div>

      {/* Business Rule */}
      {rec.business_rule && (
        <div style={{
          background: 'rgba(244,63,94,0.07)', border: '1px solid rgba(244,63,94,0.18)',
          borderRadius: 8, padding: '7px 11px', marginBottom: 10,
          display: 'flex', gap: 6, alignItems: 'flex-start',
        }}>
          <Shield size={12} color="#f43f5e" style={{ marginTop: 1, flexShrink: 0 }} />
          <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
            <span style={{ color: '#f43f5e', fontWeight: 700 }}>Rule: </span>{rec.business_rule}
          </span>
        </div>
      )}

      {/* Expanded details */}
      {expanded && (
        <div className="animate-fade-in" style={{ marginBottom: 12 }}>
          {rec.reasoning && (
            <div style={{ background: 'var(--bg-elevated)', borderRadius: 8, padding: '10px 12px', marginBottom: 8 }}>
              <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 6 }}>Reasoning</div>
              <p style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.6 }}>{rec.reasoning}</p>
            </div>
          )}
          {rec.evidence_source?.length > 0 && (
            <div>
              <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 6 }}>Evidence Sources</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {rec.evidence_source.map((e: string, i: number) => (
                  <span key={i} style={{
                    fontSize: 10, padding: '2px 9px', borderRadius: 20, fontWeight: 600,
                    background: 'var(--electric-dim)', color: 'var(--text-accent)',
                    border: '1px solid rgba(99,102,241,0.25)',
                  }}>📄 {e}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <button
        onClick={() => setExpanded(!expanded)}
        style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: 12, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 5 }}
      >
        <Eye size={12} /> {expanded ? 'Hide' : 'Show'} reasoning & evidence
      </button>

      {/* HITL Actions */}
      {isPending && !isOverriding && (
        <div style={{ display: 'flex', gap: 8, paddingTop: 4, borderTop: '1px solid var(--border)' }}>
          <button className="btn-approve" onClick={onApprove} disabled={isPendingMutation}>
            {isPendingMutation ? <Loader2 size={12} className="animate-spin" /> : <CheckCircle size={13} />} Approve
          </button>
          <button className="btn-reject" onClick={onReject} disabled={isPendingMutation}>
            <XCircle size={13} /> Reject
          </button>
          <button className="btn-override" onClick={onOverride} disabled={isPendingMutation}>
            <RefreshCw size={12} /> Override
          </button>
        </div>
      )}

      {isOverriding && (
        <div className="animate-fade-in" style={{ paddingTop: 10, borderTop: '1px solid var(--border)' }}>
          <div style={{ fontSize: 12, color: 'var(--amber)', fontWeight: 600, marginBottom: 8 }}>
            ✏ Enter your custom action:
          </div>
          <input
            className="adip-input"
            value={overrideText}
            onChange={e => setOverrideText(e.target.value)}
            placeholder="Describe your alternative action..."
            style={{ marginBottom: 8 }}
          />
          <button className="btn-override" onClick={onSubmitOverride} disabled={!overrideText.trim()}>
            <CheckCircle size={12} /> Submit Override
          </button>
        </div>
      )}
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// INSIGHTS VIEW
// ══════════════════════════════════════════════════════════════════════════
function InsightsView({ analytics, customers }: { analytics: any; customers: Customer[] }) {
  return (
    <div style={{ maxWidth: 1100 }}>
      <div className="animate-fade-in-up" style={{ marginBottom: 28 }}>
        <h1 className="font-display" style={{ fontSize: 26, fontWeight: 800, marginBottom: 6 }}>
          Platform <span className="gradient-text">Insights</span>
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>Operational analytics, agent execution transparency, and memory intelligence.</p>
      </div>

      {analytics && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 28 }}>
          {[
            { label: 'Total Recommendations', value: analytics.total_recommendations, icon: Star, color: '#6366f1', glow: 'rgba(99,102,241,0.25)' },
            { label: 'Approvals', value: analytics.approved_count, icon: CheckCircle, color: '#10b981', glow: 'rgba(16,185,129,0.25)' },
            { label: 'Rejections', value: analytics.rejected_count, icon: XCircle, color: '#f43f5e', glow: 'rgba(244,63,94,0.25)' },
            { label: 'Overrides', value: analytics.overridden_count, icon: AlertTriangle, color: '#f59e0b', glow: 'rgba(245,158,11,0.2)' },
            { label: 'Approval Rate', value: `${analytics.approval_rate}%`, icon: TrendingUp, color: '#10b981', glow: 'rgba(16,185,129,0.25)' },
            { label: 'Memory Records', value: analytics.memory_records, icon: Database, color: '#a855f7', glow: 'rgba(168,85,247,0.25)' },
          ].map((m, i) => (
            <KpiCard key={m.label} label={m.label} value={String(m.value)} icon={m.icon} color={m.color} glow={m.glow} delay={i * 60} />
          ))}
        </div>
      )}

      {/* Customer Health Grid */}
      <div className="glass animate-fade-in-up" style={{ padding: 22, marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 18 }}>
          <Activity size={15} color="var(--text-accent)" />
          <span style={{ fontWeight: 700, fontSize: 14 }}>Customer Health Breakdown</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 14 }}>
          {customers.map((c, i) => {
            const color = healthColor(c.health_score)
            const adoption = c.licensed_users > 0 ? Math.round(c.active_users / c.licensed_users * 100) : 0
            return (
              <div key={c.customer_id} className="glass-sm" style={{ padding: 16, animationDelay: `${i * 80}ms` }} >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 2 }}>{c.company_name}</div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{c.industry}</div>
                  </div>
                  <HealthRing score={c.health_score} />
                </div>
                <div style={{ marginBottom: 8 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>
                    <span>Adoption</span><span style={{ color: adoption < 60 ? '#f59e0b' : '#10b981', fontWeight: 700 }}>{adoption}%</span>
                  </div>
                  <div className="conf-bar"><div className="conf-fill" style={{ width: `${adoption}%`, background: adoption < 60 ? 'linear-gradient(90deg, #f59e0b, #f43f5e)' : undefined }} /></div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--text-muted)' }}>
                  <span>Renewal: {c.renewal_date}</span>
                  <span>{c.active_users}/{c.licensed_users} users</span>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Architecture Callout */}
      <div className="glass" style={{ padding: 22, borderColor: 'rgba(99,102,241,0.25)', background: 'rgba(99,102,241,0.04)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
          <Layers size={15} color="var(--text-accent)" />
          <span style={{ fontWeight: 700, fontSize: 14 }}>Platform Architecture</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
          {[
            { label: 'Context Agent', desc: 'Extracts signals from raw customer text', color: '#22d3ee' },
            { label: 'Dynamic Planner', desc: 'Generates execution plan via LLM reasoning', color: '#6366f1' },
            { label: 'Retrieval Agent', desc: 'FAISS similarity search across knowledge base', color: '#818cf8' },
            { label: 'Risk Agent', desc: 'Assesses churn probability and satisfaction risk', color: '#f43f5e' },
            { label: 'Business Rules', desc: 'Deterministic threshold-based escalation rules', color: '#f59e0b' },
            { label: 'Confidence Engine', desc: 'Mathematical, non-LLM confidence scoring', color: '#10b981' },
          ].map((a, i) => (
            <div key={a.label} style={{ padding: '12px 14px', borderRadius: 10, background: 'var(--bg-card)', border: '1px solid var(--border)', animationDelay: `${i * 60}ms` }}>
              <div style={{ fontSize: 12, fontWeight: 700, color: a.color, marginBottom: 4 }}>{a.label}</div>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', lineHeight: 1.5 }}>{a.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ══════════════════════════════════════════════════════════════════════════
// SMALL COMPONENTS
// ══════════════════════════════════════════════════════════════════════════

function CustomerHeader({ customer: c }: { customer: Customer }) {
  const color = healthColor(c.health_score)
  const adoption = c.licensed_users > 0 ? Math.round(c.active_users / c.licensed_users * 100) : 0
  return (
    <div className="glass animate-fade-in" style={{ padding: '18px 22px', display: 'flex', alignItems: 'center', gap: 20 }}>
      <div style={{ width: 52, height: 52, borderRadius: 16, background: `${color}18`, border: `1px solid ${color}40`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Building2 size={24} color={color} />
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 6 }}>
          <h2 className="font-display" style={{ fontSize: 20, fontWeight: 800 }}>{c.company_name}</h2>
          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{c.industry}</span>
          <HealthPill score={c.health_score} />
        </div>
        <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
          <CustStat label="Health Score" value={String(c.health_score)} color={color} />
          <CustStat label="Renewal Date" value={c.renewal_date} />
          <CustStat label="Adoption" value={`${adoption}%`} color={adoption < 60 ? '#f59e0b' : '#10b981'} />
          <CustStat label="ARR" value={`$${(c.contract_value / 1000).toFixed(0)}k`} />
          <CustStat label="Champion" value={c.champion_status} color={c.champion_status === 'resigned' ? '#f43f5e' : undefined} />
          <CustStat label="Active Users" value={`${c.active_users}/${c.licensed_users}`} />
        </div>
      </div>
      <HealthRing score={c.health_score} size={64} />
    </div>
  )
}

function CustomerSidebarItem({ customer: c, selected, onClick }: { customer: Customer; selected: boolean; onClick: () => void }) {
  const color = healthColor(c.health_score)
  return (
    <div className={`sidebar-item ${selected ? 'active' : ''}`} onClick={onClick}>
      <div style={{ width: 36, height: 36, borderRadius: 10, background: `${color}15`, border: `1px solid ${color}30`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Building2 size={16} color={color} />
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{c.company_name}</div>
        <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 1 }}>{c.active_users}/{c.licensed_users} users · {healthLabel(c.health_score)}</div>
      </div>
      <div style={{ fontWeight: 800, fontSize: 14, color, flexShrink: 0 }}>{c.health_score}</div>
    </div>
  )
}

function HealthRing({ score, size = 48 }: { score: number; size?: number }) {
  const color = healthColor(score)
  const r = (size - 6) / 2
  const circ = 2 * Math.PI * r
  const offset = circ - (score / 100) * circ
  return (
    <svg width={size} height={size} style={{ transform: 'rotate(-90deg)', flexShrink: 0 }}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={4} />
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth={4}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round"
        style={{ filter: `drop-shadow(0 0 6px ${color})`, transition: 'stroke-dashoffset 1s ease' }}
      />
      <text x={size / 2} y={size / 2} textAnchor="middle" dominantBaseline="middle"
        style={{ transform: `rotate(90deg) translate(0, -${size}px)`, transformOrigin: `${size / 2}px ${size / 2}px` }}
        fill={color} fontSize={size > 50 ? 14 : 10} fontWeight={800} fontFamily="Inter, sans-serif">
        {score}
      </text>
    </svg>
  )
}

function HealthPill({ score }: { score: number }) {
  const color = healthColor(score)
  const label = healthLabel(score)
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: '3px 10px', borderRadius: 20, background: `${color}15`, border: `1px solid ${color}30`, fontSize: 11, fontWeight: 700, color }}>
      <span style={{ width: 5, height: 5, borderRadius: '50%', background: color, boxShadow: `0 0 5px ${color}` }} />
      {label} · {score}
    </span>
  )
}

function AdoptionBar({ value }: { value: number }) {
  const color = value >= 70 ? '#10b981' : value >= 40 ? '#f59e0b' : '#f43f5e'
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <div style={{ width: 60, height: 5, borderRadius: 3, background: 'rgba(255,255,255,0.06)', overflow: 'hidden' }}>
        <div style={{ height: '100%', width: `${value}%`, background: color, borderRadius: 3, transition: 'width 0.8s ease' }} />
      </div>
      <span style={{ fontSize: 12, fontWeight: 700, color }}>{value}%</span>
    </div>
  )
}

function KpiCard({ label, value, unit = '', icon: Icon, color, glow, delay = 0 }: {
  label: string; value: string; unit?: string; icon: any; color: string; glow: string; delay?: number
}) {
  return (
    <div className="metric-card animate-fade-in-up" style={{ '--accent-glow': glow, animationDelay: `${delay}ms` } as any}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
        <span style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</span>
        <div style={{ width: 34, height: 34, borderRadius: 10, background: `${color}15`, border: `1px solid ${color}30`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Icon size={16} color={color} />
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 3 }}>
        <span style={{ fontSize: 30, fontWeight: 900, color, lineHeight: 1 }}>{value}</span>
        {unit && <span style={{ fontSize: 14, color, fontWeight: 600 }}>{unit}</span>}
      </div>
    </div>
  )
}

function CustStat({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <div>
      <div style={{ fontSize: 9, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: 0.8, marginBottom: 2, fontWeight: 700 }}>{label}</div>
      <div style={{ fontSize: 13, fontWeight: 600, color: color || 'var(--text-primary)' }}>{value}</div>
    </div>
  )
}

function QuickStat({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div style={{ textAlign: 'right' }}>
      <div style={{ fontSize: 9, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: 0.8 }}>{label}</div>
      <div style={{ fontSize: 14, fontWeight: 800, color }}>{value}</div>
    </div>
  )
}

function SidebarStat({ label, value, icon: Icon }: { label: string; value: string; icon: any }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 7 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, color: 'var(--text-muted)' }}>
        <Icon size={11} color="var(--text-muted)" />
        {label}
      </div>
      <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-accent)' }}>{value}</span>
    </div>
  )
}
