# Umbrella Backend MVP Apps

## 1. users
Handles viewer and creator user accounts.

Minimum features:
- Register user
- JWT login and refresh
- View/update current profile
- Roles: viewer, creator, staff

## 2. creators
Handles creator identity and dashboard.

Minimum features:
- Create creator profile
- Creator verification status
- Payout details placeholder
- Creator dashboard foundation

## 3. subscriptions
Controls access to content.

Minimum features:
- Basic, Standard, Premium plans
- Active subscription checking
- Current subscription endpoint
- Development-only subscription activation endpoint

## 4. payments
Stores payment attempts and payment status.

Minimum features:
- Initiate payment record
- Store provider, amount, currency, phone, status
- Ready for future mobile money or card callback integration

## 5. content
Handles long-form content.

Minimum features:
- Movies, series, documentaries, education, premium creator content
- Metadata and video asset records
- Draft, pending review, approved, rejected workflow
- Streaming URL endpoint for subscribed users

## 6. reels
Handles short-form vertical videos.

Minimum features:
- Creator reel uploads through URL metadata
- Feed endpoint
- Streaming endpoint for subscribed users
- Moderation workflow

## 7. engagement
Handles social actions.

Minimum features:
- Like/unlike
- Comment
- Vote 1-5
- Follow/unfollow creator
- Award creator using points

## 8. analytics
Tracks watching behavior.

Minimum features:
- Start watch session
- End watch session
- Valid views after 10 watched seconds
- Update content/reel total views and watch seconds

## 9. rewards
Handles creator monetization.

Minimum features:
- Reward configuration
- Creator earning records
- Payout records
- Celery task placeholder for monthly calculations

## 10. moderation
Handles safety and legal reporting.

Minimum features:
- Report content or reels
- Store moderation action records
- Admin review through Django Admin

## 11. notifications
Handles user alerts.

Minimum features:
- Store notifications
- List notifications
- Mark notification as read
