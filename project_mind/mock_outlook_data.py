"""Mock Outlook email data"""

EMAILS = [
    {
        "id": "email-001",
        "subject": "RE: SSL Certificate for Payment Gateway",
        "from": "vendor@paymentprovider.com",
        "to": "devops@company.com",
        "cc": ["pm@company.com"],
        "date": "2026-01-22",
        "project": "Payment Gateway Integration",
        "body": """
Hi Team,

We have processed your SSL certificate request. The new certificate will be 
issued within 24-48 hours. You will receive it via secure email.

Please note:
- Certificate validity: 2 years
- Support for TLS 1.3
- Wildcard certificate for *.payment.company.com

Best regards,
Payment Provider Support Team
        """,
        "thread_id": "thread-001",
        "tags": ["ssl", "blocker-resolution"]
    },
    {
        "id": "email-002",
        "subject": "Sprint 15 - Blocker Alert",
        "from": "scrum.master@company.com",
        "to": "team@company.com",
        "date": "2026-01-21",
        "project": "Payment Gateway Integration",
        "body": """
Team,

We have 3 active blockers affecting Sprint 15:

1. PAY-1234: SSL Certificate - Waiting on vendor (5 days blocked)
2. PAY-1256: PCI Compliance - Security review scheduled for tomorrow
3. PAY-1267: API Rate Limiting - Backend team investigating

Action Required:
- Tech Lead: Follow up with vendor on SSL
- Security Team: Prioritize PCI review
- Backend: Present rate limiting solution by EOD

Sprint goal is at risk. Let's discuss in today's standup.

Thanks,
Scrum Master
        """,
        "thread_id": "thread-002",
        "tags": ["sprint", "blockers", "urgent"]
    },
    {
        "id": "email-003",
        "subject": "OAuth2 Implementation - Architecture Decision",
        "from": "tech.lead@company.com",
        "to": "dev.team@company.com",
        "cc": ["product.owner@company.com"],
        "date": "2026-01-18",
        "project": "Mobile App Rewrite",
        "body": """
Hi Team,

After reviewing the OAuth2 implementation options, we've decided to go with:

**Decision**: Use AppAuth library for OAuth2/OIDC
- Supports PKCE out of the box
- Well-maintained and battle-tested
- Good documentation

**Rationale**:
- Security: PKCE prevents authorization code interception
- Standards compliance: Follows RFC 8252
- Cross-platform: Works on iOS and Android

Implementation should follow the pattern documented in Confluence:
https://confluence.company.com/oauth2-mobile-pattern

Please review and let me know if you have concerns.

Tech Lead
        """,
        "thread_id": "thread-003",
        "tags": ["architecture", "decision", "oauth"]
    },
    {
        "id": "email-004",
        "subject": "Q1 Roadmap - Stakeholder Feedback",
        "from": "stakeholder@company.com",
        "to": "product.manager@company.com",
        "date": "2026-01-20",
        "project": "Mobile App Rewrite",
        "body": """
Hi PM,

I reviewed the Q1 roadmap for the mobile app. Overall looks great! 
A few thoughts:

Positives:
✓ OAuth2 authentication is much needed
✓ Push notifications will drive engagement
✓ Offline mode is a game-changer

Concerns:
- Timeline seems aggressive for Q1
- Need more details on data sync for offline mode
- What about tablet optimization?

Can we schedule a call to discuss?

Best,
VP Product
        """,
        "thread_id": "thread-004",
        "tags": ["roadmap", "feedback", "stakeholder"]
    }
]