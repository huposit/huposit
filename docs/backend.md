# Backend Direction

ver. 0.1.0_26.06.21

이 문서는 HUP-8의 결과물이다. 휴포짓 백엔드를 본격 구현하기 전에, 개인 슬라이드/파일 관리 콘솔과 AI 맥락 저장소에 적합한 백엔드 구현 방향을 정리한다.

## 결론

휴포짓 백엔드는 작은 서버에서 오래 안정적으로 돌아가는 구조를 우선한다. 초기 목표는 많은 기능을 빠르게 붙이는 것이 아니라, 파일 업로드, 슬라이드 추출, 처리 작업, 검색, 자체 로그인의 경계를 작고 명확하게 만드는 것이다.

첫 방향은 다음과 같다.

- 런타임: FastAPI
- 데이터베이스: PostgreSQL 17 + pgvector
- 작업 처리: Python worker
- API 계약: FastAPI OpenAPI 스펙을 기준으로 프론트 타입/클라이언트 동기화
- 배포 제약: AWS Lightsail 2GB에서도 동작하는 가벼운 구조
- 인증: 외부 Auth 서비스에 의존하지 않되, 검증된 라이브러리와 OWASP 기준을 사용
- 구조: app, api, domain, schemas, services, repositories, workers로 책임 분리
- 동시성: idempotency, transaction, lock, retry, job 상태 전이를 명시적으로 관리
- 벤더 종속: 외부 플랫폼 종속은 줄이고, 검증된 라이브러리와 PostgreSQL 기능은 사용

이번 문서는 구현을 하지 않는다. 이후 티켓이 이 방향을 기준으로 구현 단위를 나누도록 돕는 문서다.

## 프론트와 맞출 도메인 언어

`docs/frontend.md`와 같은 도메인 용어를 사용한다. 프론트 화면 용어와 백엔드 모델 용어가 어긋나면 OpenAPI 타입, DTO, 화면 상태가 계속 흔들린다.

권장 도메인 용어:

- `SourceFile`: 사용자가 업로드한 원본 파일
- `Deck`: 하나의 발표 자료 또는 슬라이드 묶음
- `Slide`: 슬라이드 한 장
- `SlideBlock`: 슬라이드에서 추출된 텍스트, 이미지, 표, 도형 등의 구조화 단위
- `ProcessingJob`: 파일 추출, 변환, 임베딩, 요약 같은 비동기 작업
- `Collection`: 사용자가 자료를 묶는 컬렉션
- `Tag`: 자유롭게 붙이는 태그
- `SavedSearch`: 재사용 가능한 검색 조건
- `User`: 자체 로그인으로 식별되는 사용자
- `Session`: 로그인 상태를 나타내는 서버 측 세션 또는 세션 토큰

초기 제품 루프는 다음 흐름을 기준으로 한다.

```txt
User
  -> SourceFile upload
  -> ProcessingJob created
  -> Worker extracts Deck / Slides / SlideBlocks
  -> API exposes Library / Jobs / Deck / Slide / Search data
  -> Web console renders the state
```

## 현재 상태

현재 백엔드는 최소 구조만 있다.

- `apps/api`: FastAPI 앱
- `apps/api/app/main.py`: API 앱 조립, CORS 설정, 공통 exception handler 등록, router include
- `apps/api/app/core/config.py`: `.env` 기반 설정
- `apps/api/app/core/cors.py`: 로컬 web origin CORS 설정
- `apps/api/app/core/errors.py`: 도메인 예외를 HTTP JSON 응답으로 변환하는 공통 handler
- `apps/api/app/core/security.py`: Argon2id password hash helper
- `apps/api/app/db/session.py`: SQLAlchemy async engine/session
- `apps/api/app/db/base.py`: SQLAlchemy `Base`와 `TimestampMixin`
- `apps/api/app/db/migrations`: Alembic migration 설정과 revision 파일
- `apps/api/app/features/auth`: 회원가입 API, 회원 목록 개발 검증 API, schema, service, repository, User 모델, auth 도메인 예외
- `apps/api/app/features/health`: `/health`, `/health/db`, `/health/worker`
- `apps/api/app/tools/export_openapi.py`: 서버 실행 없이 OpenAPI JSON을 생성하는 도구
- `apps/worker`: Python worker 앱
- `apps/worker/app/main.py`: heartbeat loop
- `infra/compose.yml`: PostgreSQL 17 + pgvector

인증은 HUP-13에서 email/password 회원가입 흐름부터 구현을 시작했다. 현재 범위는 email 기반 사용자 생성, Argon2id password hash, 중복 email 처리, 회원가입 응답 계약, OpenAPI/web type 연결까지다. 아직 로그인, 세션, 이메일 인증 메일 발송은 구현하지 않았으며, 다음 구현도 현재 계층 책임을 유지해 작게 확장한다.

## 배포 제약

초기 배포 타깃은 AWS Lightsail 2GB에서도 버틸 수 있는 구조로 잡는다.

원칙:

- API 서버, worker, PostgreSQL이 같은 작은 머신에서 돌 수 있음을 전제로 한다.
- 메모리 사용량이 큰 상주 프로세스를 늘리지 않는다.
- worker concurrency는 낮은 기본값에서 시작한다.
- 파일 처리 작업은 한 번에 너무 많은 파일을 메모리에 올리지 않는다.
- 추출 결과와 원본 파일은 DB에 무작정 넣지 않고 저장 전략을 분리한다.
- polling, background task, retry 주기는 보수적으로 잡는다.
- 대용량 파일 업로드와 임베딩 작업은 나중에 병목을 측정한 뒤 확장한다.

초기에는 단일 PostgreSQL과 단일 worker로 시작한다. 큐 시스템은 DB 기반 job table로 먼저 구현하고, Redis/Celery 같은 추가 인프라는 실제 병목이 확인된 뒤 검토한다.

## 아키텍처 원칙

백엔드는 계층을 얇게 나누되, 과도한 추상화는 피한다.

권장 계층:

```txt
apps/api/app/
  main.py
  core/
    config.py
    security.py
    errors.py
  db/
    base.py
    session.py
    migrations/
  api/
    routes/
      auth.py
      source_files.py
      processing_jobs.py
      decks.py
      slides.py
      search.py
  domain/
    source_files/
    processing_jobs/
    decks/
    slides/
    search/
    users/
  schemas/
    source_files.py
    processing_jobs.py
    decks.py
    slides.py
    search.py
    users.py
  services/
    source_file_service.py
    processing_job_service.py
    deck_service.py
    search_service.py
    auth_service.py
  repositories/
    source_file_repository.py
    processing_job_repository.py
    deck_repository.py
    user_repository.py
```

`apps/worker`도 같은 도메인 용어를 사용한다.

```txt
apps/worker/app/
  main.py
  core/
    config.py
  jobs/
    runner.py
    handlers/
      extract_deck.py
      embed_slide_blocks.py
      summarize_deck.py
  services/
    pptx_extractor.py
    embedding_service.py
  repositories/
    processing_job_repository.py
    deck_repository.py
```

구현 원칙:

- `api/routes`: HTTP 요청/응답, dependency, status code만 다룬다.
- `schemas`: OpenAPI로 노출할 DTO를 정의한다.
- `services`: use case를 담당한다.
- `repositories`: DB query를 담당한다.
- `features/<feature>/error.py`: 해당 feature의 도메인 예외를 둔다.
- `core/errors.py`: 도메인 예외를 HTTP response로 변환하는 공통 FastAPI exception handler를 둔다.
- `domain`: 상태 전이, enum, 도메인 규칙을 둔다.
- `worker/jobs`: job type별 실행 흐름을 담당한다.
- Python 패키지는 namespace package 방식을 사용하고, 새 디렉터리를 만들 때 `__init__.py`를 추가하지 않는다.
- SQLAlchemy 모델은 `app/db/base.py`의 `Base`를 상속한다.
- `created_at`, `updated_at`이 필요한 테이블은 `TimestampMixin`을 함께 상속한다.

중복 제거는 service 계층에서 시작한다. repository를 너무 일찍 generic하게 만들지 않는다.

현재 `features/auth` 구현 패턴:

- `router.py`: FastAPI request schema를 받고 response schema를 조립한다. 성공 흐름만 작성하고 중복 이메일 같은 도메인 실패를 직접 `try/except`로 처리하지 않는다.
- `schema.py`: OpenAPI에 노출되는 request/response DTO를 정의한다.
- `service.py`: email 정규화, password hash, repository 호출 같은 회원가입 use case 흐름을 담당한다. FastAPI response 객체를 만들지 않는다.
- `repository.py`: 필요한 시점에 `AsyncSessionLocal`을 열고 닫으며 SQLAlchemy query와 commit/rollback을 담당한다.
- `error.py`: `DuplicateEmailError`처럼 auth 도메인에서 의미 있는 예외를 정의한다.
- `core/errors.py`: `DuplicateEmailError`를 `SignupResponse(status="error", ...)` JSON 응답으로 변환한다.
- `GET /auth/users`: HUP-13 개발 중 사용자 저장 여부를 확인하기 위한 임시 조회 API다. 운영 전에는 관리자 전용으로 보호하거나 제거한다.

DB session 관리:

- 현재 회원가입은 repository 안에서 `AsyncSessionLocal`을 직접 열고 닫는다.
- `DbSession` dependency는 SQLAlchemy 필수 요소가 아니라 FastAPI 요청 단위 session 주입 도구다.
- 하나의 요청에서 여러 repository 작업을 같은 transaction으로 묶어야 할 때 `DbSession` 또는 explicit transaction boundary 도입을 검토한다.
- `DbSession`을 쓰더라도 `commit`, `rollback`, `refresh`는 자동이 아니며 service 또는 repository에서 명시한다.

## DB Migration

DB schema 변경은 Alembic revision으로 관리한다. Docker init SQL은 PostgreSQL 확장 설치처럼 초기 인프라에 필요한 작업에만 사용하고, 애플리케이션 테이블 변경은 migration으로 남긴다.

원칙:

- migration 설정은 `apps/api/app/db/migrations` 아래에 둔다.
- migration 실행 URL은 `alembic.ini`에 직접 하드코딩하지 않고 `app.core.config.settings.database_url`을 사용한다.
- 앱이 `postgresql+asyncpg` URL을 사용하므로 Alembic env도 async engine으로 실행한다.
- autogenerate가 모델을 감지할 수 있도록 migration env에서 모델 모듈을 import한다.
- 생성된 revision 파일은 적용 전에 사람이 검토한다.

루트 명령:

```bash
pnpm db:revision -- -m "create users table"
pnpm db:migration
```

API 패키지 명령:

```bash
pnpm --filter @huposit/api db:revision -- -m "create users table"
pnpm --filter @huposit/api db:migration
```

## API 계약과 OpenAPI

FastAPI는 OpenAPI 스펙을 자동 생성한다. 휴포짓은 이 장점을 적극 활용한다.

원칙:

- 프론트와 백엔드의 DTO 동기화 기준은 `/openapi.json`이다.
- 모노레포 검증과 타입 생성에는 서버를 띄우지 않고 `app.openapi()`에서 생성한 `generated/openapi.json`을 사용한다.
- API 응답 모델은 Pydantic schema로 명시한다.
- 공개 endpoint는 필요하면 안정적인 `operation_id`를 명시해 생성 타입과 future client 이름이 흔들리지 않게 한다.
- schema 이름은 프론트 도메인 용어와 맞춘다.
- 생성된 프론트 타입은 사람이 직접 수정하지 않는다.
- breaking change는 `docs/frontend.md`와 `docs/backend.md`에 반영한다.

후보 도구:

- `openapi-typescript`
- `openapi-fetch`
- `orval`

권장 순서:

1. API가 안정되기 전에는 수동 fetch 래퍼로 시작한다.
2. OpenAPI 타입은 `openapi-typescript`로 생성해 수동 타입 선언을 줄인다.
3. 타입 생성이 안정되면 API client 자동 생성을 검토한다.
4. 프론트에서 cache와 polling이 늘어나면 TanStack Query hooks 생성을 검토한다.

초기 API 경계:

```txt
GET    /health
GET    /health/db
GET    /health/worker

POST   /auth/signup
GET    /auth/users  # HUP-13 개발 검증용. 운영 전 보호 또는 제거
POST   /auth/login
POST   /auth/logout
GET    /auth/me
POST   /auth/verify-email
POST   /auth/resend-verification-email

POST   /source-files
GET    /source-files
GET    /source-files/{source_file_id}

POST   /processing-jobs
GET    /processing-jobs
GET    /processing-jobs/{job_id}

GET    /decks
GET    /decks/{deck_id}
GET    /decks/{deck_id}/slides
GET    /decks/{deck_id}/slides/{slide_id}

GET    /search
```

파일 업로드 API는 실제 저장 전략을 정한 뒤 세부 설계를 확정한다.

## 자체 로그인 방향

외부 Auth 서비스에는 의존하지 않는다. 단, 인증 보안 기능을 직접 발명하지 않고, 검증된 라이브러리와 OWASP 기준을 따른다. 초기 인증은 단일 사용자 소유 모델에 필요한 최소 범위로 제한한다.

이 방향의 목적은 인증 데이터와 사용자 소유 모델을 휴포짓 안에서 제어하는 것이다. 자체 로그인은 암호 알고리즘, session token, cookie 보안, CSRF 방어를 직접 고안한다는 뜻이 아니다. 보안이 필요한 부분은 표준 라이브러리, 프레임워크 기능, OWASP 권장사항을 기준으로 선택하고, 선택 근거를 인증 설계 티켓에 남긴다.

외부 managed Auth provider는 초기 방향에서 제외한다. 인증 라이브러리는 외부 서비스가 아니므로 별도 설계 티켓에서 후보를 비교할 수 있다.

최소 보안 기준:

- 비밀번호는 평문 저장 금지
- 비밀번호 hash는 Argon2id 또는 bcrypt 계열 사용
- 세션은 HttpOnly, Secure, SameSite cookie 기반을 우선 검토
- CSRF 방어 정책을 명시
- 로그인 실패 rate limit
- password reset token은 단기 만료와 1회성 사용
- 세션 rotation과 logout 무효화
- user id는 UUID 사용
- 인증 이벤트는 audit log 후보로 남긴다.

초기 MVP 인증 정책:

- 이메일/비밀번호 회원가입과 로그인
- `email`은 유니크한 로그인 식별자로 사용
- `username`은 초기 범위에서 제외
- `email_verified`로 이메일 인증 상태를 저장
- 비밀번호 hash는 Argon2id 사용
- 세션은 DB-backed session으로 관리
- 브라우저 세션 전달은 HttpOnly, Secure, SameSite=Lax cookie를 사용
- 이메일 인증 메일은 Mailgun을 사용하고 발신자는 `Huposit <info@huposit.kr>`로 시작

초기 MVP 인증 API 범위:

- 이메일/비밀번호 회원가입
- 로그인
- 로그아웃
- 현재 사용자 조회
- 이메일 인증
- 이메일 인증 메일 재발송
- 비밀번호 변경 또는 재설정은 별도 티켓

초기에는 organization/team 기능을 만들지 않는다. 모든 데이터는 단일 `user_id` 소유 모델에서 시작한다.

HUP-13에서 구현된 현재 범위:

- `POST /auth/signup`
- `GET /auth/users` 개발 검증용 조회
- email unique users table
- `email_verified=false` 기본 생성
- Argon2id password hash
- `DuplicateEmailError`와 공통 exception handler 기반 중복 email 응답
- 서버 실행 없이 OpenAPI 생성 후 web generated type 갱신

현재 회원가입 응답 계약:

```json
{
  "status": "success",
  "email": "user@example.com",
  "email_verified": false,
  "message": "User created successfully"
}
```

- `SignupResponse.status`는 `"success" | "error"`를 사용한다.
- 성공 응답은 router에서 `SignupResponse`로 조립한다.
- 중복 이메일 같은 예상 가능한 도메인 실패는 `DuplicateEmailError`를 raise하고 `core/errors.py`에서 `SignupResponse(status="error", ...)`로 변환한다.
- 비밀번호는 Argon2id hash로 저장하고 평문 password는 저장하거나 로그로 남기지 않는다.
- email은 저장 전에 `strip().lower()`로 정규화한다.

HUP-14 로그인 구현 전 기준:

- `POST /auth/login`은 HUP-13에서 생성한 email/password 계정으로 access token을 발급하는 MVP endpoint다.
- 로그인 입력은 `email`, `password`로 시작하며, email은 회원가입과 같은 방식으로 `strip().lower()` 정규화 후 조회한다.
- 존재하지 않는 email과 잘못된 password는 같은 인증 실패 응답으로 처리해 사용자 존재 여부를 노출하지 않는다.
- password 검증은 HUP-13의 Argon2id hash helper를 재사용하거나 같은 `core/security.py` 경계 안에 둔다.
- access token 생성은 route 내부에 길게 두지 않고 auth service 또는 token helper로 분리한다.
- 로그인 성공 응답은 refresh token을 당장 포함하지 않고 `access_token`, `token_type`, `expires_in` 형태로 둔다.
- refresh token, token rotation, DB-backed long-lived session, logout/session revoke는 HUP-14 범위 밖이며 후속 티켓에서 정책을 확정한다.
- 다만 HUP-14의 token 발급 함수와 response schema는 후속 refresh token 티켓에서 재사용하기 어렵지 않은 구조로 둔다.
- API 계약이 바뀌므로 구현 후 `pnpm openapi:generate`로 OpenAPI와 web generated type을 갱신한다.

미인증 사용자 정책:

- `email_verified=false` 상태에서도 로그인은 허용할 수 있다.
- 앱 화면에서는 이메일 인증 필요 상태를 명확히 보여준다.
- 파일 업로드와 개인 데이터 생성 같은 주요 기능은 서버에서 `email_verified=true`를 요구한다.
- 일정 기간 동안 인증되지 않았고 개인 데이터가 없는 계정은 정리 대상이 될 수 있다.

주의:

- 인증 구현은 반드시 별도 티켓으로 분리한다.
- 인증 티켓은 테스트를 포함해야 한다.
- 보안 기능은 직접 구현하지 않는다. hash, token, cookie 처리에는 검증된 라이브러리를 사용한다.
- OWASP 기준과 다르게 구현해야 하는 경우에는 설계 티켓에 이유와 보완책을 남긴다.

## 데이터 모델 방향

초기 테이블 후보:

```txt
users
sessions

source_files
processing_jobs

decks
slides
slide_blocks

collections
collection_items
tags
taggings
saved_searches
```

핵심 관계:

```txt
users 1 -- n source_files
source_files 1 -- n processing_jobs
source_files 1 -- 0..1 decks
decks 1 -- n slides
slides 1 -- n slide_blocks
users 1 -- n collections
users 1 -- n tags
users 1 -- n saved_searches
```

초기에는 `collections`, `tags`, `saved_searches`를 미리 구현하지 않아도 된다. 다만 모델 방향은 열어둔다.

권장 enum:

```txt
source_file_status:
  uploaded
  processing
  ready
  failed

processing_job_type:
  extract_deck
  embed_slide_blocks
  summarize_deck

processing_job_status:
  queued
  running
  succeeded
  failed
  canceled
```

상태 enum은 프론트 badge와 직접 연결된다. 상태 이름은 한 번 정하면 자주 바꾸지 않는다.

## 파일 저장 방향

초기 파일 저장은 벤더 종속을 줄이고 작은 서버에서 다룰 수 있게 시작한다.

가능한 선택:

- 로컬 디스크 저장
- PostgreSQL에는 파일 메타데이터와 경로만 저장
- 추후 S3 호환 object storage로 이동 가능하게 storage adapter 경계 유지

권장 원칙:

- DB에는 원본 파일 blob을 저장하지 않는다.
- 원본 파일 경로, MIME type, size, checksum, upload status를 저장한다.
- 파일명은 사용자 입력값을 그대로 경로로 쓰지 않는다.
- checksum으로 중복 업로드와 idempotency를 보조한다.
- 삭제 정책은 soft delete를 먼저 검토한다.

## worker와 job 처리

처리 작업은 `ProcessingJob` 중심으로 관리한다.

원칙:

- API는 job을 생성하고 빠르게 응답한다.
- worker는 queued job을 가져와 running으로 바꾸고 처리한다.
- worker는 같은 job을 두 번 처리해도 데이터가 깨지지 않게 idempotent하게 설계한다.
- 실패는 status와 error message로 기록한다.
- retry 횟수와 next_run_at을 둔다.
- 오래 걸리는 작업은 heartbeat 또는 locked_at을 둔다.

DB 기반 queue 초안:

```txt
processing_jobs
  id
  user_id
  source_file_id
  type
  status
  attempts
  max_attempts
  locked_by
  locked_at
  next_run_at
  started_at
  finished_at
  error_code
  error_message
  created_at
  updated_at
```

worker concurrency:

- 초기 기본값은 1
- 파일 추출과 임베딩 작업은 분리 가능하게 job type을 둔다.
- lock 만료 시간을 두어 worker crash 후 job이 영원히 running에 머물지 않게 한다.

## 동시성 원칙

동시성은 기능이 커진 뒤 고치기 어렵다. MVP부터 최소 규칙을 둔다.

원칙:

- mutation은 transaction 안에서 처리한다.
- job claim은 row lock 또는 advisory lock을 사용한다.
- 같은 파일 업로드/처리 요청은 idempotency key 또는 checksum으로 중복을 막는다.
- 상태 전이는 허용된 방향만 통과한다.
- retry는 같은 결과를 여러 번 insert하지 않도록 upsert 또는 unique constraint를 사용한다.
- worker는 job 단위로 commit boundary를 명확히 한다.

상태 전이 예:

```txt
queued -> running -> succeeded
queued -> running -> failed
failed -> queued
running -> queued  # lock timeout recovery
queued -> canceled
```

허용되지 않는 상태 전이는 service 계층에서 막는다.

## 검색과 pgvector

검색은 단계적으로 키운다.

1. 키워드 검색
2. slide/block 단위 검색
3. pgvector 기반 semantic search
4. hybrid search
5. saved search

초기 원칙:

- 임베딩은 `SlideBlock` 단위부터 검토한다.
- deck/slide/block 결과 타입을 API 응답에 명시한다.
- 검색 결과는 프론트의 `Search` 화면에서 같은 타입 이름을 사용한다.
- vector index는 데이터량을 보고 도입한다.
- embedding provider는 adapter로 감싸 벤더 교체 가능성을 남긴다.

## 벤더 종속 기준

벤더 종속을 줄이는 것이 목표지만 모든 것을 직접 구현하지 않는다.

직접 구현할 것:

- 도메인 service
- API endpoint
- job 상태 관리
- storage adapter 경계
- OpenAPI 기반 타입 생성 스크립트
- 사용자 소유 모델과 session 저장 schema

직접 구현하지 않을 것:

- password hashing 알고리즘
- JWT/signature crypto primitive
- CSRF token primitive
- SQL driver
- migration framework
- PPT parsing library
- vector distance function

검증된 라이브러리와 PostgreSQL 기능은 적극 사용한다. 벤더 종속을 피하려다 보안과 안정성을 잃으면 안 된다.

## 오류 처리와 응답 형식

API 오류 응답은 프론트가 일관되게 처리할 수 있어야 한다.

인증 MVP의 회원가입처럼 화면 상태와 직접 연결되는 endpoint는 response schema 안에서 `status`와 `message`를 반환할 수 있다. 이 경우 예상 가능한 도메인 실패는 feature 예외로 표현하고, `core/errors.py`의 FastAPI exception handler에서 response schema로 변환한다.

권장 형식:

```json
{
  "error": {
    "code": "source_file_not_found",
    "message": "Source file not found",
    "details": {}
  }
}
```

원칙:

- 사용자가 이해해야 할 message와 내부 error를 분리한다.
- validation error는 FastAPI 기본 형식을 그대로 쓸지 별도 adapter를 둘지 결정한다.
- error code는 문서화한다.
- job 실패 error는 API error와 별도로 job row에 저장한다.

## 설정과 환경 변수

설정은 `pydantic-settings`를 계속 사용한다.

초기 후보:

```txt
DATABASE_URL
APP_ENV
APP_SECRET_KEY
SESSION_COOKIE_NAME
SESSION_COOKIE_SECURE
STORAGE_ROOT
WORKER_ID
WORKER_CONCURRENCY
JOB_LOCK_TIMEOUT_SECONDS
```

원칙:

- `.env`는 로컬 개발용이다.
- secret은 git에 커밋하지 않는다.
- 운영 설정은 서버 환경 변수로 주입한다.
- 기본값은 개발 편의와 운영 안전을 구분한다.

## 마이그레이션 방향

현재 migration 도구는 아직 없다. 다음 구현 전 선택이 필요하다.

후보:

- Alembic
- SQL 파일 기반 수동 migration

권장:

- FastAPI + SQLAlchemy를 유지한다면 Alembic을 우선 검토한다.
- migration은 리뷰 가능한 작은 파일로 유지한다.
- schema 변경은 관련 API/프론트 타입 변경과 함께 PR에 설명한다.

이번 HUP-8에서는 migration을 만들지 않는다.

## 프론트/백엔드 문서 갱신 룰

실제 구현 티켓을 완료할 때마다 다음을 확인한다.

- 프론트 라우트, 화면 구조, UI 상태가 바뀌면 `docs/frontend.md` 갱신
- 백엔드 도메인 모델, API, 인증, job 처리, storage, 검색 방향이 바뀌면 `docs/backend.md` 갱신
- OpenAPI 응답 모델 이름이 바뀌면 두 문서의 도메인 용어 충돌 확인
- 후속 티켓 순서가 바뀌면 관련 문서의 후속 티켓 섹션 갱신
- 문서를 갱신하지 않는다면 PR 본문에 "방향 문서 변경 없음"을 명시

Codex는 프론트 또는 백엔드 구현 티켓을 시작할 때 `docs/workflow.md`, Linear issue, 관련 방향 문서를 읽어야 한다.

## 후속 구현 티켓 초안

아래 순서로 Linear issue를 분리하는 것을 권장한다.

### 1. 백엔드 폴더 구조 정리

Goal: FastAPI 앱의 도메인별 폴더 구조와 기본 계층을 만든다.

Scope:

- `api/routes`, `schemas`, `services`, `repositories`, `domain` 폴더 추가
- 기존 health endpoint 위치 정리
- 공통 error/config 구조 초안
- 동작 변경 최소화

Done when:

- `/health`, `/health/db`가 계속 동작한다
- `pnpm --filter @huposit/api typecheck` 통과
- `pnpm --filter @huposit/api test` 통과

### 2. migration 도구와 기본 DB 스키마 결정

Goal: PostgreSQL schema 변경을 리뷰 가능한 방식으로 관리한다.

Scope:

- Alembic 또는 SQL migration 방식 결정
- `users`, `source_files`, `processing_jobs` 초기 migration 작성
- 로컬 DB 적용 방법 문서화

Done when:

- 로컬 DB에 migration을 적용할 수 있다
- rollback 또는 재생성 방식이 문서화된다
- health/db 검증 통과

### 3. 자체 인증 모델과 세션 설계

Goal: 외부 Auth 서비스에 의존하지 않는 최소 로그인 모델을 확정한다.

Scope:

- OWASP 기준에 맞춘 인증 보안 원칙 정리
- 인증 라이브러리 후보 비교
- password hash 라이브러리 선택
- users/sessions schema 설계
- session cookie 정책 문서화
- rate limit, CSRF, password reset은 구현 여부를 분리

Done when:

- 인증 구현 전 설계 문서 또는 ADR이 남는다
- 보안 체크리스트가 티켓에 포함된다
- 외부 managed Auth provider를 쓰지 않는 이유와 라이브러리 선택 근거가 기록된다
- 구현 티켓이 2개 이상으로 분리된다

### 4. 로그인/로그아웃 MVP

Goal: HUP-13에서 만든 email/password 회원가입 기반 위에 자체 로그인 MVP를 구현한다.

Scope:

- 로그인
- 로그아웃
- 현재 사용자 조회
- 세션 cookie 설정
- 기본 테스트

Done when:

- 유효한 email/password로 로그인할 수 있다
- `/auth/me`가 로그인 상태를 반환한다
- logout 후 세션이 무효화된다
- 잘못된 로그인 시 안전한 오류가 반환된다
- 인증 테스트가 통과한다

### 5. SourceFile 업로드 메타데이터 API

Goal: 파일 업로드 전후의 메타데이터를 저장하고 조회한다.

Scope:

- source_files schema
- 파일 메타데이터 생성 API
- 목록/상세 조회 API
- user_id 소유권 검사
- 실제 파일 저장은 최소 또는 mock 가능

Done when:

- 프론트 Library/Uploads가 필요한 기본 필드를 받을 수 있다
- OpenAPI schema가 명확하다
- 테스트 통과

### 6. ProcessingJob DB queue MVP

Goal: worker가 처리할 수 있는 DB 기반 job queue를 만든다.

Scope:

- processing_jobs schema
- job 생성 API
- job 목록/상세 조회 API
- queued/running/succeeded/failed 상태 전이
- lock timeout 설계

Done when:

- API가 job을 생성한다
- worker가 claim할 수 있는 query가 있다
- 중복 claim 방지 테스트가 있다

### 7. worker job runner MVP

Goal: DB queue에서 job을 가져와 실행하는 worker 구조를 만든다.

Scope:

- worker config
- job polling loop
- lock/heartbeat/timeout 처리
- extract_deck handler placeholder
- 실패 기록

Done when:

- worker가 queued job을 running으로 바꾸고 완료/실패 처리한다
- worker crash 후 회복 기준이 문서화된다
- 테스트 또는 수동 검증 방법이 있다

### 8. PPTX 추출 파이프라인 MVP

Goal: PPTX 파일에서 Deck, Slide, SlideBlock을 생성한다.

Scope:

- python-pptx 기반 추출 service
- deck/slides/slide_blocks schema
- source_file -> deck 관계
- 텍스트 block 우선 추출
- 이미지/표/도형은 후속 확장 가능하게 구조만 열어둔다

Done when:

- 샘플 PPTX로 deck/slides/slide_blocks가 생성된다
- 실패 시 job이 failed로 기록된다
- 긴 텍스트와 빈 슬라이드를 처리한다

### 9. OpenAPI 타입 생성 흐름 확장

Goal: HUP-12에서 시작한 OpenAPI 기반 타입 생성 흐름을 health 외 API로 확장한다.

Scope:

- 신규 API response model에 안정적인 schema 이름과 `operation_id`를 부여한다.
- `pnpm openapi:generate`로 `generated/openapi.json`과 web 타입을 갱신한다.
- health 외 도메인 API 타입을 생성 타입 기반으로 교체한다.
- API client 자동 생성이 필요한지 별도 검토한다.

Done when:

- health 외 신규 API 타입이 생성 타입 기반으로 import된다
- 생성 파일 변경이 PR에서 확인 가능하다
- `pnpm openapi:generate`와 루트 검증 명령이 통과한다

### 10. 검색 API 1차

Goal: Deck, Slide, SlideBlock을 키워드로 검색할 수 있게 한다.

Scope:

- keyword search endpoint
- 결과 타입 구분
- pagination
- user_id 소유권 검사
- pgvector semantic search는 제외

Done when:

- `/search`가 deck/slide/block 결과를 반환한다
- 프론트 검색 화면과 DTO가 맞다
- 테스트 통과

### 11. pgvector 기반 semantic search

Goal: SlideBlock 단위 semantic search를 추가한다.

Scope:

- embedding 저장 컬럼
- embedding 생성 job
- vector index 검토
- provider adapter
- hybrid search는 후속 가능

Done when:

- slide block embedding이 저장된다
- semantic search 결과가 반환된다
- provider 교체 지점이 service로 분리된다

## 보류할 것

다음은 아직 도입하지 않는다.

- Redis/Celery 기반 queue
- S3 전용 저장 구조
- organization/team 권한 모델
- 결제/구독
- 외부 Auth provider
- multi-region 또는 horizontal scaling
- 복잡한 이벤트 소싱 구조
- 독자 암호화 알고리즘

필요해질 때 작은 티켓으로 도입한다.

## 검증 기준

백엔드 구현 티켓은 기본적으로 다음을 검증한다.

- `pnpm --filter @huposit/api typecheck`
- `pnpm --filter @huposit/api test`
- `pnpm --filter @huposit/api lint`
- worker 변경 시 `pnpm --filter @huposit/worker typecheck`
- worker 변경 시 `pnpm --filter @huposit/worker test`
- API 변경 시 `/openapi.json` 확인
- 프론트 계약에 영향이 있으면 `docs/frontend.md`와 `docs/backend.md` 동시 확인

문서만 변경하는 티켓은 링크, 오탈자, 범위 준수 여부를 확인한다.
