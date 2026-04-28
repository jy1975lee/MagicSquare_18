# MagicSquare (4×4) — TDD 연습용 마방진 완성

**단일 진실 공급원(요구·검증·To-Do):** [`docs/PRD-4x4-magic-square-tdd.md`](docs/PRD-4x4-magic-square-tdd.md) — 부분 채움 4×4 보드(빈칸 `0` 정확히 2개)를 계약에 따라 완성하거나, 실패 시 고정 오류로 거부한다.

**문서 관계(한 줄, Report/5):** [`report/05.magic-square-prd-authoring-export-report.md`](report/05.magic-square-prd-authoring-export-report.md)는 PRD 작성 작업의 범위·근거·핵심 결정·산출물 위치를 기록한 보고서이며, **구현·승인 기준의 중심은 항상 위 PRD**이고 Report 05는 그 PRD를 “어떻게 만들었는지”를 추적한다.

---

## GUI 실행 (공식 경로)

- `python -m magic_square.gui`

---

## 1. 프로젝트 목적 (PRD 중심)

- 표면 과제는 “마방진을 채운다”가 아니라, **고정된 입력/출력 계약**과 **불변조건(I1~I9, BR-01~15)** 아래에서 **검증 → 도메인 솔브**가 결정론적으로 재현되는지 연습하는 것이다.
- **In-Scope (PRD §4):** 4×4 입력 검증(FR-01), 빈칸 2곳·row-major 첫 빈칸 정의(FR-02), 누락 두 수 `n_low < n_high`(FR-03), 10개 라인 합 34 판정(FR-04), 두 순열 시도 및 `int[6]` 또는 `E_DOMAIN_NO_SOLUTION`(FR-05), 트레이서빌리티(§12).
- **Out-of-Scope:** 별도 UI·DB·Web, N×N 일반화(본 릴리스), Data 레이어 및 PRD에 없는 `E_DATA_*` 요구.

---

## 2. 문서 맵

| 문서 | 역할 |
|------|------|
| [docs/PRD-4x4-magic-square-tdd.md](docs/PRD-4x4-magic-square-tdd.md) | FR/BR/NFR, Dual-Track, 테스트 플랜, 아키텍처, **Traceability Matrix** — 본문·To-Do·검증 기준의 중심 |
| [report/04.user-journey-epic-to-level5-report.md](report/04.user-journey-epic-to-level5-report.md) | 에픽·여정·**User Story 1~5**·Gherkin 시나리오 표현 |
| [report/02.magic-square-dual-track-ui-logic-tdd-clean-architecture-report.md](report/02.magic-square-dual-track-ui-logic-tdd-clean-architecture-report.md) | 입력/출력 스키마, **오류 코드·고정 메시지**, Dual-Track 계약 테스트 ID |
| [report/03.cursorrules-design-and-implementation-report.md](report/03.cursorrules-design-and-implementation-report.md) | ECB·TDD 단계·pytest·커버리지·금지 패턴과 `.cursorrules` 반영 요약 |
| [src/.cursor/rules/.cursorrules](src/.cursor/rules/.cursorrules) | Cursor 에이전트용 **실행 규칙**(Python 3.10+, PEP8, Google docstring, RED/GREEN/REFACTOR, mock 남용 금지 등) |
| [report/05.magic-square-prd-authoring-export-report.md](report/05.magic-square-prd-authoring-export-report.md) | PRD 산출 경로·선행 report 매핑·핵심 결정 요약 |
| [report/06.magic-square-readme-and-session-deliverables-report.md](report/06.magic-square-readme-and-session-deliverables-report.md) | README·C2C §7~8·세션 산출·부록(Task 체계·001~037 매핑) **보낸 기록** |

**`pyproject.toml`:** 저장소 루트에 아직 없을 수 있다. 추가 시 **Python 3.10+**, **pytest**, **AAA 패턴**을 기본으로 두고, **커버리지 임계값은 PRD NFR(도메인 ≥95%, Boundary ≥85%)**을 우선한다(`.cursorrules`의 80% 일반 하한과 불일치하면 **PRD가 우선**).

---

## 3. 사용자 스토리 요약 (Report/4)

| # | 스토리 | 요지 |
|---|--------|------|
| 1 | 입력 검증 | 4×4, 빈칸 2개, 범위, 비0 중복 없음 — 실패 시 도메인으로 넘기지 않는다. |
| 2 | 빈칸 탐색 | `0` 위치 2개, **row-major**로 첫/둘째 빈칸, 좌표는 **1-index**. |
| 3 | 누락 숫자 | 1~16 중 나타나지 않은 수 2개, **`n_low < n_high`**. |
| 4 | 마방진 판정 | 4행+4열+2대각선(10라인), 상수 **34**. |
| 5 | 두 조합 시도 | (작은 수→첫 빈칸, 큰 수→둘째) 후 실패 시 반대 배치; 성공 시 길이 6 배열 규칙(PRD BR-11, BR-12). |

Gherkin·표본 행렬은 Report/4 및 PRD §9.3 **TD-OK-01**을 참고한다.

---

## 4. 계약·오류 요약 (Report/2 + PRD 정합)

**입력:** `int[][]` — 정확히 4행·각 행 길이 4; `0` 정확히 2개; 셀 값은 `0` 또는 `1~16`; `0` 제외 중복 없음.

**출력(성공):** `int[6]`, 좌표 **1-index**, 시도 1·2에 따른 순서는 PRD FR-05·BR-11·BR-12.

| 코드 | 고정 메시지(요지) | 조건 |
|------|-------------------|------|
| `E_INPUT_SIZE` | 입력 행렬 크기는 4x4이어야 합니다. | 형태 ≠ 4×4 |
| `E_EMPTY_COUNT` | 빈칸(0)의 개수는 정확히 2개여야 합니다. | `count(0) ≠ 2` |
| `E_VALUE_RANGE` | 각 값은 0 또는 1~16 범위여야 합니다. | 범위 위반 |
| `E_DUPLICATE_NONZERO` | 0을 제외한 숫자는 중복될 수 없습니다. | 비0 중복 |
| `E_DOMAIN_NO_SOLUTION` | 두 조합 모두 마방진 조건을 만족하지 않습니다. | 두 순열 모두 실패 |

PRD 범위에서는 **Data 레이어·`E_DATA_*`는 구현 요구에서 제외**한다.

---

## 5. 아키텍처·실행·TDD (Report/3 + Cursor 규칙 + pyproject)

- **ECB:** Boundary는 입출력·검증 호출 순서·오류 표준화; Control은 유스케이스 조립(검증 → 솔브); Entity는 보드 상태·빈칸/누락/판정/두 순열 솔버 등 순수 도메인. **도메인은 Boundary를 참조하지 않는다**(PRD §10.3).
- **Dual-Track:** 동일 FR 조각에 대해 **Boundary(계약) 테스트**와 **Domain 테스트**를 병렬로 RED → 각 GREEN → REFACTOR에서 중복 제거(PRD §8.3).
- **실행:** `pytest`를 사용한다([`src/.cursor/rules/.cursorrules`](src/.cursor/rules/.cursorrules): AAA, function 스코프 fixture 우선). 소스는 `src/magic_square/`, 테스트는 `tests/` 구조에 맞춘다.
- **`pyproject.toml` 권장 키:** `[project]` `requires-python = ">=3.10"`, `[tool.pytest.ini_options]` `pythonpath = ["src"]` 등 — 추가 후 `pytest` 및 `pytest --cov=...`로 PRD NFR을 게이트할 수 있다.

---

## 6. 검증 기준 체크리스트 (PRD)

- [ ] **FR-01:** AC-FR-01-01 ~ 05 (크기, 행 길이, 빈칸 개수, 범위, 비0 중복).
- [ ] **FR-02:** 빈칸 2좌표, row-major 첫 `0`, 1-index (AC-FR-02-01~03).
- [ ] **FR-03:** 누락 2수, `n_low < n_high` (AC-FR-03-01~03).
- [ ] **FR-04:** 알려진 마방진 True, 한 셀 깨짐 False, 10라인만 사용 (AC-FR-04-01~03).
- [ ] **FR-05:** 시도 1만 성공·시도 2만 성공·이중 실패·출력 길이·좌표 범위 (AC-FR-05-01~04, TP-01~03).
- [ ] **BR-14 / NFR-04:** 입력 행렬 비변경(내부 복사 후 채움).
- [ ] **BR-15:** 검증 실패 시 솔버 미호출(계약 테스트로 고정).
- [ ] **NFR-01~02:** 도메인 라인 커버리지 ≥95%, Boundary ≥85% (측정 시 패키지 경로는 구현에 맞게 조정).
- [ ] **NFR-03:** 동일 입력 → 동일 성공 배열 또는 동일 오류 코드.

대표 픽스처: PRD §9.3 **TD-OK-01** 기대 출력 `[4, 4, 1, 3, 3, 6]`; **TD-NS-01**은 픽스처 파일에 고정해 TP-03과 연결한다(Report/5 후속 권장과 동일).

---

## 7. Concept-to-Code(C2C) To-Do List

**추적 사슬:** `Task → Req(FR/AC/NFR) → Scenario(L0~L3·L-B) → Test → Code(ECB)` — PRD §12 Traceability Matrix와 동일한 정보를 **개발 보드** 형태로 유지한다.

### 7.1 기호·시나리오 레벨

| 표기 | 의미 |
|------|------|
| **L0** | 개요·리팩터·품질 게이트(기능 단위 “설명”) |
| **L1** | 정상 흐름(Happy) |
| **L2** | 경계·불변조건(Edge: 비변경, 결정론 등) |
| **L3** | 실패·오류(Fail) |
| **L-B** | Boundary 계약(이 PRD에서 “UI” 트랙 — 호출 경계·오류 스키마) |
| **RED / GREEN / REFACTOR** | TDD 단계([`src/.cursor/rules/.cursorrules`](src/.cursor/rules/.cursorrules)) |

**체크포인트(비기능):** 작업을 끝낼 때 해당 행의 체크박스를 갱신한다.

- [ ] **[Checkpoint] NFR-01** 도메인 패키지 라인 커버리지 ≥ **95%**
- [ ] **[Checkpoint] NFR-02** Boundary 패키지 라인 커버리지 ≥ **85%**
- [ ] **[Checkpoint] NFR-04 / BR-14** 입력 행렬 **비변경**(복사본에서만 채움·테스트로 단언)
- [ ] **[Checkpoint] NFR-05(선택)** 단일 호출 상한(예: 50ms) — 환경 의존 시 스킵 조건 명시(PRD NFR-05)
- [ ] **[Checkpoint] BR-15** 검증 실패 시 **도메인 솔버 미호출**(스파이·플래그 등 최소 수단)

---

### 7.2 Epic → User Story → Task (체크리스트)

## Epic-001: 4×4 Magic Square 완성·계약 검증 시스템

### US-001: 입력 계약을 만족하는지 검증한다 (FR-01, BR-01~04, BR-15)

- [ ] **TASK-001:** `BOARD_SIZE`, `MAGIC_SUM`(34) 명명 상수 및 `MagicSquareBoard` 4×4 상태 보관 — **GREEN** · Entity · `test_board_and_constants_represent_4x4`
- [ ] **TASK-002:** `CellPosition`(1-index, 1~4) 불변 VO — **GREEN** · Entity · `test_cell_position_one_index`
- [ ] **TASK-003:** **I1** 외곽 4×4 아님 → `E_INPUT_SIZE` (Dual-Track 한 조각)
  - [ ] **TASK-003-1:** **RED** · L-B · `test_bt_rejects_non_4x4_matrix` (BT-02) · Boundary — 솔버 미호출
  - [ ] **TASK-003-2:** **RED** · L3 · `test_dt_rejects_wrong_dimensions` (DT-01a) · `BoardInvariantValidator`
  - [ ] **TASK-003-3:** **GREEN** · I1 구현으로 위 테스트 통과
  - [ ] **TASK-003-4:** **REFACTOR** · L0 · 오류 코드·고정 문구 단일 모듈(`errors` 등) — Report/02 표와 문자열 동기화
- [ ] **TASK-004:** **I2** `0` 개수 ≠2 → `E_EMPTY_COUNT`
  - [ ] **TASK-004-1:** **RED** · L-B · `test_bt_rejects_bad_empty_count` (BT-03)
  - [ ] **TASK-004-2:** **RED** · L3 · `test_dt_rejects_wrong_zero_count` (DT-01b)
  - [ ] **TASK-004-3:** **GREEN** · I2 구현
  - [ ] **TASK-004-4:** **REFACTOR** · 검증 순서(크기→빈칸 수→값) 가독성만 개선, 동작 불변
- [ ] **TASK-005:** **I3·I4** 범위 위반·비0 중복 → `E_VALUE_RANGE`, `E_DUPLICATE_NONZERO`
  - [ ] **TASK-005-1:** **RED** · L-B · `test_bt_value_range`, `test_bt_duplicate_nonzero` (BT-04, BT-05)
  - [ ] **TASK-005-2:** **RED** · L3 · `test_dt_out_of_range`, `test_dt_duplicate_nonzero` (DT-01c, d)
  - [ ] **TASK-005-3:** **GREEN** · I3·I4 구현 — AC-FR-01-04, AC-FR-01-05
  - [ ] **TASK-005-4:** **REFACTOR** · Boundary는 **검증기 호출만**(규칙 중복 없음)

### US-002: 빈칸 두 곳과 누락 수 쌍을 산출한다 (FR-02, FR-03, BR-05~06)

- [ ] **TASK-010:** 빈칸 row-major·1-index — **TASK-010-1** RED `test_dt_find_blanks_row_major` (DT-02) · **TASK-010-2** GREEN `BlankFinder` · **TASK-010-3** REFACTOR 반환 타입 `CellPosition`×2 통일 · Entity
- [ ] **TASK-011:** 누락 두 수 `n_low < n_high` — **TASK-011-1** RED `test_dt_missing_pair_order` (DT-03) · **TASK-011-2** GREEN `MissingNumberFinder`, `MissingPair` · **TASK-011-3** REFACTOR · Entity

### US-003: 완전히 채운 보드가 마방진인지 판정한다 (FR-04, BR-07~08)

- [ ] **TASK-020:** `MagicSquareJudge` — **TASK-020-1** RED L1 `test_judge_known_magic_true` · L2 `test_judge_one_cell_breaks_false` · L0 `test_judge_uses_exactly_ten_lines` (AC-FR-04-01~03, DT-04) · **TASK-020-2** GREEN · **TASK-020-3** REFACTOR · Entity — `0` 포함 호출은 계약 위반(호출부에서 금지)

### US-004: 두 순열로 채워 해를 구하고 `int[6]` 또는 도메인 실패를 반환한다 (FR-05, BR-11~14)

- [ ] **TASK-030:** `TwoPermutationSolver` + 내부 복사
  - [ ] **TASK-030-1:** **RED** · L1 · 시도 1만 성공 픽스처 → `[r_first,c_first,n_low,r_second,c_second,n_high]` (TP-01, DT-05, AC-FR-05-01)
  - [ ] **TASK-030-2:** **RED** · L1 · TD-OK-01(PR §9.3) 시도 2 성공 → `[4,4,1,3,3,6]` (TP-02, DT-06, AC-FR-05-02, BR-12)
  - [ ] **TASK-030-3:** **RED** · L3 · TD-NS-01 두 시도 실패 → `E_DOMAIN_NO_SOLUTION` (TP-03, DT-07)
  - [ ] **TASK-030-4:** **RED** · L2 · `test_solver_does_not_mutate_input` (DT-08, NFR-04, BR-14)
  - [ ] **TASK-030-5:** **GREEN** · 위 전부 통과하는 최소 솔버 + `MagicSquareJudge` 재사용
  - [ ] **TASK-030-6:** **REFACTOR** · L0 · `SolveResult`/`int[6]` 스키마 명확화, 중복 제거

### US-005: Boundary가 검증→솔브 흐름과 오류 응답을 표준화한다 (PRD §8.1 Track A)

- [ ] **TASK-040:** 공개 경계 API — **TASK-040-1** RED L-B `test_bt_success_length6_one_index` (BT-01) · **TASK-040-2** RED L-B `test_bt_domain_no_solution_mapped` (BT-06) · **TASK-040-3** RED L-B `test_bt_solver_not_called_when_validation_fails` (BT-07, BR-15)
- [ ] **TASK-040-4:** **GREEN** · Control `CompleteMagicSquareUseCase`(검증→솔브 조립만) + Boundary 응답/오류 매퍼
- [ ] **TASK-040-5:** **REFACTOR** · L0 · 도메인 규칙이 Boundary에 새지 않았는지 의존성 방향 재점검

### US-006: 통합 실패 시나리오·품질 게이트를 닫는다 (TP-04~05, NFR-01~03, §9)

- [ ] **TASK-050:** **RED** · L3 · `test_tp_04_shape_errors`, `test_tp_05_semantic_validation_errors` — 공개 API 관통
- [ ] **TASK-051:** **GREEN** · 위 통과 + 결정론 `test_same_input_same_output` (NFR-03)
- [ ] **TASK-052:** **REFACTOR** · §7.1 **Checkpoint** 전부 충족 + `pyproject.toml`/CI에 pytest·커버리지 게이트 반영(가능 시)

---

## 8. Requirements Traceability Matrix (요구–시나리오–테스트)

구현 진행에 따라 **상태** 열을 `⬜ TODO` → `🔴 RED` → `✅ PASS`로 갱신한다.

| Task ID | Req ID | Scenario | 테스트 (제안 이름) | 상태 |
|---------|--------|----------|-------------------|------|
| TASK-001 | NFR-06, §10.2 | L0 | `test_board_and_constants_represent_4x4` | ⬜ TODO |
| TASK-002 | FR-02, BR-09 | L1 | `test_cell_position_one_index` | ⬜ TODO |
| TASK-003 | FR-01, AC-FR-01-01~02 | L3 / L-B | `test_bt_rejects_non_4x4_matrix`, `test_dt_rejects_wrong_dimensions` | ⬜ TODO |
| TASK-004 | FR-01, AC-FR-01-03 | L3 / L-B | `test_bt_rejects_bad_empty_count`, `test_dt_rejects_wrong_zero_count` | ⬜ TODO |
| TASK-005 | FR-01, AC-FR-01-04~05 | L3 / L-B | `test_bt_value_range`, `test_dt_out_of_range`, … | ⬜ TODO |
| TASK-010 | FR-02, AC-FR-02-01~03 | L1 | `test_dt_find_blanks_row_major` | ⬜ TODO |
| TASK-011 | FR-03, AC-FR-03-01~03 | L1 | `test_dt_missing_pair_order` | ⬜ TODO |
| TASK-020 | FR-04, AC-FR-04-01~03 | L1 / L2 / L0 | `test_judge_known_magic_true`, `test_judge_one_cell_breaks_false`, `test_judge_uses_exactly_ten_lines` | ⬜ TODO |
| TASK-030 | FR-05, AC-FR-05-01~04 | L1 / L3 / L2 | `test_try1_success_output`, `test_td_ok_01_try2_output`, `test_td_ns_01_no_solution`, `test_solver_does_not_mutate_input` | ⬜ TODO |
| TASK-040 | FR-01+FR-05, §8.1 | L-B / L3 | `test_bt_success_length6_one_index`, `test_bt_domain_no_solution_mapped`, `test_bt_solver_not_called_when_validation_fails` | ⬜ TODO |
| TASK-050~052 | TP-04~05, NFR-01~03 | L3 / L0 | `test_tp_04_shape_errors`, `test_tp_05_semantic_validation_errors`, 커버리지·결정론 테스트 | ⬜ TODO |

세부 서브태스크(예: TASK-003-1)는 동일 **Req ID**·**Scenario**를 상속하고, PRD §12의 `BT-*` / `DT-*` / `TP-*` ID로 테스트 케이스를 더 쪼개도 된다.

---

## 9. 참고 링크

- PRD 트레이서빌리티: [docs/PRD-4x4-magic-square-tdd.md §12](docs/PRD-4x4-magic-square-tdd.md)
- Cursor 규칙 파일: [src/.cursor/rules/.cursorrules](src/.cursor/rules/.cursorrules)
