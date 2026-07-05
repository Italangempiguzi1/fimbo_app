# Umbrella v2 Platform Overview

Umbrella v2 is designed around four clients and one backend:

1. Flutter mobile app for Android and iOS.
2. React web app for browser streaming, creator studio and admin operations.
3. Native Java Android TV app for TV-style browsing and playback.
4. Django backend with PostgreSQL, Redis and Celery.

The backend is subscription-gated: users can browse the UI and metadata without a subscription, but stream/download endpoints return `402 Payment Required` until the user has an active subscription.

The reels feed uses a lightweight recommendation algorithm based on watch time, views, likes, comments, votes, awards, shares and freshness. This avoids simply returning items in database order.
