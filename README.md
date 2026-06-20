# Huposit

개인 맥락을 AI가 이해하기 쉬운 구조로 저장하고 검색하기 위한 서비스입니다.

초기 목표는 PowerPoint 파일을 업로드하면 슬라이드별로 내용을 추출하고, 이후 AI가 이해할 수 있는 구조로 변환해 검색할 수 있게 만드는 것입니다.

## Tech Stack

- Monorepo: pnpm workspace
- Task runner: Turborepo
- Web: React Router
- API: FastAPI
- Worker: Python + uv
- Database: PostgreSQL 17 + pgvector
- Local infra: Docker Compose
- Package manager: pnpm 11.8.0
- Python environment: uv

## Requirements

- Node.js 24.17.0
- pnpm 11.8.0
- uv
- Git

Node 버전은 nvm 사용을 권장합니다.

```bash
nvm use
```

pnpm은 Corepack으로 활성화합니다.

```bash
corepack enable
corepack prepare pnpm@11.8.0 --activate
```

## Setup

저장소를 받은 뒤 루트에서 실행합니다.

```bash
pnpm install
pnpm sync:py
```

`pnpm install`은 JS/TS workspace 의존성을 설치합니다.

`pnpm sync:py`는 `apps/api`, `apps/worker`의 Python 의존성을 `uv sync`로 동기화합니다.

## Development

전체 개발 프로세스를 실행합니다.

```bash
pnpm dev
```

개별 실행도 가능합니다.

```bash
pnpm --filter @huposit/web dev
pnpm --filter @huposit/api dev
pnpm --filter @huposit/worker dev
```

기본 주소는 다음과 같습니다.

- Web: http://localhost:5173
- API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

API health check:

```bash
curl http://127.0.0.1:8000/health
```

## Database

로컬 개발 DB는 Docker Compose로 실행합니다.

```bash
pnpm db:up
```


## Commands

```bash
pnpm dev        # workspace dev task 실행
pnpm build      # workspace build task 실행
pnpm test       # workspace test task 실행
pnpm typecheck  # workspace typecheck task 실행
pnpm sync:py    # Python 앱 uv sync 실행
pnpm db:up      # PostgreSQL + pgvector 컨테이너 실행
```

## Project Structure

```txt
apps/
  web/       # React Router app
  api/       # FastAPI app
  worker/    # background worker

packages/    # shared packages, added as needed
infra/       # infrastructure files, added as needed
```

## Notes

- Git은 루트 저장소 하나만 사용합니다.
- `node_modules`, `.venv`, build outputs는 Git에 올리지 않습니다.
- `apps/api`와 `apps/worker`는 각각 독립된 uv 가상환경을 사용합니다.
- 현재 worker는 job queue 없이 heartbeat만 출력하는 최소 실행 프로세스입니다.
