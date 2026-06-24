# Testflow

ver. 1.0.0_26.06.21

이 문서는 Huposit monorepo의 테스트와 검증 명령 기준을 정의한다.

`docs/workflow.md`는 Linear, branch, commit, PR, merge 절차의 기준이다. 이 문서는 그 절차 안에서 어떤 검증 명령을 언제 실행하고 어떻게 보고할지 다룬다.

## 1. 기본 원칙

- `build`, `test`, `lint`, `typecheck`는 `apps/web`, `apps/api`, `apps/worker`가 공통으로 지원한다.
- 루트 검증 명령은 Turborepo를 통해 각 앱의 같은 이름 script를 실행한다.
- 테스트는 기본적으로 DB, Docker, 외부 네트워크 없이 실행 가능해야 한다.
- DB, Docker, 네트워크가 필요한 검증은 일반 `test`와 분리하고 Linear issue 또는 PR 확인 항목에 명시한다.
- 검증 결과를 보고할 때는 실행한 명령과 성공/실패 여부를 그대로 남긴다.

## 2. 루트 검증 명령

저장소 루트에서 실행한다.

```bash
pnpm build
pnpm test
pnpm lint
pnpm typecheck
```

각 명령의 의미는 다음과 같다.

| 명령 | 목적 | 현재 실행 내용 |
| --- | --- | --- |
| `pnpm build` | 앱이 빌드 또는 빌드에 준하는 검증을 통과하는지 확인 | Web은 React Router production build, API/worker는 Python `compileall` |
| `pnpm test` | 자동 테스트 실행 | Web은 Vitest, API/worker는 pytest |
| `pnpm lint` | 정적 규칙과 위험 패턴 확인 | Web은 ESLint, API/worker는 Ruff |
| `pnpm typecheck` | 타입 검사 | Web은 React Router typegen + TypeScript, API/worker는 mypy |

루트 명령은 PR 전 전체 검증에 사용한다. 작은 문서 변경처럼 영향 범위가 좁은 경우에도 Linear issue의 `Done when`에 명시된 검증은 실행한다.

## 3. 앱별 검증 명령

앱 하나만 변경했거나 실패 지점을 좁힐 때는 `--filter`를 사용한다.

### Web

```bash
pnpm --filter @huposit/web build
pnpm --filter @huposit/web test
pnpm --filter @huposit/web lint
pnpm --filter @huposit/web typecheck
```

- `build`: React Router production build를 실행한다.
- `test`: Vitest 테스트를 실행한다.
- `lint`: ESLint 규칙을 검사한다.
- `typecheck`: React Router typegen 후 TypeScript 검사를 실행한다.

화면 UI를 바꾸는 작업은 자동 검증 외에도 데스크톱과 모바일 폭에서 직접 확인한다.

### API

```bash
pnpm --filter @huposit/api build
pnpm --filter @huposit/api test
pnpm --filter @huposit/api lint
pnpm --filter @huposit/api typecheck
```

- `build`: `python -m compileall -q app`으로 앱 코드의 문법과 import 가능성을 검증한다.
- `test`: pytest 테스트를 실행한다.
- `lint`: Ruff 규칙을 검사한다.
- `typecheck`: mypy로 `app` 패키지를 검사한다.

API 테스트는 기본적으로 실제 DB에 연결하지 않는다. DB 연결을 검증해야 할 때는 별도 통합 테스트 또는 수동 확인 항목으로 분리한다.

### Worker

```bash
pnpm --filter @huposit/worker build
pnpm --filter @huposit/worker test
pnpm --filter @huposit/worker lint
pnpm --filter @huposit/worker typecheck
```

- `build`: `python -m compileall -q app`으로 앱 코드의 문법과 import 가능성을 검증한다.
- `test`: pytest 테스트를 실행한다.
- `lint`: Ruff 규칙을 검사한다.
- `typecheck`: mypy로 `app` 패키지를 검사한다.

Worker 테스트도 기본적으로 DB, Docker, 네트워크 없이 실행 가능해야 한다.

## 4. Python build 의미

API와 worker의 `build`는 현재 배포 패키지를 생성하지 않는다.

```bash
uv run python -m compileall -q app
```

이 명령은 Python 파일이 컴파일 가능한지 확인한다. 지금 단계에서 Python 앱의 build는 다음을 뜻한다.

- 문법 오류가 없다.
- `app` 패키지 코드가 bytecode compile을 통과한다.
- 패키징 산출물을 만들지는 않는다.

나중에 wheel, container image, 배포 artifact를 만들게 되면 이 문서와 각 앱의 `package.json` script를 함께 갱신한다.

## 5. 테스트 독립성 기준

기본 `pnpm test`는 다음에 의존하지 않아야 한다.

- 로컬 PostgreSQL 또는 pgvector 컨테이너
- Docker Compose 실행 상태
- 외부 API 또는 인터넷 연결
- 개발자의 개인 `.env` 파일

테스트가 설정값 import를 위해 환경변수가 필요하면 테스트용 dummy 값을 사용한다. dummy 값은 실제 로컬 서비스처럼 보이지 않게 작성한다.

예:

```txt
postgresql+asyncpg://test:test@127.0.0.1:1/test
```

실제 DB 연결을 검증하는 테스트가 필요하면 일반 unit/smoke test와 분리하고, 실행 조건과 명령을 문서에 명시한다.

## 6. PR 전 권장 검증 순서

일반 구현 티켓은 다음 순서로 확인한다.

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

문서만 변경한 티켓은 최소 다음을 확인한다.

```bash
pnpm lint
pnpm typecheck
```

단, Linear issue의 `Done when`이 더 넓은 검증을 요구하면 그 기준을 따른다.

변경 범위가 특정 앱에만 닿는 경우에는 앱별 명령으로 빠르게 확인한 뒤, PR 전에는 필요한 루트 명령을 실행한다.

API response model, route, `operation_id`, OpenAPI schema, 생성 타입, web API 타입 연결이 바뀌는 티켓은 루트 검증 전에 다음 명령을 실행한다.

```bash
pnpm openapi:generate
```

이 명령은 서버를 띄우지 않고 `generated/openapi.json`과 `apps/web/app/core/api/openapi-types.ts`를 갱신한다. 생성 파일은 직접 수정하지 않고, PR에서 API 계약 변경을 확인할 수 있도록 함께 커밋한다.

## 7. 검증 보고 형식

Codex 또는 작업자는 구현 후 다음 정보를 보고한다.

```md
## 확인

- `pnpm openapi:generate` 성공  # OpenAPI 계약 또는 생성 타입이 바뀐 경우
- `pnpm lint` 성공
- `pnpm typecheck` 성공
- `pnpm test` 성공
- `pnpm build` 성공
```

실패한 명령이 있으면 실패 명령, 원인, 남은 조치 또는 후속 issue 후보를 함께 남긴다.

## 8. 문서 갱신 기준

다음 변경이 생기면 이 문서를 함께 갱신한다.

- 루트 검증 명령이 추가, 삭제, 변경된다.
- 앱별 `build`, `test`, `lint`, `typecheck` 의미가 바뀐다.
- 테스트가 DB, Docker, 네트워크에 의존하는 별도 계층으로 분리된다.
- PR 전 필수 검증 기준이 바뀐다.
