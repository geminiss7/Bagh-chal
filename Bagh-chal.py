import streamlit as st

def Goat_move():
  i, j = st.session_state.click1
  m, n = st.session_state.click2
  
  # 현재 있는 칸에서 상하좌우, 대각선으로 한칸인 경우에서
  if (abs(i - m) == 1 and j == n) or (i == m and abs(j - n) == 1) or (abs(i - m) == 1 and abs(j - n) == 1):
    if st.session_state.board[m][n] == "":                   # 이동하려는 칸이 비어있다면
      st.session_state.board[i][j] = ""                      # 염소가 처음에 있던 곳을 비우고
      st.session_state.board[m][n] = "🐐"                     # 염소를 넣는다.
      st.session_state.click1 = None                         # 그 이후에 사용자가 고른 두 좌표를 초기화시킨다. (그 이후의 동작을 위해)
      st.session_state.click2 = None
      st.session_state.turn = "T"                            # 그 이후 차례를 호랑이에게 넘긴다.
    else:
      st.toast('유효하지 않은 움직임입니다!')                # 아니라면 이 문장을 출력한다.
      st.session_state.click1 = None
      st.session_state.click2 = None

def Tiger_move():
  i, j = st.session_state.click1
  m, n = st.session_state.click2
  
  # 현재 있는 칸에서 상하좌우, 대각선으로 한칸인 경우에서
  if (abs(i - m) == 1 and j == n) or (i == m and abs(j - n) == 1) or (abs(i - m) == 1 and abs(j - n) == 1):
    if st.session_state.board[m][n] == "":                   # 이동하려는 칸이 비어있다면
      st.session_state.board[m][n] = "🐯"                     # 호랑이를 넣고
      st.session_state.board[i][j] = ""                      # 호랑이가 처음에 있던 곳을 비운다.
      st.session_state.click1 = None                         # 그 이후에 사용자가 고른 두 좌표를 초기화시킨다. (그 이후의 동작을 위해)
      st.session_state.click2 = None
      st.session_state.turn = "G"                           # 그 이후 차례를 염소에게 넘긴다.
    else:
      st.toast('유효하지 않은 움직임입니다!')                # 아니라면 이 문장을 출력한다.
      st.session_state.click1 = None
      st.session_state.click2 = None
      
  # 이동 거리가 상하좌우로 두칸이거나 대각선으로 두칸인 경우에서
  elif (abs(i - m) == 2 and j == n) or (i == m and abs(j - n) == 2) or (abs(i - m) == 2 and abs(j - n) == 2):
    
    # 이동하려는 칸이 비어있고, 이동하려는 중간 칸에 염소가 있을 때
    if st.session_state.board[m][n] == "" and st.session_state.board[(i+m)//2][(j+n)//2] == "🐐":
      st.session_state.board[i][j] = ""                      # 호랑이가 있던 칸을 비우고
      st.session_state.board[m][n] = "🐯"                     # 이동하려는 칸을 T로 채운다.
      st.session_state.board[(i+m)//2][(j+n)//2] = ""        # 염소가 있는 칸을 비우고
      st.session_state.catch += 1                            # 잡은 염소의 수를 1 올려라.
      st.toast(f"잡은 염소의 수 {st.session_state.catch}")   # 그리고 알려라.
      st.session_state.click1 = None                         # 그 이후에 사용자가 고른 두 좌표를 초기화시킨다. (그 이후의 동작을 위해)
      st.session_state.click2 = None
      st.session_state.turn = "G"                            # 그 이후 차례를 염소에게 넘긴다.
    else:
      st.toast('유효하지 않은 움직임입니다!')                # 아니라면 이 문장을 출력한다.
      st.session_state.click1 = None
      st.session_state.click2 = None

  else:
    st.toast('유효하지 않은 움직임입니다!')                  # 아니라면 이 문장을 출력한다.
    st.session_state.click1 = None
    st.session_state.click2 = None

def check():
  if st.session_state.turn == "G" and st.session_state.catch >= 4: # 염소를 4개 잡았을 때 게임을 끝낸다.
    st.success("호랑이가 염소를 4마리 잡았습니다! 🐯 호랑이 승리!")

  cannot_move_count = 0                                            # 움직일 수 없는 호랑이 수

    for i in range(5):
      for j in range(5):
        if st.session_state.board[i][j] == "🐯":                  # 호랑이의 좌표를 찾음
          tiger_can_move = False
          for di in [-2, -1, 0, 1, 2]:                            # 가로로 움직일 수 있는 거리
            for dj in [-2, -1, 0, 1, 2]:                          # 세로로 움직일 수 있는 거리
              ni, nj = i + di, j + dj                             # 움직인 새로운 좌표
              if 0 <= ni < 5 and 0 <= nj < 5:                     # 움직인 새로운 좌표가 보드게임 안에 있고
                if abs(di) <= 1 and abs(dj) <= 1:                 # 상하좌우로 한칸만 움직일 때
                  if st.session_state.board[ni][nj] == "":        # 움직인 좌표가 비었다면 움직일 수 있다.
                    tiger_can_move = True
                    break                                         # 움직일 수 있으면 이 반복문을 탈출한다.
                elif (abs(di) == 2 and dj == 0) or (di == 0 and abs(dj) == 2) or (abs(di) == 2 and abs(dj) == 2): # 염소를 먹으려고 할 때
                    mid_i, mid_j = (i + ni) // 2, (j + nj) // 2
                    if (st.session_state.board[ni][nj] == "" and st.session_state.board[mid_i][mid_j] == "🐐"):   # 염소가 중간에 있고 움직이려는 칸이 비었다면
                      tiger_can_move = True                                                                       # 움직일 수 있다.
                      break                                                                                       # 움직일 수 있으면 이 반복문을 탈출한다.
            if tiger_can_move:
                break                                                                                             # 움직일 수 있으면 이 반복문을 탈출한다.
        if not tiger_can_move:
            cannot_move_count += 1                                                                                # 이 호랑이는 못 움직임

    if cannot_move_count == 4:                                                                                    # 4개가 전부 못 움직이면 염소가 승리한다.
        st.success("호랑이의 모든 움직임이 막혔습니다! 🐐 염소 승리!")
        st.session_state.start = False
  

# 게임의 시작 조건 정의
if "start" not in st.session_state:
  st.session_state.start = False

# 게임이 시작하기 전 화면에서 실행
if not st.session_state.start:
  # 시작 화면
  st.title('바그 찰(Bagh-chal) 게임')
  rule = st.selectbox('알고 싶은 것을 골라주세요 : ', ['룰-염소(G)', '룰-호랑이(🐯)'])
  rule_data = {
    '룰-호랑이(T)' : {
                  '말의_개수' :  '호랑이는 총 4개', 
                  '말의_위치' : '게임 시작 시 이미 보드 위에 배치되어 있다.',
                  '플레이_방법과_승리조건' : ('인접한 칸으로 이동하거나, 직선경로를 따라 염소를 하나 건너뛰어 잡을 수 있다.''염소를 최소 5마리 이상 잡거나, 끝까지 포위되지 않으면 호랑이가 승리한다.')},
    '룰-염소(G)' : {
                  '말의_개수' : '염소는 총 20개', 
                  '말의_위치' : '차례대로 하나씩 보드에 배치한다.',
                  '플레이_방법과_승리조건' : ('모든 염소가 배치된 후에 배치된 염소들을 인접한 칸으로 한 칸씩만 이동할 수 있다.''이때 말을 뛰어넘거나 호랑이를 잡을 수 없다.''호랑이의 움직임을 모두 막으면 염소가 승리한다.')}
              }
  
  if st.button('룰 설명'):
    if rule in rule_data:
      말의_개수 = rule_data[rule]['말의_개수']
      말의_위치 = rule_data[rule]['말의_위치']
      플레이_방법과_승리조건 = rule_data[rule]['플레이_방법과_승리조건']
  
      st.write(f"**말의 개수**: {말의_개수}")
      st.write(f"**말의 위치**: {말의_위치}")
      st.write(f"**플레이 방법과 승리조건**: {플레이_방법과_승리조건}")
      st.write("게임은 염소가 먼저 시작합니다. 말을 움직일 경우엔 움직이고 싶은 말을 클릭하고 움직이고 싶은 위치를 [두번] 클릭하시면 됩니다.")
      
  # 게임 시작하고 보드게임 판, 클릭유무, 차례, 염소 말의 수를 저장하는 변수, 잡힌 염소의 수를 저장하는 변수, 움직일 수 없는 호랑이의 수를 저장하는 변수 생성, 저장
  if st.button('게임 시작'):
    st.session_state.start = True
    st.session_state.turn = "G"
    st.session_state.click1 = None
    st.session_state.click2 = None
    st.session_state.count = 0
    st.session_state.catch = 0
    st.session_state.tiger = 0
    st.session_state.board = [["" for _ in range(5)] for _ in range(5)]
    st.session_state.board[0][0] = "🐯"
    st.session_state.board[0][4] = "🐯"
    st.session_state.board[4][0] = "🐯"
    st.session_state.board[4][4] = "🐯"

else:
  
  # 차례 안내 - 염소차례라면
  if st.session_state.turn=="G":
    st.title('바그 찰(Bagh-chal) 게임 - 염소')

    # 보드판 생성(위에서 한 것은 값의 저장용, 이것은 보이게 해주는 코드)
    for i in range(5):
      cols = st.columns(5)
      for j in range(5):
        text = st.session_state.board[i][j] or ""
        
        # 버튼이 눌렸는데
        if cols[j].button(text,key=f"{i}-{j}"):
          # 선택한 좌표가 비어있고, 판 위에 놓인 염소의 수가 20개 미만인 경우
          if st.session_state.board[i][j] == "" and st.session_state.count < 20:
            st.session_state.click1 = (i,j)                  # 선택된 좌표를 저장하고
            st.session_state.board[i][j] = "🐐"               # 선택한 좌표에 값을 채워넣고
            st.session_state.count += 1                      # 놓은 염소의 수를 하나 늘린다.
            st.toast(f"놓은 말의 수 : {st.session_state.count}")
            st.session_state.turn = "T"                      # 그 이후 차례를 호랑이에게 넘긴다.
            st.session_state.click1 = None                   # 그 이후에 사용자가 고른 두 좌표를 초기화시킨다. (그 이후의 동작을 위해)
            st.session_state.click2 = None
          
          # 선택한 좌표가 염소로 채워져있고 놓은 염소의 말이 20개인 경우
          elif st.session_state.board[i][j] == "G" and st.session_state.count == 20:
            clicked_pos = (i, j)
            if st.session_state.click1 is None:               # 염소를 선택해야 하는 경우(옮길 말의 좌표가 저장되어있지 않다면)
              st.session_state.click1 = clicked_pos           # 옮길 말의 좌표를 저장해라
              st.toast("이동할 위치를 선택하세요.")            # 그 이후에 이 문장을 출력해라
              
            # 옮길 위치를 정해야 하는 경우(옮길 곳의 좌표가 저장되어 있지 않고 그 좌표가 현재 염소의 좌표와 다르다면)  
            elif st.session_state.click2 is None and clicked_pos != st.session_state.click1:
              st.session_state.click2 = clicked_pos           # 옮길 위치의 좌표를 저장해라
              Goat_move()
            else:
              st.toast('유효하지 않은 움직임입니다!')          # 처음 클릭과 두번째 클릭이 같은 경우 
          else:
            st.toast('유효하지 않은 움직임입니다!')            # 아니면 이 문장을 출력해라(말이 잡힌 상태일 때 새로운 말을 만드려는 것을 막기 위해)

  else:
    st.title('바그 찰(Bagh-chal) 게임 - 호랑이')          # 호랑이 차례일 경우
    for i in range(5):                                        # 보드판 생성
      cols = st.columns(5)
      for j in range(5):
        text = st.session_state.board[i][j] or " "
        if cols[j].button(text, key=f"{i}-{j}"):
            clicked_pos = (i, j)

            if st.session_state.click1 is None:               # 호랑이를 선택해야 하는 경우(옮길 말의 좌표가 저장되어있지 않다면)
              if st.session_state.board[i][j] == "🐯":         # 선택한 좌표가 호랑이로 채워져있을 때
                st.session_state.click1 = clicked_pos         # 옮길 호랑이의 좌표를 저장하고
                st.toast("이동할 위치를 선택하세요.")          # 이 문장을 출력해라
              else:
                st.toast("호랑이를 선택하세요.")               # 아니면 이 문장을 출력해라

            # 옮길 위치를 정해야 하는 경우(옮길 곳의 좌표가 저장되어 있지 않고 그 좌표가 현재 호랑이의 좌표와 다르다면)
            elif st.session_state.click2 is None and clicked_pos != st.session_state.click1:
              st.session_state.click2 = clicked_pos           # 옮길 위치의 좌표를 저장하고
              Tiger_move()
          
            else:
              st.toast('유효하지 않은 움직임입니다!')         # 염소의 말이 있는 칸이나 빈 칸을 클릭했을 경우

  st.sidebar.markdown("### 염소 상태 🐐")
  st.sidebar.write("남은 염소:", st.session_state.goat_left)
  st.sidebar.write("잡힌 염소:", st.session_state.catch)
  check()
