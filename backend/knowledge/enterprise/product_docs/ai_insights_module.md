# NimbusCRM — AI Insights Module: Feature Documentation

## Overview
AI Insights is NimbusCRM's machine learning-powered intelligence layer, available exclusively on the Enterprise and Enterprise Plus tiers. It analyzes account behavior patterns, communication signals, and usage data to generate actionable predictions and recommendations.

## Features

### 1. Churn Probability Score
A real-time score (0–100) predicting the likelihood of churn within the next 90 days.

**Inputs:**
- Login frequency and active user count
- Feature adoption depth
- Support ticket volume and resolution time
- Communication sentiment from emails and call logs
- Contract age and renewal proximity

**Output:**
- Churn probability percentage
- Top 3 contributing risk factors
- Recommended intervention actions

**Thresholds:**
- 0–30: Low risk (green)
- 31–60: Medium risk (yellow)
- 61–80: High risk (orange)
- 81–100: Critical risk (red) — triggers automatic CSM alert

---

### 2. Deal Close Prediction
Predicts the likelihood of a deal closing within the current quarter based on engagement signals.

**Inputs:**
- Email open and reply rates
- Meeting frequency with prospects
- Demo completion and follow-up speed
- Competitor mentions in conversations

---

### 3. Account Health Score
A composite score (0–100) reflecting the overall health of a customer relationship.

**Formula:**
```
Health Score = (Adoption × 0.35) + (Engagement × 0.25) + (Support × 0.20) + (Sentiment × 0.20)
```

**Components:**
- **Adoption (35%)**: Active users / Licensed users ratio, feature usage breadth
- **Engagement (25%)**: QBR attendance, CSM meeting frequency, email responsiveness
- **Support (20%)**: Open ticket count, ticket age, severity distribution
- **Sentiment (20%)**: Communication tone analysis, NPS, survey responses

---

### 4. Automated Next-Action Suggestions
Based on detected signals, AI Insights surfaces recommended next actions for the CSM directly in the account view.

**Examples:**
- "Schedule adoption review — 3 users went inactive this week"
- "Renewal approaching — champion has not responded in 14 days"
- "Expansion signal — 92% seat utilization detected"

---

## Data Privacy
All AI Insights processing is performed on aggregated, anonymized behavioral data. No personally identifiable information (PII) from customer communications is stored in the prediction models. Customers can opt out of sentiment analysis at any time.

## Accessing AI Insights
1. Navigate to the Account page in NimbusCRM
2. Click the **AI Insights** tab in the top navigation
3. All predictions refresh every 24 hours automatically
4. Manual refresh is available for Enterprise Plus customers

## Integration with ADIP
The AI Insights module feeds signals into the Agentic Decision Intelligence Platform (ADIP) for multi-agent analysis, providing richer context for CSM decision support.
