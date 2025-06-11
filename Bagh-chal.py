import streamlit as st

# --- 헬퍼 함수: 게임 상태 초기화 ---
def initialize_game_state():
    """게임의 모든 세션 상태 변수를 초기화하고 보드를 설정한다."""
    st.session_state.start = False # 게임 시작 여부
    st.session_state.turn = "G" # 현재 턴 (Goat: 염소, Tiger: 호랑이)
    st.session_state.click1 = None # 첫 번째 클릭 좌표
    st.session_state.click2 = None # 두 번째 클릭 좌표
    st.session_state.goat_placed_count = 0 # 보드에 놓인 염소 수
    st.session_state.tiger_catch_count = 0 # 호랑이가 잡은 염소 수
    st.session_state.movable_tigers_count = 4 # 움직일 수 있는 호랑이 수 (염소 승리 조건용)

    # 보드 초기화 및 초기 호랑이 배치
    st.session_state.board = [["" for _ in range(5)] for _ in range(5)]
    st.session_state.board[0][0] = "🐯"
    st.session_state.board[0][4] = "🐯"
    st.session_state.board[4][0] = "🐯"
    st.session_state.board[4][4] = "🐯"

# --- 헬퍼 함수: 클릭 상태 초기화 ---
def _reset_clicks():
    """사용자가 선택한 클릭 좌표를 초기화한다."""
    st.session_state.click1 = None
    st.session_state.click2 = None

# --- 헬퍼 함수: 특정 말의 이동이 유효한지 검사 ---
def _is_valid_move(piece_type, r1, c1, r2, c2, current_board):
    """
    말(piece_type)이 (r1, c1)에서 (r2, c2)로 이동하는 것이 유효한지 검사한다.
    current_board는 현재 게임 보드 상태이다.
    반환값: (이동 유효 여부, 염소 잡기 이동 여부)
    """
    # 보드 경계 확인
    if not (0 <= r2 < 5 and 0 <= c2 < 5):
        return False, False

    # 같은 칸으로 이동하는 것은 유효하지 않음
    if r1 == r2 and c1 == c2:
        return False, False

    dr, dc = r2 - r1, c2 - c1 # 행, 열 변화량

    if piece_type == "🐐":
        # 염소는 상하좌우, 대각선으로 한 칸만 이동 가능
        if (abs(dr) <= 1 and abs(dc) <= 1) and not (dr == 0 and dc == 0):
            return current_board[r2][c2] == "", False # 목표 칸이 비어있어야 함
        return False, False

    elif piece_type == "🐯":
        # 1칸 이동 (상하좌우, 대각선)
        if (abs(dr) <= 1 and abs(dc) <= 1) and not (dr == 0 and dc == 0):
            return current_board[r2][c2] == "", False # 목표 칸이 비어있어야 함

        # 2칸 이동 (염소 잡기)
        elif (abs(dr) == 2 and dc == 0) or \
             (dr == 0 and abs(dc) == 2) or \
             (abs(dr) == 2 and abs(dc) == 2):
            mid_r, mid_c = (r1 + r2) // 2, (c1 + c2) // 2 # 중간 칸 좌표
            # 목표 칸이 비어있고, 중간 칸에 염소가 있어야 함
            if current_board[r2][c2] == "" and current_board[mid_r][mid_c] == "🐐":
                return True, True # 유효한 잡기 이동
        return False, False # 유효하지 않은 호랑이 이동

    return False, False # 알 수 없는 말 타입

# --- 헬퍼 함수: 단일 호랑이가 움직일 수 있는지 확인 ---
def _can_single_tiger_move(r_tiger, c_tiger, current_board):
    """
    주어진 위치 (r_tiger, c_tiger)에 있는 호랑이가
    현재 보드(current_board)에서 이동할 수 있는지(1칸 이동 또는 염소 잡기) 확인한다.
    """
    # 호랑이가 이동할 수 있는 모든 가능한 방향을 탐색 (2칸 반경)
    for dr in [-2, -1, 0, 1, 2]:
        for dc in [-2, -1, 0, 1, 2]:
            nr, nc = r_tiger + dr, c_tiger + dc # 새로운 (목표) 좌표

            # 1. 현재 위치는 스킵
            if dr == 0 and dc == 0:
                continue

            # 2. _is_valid_move 헬퍼 함수를 사용하여 이동 가능성 체크
            is_valid, _ = _is_valid_move("🐯", r_tiger, c_tiger, nr, nc, current_board)
            if is_valid:
                return True # 움직일 수 있는 경로를 찾았으므로 즉시 반환

    # 모든 가능한 이동 경로를 탐색했지만 움직일 수 없었다면
    return False

# --- 게임 상태(승패) 확인 함수 ---
def check_game_status():
    """현재 게임 상태를 확인하여 승리 조건을 판단한다."""
    # 1. 호랑이 승리 조건: 염소를 4마리 잡았는지 확인
    if st.session_state.tiger_catch_count >= 4:
        st.session_state.start = False # 게임 종료 (호랑이 승리)
        return

    # 2. 염소 승리 조건: 모든 호랑이가 움직일 수 없는지 확인
    immobile_tigers_count = 0 # 움직일 수 없는 호랑이 수
    for r in range(5):
        for c in range(5):
            if st.session_state.board[r][c] == "🐯":
                # 각 호랑이가 움직일 수 있는지 헬퍼 함수로 확인
                if not _can_single_tiger_move(r, c, st.session_state.board):
                    immobile_tigers_count += 1

    # 움직일 수 있는 호랑이 수 업데이트
    st.session_state.movable_tigers_count = 4 - immobile_tigers_count

    # 모든 호랑이가 갇혔다면 염소 승리
    if st.session_state.movable_tigers_count == 0:
        st.session_state.start = False # 게임 종료 (염소 승리)

# --- 염소 놓기 처리 함수 ---
def _handle_goat_placement(r, c):
    """염소를 보드에 놓는 작업을 처리한다."""
    if st.session_state.board[r][c] == "": # 빈 칸에만 놓을 수 있음
        st.session_state.board[r][c] = "🐐"
        st.session_state.goat_placed_count += 1
        st.session_state.turn = "T" # 턴을 호랑이에게 넘김
        check_game_status() # 염소 놓은 후 게임 상태(승패) 확인
    else:
        st.toast("빈 칸에 염소를 놓으세요!")
    _reset_clicks() # 클릭 상태 초기화

# --- 염소 이동 처리 함수 ---
def handle_goat_move():
    """염소의 이동을 처리한다."""
    i, j = st.session_state.click1
    m, n = st.session_state.click2

    is_valid, _ = _is_valid_move("🐐", i, j, m, n, st.session_state.board)

    if is_valid:
        st.session_state.board[i][j] = "" # 원래 위치 비우기
        st.session_state.board[m][n] = "🐐" # 새 위치로 염소 이동
        st.session_state.turn = "T" # 턴을 호랑이에게 넘김
        check_game_status() # 이동 후 게임 상태(승패) 확인
    else:
        st.toast('유효하지 않은 움직임입니다! 염소는 빈 칸으로 한 칸만 이동할 수 있습니다.')
    _reset_clicks() # 클릭 상태 초기화

# --- 호랑이 이동 처리 함수 ---
def handle_tiger_move():
    """호랑이의 이동을 처리한다."""
    i, j = st.session_state.click1
    m, n = st.session_state.click2

    is_valid, is_capture = _is_valid_move("🐯", i, j, m, n, st.session_state.board)

    if is_valid:
        st.session_state.board[i][j] = "" # 원래 위치 비우기
        st.session_state.board[m][n] = "🐯" # 새 위치로 호랑이 이동
        if is_capture:
            mid_r, mid_c = (i + m) // 2, (j + n) // 2
            st.session_state.board[mid_r][mid_c] = "" # 잡은 염소 제거
            st.session_state.tiger_catch_count += 1 # 잡은 염소 수 증가
        st.session_state.turn = "G" # 턴을 염소에게 넘김
        check_game_status() # 이동 후 게임 상태(승패) 확인
    else:
        st.toast('유효하지 않은 움직임입니다! 호랑이는 한 칸 이동하거나 염소를 뛰어넘어 잡을 수 있습니다.')
    _reset_clicks() # 클릭 상태 초기화


# --- Streamlit 앱 메인 로직 시작 ---

# 게임 시작 시 또는 새로고침 시 상태 초기화
if "start" not in st.session_state:
    initialize_game_state()

# --- 게임 시작 전 화면 (규칙 설명) ---
# 염소 승리 조건 (movable_tigers_count == 0)도 여기서 처리되도록
# 호랑이 승리 조건 (tiger_catch_count >= 4)도 여기서 처리되도록
if not st.session_state.start:
    st.title('바그 찰(Bagh-chal) 게임')

    # 게임 종료 후 화면 (호랑이 승리)
    if st.session_state.tiger_catch_count >= 4:
        st.success("호랑이가 염소를 4마리 잡았습니다! 🐯 호랑이 승리!")
        if st.button('다시 시작'):
            initialize_game_state() # 게임 상태를 완전히 초기화

    # 게임 종료 후 화면 (염소 승리)
    elif st.session_state.movable_tigers_count == 0:
        st.success("호랑이가 포위당했습니다! 🐐 염소 승리!")
        if st.button('다시 시작'):
            initialize_game_state() # 게임 상태를 완전히 초기화

    # 게임 시작 전 규칙 설명 화면
    else:
        st.write("바그 찰은 염소와 호랑이가 싸우는 2인용 보드 게임입니다.")
        st.write("아래에서 규칙을 확인하고 게임을 시작하세요.")

        rule_data = {
            '룰 - 호랑이(🐯)': {
                '말의_개수': '총 4개',
                '말의_위치': '게임 시작 시 보드 모퉁이에 배치됩니다.',
                '플레이_방법과_승리조건': ('인접한 칸으로 이동하거나, 직선 경로를 따라 염소를 하나 건너뛰어 잡을 수 있습니다.'
                                       '염소를 5마리 이상 잡거나, 끝까지 포위되지 않으면 호랑이가 승리합니다.')
            },
            '룰 - 염소(🐐)': {
                '말의_개수': '총 20개',
                '말의_위치': '차례대로 하나씩 보드에 배치합니다.',
                '플레이_방법과_승리조건': ('모든 염소가 배치된 후에 배치된 염소들을 인접한 칸으로 한 칸씩만 이동할 수 있습니다.'
                                       '이때 말을 뛰어넘거나 호랑이를 잡을 수 없습니다.'
                                       '호랑이의 움직임을 모두 막으면 염소가 승리합니다.')
            }
        }

        selected_rule = st.selectbox('알고 싶은 것을 골라주세요:', list(rule_data.keys()))

        if st.button('룰 설명 보기'):
            info = rule_data[selected_rule]
            st.markdown(f"**말의 개수**: {info['말의_개수']}")
            st.markdown(f"**말의 위치**: {info['말의_위치']}")
            st.markdown(f"**플레이 방법과 승리조건**: {info['플레이_방법과_승리조건']}")
            st.info("게임은 염소가 먼저 시작합니다. 말을 움직일 경우, 움직이고 싶은 말을 클릭하고 이동할 위치를 [두 번] 클릭하세요.")

        if st.button('게임 시작하기'):
            initialize_game_state() # 게임 상태를 완전히 초기화
            st.session_state.start = True
            st.session_state.turn = "G"
            check_game_status() # 초기 상태에서 호랑이의 이동 가능성 미리 계산


# --- 게임 플레이 중 화면 ---
else:
    # 현재 턴 안내
    current_turn_emoji = "🐐" if st.session_state.turn == "G" else "🐯"
    st.title(f'바그 찰(Bagh-chal) 게임 - {current_turn_emoji} 차례')

    # 보드판 렌더링
    for r in range(5):
        cols = st.columns(5)
        for c in range(5):
            cell_content = st.session_state.board[r][c] or " " # 빈 칸은 공백으로 표시
            button_key = f"board_cell_{r}-{c}" # 각 버튼에 고유한 키 부여

            if cols[c].button(cell_content, key=button_key):
                clicked_pos = (r, c)

                if st.session_state.turn == "G": # 염소 턴 로직
                    if st.session_state.goat_placed_count < 20: # 염소 놓기 단계
                        _handle_goat_placement(r, c)
                    else: # 염소 이동 단계
                        if st.session_state.click1 is None: # 첫 번째 클릭 (옮길 염소 선택)
                            if st.session_state.board[r][c] == "🐐":
                                st.session_state.click1 = clicked_pos
                                st.toast("이동할 위치를 선택하세요.")
                            else:
                                st.toast("염소를 선택하세요.")
                        else: # 두 번째 클릭 (이동할 위치 선택)
                            st.session_state.click2 = clicked_pos
                            handle_goat_move() # 염소 이동 처리 함수 호출
                else: # 호랑이 턴 로직
                    if st.session_state.click1 is None: # 첫 번째 클릭 (옮길 호랑이 선택)
                        if st.session_state.board[r][c] == "🐯":
                            st.session_state.click1 = clicked_pos
                            st.toast("이동할 위치를 선택하세요.")
                        else:
                            st.toast("호랑이를 선택하세요.")
                    else: # 두 번째 클릭 (이동할 위치 선택)
                        st.session_state.click2 = clicked_pos
                        handle_tiger_move() # 호랑이 이동 처리 함수 호출

    # --- 사이드바에 게임 상태 표시 ---
    st.sidebar.markdown("### 현재 게임 상태")
    st.sidebar.write(f"현재 턴: {'염소 🐐' if st.session_state.turn == 'G' else '호랑이 🐯'}")
    st.sidebar.write("놓은 염소 수:", st.session_state.goat_placed_count)
    st.sidebar.write("잡힌 염소 수:", st.session_state.tiger_catch_count)
    st.sidebar.write("움직일 수 있는 호랑이 수:", st.session_state.movable_tigers_count)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 보드 현황")
    for r_idx in range(5):
        # 보드 내용을 _로 표시하여 빈칸과 구분
        row_display = " ".join([st.session_state.board[r_idx][c_idx] if st.session_state.board[r_idx][c_idx] else "_" for c_idx in range(5)])
        st.sidebar.text(f"행 {r_idx}: {row_display}")
