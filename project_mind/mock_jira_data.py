"""Mock JIRA data for testing"""

JIRA_ISSUES = [
    {
        "id": "JIRA-1234",
        "key": "PAY-1234",
        "type": "Bug",
        "status": "Blocked",
        "priority": "Critical",
        "summary": "Payment gateway SSL certificate issue",
        "description": "SSL certificate for payment gateway expired. Cannot deploy to production.",
        "project": "Payment Gateway Integration",
        "assignee": "DevOps Team",
        "reporter": "John Doe",
        "created": "2026-01-18",
        "updated": "2026-01-23",
        "blocked_days": 5,
        "components": ["payment-module", "infrastructure"],
        "labels": ["blocker", "production", "ssl"],
        "comments": [
            {
                "author": "Jane Smith",
                "created": "2026-01-20",
                "body": "Waiting on vendor response for new certificate"
            }
        ]
    },
    {
        "id": "JIRA-1256",
        "key": "PAY-1256",
        "type": "Task",
        "status": "Blocked",
        "priority": "High",
        "summary": "PCI compliance review pending",
        "description": "Security team needs to complete PCI DSS compliance review before processing live transactions.",
        "project": "Payment Gateway Integration",
        "assignee": "Security Team",
        "reporter": "Alice Johnson",
        "created": "2026-01-20",
        "updated": "2026-01-23",
        "blocked_days": 3,
        "components": ["payment-module", "security"],
        "labels": ["compliance", "security", "blocker"]
    },
    {
        "id": "JIRA-1267",
        "key": "PAY-1267",
        "type": "Bug",
        "status": "Blocked",
        "priority": "High",
        "summary": "Third-party API rate limiting",
        "description": "Payment processor API is rate limiting our requests during peak hours.",
        "project": "Payment Gateway Integration",
        "assignee": "Backend Team",
        "reporter": "Bob Wilson",
        "created": "2026-01-21",
        "updated": "2026-01-23",
        "blocked_days": 2,
        "components": ["payment-module", "api"],
        "labels": ["performance", "third-party"]
    },
    {
        "id": "JIRA-2001",
        "key": "MOB-2001",
        "type": "Story",
        "status": "In Progress",
        "priority": "Medium",
        "summary": "Implement OAuth2 authentication",
        "description": "As a user, I want to login using OAuth2 providers like Google and Facebook.",
        "project": "Mobile App Rewrite",
        "assignee": "Sarah Lee",
        "reporter": "Product Owner",
        "created": "2026-01-15",
        "updated": "2026-01-23",
        "story_points": 8,
        "components": ["authentication", "mobile"],
        "labels": ["oauth", "security"]
    },
    {
        "id": "JIRA-2010",
        "key": "MOB-2010",
        "type": "Task",
        "status": "Done",
        "priority": "Medium",
        "summary": "Design new login screen UI",
        "description": "Create mockups and designs for the new mobile login screen.",
        "project": "Mobile App Rewrite",
        "assignee": "Design Team",
        "reporter": "Product Manager",
        "created": "2026-01-10",
        "updated": "2026-01-22",
        "components": ["ui", "mobile"],
        "labels": ["design", "frontend"]
    },
    {
        "id": "JIRA-3005",
        "key": "DASH-3005",
        "type": "Bug",
        "status": "Open",
        "priority": "Critical",
        "summary": "Dashboard reports showing incorrect data",
        "description": "Customer dashboard is displaying wrong revenue figures for Q4 2025.",
        "project": "Customer Dashboard v2.0",
        "assignee": "Tom Harris",
        "reporter": "QA Team",
        "created": "2026-01-22",
        "updated": "2026-01-23",
        "components": ["reporting", "dashboard"],
        "labels": ["data-integrity", "critical"]
    },
    {
        "id": "JIRA-4001",
        "key": "API-4001",
        "type": "Epic",
        "status": "In Progress",
        "priority": "High",
        "summary": "Migrate from REST to GraphQL",
        "description": "Migration of all REST APIs to GraphQL for better performance and flexibility.",
        "project": "API Migration Project",
        "assignee": "Backend Team",
        "reporter": "Tech Lead",
        "created": "2026-01-05",
        "updated": "2026-01-23",
        "components": ["api", "backend"],
        "labels": ["migration", "graphql"]
    }
]

SPRINTS = [
    {
        "id": "sprint-15",
        "name": "Sprint 15",
        "project": "Payment Gateway Integration",
        "status": "Active",
        "start_date": "2026-01-13",
        "end_date": "2026-01-26",
        "goal": "Complete payment gateway integration and pass security audit",
        "total_points": 45,
        "completed_points": 28,
        "velocity": 38,
        "issues": ["PAY-1234", "PAY-1256", "PAY-1267"]
    },
    {
        "id": "sprint-16",
        "name": "Sprint 16",
        "project": "Mobile App Rewrite",
        "status": "Active",
        "start_date": "2026-01-13",
        "end_date": "2026-01-26",
        "goal": "Complete authentication module and begin profile screen",
        "total_points": 50,
        "completed_points": 35,
        "velocity": 42,
        "issues": ["MOB-2001", "MOB-2010"]
    }
]

VELOCITY_HISTORY = [
    {"sprint": "Sprint 10", "velocity": 45, "project": "Payment Gateway Integration"},
    {"sprint": "Sprint 11", "velocity": 42, "project": "Payment Gateway Integration"},
    {"sprint": "Sprint 12", "velocity": 48, "project": "Payment Gateway Integration"},
    {"sprint": "Sprint 13", "velocity": 40, "project": "Payment Gateway Integration"},
    {"sprint": "Sprint 14", "velocity": 38, "project": "Payment Gateway Integration"},
    {"sprint": "Sprint 15", "velocity": 28, "project": "Payment Gateway Integration"},  # Current, in progress
]