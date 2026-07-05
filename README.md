# Umbrella Backend v2 - Streaming + Reels + Creator Monetization

This Django backend supports the improved Umbrella MVP:

- subscription-gated streaming access
- public browsing for unsubscribed users
- direct video/thumbnail uploads from creator/admin devices
- background media pipeline placeholders for transcoding/CDN delivery
- home hero banners with dot indicators
- horizontal branding carousel data
- Netflix-style content rows and View All endpoints
- autoplay-ready reels feed with stream URLs only for subscribed users
- comments with replies, latest comments first
- like, vote, follow, award, share counters
- watch-time analytics with heartbeat/end events
- creator application and admin verification
- verified creator upload control
- creator dashboard metrics
- app settings, language/theme preferences
- in-app offline download licenses
- legal/help pages

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

Then in another terminal:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_plans
docker compose exec web python manage.py seed_categories
```

## Main API groups

```text
/api/home/
/api/branding/
/api/content/
/api/reels/
/api/engagement/comments/
/api/creator-applications/me/
/api/downloads/
/api/settings/me/
/api/legal/pages/
/api/media-pipeline/jobs/
```

## Important production notes

The MVP accepts direct uploads and stores files under Django media storage. For production, configure S3-compatible storage, a CDN, real HLS/DASH transcoding, DRM/watermarking, anti-piracy controls, payment callbacks, monitoring and backups. The stream endpoints already enforce subscription access on the backend.
