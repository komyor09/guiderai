# Known Issues (GuideRAI)

## Step 8.4 — Dialog & UI State

### 1. Frontend state persistence is unstable
- After page reload (F5), filters and results are restored via localStorage
- In some cases UI order or timing may break (race conditions)
- Chat history restoration depends on DOM timing

### 2. UX inconsistency on reload
- Chat is restored only after repeated search
- Dialog logic is correct on backend, but frontend rendering may feel confusing

### 3. Not critical
- Backend dialog state works correctly
- Issues are frontend-only and do not affect data integrity

Planned fix:
- Step 8.5 or refactor UI state management
