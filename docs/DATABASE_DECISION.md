# Database Decision Record: MongoDB Runtime Authority

**Status:** Accepted & Enforced  
**Date:** 2026-09-03  
**Governing PRD:** RAYGO Phase 6 / Phase 7 Implementation PRD (§2.5 & §4.3.1)

---

## 1. Context

RAYGO contains two persistence designs:
1. **MongoDB / mongomock-motor**: Fully implemented across ~15 active repositories, seeded with demo scenarios, wired into all 12 API routers, and validated with full asynchronous test coverage.
2. **Supabase / Postgres**: A 19-table migration schema (`apps/api/app/db/supabase_migrations/001_initial_schema.sql`) and wrapper clients (`supabase_client.py`, `supabase_repositories.py`).

## 2. Decision

**MongoDB is the authoritative runtime database for RAYGO.**
- All services, repositories, and routers persist to MongoDB / mongomock-motor.
- The Supabase client and repository scaffold is preserved as a documented future migration candidate (`NOT ACTIVE AT RUNTIME`) to avoid dual-database state divergence.
- The `/health` and `/health/db` endpoints honestly report `"database": "mongodb"` and `"supabaseStatus": "scaffolded_not_active"`.
- Supabase environment variables are reserved and commented in `.env.example`.

## 3. Consequences

- **Stability**: Zero dual-write ambiguity or connection race conditions.
- **Fast Testing**: The entire test suite executes in ~2 seconds in memory without external network dependencies.
- **Future Migration**: If full cutover to Postgres/Supabase is scheduled in a subsequent dedicated phase, the 19-table SQL schema and entity definitions remain available as the reference blueprint.
