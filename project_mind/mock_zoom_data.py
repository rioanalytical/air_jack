"""Mock Zoom meeting transcripts"""

MEETINGS = [
    {
        "id": "zoom-001",
        "title": "Sprint 15 Planning",
        "project": "Payment Gateway Integration",
        "date": "2026-01-13",
        "duration_minutes": 90,
        "attendees": ["PM", "Tech Lead", "Dev Team", "QA Lead"],
        "transcript": """
[00:05] PM: Let's start with our sprint goal. We need to complete the payment gateway integration and pass the security audit.

[00:08] Tech Lead: We have the SSL certificate issue that's blocking us. I've escalated to the vendor.

[00:10] Dev1: How long until we get the new certificate?

[00:11] Tech Lead: They promised 48 hours, but it's been 3 days. I'll follow up again today.

[00:15] QA Lead: We also have the PCI compliance review pending. Security team needs to sign off before we can process live transactions.

[00:18] PM: When is that scheduled?

[00:19] QA Lead: Tomorrow at 2 PM. I've shared all the documentation with the security team.

[00:25] Dev2: The third-party API is rate limiting us during peak hours. We're hitting the 1000 requests/minute limit.

[00:27] Tech Lead: Can we implement request batching or caching?

[00:30] Dev2: Yes, I'll look into Redis caching for payment tokens. That should reduce API calls by 60-70%.

[00:45] PM: So our blockers are: SSL cert, PCI review, and rate limiting. Let's make these our top priority.

[01:20] Team: Sprint committed. Total 45 points.
        """,
        "key_decisions": [
            "Implement Redis caching to reduce API calls",
            "PCI review scheduled for Jan 14 at 2 PM",
            "SSL certificate escalation with vendor"
        ],
        "action_items": [
            {"owner": "Tech Lead", "task": "Follow up on SSL certificate", "due": "2026-01-14"},
            {"owner": "Dev2", "task": "Implement Redis caching for payment tokens", "due": "2026-01-16"},
            {"owner": "QA Lead", "task": "Coordinate PCI compliance review", "due": "2026-01-14"}
        ]
    },
    {
        "id": "zoom-002",
        "title": "Architecture Review - Mobile Authentication",
        "project": "Mobile App Rewrite",
        "date": "2026-01-20",
        "duration_minutes": 60,
        "attendees": ["Tech Lead", "Senior Architect", "iOS Dev", "Android Dev", "Security Engineer"],
        "transcript": """
[00:03] Senior Architect: Today we're reviewing the OAuth2 authentication approach for mobile.

[00:05] Tech Lead: I've documented three options in Confluence. My recommendation is AppAuth library.

[00:08] Security Engineer: I've reviewed it. AppAuth implements PKCE correctly which is critical for mobile security.

[00:10] iOS Dev: We've used AppAuth before on another project. It's solid and well-maintained.

[00:12] Android Dev: Agreed. Integration is straightforward on Android too.

[00:15] Senior Architect: What about token storage?

[00:18] Security Engineer: Must use Keychain on iOS and KeyStore on Android. Never SharedPreferences or UserDefaults.

[00:20] Tech Lead: Understood. I'll document that in the technical spec.

[00:25] Senior Architect: Session management?

[00:27] iOS Dev: 30-day session with refresh tokens. Auto-logout on token expiry.

[00:30] Senior Architect: Sounds good. Any concerns?

[00:32] Android Dev: Just timeline. This is 8 story points minimum with proper testing.

[00:35] Tech Lead: Agreed. I'll update the estimate in Jira.

[00:45] Senior Architect: Decision made - proceed with AppAuth, implement PKCE, secure token storage.
        """,
        "key_decisions": [
            "Use AppAuth library for OAuth2 implementation",
            "Implement PKCE for mobile security",
            "Use Keychain (iOS) and KeyStore (Android) for token storage",
            "30-day session expiry with refresh tokens"
        ],
        "action_items": [
            {"owner": "Tech Lead", "task": "Update technical spec with security requirements", "due": "2026-01-21"},
            {"owner": "Tech Lead", "task": "Update Jira story points to 8", "due": "2026-01-20"},
            {"owner": "iOS Dev", "task": "Create iOS implementation prototype", "due": "2026-01-23"}
        ]
    },
    {
        "id": "zoom-003",
        "title": "Daily Standup - Payment Team",
        "project": "Payment Gateway Integration",
        "date": "2026-01-23",
        "duration_minutes": 15,
        "attendees": ["Scrum Master", "Dev Team", "QA"],
        "transcript": """
[00:01] Scrum Master: Quick standup. What did you do yesterday?

[00:02] Dev1: Worked on payment token encryption. Done and in code review.

[00:03] Dev2: Implemented Redis caching. Reduced API calls by 65%. Ready for testing.

[00:04] QA1: Tested refund flow. Found one edge case bug, logged as PAY-1280.

[00:06] Scrum Master: Blockers?

[00:07] Dev1: Still waiting on SSL certificate. Can't deploy to staging.

[00:08] Scrum Master: Got an update this morning. Certificate should arrive today.

[00:10] Dev2: No blockers. Starting on webhook implementation.

[00:11] QA1: Waiting for Redis caching to be deployed so I can test.

[00:13] Scrum Master: Let's deploy caching to dev environment by noon. Good work everyone.
        """,
        "key_decisions": [],
        "action_items": [
            {"owner": "Dev2", "task": "Deploy Redis caching to dev environment", "due": "2026-01-23"},
            {"owner": "Scrum Master", "task": "Confirm SSL certificate delivery", "due": "2026-01-23"}
        ]
    }
]