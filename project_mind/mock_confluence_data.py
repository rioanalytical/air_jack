"""Mock Confluence data"""

CONFLUENCE_PAGES = [
    {
        "id": "conf-1001",
        "title": "Payment Gateway Integration - Technical Specification",
        "project": "Payment Gateway Integration",
        "space": "Engineering",
        "author": "Tech Lead",
        "created": "2025-12-15",
        "updated": "2026-01-20",
        "content": """
# Payment Gateway Integration - Technical Specification

## Overview
Integration with Stripe payment gateway for processing credit card transactions.

## Architecture
- Microservices-based approach
- Event-driven architecture using Kafka
- Redis for caching payment tokens
- PostgreSQL for transaction records

## Security Requirements
- PCI DSS Level 1 compliance
- End-to-end encryption
- SSL/TLS 1.3 minimum
- Token-based authentication
- No card data stored locally

## API Endpoints
- POST /api/v1/payments/process
- GET /api/v1/payments/{transaction_id}
- POST /api/v1/payments/refund

## Implementation Details
All payment processing must use the approved PaymentService class with retry logic and idempotency keys.

## Database Schema
- transactions table: id, amount, currency, status, created_at
- payment_methods table: id, user_id, token, type
        """,
        "tags": ["technical", "architecture", "payment"]
    },
    {
        "id": "conf-1002",
        "title": "Mobile App Authentication - Requirements",
        "project": "Mobile App Rewrite",
        "space": "Product",
        "author": "Product Owner",
        "created": "2026-01-10",
        "updated": "2026-01-18",
        "content": """
# Mobile App Authentication Requirements

## User Stories
1. As a user, I want to login with Google so I can access the app quickly
2. As a user, I want to login with Facebook for convenience
3. As a user, I want biometric authentication for security

## Acceptance Criteria
- OAuth2 integration with Google and Facebook
- Biometric authentication (Face ID/Touch ID) support
- Session management with 30-day expiry
- Secure token storage using Keychain/KeyStore
- Remember me functionality

## Out of Scope
- Username/password authentication (legacy)
- Two-factor authentication (Phase 2)

## Technical Requirements
- Use industry-standard OAuth2 libraries
- Implement PKCE for mobile security
- Store tokens encrypted at rest
        """,
        "tags": ["requirements", "authentication", "mobile"]
    },
    {
        "id": "conf-1003",
        "title": "Caching Strategy for Microservices",
        "project": "Payment Gateway Integration",
        "space": "Engineering",
        "author": "Senior Architect",
        "created": "2025-11-20",
        "updated": "2026-01-05",
        "content": """
# Caching Strategy

## Approved Approach
All microservices should implement caching using Redis with the following pattern:

1. Cache-aside pattern for read-heavy operations
2. Write-through pattern for critical data
3. TTL: 15 minutes for user sessions, 1 hour for reference data
4. Cache key naming: {service}:{entity}:{id}

## Example Implementation
```python
def get_user_profile(user_id):
    cache_key = f"user-service:profile:{user_id}"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    profile = db.query_user(user_id)
    redis.setex(cache_key, 900, json.dumps(profile))
    return profile
```

## Cache Invalidation
Use event-driven invalidation via Kafka topics.
        """,
        "tags": ["architecture", "caching", "best-practices"]
    },
    {
        "id": "conf-2001",
        "title": "Product Roadmap Q1 2026",
        "project": "Mobile App Rewrite",
        "space": "Product",
        "author": "Product Manager",
        "created": "2025-12-01",
        "updated": "2026-01-15",
        "content": """
# Q1 2026 Product Roadmap

## Strategic Goals
1. Increase mobile user engagement by 40%
2. Reduce authentication friction
3. Improve app store ratings to 4.5+

## Key Features
- New authentication system (OAuth2) - January
- Enhanced user profile - February
- Push notifications v2 - March
- Offline mode - March

## Business Justification
Mobile traffic represents 65% of our user base but only 40% of revenue. 
Improved mobile experience expected to increase conversion by 25%.
        """,
        "tags": ["roadmap", "strategy", "product"]
    }
]