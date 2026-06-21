# Workflow

ver. 1.0.0_26.06.20

이 문서는 Huposit 프로젝트에서 Linear, Codex, GitHub PR을 사용해 작업을 시작하고 merge 후 정리하는 기본 규칙을 정의한다.

## 1. 기본 원칙

- 모든 작업은 Linear issue에서 시작한다.
- 하나의 Linear issue는 하나의 작업 브랜치와 하나의 PR을 기본 단위로 한다.
- GitHub PR은 코드 변경, 리뷰, 검증 결과를 남기는 공간으로 사용한다.
- Linear는 작업 목적, 범위, 완료 기준, 진행 상태를 관리하는 공간으로 사용한다.
- Codex는 issue 검토, 구현 절차 안내, 코드 작성, 검증 보조에 사용하되 최종 책임은 작업자와 리뷰어가 가진다.

## 2. 작업 시작

작업을 시작하기 전 `main` branch의 최신 상태를 확인한다.

```bash
git switch main
git fetch origin
git pull --ff-only
```

Linear issue 초안에는 다음 항목을 포함한다.

```md
# Goal

작업의 목적을 작성한다.

# Scope

이번 issue에서 변경할 범위를 작성한다.

# Done when

완료 여부를 검증할 수 있는 조건을 작성한다.
```

검토가 아직 끝나지 않은 issue는 Linear 상태를 `Backlog`에 둔다.

작업 전에는 Codex에게 Linear issue를 읽고 다음 항목을 검토하게 한다.

- Goal이 명확한지
- Scope가 너무 크거나 모호하지 않은지
- Done when이 실행 가능한 검증 기준인지
- 다음 issue로 분리해야 할 항목이 있는지

작업 범위와 완료 기준이 명확해지면 Linear 상태를 `Todo`로 변경한다.

## 3. Branch 규칙

`Todo` 상태의 issue를 작업할 때는 `main`에서 새 브랜치를 만든다.

브랜치 이름 형식:

```txt
hup-00/short-english-description
```

예:

```bash
git switch -c hup-6/document-workflow
```

브랜치를 만든 뒤 Linear 상태를 `In Progress`로 변경한다.

브랜치를 만든 후 Codex에게 해당 Linear issue를 기준으로 구현 절차를 안내받거나 구현을 요청할 수 있다.

## 4. Commit 규칙

작업이 길어질 경우 사람이 검토 가능한 작은 단위의 커밋으로 나눈다.

커밋 메시지는 한글로 작성한다. 형식:

```txt
HUP-00 type: 한글 작업 요약
```

예:

```txt
HUP-6 docs: 작업 흐름 문서화
HUP-5 feat: FastAPI DB 연결 설정
HUP-4 feat: PostgreSQL pgvector compose 구성
```

자주 사용하는 type:

```txt
feat   기능 추가
fix    버그 수정
docs   문서 변경
chore  설정, 의존성, 기타 유지보수
refactor  동작 변경 없는 구조 개선
test   테스트 추가 또는 수정
```

커밋의 작업 요약은 한글로 작성한다. 커밋 후에는 필요한 경우 Linear issue에 변경사항을 짧게 남긴다. 작업이 길어질 때는 중간 커밋을 만들고 필요 시 원격에 push해 작업을 보존한다.

## 5. Codex 활용 규칙

Codex에게 작업을 맡기거나 안내를 받을 때는 다음 흐름을 기본으로 한다.

- 작업 전 Linear issue 내용을 읽게 한다.
- 구현 전 현재 branch와 `git status`를 확인하게 한다.
- 기존 코드 구조와 파일 위치를 먼저 확인하게 한다.
- 구현 후 Done when 기준에 맞는 검증 명령을 실행하게 한다.
- 검증 명령의 세부 기준은 `docs/testflow.md`를 따른다.
- 검증 결과와 남은 리스크를 PR 본문에 반영하게 한다.

Codex가 작성한 코드는 작업자가 직접 읽고 이해한 뒤 PR을 올린다.

Codex는 사용자의 명시적 승인 없이 커밋하거나 push하지 않는다. 구현만 요청받은 경우에는 검증 후 추천 커밋/푸시 명령을 보고하고 멈춘다.

## 6. PR 규칙

Done when 기준을 모두 만족하는지 확인한 뒤 작업 브랜치를 원격에 push한다.

```bash
git push -u origin hup-00/short-english-description
```

PR 제목에는 Linear issue ID를 포함한다.

```txt
HUP-00 type: 작업 요약
```

PR 본문에는 다음 항목을 포함한다.

```md
## 요약

- 주요 변경사항을 짧게 작성한다.

## Linear

Fixes HUP-00

## 확인

- 실행한 검증 명령 또는 확인 결과를 작성한다.
```

실행할 검증 명령은 Linear issue의 `Done when`과 `docs/testflow.md`를 기준으로 고른다.

PR을 올린 뒤에는 GitHub PR conversation에 Linear bot이 issue 링크를 남겼는지 확인한다. 연결이 확인되면 Linear 상태를 `In Review`로 변경한다.

다음 issue를 작업할 때는 반드시 `main`을 최신화하고 새 브랜치에서 시작한다.

## 7. PR Merge 규칙

기본 merge 방식은 `Squash and merge`를 사용한다.

merge 전에는 다음을 확인한다.

- 개발총괄 또는 리뷰어가 변경 의도를 이해할 수 있는 코드인지
- AI 도움을 받아 작성한 코드의 책임 범위와 구조가 적절한지
- Done when 기준을 만족했는지
- PR 본문에 검증 결과가 남아 있는지

코드 리뷰 댓글은 GitHub PR에 작성한다.

- 특정 코드 줄, 파일, 테스트, 동작에 대한 피드백은 GitHub PR review comment 또는 conversation에 남긴다.
- Linear에는 리뷰 상태, merge 가능 여부, 범위 변경, 후속 issue 후보 같은 작업 관리 요약만 남긴다.
- GitHub 리뷰 댓글을 반영한 뒤에는 실행한 검증 명령과 남은 리스크를 PR 또는 Linear에 짧게 남긴다.

## 8. Merge 후 정리

PR이 `main`에 merge되면 로컬 `main`을 최신화한다.

```bash
git switch main
git pull --ff-only
```

merge된 로컬 브랜치를 삭제한다.

```bash
git branch -d hup-00/short-english-description
```

Squash merge 때문에 Git이 완전히 merge된 브랜치로 인식하지 못하면, GitHub에서 merge 여부를 확인한 뒤 로컬 브랜치를 강제 삭제한다.

```bash
git branch -D hup-00/short-english-description
```

원격 브랜치는 GitHub의 `Delete branch` 버튼으로 삭제하거나 다음 명령으로 삭제한다.

```bash
git push origin --delete hup-00/short-english-description
```

Linear issue가 자동으로 `Done`이 되었는지 확인한다. 자동 변경이 되지 않으면 수동으로 `Done`으로 변경한다.
