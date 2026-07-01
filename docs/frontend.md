# Frontend Direction

ver. 0.1.0_26.06.21

이 문서는 HUP-7의 결과물이다. 휴포짓 프론트엔드를 백엔드와 본격 연결하기 전에, 개인 슬라이드/파일 관리 콘솔에 적합한 구현 방향과 후속 작업 순서를 정리한다.

## 결론

휴포짓의 프론트엔드는 초기에 파일 관리 시스템처럼 익숙해야 하지만, 장기적으로는 개인 맥락 저장소로 확장될 수 있어야 한다.

따라서 첫 방향은 다음과 같다.

- 구조: 콘솔형 앱 셸
- 시각 톤: 버건디를 핵심 브랜드 색으로 쓰되, 전체 화면은 조용한 뉴트럴 기반
- UI 구현: Tailwind CSS + shadcn/Radix 계열을 얇게 도입
- 데이터 표시: 리스트, 그리드, 디테일 패널을 함께 지원
- API 연결: FastAPI의 OpenAPI 스펙을 기준으로 타입과 클라이언트 생성을 검토
- 상태 관리: URL 상태, React Router 데이터 API, 필요한 경우 TanStack Query를 단계적으로 사용
- 확장 방향: 파일 관리에서 문서, 슬라이드, 검색, 태그, 컬렉션, 저장 검색으로 확장

초기 화면은 마케팅 사이트가 아니라 작업 콘솔이어야 한다. 사용자는 첫 화면에서 파일을 올리고, 처리 상태를 확인하고, 슬라이드 단위 결과를 탐색할 수 있어야 한다.

## 참고한 패턴

### Supabase

주요 참고 대상은 `supabase/supabase` 모노레포다.

- `apps/studio`: 실제 운영 콘솔. 사이드바, 테이블, SQL editor, API docs, 설정 화면처럼 밀도 있는 작업 UI를 참고한다.
- `packages/ui`: Supabase 공용 React UI 컴포넌트. Radix UI, shadcn/ui, Tailwind CSS 기반이다.
- `packages/ui-patterns`: `CommandMenu`, `FilterBar`, `PageHeader`, `PageContainer`, `EmptyState`, `Table`, `CodeBlock` 같은 복합 패턴을 참고한다.
- `apps/design-system`: 컴포넌트 문서화와 디자인 시스템 운영 방식을 참고한다.
- `apps/docs`: 문서, 검색, MDX, 레퍼런스 화면이 필요해질 때 참고한다.

Supabase에서 직접 가져올 핵심은 다음이다.

- Tailwind만으로 스타일링하고 하드코딩 색상보다 semantic token을 사용한다.
- 기본 컴포넌트와 복합 UI 패턴을 분리한다.
- 화면을 업무 단위 interface로 쪼갠다.
- 관리 콘솔에서는 넓은 hero보다 조밀한 정보 배치와 빠른 작업 흐름을 우선한다.

### Supaplate

로컬 참고 프로젝트인 `supaplate-master`에서는 다음을 참고한다.

- `core`와 `features` 분리
- React Router의 명시적 라우트 구성
- shadcn 스타일 컴포넌트 구성
- 폼 상태, 에러, 성공 메시지, 제출 버튼 패턴

다만 Supaplate의 인증, 결제, i18n, 이메일, Supabase 의존성은 휴포짓 MVP 범위에는 과하다. 구조와 UI 패턴만 참고한다.

### 파일 관리형 제품

휴포짓 초기 제품은 파일 관리 콘솔의 문법을 빌려야 한다.

참고할 일반 패턴은 다음이다.

- 좌측 탐색: Library, Uploads, Jobs, Search, Settings
- 중앙 작업 영역: 리스트, 그리드, 검색 결과, 슬라이드 썸네일
- 우측 디테일 패널: 선택한 파일/슬라이드의 메타데이터, 처리 상태, 추출 텍스트, 요약
- 상단 툴바: 업로드, 검색, 정렬, 필터, 보기 전환
- 빈 상태: 다음 행동이 분명한 업로드 유도
- 처리 상태: queued, processing, completed, failed를 일관되게 표시

완성형 파일 매니저 컴포넌트를 통째로 도입하지는 않는다. 휴포짓은 일반 파일 시스템보다 슬라이드, 추출 블록, 검색 문맥, AI 요약이 중요하므로 직접 조립하는 편이 낫다.

## 제품 모델

초기 프론트는 백엔드 도메인과 같은 말을 써야 한다. 화면 용어와 데이터 용어가 어긋나면 이후 API 연결이 어려워진다.

권장 도메인 용어는 다음과 같다.

- `SourceFile`: 사용자가 업로드한 원본 파일
- `Deck`: 하나의 발표 자료 또는 슬라이드 묶음
- `Slide`: 슬라이드 한 장
- `SlideBlock`: 슬라이드에서 추출된 텍스트, 이미지, 표, 도형 등의 구조화 단위
- `ProcessingJob`: 파일 추출, 변환, 임베딩, 요약 같은 비동기 작업
- `Collection`: 사용자가 자료를 묶는 컬렉션
- `Tag`: 자유롭게 붙이는 태그
- `SavedSearch`: 재사용 가능한 검색 조건

초기에는 폴더처럼 보이는 UI가 필요하지만, 내부 모델은 폴더에만 묶이면 안 된다. 개인 맥락 저장소는 폴더, 태그, 컬렉션, 저장 검색이 함께 필요하다.

## 정보 구조

초기 네비게이션은 다음 구조를 권장한다.

```txt
Library
Uploads
Jobs
Search
Settings
```

라우트 초안은 다음과 같다.

```txt
/library
/library/:itemId
/uploads
/jobs
/decks/:deckId
/decks/:deckId/slides/:slideId
/search
/settings
```

초기 화면별 역할은 다음과 같다.

- `Library`: 업로드된 자료와 추출 결과의 기본 목록
- `Uploads`: 파일 업로드와 최근 업로드 상태
- `Jobs`: 추출, 변환, 임베딩 작업의 진행 상태
- `Deck`: 슬라이드 썸네일 그리드와 자료 단위 메타데이터
- `Slide`: 슬라이드 미리보기, 추출 텍스트, 구조화 블록
- `Search`: 자연어/키워드 검색과 결과 필터
- `Settings`: 로컬 설정, API 연결 상태, 추후 계정 설정

## 앱 셸

권장 레이아웃은 콘솔 앱 셸이다.

```txt
+----------------+-------------------------------+---------------------+
| Sidebar        | Top toolbar                    | Detail panel        |
|                +-------------------------------+                     |
| Library        | Main content                   | Selected metadata   |
| Uploads        |                               | Processing status   |
| Jobs           | List / Grid / Slide preview    | Extracted text      |
| Search         |                               | AI summary          |
| Settings       |                               |                     |
+----------------+-------------------------------+---------------------+
```

구현 원칙은 다음과 같다.

- 데스크톱에서는 좌측 사이드바와 우측 디테일 패널을 적극 활용한다.
- 모바일에서는 사이드바와 디테일 패널을 sheet/drawer로 접는다.
- 중앙 영역은 리스트와 그리드 보기 전환을 지원한다.
- 검색, 필터, 정렬, 보기 전환은 상단 툴바에 둔다.
- 파일/슬라이드 선택 상태는 URL 또는 명확한 라우트로 표현한다.

## 시각 테마

전체 테마는 버건디 계열을 브랜드 중심 색으로 사용한다. 다만 화면 전체가 버건디로 뒤덮이면 작업 도구로서 피로도가 커진다. 버건디는 primary action, 선택 상태, 브랜드 강조, 중요 배지에 제한적으로 사용하고, 배경과 표면은 뉴트럴 계열로 둔다.

권장 톤은 다음과 같다.

- 브랜드: 깊은 버건디
- 배경: 거의 흰색에 가까운 저채도 뉴트럴
- 텍스트: 차분한 ink/charcoal
- 보조 영역: cool gray 또는 low-chroma neutral
- 성공/정보 상태: 버건디와 구분되는 muted green, muted blue
- 경고/오류 상태: amber, red를 의미에 맞게 사용

초기 토큰 초안:

```css
:root {
  --background: oklch(0.985 0.004 20);
  --foreground: oklch(0.17 0.012 250);
  --surface: oklch(0.972 0.005 20);
  --surface-foreground: var(--foreground);
  --muted: oklch(0.94 0.006 250);
  --muted-foreground: oklch(0.46 0.016 250);
  --border: oklch(0.88 0.006 250);
  --input: oklch(0.9 0.006 250);
  --ring: oklch(0.48 0.13 18);

  --primary: oklch(0.42 0.15 18);
  --primary-foreground: oklch(0.99 0.006 20);
  --primary-hover: oklch(0.36 0.14 18);

  --secondary: oklch(0.92 0.018 250);
  --secondary-foreground: oklch(0.22 0.014 250);
  --accent: oklch(0.93 0.035 18);
  --accent-foreground: oklch(0.3 0.11 18);

  --success: oklch(0.45 0.11 150);
  --warning: oklch(0.63 0.12 75);
  --destructive: oklch(0.55 0.18 25);

  --radius: 0.5rem;
}
```

이 값은 구현 티켓에서 실제 화면에 적용하며 조정한다. 원칙은 색상 자체보다 semantic token 이름을 유지하는 것이다.

## UI 컴포넌트 방향

휴포짓은 Tailwind CSS를 계속 사용한다. 이미 `apps/web`에 Tailwind 4 기반 설정이 있으므로 새 스타일 시스템을 추가할 이유가 없다.

shadcn/Radix는 부분 도입한다. shadcn은 패키지를 통째로 쓰는 방식이 아니라 필요한 컴포넌트 코드를 프로젝트 안에 가져오는 방식이므로 MVP에 맞게 얇게 시작할 수 있다.

초기 도입 후보:

- `Button`
- `Input`
- `Label`
- `Badge`
- `Card`
- `Alert`
- `Skeleton`
- `Tabs`
- `DropdownMenu`
- `Dialog`
- `Sheet`
- `Progress`

나중에 도입할 후보:

- `Table`
- `Command`
- `Tooltip`
- `Popover`
- `Resizable`
- `Sidebar`
- `Select`

컴포넌트 도입 원칙:

- 필요한 컴포넌트만 추가한다.
- shadcn 원본을 그대로 가져온 뒤 휴포짓 토큰에 맞게 최소 수정한다.
- UI 컴포넌트는 비즈니스 도메인을 모르게 한다.
- 도메인 화면은 `features/*` 안에서 조립한다.
- 복잡한 컴포넌트는 `core/components/ui`보다 `core/components/console` 또는 `features/*/components`에 둔다.

## 프론트 폴더 구조

React Router 앱 안에서 다음 구조를 권장한다.

```txt
apps/web/app/
  core/
    components/
      ui/
      console/
    hooks/
    lib/
    styles/
  features/
    library/
      components/
      screens/
      types.ts
    uploads/
      components/
      screens/
      types.ts
    jobs/
      components/
      screens/
      types.ts
    decks/
      components/
      screens/
      types.ts
    slides/
      components/
      screens/
      types.ts
    search/
      components/
      screens/
      types.ts
    settings/
      components/
      screens/
      types.ts
  routes.ts
  root.tsx
  app.css
```

역할 구분:

- `core/components/ui`: Button, Input, Badge 같은 원자적 UI
- `core/components/console`: AppShell, Sidebar, Toolbar, DetailPanel 같은 콘솔 공통 구조
- `core/lib`: `cn`, API 클라이언트 초기화, 날짜/파일 크기 포맷터
- `features/*/screens`: 라우트에 직접 연결되는 화면
- `features/*/components`: 특정 도메인에 묶인 컴포넌트
- `features/*/types.ts`: 프론트에서 쓰는 도메인 타입

Supabase Studio의 `components/layouts`, `components/interfaces`, `components/ui` 구분은 참고하되, 휴포짓은 React Router와 feature-first 구조에 맞게 조정한다.

## 라우팅 방향

라우트는 `apps/web/app/routes.ts`에서 명시적으로 관리한다. Supaplate의 라우트 선언 방식처럼 URL 구조와 화면 파일이 한눈에 보이도록 유지한다.

예상 구조:

```ts
export default [
  layout("core/components/console/app-shell.tsx", [
    index("features/library/screens/library.tsx"),
    route("/library", "features/library/screens/library.tsx"),
    route("/library/:itemId", "features/library/screens/item.tsx"),
    route("/uploads", "features/uploads/screens/uploads.tsx"),
    route("/jobs", "features/jobs/screens/jobs.tsx"),
    route("/decks/:deckId", "features/decks/screens/deck.tsx"),
    route(
      "/decks/:deckId/slides/:slideId",
      "features/slides/screens/slide.tsx",
    ),
    route("/search", "features/search/screens/search.tsx"),
    route("/settings", "features/settings/screens/settings.tsx"),
  ]),
];
```

실제 구현 티켓에서는 React Router 버전과 타입 생성 결과에 맞춰 조정한다.

## API 연결 방향

백엔드는 FastAPI이므로 OpenAPI 스펙을 자연스럽게 얻을 수 있다. 프론트에서는 다음 방향을 따른다.

1. 서버를 띄우지 않고 생성한 `generated/openapi.json`을 기준으로 TypeScript 타입을 생성한다.
2. 생성된 타입을 기반으로 feature별 API 응답 타입을 정의한다.
3. 파일 업로드, 처리 상태, 검색 API는 프론트 도메인별 hooks에서 감싼다.
4. 생성 코드는 사람이 직접 수정하지 않는다.

후보 도구:

- `openapi-typescript`
- `openapi-fetch`
- `orval`

초기에는 API가 자주 바뀔 수 있으므로, 바로 복잡한 SDK 구조를 만들기보다 다음 순서가 좋다.

- 1단계: 수동 fetch 래퍼
- 2단계: OpenAPI 타입 생성
- 3단계: 필요할 때 OpenAPI 기반 클라이언트 생성
- 4단계: React Query hooks 자동/반자동 생성 검토

현재 기본 위치:

- API client: `apps/web/app/core/api/client.ts`
- OpenAPI generated types: `apps/web/app/core/api/openapi-types.ts`
- OpenAPI type helpers: `apps/web/app/core/api/openapi-helpers.ts`
- Feature API wrapper 예시: `apps/web/app/features/auth/api.ts`
- Feature OpenAPI type alias 예시: `apps/web/app/features/auth/type.ts`

현재 HUP-13 회원가입 연결 패턴:

- `SignupRequest`, `SignupResponse`, `UsersInfoResponse`는 OpenAPI generated type에서 추출한다.
- `postSignupRequest()`는 `postApi<SignupResponse, SignupRequest>()`를 사용한다.
- `getUsersInfo()`는 `getApi<UsersInfoResponse>()`를 사용한다.
- generated type을 화면에서 직접 깊게 참조하지 않고 feature type/API 파일에서 한 번 감싼다.

HUP-14 로그인 연결 기준:

- 로그인 API 타입도 OpenAPI generated type에서 feature type alias로 추출한다.
- 로그인 요청 함수는 기존 `apps/web/app/features/auth/api.ts` 패턴을 이어받아 `postApi` 기반으로 얇게 감싼다.
- 최소 UI는 email/password 입력, 제출 버튼, 성공/실패 메시지, access token 수신 여부 확인까지만 담당한다.
- HUP-14에서는 token을 영구 저장하지 않는다. localStorage/sessionStorage 저장, 보호 라우트 전환, 자동 refresh, logout UX는 후속 티켓으로 둔다.
- 로그인 확인 UI는 기존 home route 또는 auth feature 안의 개발용 화면에 작게 붙이고, 장기 콘솔 앱 셸과 충돌하지 않게 유지한다.
- refresh token이 후속 티켓에서 확정될 수 있으므로, 화면은 응답의 `access_token`, `token_type`, `expires_in`을 확인하는 데 집중하고 session 모델을 먼저 고정하지 않는다.

## 데이터 패칭과 상태 관리

초기 원칙:

- 라우트 진입에 필요한 데이터는 React Router loader를 우선 검토한다.
- 폼 제출이나 route action에 맞는 작업은 React Router action을 사용한다.
- 처리 상태 polling, 검색 결과 cache, 백그라운드 갱신이 필요하면 TanStack Query를 도입한다.
- 검색어, 필터, 정렬, 보기 모드는 URL query parameter로 표현한다.
- 단순 UI 상태는 `useState`로 둔다.
- 전역 상태 라이브러리는 초기에 도입하지 않는다.

현재 HUP-13 회원가입 화면 패턴:

- home route `loader`에서 health 상태와 회원 목록을 함께 조회한다.
- home route `action`에서 회원가입 form submit을 처리한다.
- `SignupRequestPanel`은 React Router `fetcher.Form`을 사용한다.
- `fetcher.Form` submit 후 route loader가 재검증되면서 `GET /auth/users` 결과가 갱신된다.
- `UserCardList`는 가입된 사용자를 카드로 보여준다.
- 이 회원 목록 UI는 개발 중 DB 저장 여부를 눈으로 확인하기 위한 임시 검증 UI다. 운영 전에는 `/auth/users`를 보호하거나 제거한다.

HUP-14 로그인 화면 패턴:

- 로그인 확인 UI도 React Router `fetcher.Form` 또는 기존 home route action 패턴을 우선 사용한다.
- 로그인 성공 후에는 access token 원문 전체를 장기 저장하거나 여러 화면으로 전파하지 않고, 수신 여부와 만료 정보만 확인 가능한 UI로 제한한다.
- 인증 상태를 전역 store로 만들지 않는다. 보호 라우트, 현재 사용자 조회, token refresh가 필요해지는 시점에 별도 티켓에서 상태 모델을 정한다.
- 로그인 실패는 email 없음과 password 오류를 구분하지 않는 사용자 메시지로 보여준다.

도입 판단 기준:

- 같은 서버 상태를 여러 화면에서 반복해서 쓴다: TanStack Query 검토
- 긴 목록을 렌더링한다: TanStack Virtual 검토
- 복잡한 표/정렬/필터가 필요하다: TanStack Table 검토
- 사이드바 열림/닫힘 같은 UI 상태만 있다: 로컬 상태 유지

## 업로드 방향

MVP 업로드는 단순해야 한다.

1. 기본 파일 input 또는 작은 dropzone으로 시작한다.
2. 파일 형식, 크기, 중복 여부를 클라이언트에서 1차 검증한다.
3. 업로드 후 `ProcessingJob`을 생성하고 `/jobs` 또는 해당 파일 상세에서 상태를 보여준다.
4. 실패 시 재시도 가능한 상태를 제공한다.

큰 PPT 파일, 재개 가능한 업로드, 업로드 진행률이 중요해지는 시점에는 Uppy와 Tus를 검토한다. 이번 HUP-7에서는 의존성을 추가하지 않는다.

## 핵심 화면 패턴

### Library

목표: 사용자가 저장한 자료를 빠르게 찾고 열 수 있게 한다.

필요 요소:

- 리스트/그리드 전환
- 검색 입력
- 정렬: 최근 업로드, 최근 수정, 이름
- 필터: 처리 상태, 파일 유형, 태그
- 빈 상태: 첫 PPT 업로드 유도
- 우측 디테일 패널

### Uploads

목표: 파일을 넣고 처리 흐름에 들어가게 한다.

필요 요소:

- 드래그 앤 드롭 영역
- 허용 형식 안내
- 업로드 전 파일 목록
- 업로드 후 생성된 job 상태
- 실패 사유와 재시도 액션

### Jobs

목표: 비동기 처리 상태를 투명하게 보여준다.

필요 요소:

- 상태 배지: queued, processing, completed, failed
- 진행률 또는 단계 표시
- 대상 파일 링크
- 시작/완료 시간
- 실패 상세

### Deck

목표: 발표 자료 단위로 슬라이드를 훑을 수 있게 한다.

필요 요소:

- 슬라이드 썸네일 그리드
- 자료 메타데이터
- 전체 추출 상태
- 슬라이드 검색
- 추후 요약/태그/컬렉션 액션

### Slide

목표: 한 장의 슬라이드를 AI가 이해할 수 있는 구조로 확인한다.

필요 요소:

- 슬라이드 미리보기
- 추출 텍스트
- 구조화 블록 목록
- 이미지/표/도형 정보
- AI 요약 또는 관련 맥락
- 원본 deck으로 돌아가기

### Search

목표: 개인 맥락을 다시 꺼낼 수 있게 한다.

필요 요소:

- 키워드/자연어 검색
- 결과 타입: deck, slide, block
- 필터: 날짜, 태그, 컬렉션, 파일 유형
- 결과 미리보기
- 관련 슬라이드 열기
- 추후 저장 검색

## 접근성과 사용성

콘솔 UI는 반복 사용을 전제로 한다.

- 모든 주요 액션은 키보드 포커스가 보여야 한다.
- 아이콘 버튼은 tooltip 또는 accessible label을 가져야 한다.
- 색상만으로 상태를 구분하지 않는다.
- 긴 텍스트와 긴 파일명이 레이아웃을 깨지 않게 한다.
- 모바일에서는 보기 전환보다 핵심 흐름을 우선한다.
- 빈 상태, 로딩 상태, 실패 상태를 화면별로 준비한다.

## 후속 구현 티켓 초안

아래 순서로 Linear issue를 분리하는 것을 권장한다.

### HUP-11. 초기 랜딩 상태 체크 화면

Goal: 모노레포 개발환경 마무리 단계로, 프론트에서 API health, DB connection, worker 상태 체크 흐름을 확인한다.

이 티켓은 장기 콘솔 앱 셸을 완성하는 작업이 아니라, 프론트와 백엔드가 같은 개발환경에서 연결되는지 확인하는 임시 초기 화면이다. 이후 콘솔 앱 셸과 네비게이션이 들어오면 이 화면은 `Settings`의 API 연결 상태 영역이나 별도 개발 진단 화면으로 이동할 수 있다.

Scope:

- shadcn 스타일 `Button`, `Card`를 최소 범위로 추가한다.
- home route에서 간단한 휴포짓 소개 문구와 상태 체크 패널을 보여준다.
- React Router loader로 초기 상태를 조회한다.
- React Router `useRevalidator()`로 Health Check, DB Connection Check, Worker Check 버튼 요청을 처리한다.
- Worker Check는 실제 job queue 구현이 아니라 현재 worker 연결 확인에 필요한 최소 상태 응답으로 제한한다.
- 프론트 코드는 간결하고 읽기 쉽게 작성한다.

Non-goal:

- 네비게이션, 파일 업로드, 검색, 실제 processing job queue UI는 만들지 않는다.
- DB 데이터 삽입은 하지 않는다.
- React Router action 기반의 버튼별 독립 체크는 하지 않는다.
- 카드별 `useFetcher()` 또는 resource route 구현은 후속 티켓으로 분리한다.
- FastAPI `/openapi.json` 기반 TypeScript typegen과 장기 API client 생성 도구 비교는 하지 않는다.
- 한국시간 기준 체크 시간 표시는 후속 티켓으로 분리한다.
- 버건디 기반 semantic token 정리는 별도 UI 토큰 티켓에서 다룬다.

Done when:

- `pnpm dev` 실행 후 home 화면에서 3개 상태 체크가 가능하다.
- loader로 초기 상태가 표시된다.
- 버튼 클릭 시 현재 health loader가 다시 실행된다.
- `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`가 통과한다.

### HUP-13. email/password 회원가입 요청 화면

Goal: 자체 로그인 MVP의 첫 단계로 email + password 회원가입 요청을 프론트에서 보내고, 실제 생성된 회원을 화면에서 확인한다.

이 티켓은 장기 인증 UI 완성이 아니라 회원가입 API와 프론트 연결이 같은 OpenAPI 계약을 기준으로 동작하는지 확인하는 단계다.

Scope:

- home route action에서 `POST /auth/signup` 요청을 처리한다.
- 회원가입 form은 React Router `fetcher.Form`을 사용한다.
- API 요청/응답 타입은 OpenAPI generated type에서 feature type alias로 추출한다.
- home route loader에서 `GET /auth/users`를 조회한다.
- 가입된 회원 목록을 카드로 표시해 DB 저장 여부를 확인한다.

Non-goal:

- 로그인, 로그아웃, `/auth/me`
- session cookie 처리
- 이메일 인증 메일 발송
- 비밀번호 재설정
- 운영용 회원 관리 화면

Done when:

- email + password로 회원가입 요청을 보낼 수 있다.
- 성공/실패 메시지가 화면에 표시된다.
- 가입 후 회원 카드 목록에서 새 계정을 확인할 수 있다.
- `pnpm openapi:generate`, `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`가 통과한다.

### HUP-14. email/password 로그인 요청 화면

Goal: HUP-13에서 생성한 계정으로 로그인 요청을 보내고, 프론트에서 access token 발급 성공/실패를 간단히 확인한다.

이 티켓은 장기 인증 UI 완성이 아니라 로그인 API와 프론트 연결이 같은 OpenAPI 계약을 기준으로 동작하는지 확인하는 단계다. refresh token과 session UX는 후속 티켓에서 정책을 확정한다.

Scope:

- home route 또는 auth feature의 개발용 영역에서 `POST /auth/login` 요청을 처리한다.
- 로그인 form은 email/password 입력과 제출 버튼만 포함한다.
- API 요청/응답 타입은 OpenAPI generated type에서 feature type alias로 추출한다.
- 성공 시 access token 수신 여부, token type, 만료 시간을 확인할 수 있게 표시한다.
- 실패 시 사용자 존재 여부를 노출하지 않는 공통 인증 실패 메시지를 표시한다.

Non-goal:

- refresh token 저장 또는 rotation
- localStorage/sessionStorage 기반 장기 저장
- 보호 라우트 전환
- logout UX
- `/auth/me` 기반 전역 인증 상태

Done when:

- 올바른 email + password로 로그인 요청을 보낼 수 있다.
- 성공 시 access token 수신 여부가 화면에서 확인된다.
- 잘못된 email/password는 같은 실패 메시지로 표시된다.
- `pnpm openapi:generate`와 변경 범위에 맞는 API/Web 검증 명령이 통과한다.

### 1. 프론트 UI 토큰과 기본 컴포넌트 도입

Goal: 버건디 기반 UI 토큰과 최소 shadcn/Radix 컴포넌트 기반을 만든다.

Scope:

- `app.css`에 semantic token 추가
- `core/lib/utils.ts`에 `cn` 추가
- `Button`, `Input`, `Label`, `Badge`, `Card`, `Skeleton` 추가
- 기존 welcome 화면은 유지하거나 최소 수정

Done when:

- `pnpm --filter @huposit/web typecheck` 통과
- 기본 컴포넌트가 한 화면에서 import 가능

### 2. 콘솔 앱 셸과 기본 네비게이션 구현

Goal: 휴포짓의 첫 화면을 콘솔형 앱 셸로 전환한다.

Scope:

- `core/components/console` 추가
- Sidebar, TopToolbar, MainContent shell 구현
- `Library`, `Uploads`, `Jobs`, `Search`, `Settings` 네비게이션 추가
- 모바일에서는 사이드바를 접을 수 있게 구성

Done when:

- `/library`, `/uploads`, `/jobs`, `/search`, `/settings` 라우트가 보인다
- 현재 위치가 네비게이션에서 표시된다
- typecheck 통과

### 3. 업로드 화면 MVP

Goal: 사용자가 PPT 파일을 선택하고 업로드 요청을 시작할 수 있는 화면을 만든다.

Scope:

- `/uploads` 화면 구현
- 파일 선택 UI
- 허용 파일 형식/크기 안내
- 업로드 전 파일 목록
- API 연결 전 mock 상태 표시

Done when:

- PPT 파일 선택 시 목록에 표시된다
- 잘못된 파일 형식에 사용자 메시지가 나온다
- 실제 API 연결 코드는 아직 없다

### 4. 처리 작업 목록 화면

Goal: 파일 처리 상태를 볼 수 있는 `Jobs` 콘솔을 만든다.

Scope:

- `/jobs` 화면 구현
- queued, processing, completed, failed 상태 배지
- mock job list
- 실패 상태와 재시도 버튼의 UI만 구현

Done when:

- 상태별 표시가 구분된다
- 빈 상태와 로딩 상태가 있다
- typecheck 통과

### 5. Library 리스트/그리드 화면

Goal: 업로드된 자료를 파일 관리 시스템처럼 탐색할 수 있게 한다.

Scope:

- `/library` 화면 구현
- 리스트/그리드 보기 전환
- 검색 input, 정렬 select, 상태 filter UI
- 우측 디테일 패널 mock

Done when:

- 보기 전환이 작동한다
- 선택한 항목의 디테일 패널이 열린다
- mock 데이터 기반으로 화면이 깨지지 않는다

### 6. Deck/Slide 탐색 화면

Goal: PPT 자료를 슬라이드 단위로 탐색하는 화면을 만든다.

Scope:

- `/decks/:deckId` 화면 구현
- 슬라이드 썸네일 그리드
- `/decks/:deckId/slides/:slideId` 화면 구현
- 슬라이드 미리보기, 추출 텍스트, 구조화 블록 mock

Done when:

- deck에서 slide로 이동할 수 있다
- slide 화면에서 deck으로 돌아갈 수 있다
- 긴 추출 텍스트가 레이아웃을 깨지 않는다

### 7. OpenAPI 타입 생성 흐름 확장 및 API 클라이언트 검토

Goal: HUP-12에서 시작한 OpenAPI 타입 생성 흐름을 실제 도메인 API로 확장하고, API client 자동 생성 여부를 결정한다.

Scope:

- 신규 API 타입을 `openapi-typescript` 생성 타입 기반으로 연결한다.
- `core/api/client.ts`의 수동 fetch 래퍼가 충분한지 확인한다.
- 필요하면 `openapi-fetch` 또는 `orval` 도입 여부를 비교한다.
- 실제 화면 연결은 API별 구현 티켓에서 다룬다.

Done when:

- health 외 API 타입이 생성 타입 기반으로 연결된다
- API client 자동 생성 여부와 이유가 문서화된다
- 후속 API 연결 티켓이 분리된다

### 8. 백엔드 API와 업로드/작업 상태 연결

Goal: 업로드 화면과 jobs 화면을 실제 백엔드와 연결한다.

Scope:

- 업로드 API 연결
- job 생성/조회 API 연결
- polling 또는 server-sent events 검토
- 에러/재시도 처리

Done when:

- 실제 파일 업로드 후 job 상태가 표시된다
- 실패 응답이 사용자에게 표시된다
- 백엔드가 꺼져 있을 때도 앱이 깨지지 않는다

### 9. 검색 화면 API 연결

Goal: 개인 자료 검색의 첫 버전을 구현한다.

Scope:

- `/search` 화면을 실제 검색 API와 연결
- 검색어, 필터, 정렬을 URL query parameter에 반영
- 결과 타입별 표시
- 빈 결과와 오류 상태

Done when:

- 검색어 입력 후 결과가 표시된다
- URL을 공유해도 같은 검색 상태가 복원된다
- typecheck와 기본 검증 통과

## 보류할 것

다음은 아직 도입하지 않는다.

- 전체 디자인 시스템 앱
- Storybook 또는 별도 UI 문서 사이트
- 복잡한 전역 상태 라이브러리
- 완성형 파일 매니저 컴포넌트
- Uppy/Tus 기반 재개 가능 업로드
- Monaco editor, advanced command menu, 복잡한 data grid
- 인증, 결제, 팀/조직 관리 UI

필요해질 때 작은 티켓으로 도입한다.

## 참고 링크

- Supabase monorepo: <https://github.com/supabase/supabase>
- Supabase Studio: <https://github.com/supabase/supabase/tree/master/apps/studio>
- Supabase UI package: <https://github.com/supabase/supabase/tree/master/packages/ui>
- Supabase UI patterns package: <https://github.com/supabase/supabase/tree/master/packages/ui-patterns>
- Supabase Design System app: <https://github.com/supabase/supabase/tree/master/apps/design-system>
- React Router: <https://reactrouter.com>
- TanStack Query: <https://tanstack.com/query/latest>
- TanStack Table: <https://tanstack.com/table/latest>
- TanStack Virtual: <https://tanstack.com/virtual/latest>
- Uppy Tus upload: <https://uppy.io/docs/tus/>
- shadcn/ui: <https://ui.shadcn.com>
- Radix UI: <https://www.radix-ui.com>

## 검증 기준

프론트 구현 티켓은 기본적으로 다음을 검증한다.

- `pnpm --filter @huposit/web typecheck`
- 필요한 경우 `pnpm --filter @huposit/web build`
- 화면이 있는 변경은 데스크톱과 모바일 폭에서 직접 확인
- 텍스트가 버튼, 카드, 패널 밖으로 넘치지 않는지 확인
- 빈 상태, 로딩 상태, 실패 상태 확인
- API 연결 화면은 백엔드가 켜진 상태와 꺼진 상태를 모두 확인

문서만 변경하는 티켓은 링크, 오탈자, 범위 준수 여부를 확인한다.
