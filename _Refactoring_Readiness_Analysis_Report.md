# Refactoring Readiness Analysis Report

## 1) 문서 목적

- 본 문서는 `MagicSquare_18` 프로젝트에서 수행한 리팩토링 준비 분석과 실제 1회 리팩토링 실행 결과를 한 곳에 통합 기록한다.
- 범위: 코드 스멜 점검, ECB/SRP 분석, 리팩토링 계획, 안전망 테스트, 실제 변경 내역 및 검증 결과.

작성일: 2026-04-28

---

## 2) 점검 대상 및 전제

- 요청 기준 대상:
  - `src/magic_square/domain.py`
  - `src/magic_square/boundary.py`
  - `src/magic_square/gui/main_window.py`
- 실제 저장소 확인 결과:
  - `src/magic_square/gui/main_window.py`는 미존재
  - 대응 GUI 파일은 `src/magic_square/gui/app.py`
- 테스트 파일(`test_*.py`) 존재 확인:
  - `tests/domain/test_magic_square_domain_red.py`
  - `tests/boundary/test_magic_square_boundary_red.py`
  - `tests/entity/test_user.py`

---

## 3) 사전 분석 요약 (Code Smell / ECB / SRP)

### 3.1 Code Smell 주요 항목

| 파일명 | 줄/위치 | 스멜 종류 | 설명 | 우선순위 |
|---|---|---|---|---|
| `src/magic_square/boundary.py` | `solve(board)` | 미사용 파라미터 | `board`가 함수 본문에서 사용되지 않음(스텁 예외만 발생) | 중 |
| `src/magic_square/boundary.py` | `validate()` docstring | 문서상 매직 표현 | `4x4` 고정 표기(상수 변경 시 문서 불일치 가능성) | 하 |
| `src/magic_square/boundary.py` | `validate`, `solve` 명명 | 의미 모호성 | 모듈 밖 맥락에서 책임이 즉시 드러나지 않음 | 하 |

### 3.2 ECB 관점

- `domain.py`: Entity 보관보다는 Control 성격(연산 함수 중심)
- `boundary.py`: 입력 형태 검증은 Boundary 적합, `solve()`는 아직 도메인 위임 대신 미구현 예외로 스텁 상태
- `gui/app.py`: UI 중심이나 입력 파싱/정규화 책임 일부 포함(`_read_board`)

### 3.3 SRP 관점

- 위반 후보:
  - `src/magic_square/gui/app.py`의 `_on_solve_clicked()`가 이벤트 처리/검증 호출/실행 호출/결과 반영/오류 처리까지 다중 책임
- 명확한 위반 없음:
  - `domain.py`, `boundary.py`에서 클래스 단위 데이터+검증 혼합은 확인되지 않음
  - UI가 `if total == 34` 같은 도메인 판단식을 직접 계산하는 코드는 확인되지 않음

---

## 4) 리팩토링 계획(사전 수립)

우선순위 계획(요약):

1. `boundary.solve()` 책임 정리(실제 제어 흐름 위임 구조 준비)
2. `gui/app.py` 이벤트 핸들러 다중 책임 분리(메서드 추출)
3. `gui/app.py` 입력 파싱/정규화 규칙의 Boundary 이동 검토
4. `domain.py` 내 데이터 표현과 연산 로직 경계 명확화
5. 에러 메시지/문서 상수화로 스키마 일관성 강화

테스트 선행 필요 함수:

- `boundary.solve()`
- `gui/app.py`의 `_read_board()`, `_on_solve_clicked()`
- `domain.find_blank_coords()`

---

## 5) 실제 수행된 1회 리팩토링 (Dual-Track REFACTOR)

### 5.1 기준선 확인

- 실행 명령: `python -m pytest -q`
- 기준선 결과: `13 failed, 9 passed`
- 해석: 저장소가 RED 테스트 스켈레톤을 포함한 상태로, 전체 GREEN 기준선은 애초에 성립하지 않음.

### 5.2 이번 변경에서 선택한 목표

- `R-U2`: Boundary 에러 코드/메시지 생성 스키마 단일화
- `R-L3`: Domain의 1-index 시작값 리터럴 상수화(매직 넘버 완화)

### 5.3 변경 내용

#### UI Track (`src/magic_square/boundary.py`)

- `_build_error_message(code, detail)` 헬퍼 추가
- `validate()`와 `solve()`에서 예외 메시지 생성 경로를 헬퍼로 통일
- `solve(board)`의 미사용 파라미터 의도 명시: `_ = board`

#### Logic Track (`src/magic_square/domain.py`)

- `ONE_BASE_INDEX = 1` 상수 도입
- `find_blank_coords()`의 `enumerate(start=1)`를 `start=ONE_BASE_INDEX`로 치환
- 외부 계약(좌표 1-index, row-major) 변경 없음

### 5.4 보호 테스트 최소 보강

수정 파일: `tests/boundary/test_magic_square_boundary_red.py`

- 추가 테스트:
  - `test_ui_red_01b_solve_not_implemented_preserves_error_code_message`
- 목적:
  - `solve()` 스텁이 기존 `E_DOMAIN_NO_SOLUTION` 에러 코드 계약을 유지하는지 회귀 보호

### 5.5 리팩토링 후 재검증

- 실행 명령: `python -m pytest -q`
- 결과: `13 failed, 10 passed`
- 판정:
  - 기존 RED 실패 패턴은 유지(실패 증가 없음)
  - 보호 테스트 1건 추가 통과
  - 즉, 기능/계약 회귀 없이 리팩토링 반영됨

---

## 6) Git 작업 이력(이번 세션)

- 브랜치 생성/전환:
  - `refactoring` 브랜치 생성 완료
- 업로드 완료:
  - 커밋: `b8ff9d6`
  - 메시지: `docs(report): add refactoring analysis and execution plan report`
  - 원격: `origin/refactoring` 푸시 및 upstream 설정 완료
- 참고:
  - 보고서 파일 `report/11.refactoring-analysis-and-plan-report.md`가 이미 생성/푸시됨

---

## 7) 위험 요소 및 롤백 포인트

- 위험 요소
  - 에러 메시지 생성 경로 통합으로 문자열 포맷 미세 변화 가능성
  - 1-index 상수화 과정에서 향후 상수명 변경 시 가독성/추적성 영향 가능성
- 롤백 포인트
  - `src/magic_square/boundary.py`의 `_build_error_message` 적용부 되돌리기
  - `src/magic_square/domain.py`의 `ONE_BASE_INDEX` 치환부 되돌리기
  - 보호 테스트(`test_ui_red_01b_*`) 개별 롤백 가능

---

## 8) 결론

- 리팩토링 준비 분석(스멜/ECB/SRP)과 계획 수립은 완료되었고, 저위험 단위 리팩토링 1회가 회귀 없이 반영되었다.
- 현재 저장소는 의도된 RED 테스트를 포함한 상태이므로, 다음 단계는 기능 구현 커밋에서 RED 항목을 순차적으로 GREEN으로 전환하는 것이 적절하다.
