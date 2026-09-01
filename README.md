# Steadfast

A small, modern goal-tracking web app used as the reference project for this
repository's development environment. Track daily/weekly goals, toggle them
complete, and watch your streaks grow.

- **Frontend:** React 19 + TypeScript + Vite + Tailwind CSS
- **Backend:** Express 5 + TypeScript (run with `tsx`), in-memory store
- **Tests:** Vitest + Supertest (API)

## Getting started

```bash
npm install        # install dependencies
npm run dev        # start API (:3001) and web (:5173) together
```

Then open http://localhost:5173. The Vite dev server proxies `/api/*` to the
Express API on port `3001`, so a single origin serves the whole app in
development.

## Scripts

| Command             | Description                                         |
| ------------------- | --------------------------------------------------- |
| `npm run dev`       | Run the API and web dev servers concurrently        |
| `npm run dev:server`| Run only the Express API (`:3001`, watch mode)      |
| `npm run dev:client`| Run only the Vite web dev server (`:5173`)          |
| `npm run build`     | Type-check and build the production web bundle      |
| `npm run preview`   | Preview the production build                         |
| `npm run typecheck` | Type-check the project without emitting             |
| `npm test`          | Run the Vitest test suite                            |

## API

| Method   | Path                     | Description                    |
| -------- | ------------------------ | ------------------------------ |
| `GET`    | `/api/health`            | Health check                   |
| `GET`    | `/api/goals`             | List goals                     |
| `POST`   | `/api/goals`             | Create a goal `{ title, cadence }` |
| `POST`   | `/api/goals/:id/toggle`  | Toggle a goal's completion     |
| `DELETE` | `/api/goals/:id`         | Delete a goal                  |

## Cloud Agent environment

`.cursor/environment.json` installs dependencies with `npm ci` and starts the
`api` and `web` dev servers as named terminals. The app uses an in-memory store,
so no database or external service is required to run it end to end.
