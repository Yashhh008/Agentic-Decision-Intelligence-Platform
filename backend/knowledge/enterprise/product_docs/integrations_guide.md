# NimbusCRM — Integrations Guide

## Overview
NimbusCRM connects with your existing business tools to create a unified workflow. This guide covers all available integrations, setup requirements, and troubleshooting steps.

## Native Integrations (No-Code Setup)

### CRM & Sales Tools
| Integration | Tier Required | Sync Type | Frequency |
|---|---|---|---|
| Salesforce | Professional+ | Bi-directional | Real-time |
| HubSpot | Starter+ | Bi-directional | Every 15 min |
| Pipedrive | Starter+ | One-way pull | Hourly |

### Marketing Automation
| Integration | Tier Required | Sync Type |
|---|---|---|
| Marketo | Enterprise | Contact & campaign sync |
| Mailchimp | Professional+ | List and segment sync |
| ActiveCampaign | Professional+ | Contact and tag sync |

### Project Management
| Integration | Tier Required | Sync Type |
|---|---|---|
| Jira | Professional+ | Ticket creation from CRM tasks |
| Asana | Professional+ | Task sync |
| Procore | Enterprise | Project and contact sync |

### Communication
| Integration | Tier Required | Sync Type |
|---|---|---|
| Slack | Starter+ | Notifications and alerts |
| Microsoft Teams | Professional+ | Notifications and alerts |
| Zoom | Professional+ | Meeting logging |
| Gmail | Starter+ | Email activity logging |
| Outlook | Starter+ | Email activity logging |

### Data & Analytics
| Integration | Tier Required | Sync Type |
|---|---|---|
| Looker | Enterprise | Data export |
| Tableau | Enterprise | Data export |
| Google Sheets | Professional+ | Export and import |

---

## API Integration (Enterprise & Enterprise Plus)

NimbusCRM provides a REST API for custom integrations.

### Key Endpoints
- `GET /api/v1/accounts` — List all accounts
- `GET /api/v1/accounts/{id}` — Get account details
- `POST /api/v1/accounts/{id}/activities` — Log an activity
- `GET /api/v1/deals` — List all deals
- `POST /api/v1/webhooks` — Register a webhook

### Rate Limits
| Tier | Requests/minute | Requests/day |
|---|---|---|
| Enterprise | 300 | 50,000 |
| Enterprise Plus | 1,000 | 200,000 |

### Authentication
All API calls require a Bearer token. Tokens are generated in **Settings → API → Generate Token**.

---

## Setting Up an Integration

1. Go to **Settings → Integrations** in NimbusCRM
2. Select the integration from the list
3. Click **Connect** and authorize with your provider credentials
4. Configure sync settings (fields, frequency, direction)
5. Run a test sync and verify data in both systems

## Common Troubleshooting

### Integration shows "Disconnected"
- Re-authorize the connection (tokens expire after 90 days for some providers)
- Check that your provider account still has API access enabled

### Data not syncing
- Verify field mapping is correct in the integration settings
- Check the sync log under **Settings → Integrations → [Name] → Sync Log**
- Contact support if sync errors persist for more than 2 hours

### Procore-specific setup
- Requires NimbusCRM Solutions Engineering team involvement for initial setup
- IT admin access to Procore required from customer side
- Typical setup time: 3–5 business days after access is provisioned
