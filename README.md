# Huposit

개인 맥락을 AI가 이해하기 쉬운 구조로 저장하고 검색하기 위한 서비스입니다.

첫 제품 루프는 PowerPoint 파일을 입력받아 슬라이드별 내용을 추출하고, AI가 이해할 수 있는 구조로 변환해 검색할 수 있게 만드는 것입니다.

## Current Setup

현재 저장소는 초기 개발환경과 최소 앱 구성이 완료된 상태입니다.

- Monorepo: pnpm workspace
- Task runner: Turborepo
- Web: React Router
- API: FastAPI
- Worker: Python + uv
- Database: PostgreSQL 17 + pgvector
- Local infra: Docker Compose
- Package manager: pnpm 11.8.0
- Python environment: uv

작업 이력은 Linear 티켓의 Done 시점을 기준으로 [docs/logs/README.md](docs/logs/README.md)에 정리합니다.

## Requirements

- Node.js 24.17.0
- pnpm 11.8.0
- uv
- Docker
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

저장소 루트에서 의존성을 설치합니다.

```bash
pnpm install
pnpm sync:py
```

로컬 PostgreSQL + pgvector DB를 실행합니다.

```bash
pnpm db:up
```

## Development

전체 앱을 실행합니다.

```bash
pnpm dev
```

개별 앱만 실행할 수도 있습니다.

```bash
pnpm --filter @huposit/web dev
pnpm --filter @huposit/api dev
pnpm --filter @huposit/worker dev
```

기본 주소:

- Web: http://localhost:5173
- API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

API 확인:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/db
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

infra/       # Docker Compose and local infrastructure
docs/
  logs/      # Linear Done time based development logs
  workflow.md
```

## Workflow

개발 작업은 Linear issue에서 시작하고 GitHub PR로 merge합니다.

- 상세 작업 규칙: [docs/workflow.md](docs/workflow.md)
- Codex 작업 규칙: [AGENTS.md](AGENTS.md)
- 개발 로그 색인: [docs/logs/README.md](docs/logs/README.md)

커밋과 push는 반드시 사용자 승인 후 진행합니다.
