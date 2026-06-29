# NimbusCRM — Release Notes

## Version 2.5 — June 2026

**Release Date:** June 3, 2026  
**Type:** Minor Release — Feature + Stability

---

### New Features

**AI Insights Dashboard (Enterprise)**  
A new AI-powered analytics view that surfaces account health trends, risk indicators, and deal probability predictions using machine learning trained on aggregate anonymized customer data. Available exclusively to Enterprise plan customers.

**Onboarding Wizard v2**  
Redesigned 5-step onboarding experience with progress persistence (users can resume from where they left off), improved role assignment UX, and inline help tooltips.

**Bulk User Management**  
Administrators can now import, assign, and deactivate users in bulk via CSV. Supports role assignment in bulk upload.

---

### Improvements

- Salesforce sync now handles duplicate detection with configurable merge rules
- API rate limits increased from 1,000 to 5,000 requests/hour on Business plan
- Export timeout increased to 120 seconds (previously 45 seconds) — fixes bulk export issues

---

### Bug Fixes

- Fixed: CSV export timeout for datasets >10,000 records (**addresses ACME-0038 class of issue**)
- Fixed: Onboarding wizard Step 3 freeze in Firefox and Safari (**addresses ACME-0041 class of issue**)
- Fixed: Dashboard filter showing stale pipeline totals (**addresses NOVA-0017 class of issue**)

---

## Version 2.4 — March 2026

**Release Date:** March 15, 2026

### New Features

**Custom Dashboard Widgets**  
Users can now create custom metric widgets using the Widget Builder. Supports formula-based KPIs, multiple data source combinations, and custom chart types.

**Slack Integration v2**  
Real-time deal activity notifications, configurable channel routing, and two-way Slack-to-CRM action support (e.g., update deal stage from Slack).

**Expanded API**  
New webhooks for `deal_stage_changed`, `contact_created`, `user_login`, and `support_ticket_created` events.

---

## Version 2.3 — December 2025

**Release Date:** December 10, 2025

### New Features

**Renewal Tracking Module**  
Dedicated module for tracking customer contract renewals, renewal health scores, and automated renewal reminders at 90, 60, and 30-day intervals.

**User Activity Analytics**  
Administrators can view per-user login frequency, feature usage, and session duration in the Admin Analytics panel.

---

*Full release notes archive: help.nimbuscrm.com/releases*
