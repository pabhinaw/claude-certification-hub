---
paths:
  - "src/api/**/*.ts"
---
- Validate every request body with zod before using it.
- Return errors as { code, message }; never leak stack traces.
