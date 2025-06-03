import streamlit as st

def Goat_move(space1, space2):
  i, j = space1
  m, n = space2

  if (abs(i - m) == 1 and j == n) or (i == m and abs(j - n) == 1) or (abs(i - m) == 1 and abs(j - n) == 1):
    if st.session_state.board[m][n] == "":
      st.session_state.board[m][n] = "G"
      st.session_state.board[i][j] = ""
      st.session_state.click1 = None
      st.session_state.click2 = None
      st.session_state.turn = "T"
    else:
      st.toast('유효하지 않은 움직임입니다!')
      st.session_state.click2 = None

def Tiger_move(space1, space2):
  i, j = space1
  m, n = space2

  if (abs(i - m) == 1 and j == n) or (i == m and abs(j - n) == 1) or (abs(i - m) == 1 and abs(j - n) == 1):
    if st.session_state.board[m][n] == "":
      st.session_state.board[m][n] = "T"
      st.session_state.board[i][j] = ""
      st.session_state.click1 = None
      st.session_state.click2 = None
      st.session_state.turn = "G"
    else:
      st.toast('유효하지 않은 움직임입니다!')
      st.session_state.click2 = None

  elif (abs(i - m) == 2 and j == n) or (i == m and abs(j - n) == 2) or (abs(i - m) == 2 and abs(j - n) == 2):
    if st.session_state.board[m][n] == "" and st.session_state.board[(i+m)//2][(j+n)//2] == "G":
      st.session_state.board[i][j] = ""
      st.session_state.board[m][n] = "T"
      st.session_state.board[(i+m)//2][(j+n)//2] = ""
      st.session_state.catch += 1
      st.toast(f"잡은 염소의 수 {st.session_state.catch}")
      st.session_state.click1 = None
      st.session_state.click2 = None
      st.session_state.turn = "G"
    else:
      st.toast('유효하지 않은 움직임입니다!')
      st.session_state.click2 = None

  else:
    st.toast('유효하지 않은 움직임입니다!')
    st.session_state.click2 = None

def check():
  if st.session_state.turn == "G" and st.session_state.catch >= 4:
    st.success("호랑이가 염소를 4마리 잡았습니다! 🐯 호랑이 승리!")
    st.session_state.start = False

  tiger_can_move = False
  for i in range(5):
    for j in range(5):
      if st.session_state.board[i][j] == "T":
        for di in [-2, -1, 0, 1, 2]:
          for dj in [-2, -1, 0, 1, 2]:
            ni, nj = i + di, j + dj
            if 0 <= ni < 5 and 0 <= nj < 5:
              if st.session_state.board[ni][nj] == "":
                if abs(di) <= 1 and abs(dj) <= 1:
                  tiger_can_move = True
                elif abs(di) == 2 or abs(dj) == 2:
                  mid_i, mid_j = (i + ni)//2, (j + nj)//2
                  if st.session_state.board[mid_i][mid_j] == "G":
                    tiger_can_move = True
  if not tiger_can_move:
    st.success("호랑이의 모든 움직임이 막혔습니다! 🐐 염소 승리!")
    st.session_state.start = False

if "start" not in st.session_state:
  st.session_state.start = False

if not st.session_state.start:
  st.title('바그 찰(Bagh-chal) 게임')
  rule = st.selectbox('알고 싶은 것을 골라주세요 : ', ['룰-염소(G)', '룰-호랑이(T)'])
  rule_data = {
    '룰-호랑이(T)' : {
      '말의_개수' : '호랑이는 총 4개',
      '말의_위치' : '게임 시작 시 이미 보드 위에 배치되어 있다.',
      '플레이_방법과_승리조건' : ('인접한 칸으로 이동하거나, 선을 따라 염소를 하나 건너뛰어 잡을 수 있다.''염소를 최소 5마리 이상 잡거나, 끝까지 포위되지 않으면 호랑이가 승리한다.')},
    '룰-염소(G)' : {
      '말의_개수' : '염소는 총 20개',
      '말의_위치' : '차례대로 하나씩 보드에 배치한다.',
      '플레이_방법과_승리조건' : ('모든 염소가 배치된 후에 배치된 염소들을 인접한 칸으로 한 칸씩만 이동할 수 있다.''이때 말을 뛰어넘거나 호랑이를 잡을 수 없다.''호랑이의 움직임을 모두 막으면 염소가 승리한다.')}
  }

  if st.button('룰 설명'):
    if rule in rule_data:
      st.write(f"**말의 개수**: {rule_data[rule]['말의_개수']}")
      st.write(f"**말의 위치**: {rule_data[rule]['말의_위치']}")
      st.write(f"**플레이 방법과 승리조건**: {rule_data[rule]['플레이_방법과_승리조건']}")
      st.write("게임은 염소가 먼저 시작합니다. 말을 움직일 경우엔 움직이고 싶은 말을 클릭하고 움직이고 싶은 위치로 움직이면 됩니다.")

  if st.button('게임 시작'):
    st.session_state.start = True
    st.session_state.turn = "G"
    st.session_state.click1 = None
    st.session_state.click2 = None
    st.session_state.count = 0
    st.session_state.catch = 0
    st.session_state.board = [["" for _ in range(5)] for _ in range(5)]
    st.session_state.board[0][0] = "T"
    st.session_state.board[0][4] = "T"
    st.session_state.board[4][0] = "T"
    st.session_state.board[4][4] = "T"

else:
  if st.session_state.turn == "G":
    st.title('바그 찰(Bagh-chal) 게임 - 염소')
    for i in range(5):
      cols = st.columns(5)
      for j in range(5):
        text = st.session_state.board[i][j] or " "
        if cols[j].button(text, key=f"{i}-{j}"):
          if st.session_state.board[i][j] == "" and st.session_state.count < 20:
            st.session_state.click1 = (i,j)
            st.session_state.board[i][j] = "G"
            st.session_state.count += 1
            st.session_state.turn = "T"
            st.session_state.click1 = None
            st.session_state.click2 = None

          elif st.session_state.board[i][j] == "G" and st.session_state.count == 20:
            clicked_pos = (i, j)
            if st.session_state.click1 is None:
              st.session_state.click1 = clicked_pos
              st.toast("이동할 위치를 선택하세요.")
            elif st.session_state.click2 is None and clicked_pos != st.session_state.click1:
              st.session_state.click2 = clicked_pos
              space1 = st.session_state.click1
              space2 = clicked_pos
              Goat_move(space1, space2)
            else:
              st.toast('유효하지 않은 움직임입니다!')
          else:
            st.toast('유효하지 않은 움직임입니다!')

  else:
    st.title('바그 찰(Bagh-chal) 게임 - 호랑이')
    for i in range(5):
      cols = st.columns(5)
      for j in range(5):
        text = st.session_state.board[i][j] or " "
        if cols[j].button(text, key=f"{i}-{j}"):
            clicked_pos = (i, j)
            if st.session_state.click1 is None:
              if st.session_state.board[i][j] == "T":
                st.session_state.click1 = clicked_pos
                st.toast("이동할 위치를 선택하세요.")
              else:
                st.toast("호랑이를 선택하세요.")
            elif st.session_state.click2 is None and clicked_pos != st.session_state.click1:
              st.session_state.click2 = clicked_pos
              space1 = st.session_state.click1
              space2 = clicked_pos
              Tiger_move(space1, space2)
            else:
              st.toast('유효하지 않은 움직임입니다!')
  check()
