import streamlit as st

# 시작 화면
st.title('바그 찰(Bagh-chal) 게임')

# 게임의 시작 조건 정의
if "start" not in st.session_state:
  st.session_state.start = False

# 게임이 시작하기 전 화면에서 실행
if not st.session_state.start:
  rule = st.selectbox('알고 싶은 것을 골라주세요 : ', ['룰-염소(G)', '룰-호랑이(T)'])
  rule_data = {
    '룰-호랑이(T)' : {
                  '말의_개수' :  '호랑이는 총 4개', 
                  '말의_위치' : '게임 시작 시 이미 보드 위에 배치되어 있다.',
                  '플레이_방법과_승리조건' : ('인접한 칸으로 이동하거나, 선을 따라 염소를 하나 건너뛰어 잡을 수 있다.' 
                  '염소를 최소 5마리 이상 잡거나, 끝까지 포위되지 않으면 호랑이가 승리한다.')},
    '룰-염소(G)' : {
                  '말의_개수' : '염소는 총 20개', 
                  '말의_위치' : '차례대로 하나씩 보드에 배치한다.',
                  '플레이_방법과_승리조건' : ('모든 염소가 배치된 후에 배치된 염소들을 인접한 칸으로 한 칸씩만 이동할 수 있다.' 
                  '이때 말을 뛰어넘거나 호랑이를 잡을 수 없다.' '호랑이의 움직임을 모두 막으면 염소가 승리한다.')}
              }
  
  if st.button('룰 설명'):
    if rule in rule_data:
      말의_개수 = rule_data[rule]['말의_개수']
      말의_위치 = rule_data[rule]['말의_위치']
      플레이_방법과_승리조건 = rule_data[rule]['플레이_방법과_승리조건']
  
      st.write(f"**말의 개수**: {말의_개수}")
      st.write(f"**말의 위치**: {말의_위치}")
      st.write(f"**플레이 방법과 승리조건**: {플레이_방법과_승리조건}")
      st.write("게임은 염소가 먼저 시작합니다.")
      
  # 게임 시작하고 보드게임 판, 클릭유무, 차례 저장
  if st.button('게임 시작'):
    st.session_state.start = True
    st.session_state.board = [["" for _ in range(5)] for _ in range(5)]
    st.session_state.board[0][0] = "T"
    st.session_state.board[0][4] = "T"
    st.session_state.board[4][0] = "T"
    st.session_state.board[4][4] = "T"
    st.session_state.turn = "G"
    st.session_state.click = None

else:
  # 차례 안내
  if st.sessoion_state.turn=="G":
    st.title('바그 찰(Bagh-chal) 게임 - 염소 차례')
  else:
    st.title('바그 찰(Bagh-chal) 게임 - 호랑이 차례')

  # 보드판 생성(위에서 한 것은 값의 저장용, 이것은 보이게 해주는 코드)
  for i in range(5):
    cols = st.columns(5)
    for j in range(5):
      text = st.session_state.boardgame[i][j] or " "
      cols[j].button(text, key=f"{i}-{j}")
      if cols[j].button(text,key=f"{i}-{j}"):
        st.session_state.click = (i,j)
        if st.session_state.boardgame[i][j] == " ":
          st.session_state.boardgame[i][j] = "G"
        else:
          st.title('유효하지 않은 움직임입니다!')
        st.session_state.turn = "T"
