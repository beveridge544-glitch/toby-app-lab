# ChartPing MVP Build Plan — 2026-02-24

## Product Direction
Build **ChartPing** as a clean Android app focused on:
- Live crypto stats and charts
- Watchlist tracking
- Alerts ("pings")
- Future paid AI chart insights

Keep scope to **information + notifications only** (no trading/custody).

---

## Recommended Stack
- **Mobile:** Flutter
- **State:** Riverpod (or Provider if already started)
- **Charts:** `fl_chart`
- **Notifications:** `flutter_local_notifications`
- **Push:** `firebase_messaging` + FCM
- **Backend:** FastAPI on existing crypto scanner server
- **DB:** Postgres (or SQLite initially)

---

## Data Source Strategy
### MVP (fastest)
- Use **CoinGecko** for multi-coin markets + chart history.
- Endpoints:
  - `/coins/markets`
  - `/coins/{id}`
  - `/coins/{id}/market_chart`

### Optional v1.1 enhancement
- Add **Binance public endpoints** for exchange-specific speed/precision.
- Keep as read-only market data.

---

## Build Order (Execution)

### Phase 1 — Foundation (1-2 days)
1. App shell with bottom nav: Home, Markets, Alerts, Settings
2. Theme + currency settings persistence
3. API service and models (`Coin`, `CoinDetails`, `ChartPoint`, `AlertRule`)

### Phase 2 — Live Data + Charts (2-3 days)
1. Markets list (top coins, search)
2. Watchlist add/remove + local persistence
3. Coin details stats + timeframe chart (24h, 7d, 30d, 90d)
4. Pull-to-refresh and basic error states

### Phase 3 — Alerts (2-4 days)
1. Alert create/edit/delete UI
2. Local logic validation first (in-app checks + local notification)
3. Move checks server-side for reliability:
   - Register device + FCM token
   - Persist alert rules
   - Scanner evaluates and pushes notifications

### Phase 4 — Quality + Store Readiness (1-2 days)
1. Disclaimer + privacy links
2. Notification controls and quiet hours
3. Empty states/loading polish
4. Build Android App Bundle (.aab), target API 35

---

## API Contract (Backend)
- `POST /register-device` → `{ deviceId, fcmToken, platform }`
- `GET /alerts?deviceId=...`
- `POST /alerts`
- `PATCH /alerts/{id}`
- `DELETE /alerts/{id}`
- `GET /alerts/history?deviceId=...`

Alert payload example:
```json
{
  "deviceId": "abc123",
  "coinId": "bitcoin",
  "type": "price_above",
  "value": 50000,
  "currency": "GBP",
  "repeat": false,
  "active": true
}
```

---

## Freemium / Pro Plan (for later)

### Free
- Watchlist + charts + basic alerts
- **3 AI analyses per 24h**

### Pro
- Unlimited AI analyses
- Multi-timeframe auto trendlines
- Auto support/resistance zones
- Pattern detection summaries

Implementation note:
- Track quota by `deviceId` + rolling 24h window in backend.
- Show soft paywall after free quota is consumed.

---

## "AI Insights" Definition (honest + compliant)
Start with deterministic quant logic and present as AI-assisted insights:
- Trend classification (EMA/structure)
- Support/resistance zone clustering
- Basic pattern flags (triangle, double top/bottom, channels)
- Human-readable summary text

Always include: **"Informational only, not financial advice."**

---

## Google Play Checklist
- [ ] Target API 35
- [ ] Release as `.aab`
- [ ] Finance category metadata complete
- [ ] Privacy policy URL live
- [ ] No guaranteed return language
- [ ] No exchange/wallet/custody behavior

