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

`uv`는 설치 후 셸에서 실행 가능해야 합니다.

```bash
uv --version
```

WSL/Linux에서 `uv`를 설치했는데 명령을 찾지 못하면 `~/.local/bin`이 `PATH`에 포함되어 있는지 확인합니다.

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
curl http://127.0.0.1:8000/health/worker
```

## Editor Import Resolution

이 저장소는 API와 worker가 모두 Python 패키지 이름으로 `app`을 사용합니다.

```txt
apps/api/app/main.py
apps/worker/app/main.py
```

이 구조에서는 VS Code/Pylance 또는 Pyright가 `from app.main import ...` 같은 import를 해석할 때 API의 `app`과 worker의 `app`을 혼동할 수 있습니다. 루트의 [pyrightconfig.json](pyrightconfig.json)은 파일 위치에 따라 import 기준 경로를 분리하기 위한 에디터 설정입니다.

- `apps/api` 아래 파일은 `apps/api`를 import root로 봅니다.
- `apps/worker` 아래 파일은 `apps/worker`를 import root로 봅니다.
- 이 설정은 에디터의 빨간줄과 자동완성 해석을 돕기 위한 것이며, 앱 실행이나 pytest/mypy 검증 방식을 바꾸지 않습니다.

VS Code에서 import 빨간줄이 남아 있으면 `Python: Restart Language Server`를 실행합니다.

## Commands

```bash
pnpm dev        # workspace dev task 실행
pnpm build      # workspace build task 실행
pnpm test       # workspace test task 실행
pnpm lint       # workspace lint task 실행
pnpm typecheck  # workspace typecheck task 실행
pnpm sync:py    # Python 앱 uv sync 실행
pnpm openapi:generate  # OpenAPI schema와 web TypeScript 타입 생성
pnpm db:up      # PostgreSQL + pgvector 컨테이너 실행
```

`build`, `test`, `lint`, `typecheck`는 `apps/web`, `apps/api`, `apps/worker`에서 공통으로 지원합니다. Python 앱의 `build`는 아직 패키징을 만들지 않고 `compileall`로 앱 코드의 문법/import 가능성을 검증합니다.

검증 명령의 실행 기준과 앱별 세부 의미는 [docs/testflow.md](docs/testflow.md)를 따릅니다.

## OpenAPI Type Generation

FastAPI OpenAPI schema와 web TypeScript 타입은 서버를 띄우지 않고 생성합니다.

```bash
pnpm openapi:generate
```

이 명령은 다음 두 단계를 실행합니다.

```bash
pnpm openapi:json   # generated/openapi.json 생성
pnpm openapi:types  # apps/web/app/core/api/openapi-types.ts 생성
```

생성 파일은 API 계약 변경을 PR에서 확인할 수 있도록 커밋합니다. `apps/web/app/core/api/openapi-types.ts`는 생성 파일이므로 직접 수정하지 않고, FastAPI schema를 바꾼 뒤 `pnpm openapi:generate`로 다시 만듭니다. API client와 OpenAPI 타입 helper는 `apps/web/app/core/api` 아래에 둡니다.

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
  testflow.md
```

## Workflow

개발 작업은 Linear issue에서 시작하고 GitHub PR로 merge합니다.

- 상세 작업 규칙: [docs/workflow.md](docs/workflow.md)
- 테스트/검증 규칙: [docs/testflow.md](docs/testflow.md)
- Codex 작업 규칙: [AGENTS.md](AGENTS.md)
- 개발 로그 색인: [docs/logs/README.md](docs/logs/README.md)

커밋과 push는 반드시 사용자 승인 후 진행합니다.
