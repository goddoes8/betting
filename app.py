import streamlit as st
import numpy as np
from empiricaldist import Pmf
from scipy.stats import binom
#import matplotlib.pyplot as plt
#from collections import Counter

st.set_page_config(
  page_title='WhoWin',
  page_icon='./images/monsterball.png'
)

#def on_slider_change():
#  #st.session_state.uwsensitivity = float(osensitivity)
#  st.session_state.ufsubmit_triggered = True

class cConfig():
  uwtcntcolumn = 4 # 한화면에 컬럼 개수
  
  
class c톰슨샘플링():
  
  def __init__(self, uwtcntmachine):
    self.vanalysis_machine = []
    self.vanalysis_WL = []

    vkeys = npxs = np.linspace(0, 1, 101)
    vvalues = [1]*len(vkeys)
    self.opmfprior = Pmf(dict(zip(vkeys, vvalues)))
    self.opmfprior.normalize()
    self.diclikelihood = {
        'W': npxs,
        'L': 1-npxs
    }
    self.vopmfbeliefs = [self.opmfprior.copy() for i in range(uwtcntmachine)]

  def Mw_choose(self):
    vps = [b.choice() for b in self.vopmfbeliefs]
    uwidmachine = np.argmax(vps)
    return uwidmachine

  def Ms_play(self, uidmachine, usWL=None):
    #if np.random.rand(1) < vmachinwinprob[uwidmachine]: # 5개의 값 생성  pass
    #  usWL = 'W'
    #else:
    #  usWL = 'L'
    self.vanalysis_machine.append(uidmachine)
    self.vanalysis_WL.append(usWL)
    return uidmachine, usWL
    
  def M_update(self, uidmachine, usWL):
    opmf = self.vopmfbeliefs[uidmachine]
    opmf *= self.diclikelihood[usWL]
    opmf.normalize()
initial_vpokemons = [
    {
        "name": "피카츄",
        "W": 0,
        "L": 0,
        "usjustbeforeWL": '',
        "uwconsecutiveWL": 0,
        "types": ["전기"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/pikachu.webp"
    },
    {
        "name": "누오",
        "W": 0,
        "L": 0,
        "usjustbeforeWL": '',
        "uwconsecutiveWL": 0,
        "types": ["물", "땅"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/nuo.webp",
    },
    {
        "name": "갸라도스",
        "W": 0,
        "L": 0,
        "usjustbeforeWL": '',
        "uwconsecutiveWL": 0,
        "types": ["물", "비행"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/garados.webp",
    },
    {
        "name": "개굴닌자",
        "W": 0,
        "L": 0,
        "usjustbeforeWL": '',
        "uwconsecutiveWL": 0,
        "types": ["물", "악"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/frogninja.webp"
    },
    {
        "name": "루카리오",
        "W": 0,
        "L": 0,
        "usjustbeforeWL": '',
        "uwconsecutiveWL": 0,
        "types": ["격투", "강철"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/lukario.webp"
    },
    {
        "name": "에이스번",
        "W": 0,
        "L": 0,
        "usjustbeforeWL": '',
        "uwconsecutiveWL": 0,
        "types": ["불꽃"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/acebun.webp"
    },
  ]
if "uffirst" not in st.session_state:
  st.session_state.uffirst = False
  type_emoji_dict = {
    "노말": "⚪",
    "격투": "✊",
    "비행": "🕊",
    "독": "☠️",
    "땅": "🌋",
    "바위": "🪨",
    "벌레": "🐛",
    "고스트": "👻",
    "강철": "🤖",
    "불꽃": "🔥",
    "물": "💧",
    "풀": "🍃",
    "전기": "⚡",
    "에스퍼": "🔮",
    "얼음": "❄️",
    "드래곤": "🐲",
    "악": "😈",
    "페어리": "🧚"
  }
  example_pokemon = {
      "name": "알로라 디그다",
      "types": ["땅", "강철"],
      "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/alora_digda.webp"
  }
  
initial_uwtcntmachine = 4 # 시도할 갬블링 대수 
initial_uwsensitivity = 60
initial_uwbettingupperboound = 20

st.title('후윈(WHOWIN)')
st.text('후윈은 복권 또는 갬블링을 할 때 도움의 손길처럼 돈을 따도록 돕는다. 이것만 따라해도 패망할 일은 없다.(WHOWIN helps you win money like a helping hand when playing lottery or gambling. If you just follow this, you will not be bankrupted.)')
st.text('전략은 두가지 이며, 자신의 믿음에 따라 상황에 따라 편하게 선택 한다. 각 기계는 슬롯머신 또는 복권의 칸에 해당한다.(There are two strategies, and you can choose based on your game situation or your own beliefs. Each machine corresponds to a slot machine or a lottery slot.)')
st.text('전략1: 모든 머신은 동일한 터질 확률을 가진다고 믿는다.(Strategy 1: Believe that all machines have the same probability of Win.)\n전략2: 머신 마다 잘 터지는 것이 있고 잘 안터지는 것이 있다고 믿는다.(Strategy 2: Believe that some machines are more likely to Win)')

# 상태를 관리할 변수 선언
if "vpokemons" not in st.session_state:
  st.session_state.uwtcntmachine = initial_uwtcntmachine
  st.session_state.uwsensitivity = initial_uwsensitivity
  st.session_state.uwbettingupperboound = initial_uwbettingupperboound
  st.session_state.vpokemons = initial_vpokemons
  st.session_state.uwtcntbetting = 0
  st.session_state.ot = c톰슨샘플링(initial_uwtcntmachine)
  st.session_state.submit_triggered = False
  st.session_state.change_triggered = False

# 값 변경 이벤트 핸들러
def on_slider_change_tcntmachine():
  #st.session_state.uwtcntmachine = int(otcntmachine)
  st.session_state.submit_triggered = True  # 값 변경 시 submit 트리거 활성화

def on_slider_change_sensitivity():
  #st.session_state.uwsensitivity = int(osensitivity)
  st.session_state.change_triggered = True  # 값 변경 시

def on_slider_change_tcntbetting():
  st.session_state.change_triggered = True  # 값 변경 시


cols001 = st.columns([2, 1])  # col1은 좁고 col2는 넓게 설정
with cols001[0]:
  st.markdown("**기계 댓수 설정** (Set the number of machines):")  # 텍스트 레이블 (기울임 효과)
with cols001[1]:
  #otcntmachine = st.number_input(label="",min_value=1, max_value=10, value=st.session_state.uwtcntmachine, step=1)
  otcntmachine = st.select_slider("",options=[str(uu) for uu in range(1,10)],value=str(st.session_state.uwtcntmachine), on_change=on_slider_change_tcntmachine, label_visibility="visible")
  
cols002 = st.columns([2, 1])  # col1은 좁고 col2는 넓게 설정
with cols002[0]:
  st.markdown("**꼭 돈을 따려면 높여라** (If you want to make money, raise it):")  # 텍스트 레이블 (기울임 효과)
with cols002[1]:
  osensitivity = st.select_slider("",options=["55","60","70","80","90","95",],value=str(st.session_state.uwsensitivity), on_change=on_slider_change_sensitivity, label_visibility="visible")

cols003 = st.columns([2, 1])  # col1은 좁고 col2는 넓게 설정
with cols003[0]:
  st.markdown("**총 몇번 베팅할 것인가?** (How many times will you bet in total?):")  # 텍스트 레이블 (기울임 효과)
with cols003[1]:
  obettingupperboound = st.select_slider("",options=["20","50","100","200","1000",],value=str(st.session_state.uwbettingupperboound), on_change=on_slider_change_tcntbetting, label_visibility="visible")

#with st.form(key='formreal'):
#  submit = st.form_submit_button(label='저장(머신세팅및초기화)')
  
#if submit or st.session_state.submit_triggered:
if st.session_state.submit_triggered:
  st.session_state.uwtcntmachine = int(otcntmachine)
  st.session_state.uwsensitivity = int(osensitivity)
  st.session_state.uwbettingupperboound = int(obettingupperboound)  
  st.session_state.submit_triggered = False
  st.session_state.vpokemons = initial_vpokemons  
  st.session_state.uwtcntbetting = 0
  st.session_state.ot = c톰슨샘플링(st.session_state.uwtcntmachine)
  st.rerun()

if st.session_state.change_triggered:
  st.session_state.uwsensitivity = int(osensitivity)
  st.session_state.uwbettingupperboound = int(obettingupperboound)  
  st.session_state.change_triggered = False  # 값 변경 시
  st.rerun()

  
st.subheader('게임 시작')
st.text("""머신을 다른 사람이 하는 것을 보면서 W/L을 입력한다. 나도 하면서 W/L을 입력한다.
            * p<.05이면 95%< 신뢰
            * 전략1 & p<.05 & .5<Wratio => L에배팅
            * 전략1 & p<.05 & .5<Lratio => W에배팅
            * 전략2 & p<.05 & .5<Wratio => W에배팅 
            * 전략2 & p<.05 & .5<Lratio => L에배팅
        """)

for i in range(0, st.session_state.uwtcntmachine, cConfig.uwtcntcolumn):
  vrow_pokemons = st.session_state.vpokemons[i:min(i+cConfig.uwtcntcolumn, st.session_state.uwtcntmachine)]
  ocols01 = st.columns(cConfig.uwtcntcolumn)
  for j in range(len(vrow_pokemons)):
    with ocols01[j]:
      uidmachine = i+j
      st.text(f'machine{uidmachine}')
      ocols02 = st.columns(2)
      with ocols02[0]:
        obuttonwin = st.button(label='W i n', key='w'+str(uidmachine))
        if obuttonwin:
          uidmachine, usWL = st.session_state.ot.Ms_play(uidmachine, usWL='W')
          st.session_state.ot.M_update(uidmachine, usWL)
          st.session_state.vpokemons[uidmachine]["W"] += 1
          if st.session_state.vpokemons[uidmachine]["usjustbeforeWL"] == "W":
            st.session_state.vpokemons[uidmachine]["uwconsecutiveWL"] += 1
          else:
            st.session_state.vpokemons[uidmachine]["usjustbeforeWL"] = "W"
            st.session_state.vpokemons[uidmachine]["uwconsecutiveWL"] = 1
          st.session_state.uwtcntbetting += 1
          st.rerun()
      with ocols02[1]:
        obuttonlos = st.button(label='Loss', key='l'+str(uidmachine))
        if obuttonlos:
          uidmachine, usWL = st.session_state.ot.Ms_play(uidmachine, usWL='L')
          st.session_state.ot.M_update(uidmachine, usWL)
          st.session_state.vpokemons[uidmachine]["L"] += 1
          if st.session_state.vpokemons[uidmachine]["usjustbeforeWL"] == "L":
            st.session_state.vpokemons[uidmachine]["uwconsecutiveWL"] += 1
          else:
            st.session_state.vpokemons[uidmachine]["usjustbeforeWL"] = "L"
            st.session_state.vpokemons[uidmachine]["uwconsecutiveWL"] = 1
          st.session_state.uwtcntbetting += 1
          st.rerun()
        
      #ocols03 = st.columns(1)
      pokemon = vrow_pokemons[j]
      st.image(pokemon["image_url"])
      udw = pokemon["W"]
      udl = pokemon["L"]
      udt = udw+udl
      udwratio = udw/udt if udt > 0 else 0
      udlratio = udl/udt if udt > 0 else 0
      udp20 = min(0.999, binom.cdf(min(udw, udl), udt, p=0.5)*2)
      st.text(f"""W:{udw} L:{udl}
              Wratio: {udwratio:.3f}
              Lratio: {udlratio:.3f}
              p-value: {udp20:.3f}
              """)
      if 60 < st.session_state.uwsensitivity: # 승패에 예민한 사람
        if udp20 < .05 and 0.55 < udwratio:
          st.text('V전략1이라면 L에 배팅하세요')
        if udp20 < .05 and 0.55 < udlratio:
          st.text('V전략1이라면 W에 배팅하세요')

        if udp20 < .05 and 0.55 < udwratio:
          st.text('V전략2이라면 W에 배팅하세요')
        if udp20 < .05 and 0.55 < udlratio:
          st.text('V전략2이라면 L에 배팅하세요')
          
      else: # 승패보단 많이 해보고 싶은 사람
        if udp20 < .1 and 0.55 < udwratio:
          st.text('V전략1이라면 L에 배팅하세요')
        if udp20 < .1 and 0.55 < udlratio:
          st.text('V전략1이라면 W에 배팅하세요')

        if udp20 < .1 and 0.55 < udwratio:
          st.text('V전략2이라면 W에 배팅하세요')
        if udp20 < .1 and 0.55 < udlratio:
          st.text('V전략2이라면 L에 배팅하세요')


      uwbettingupperboound = st.session_state.uwbettingupperboound
      uwtcntbetting = st.session_state.uwtcntbetting
      uwconsecutiveWL = pokemon["uwconsecutiveWL"]
      udpconsecutiveWL = (0.5)**uwconsecutiveWL
      st.text(f"""연속성기준
      연속횟수: {uwconsecutiveWL}
      연속확률: {udpconsecutiveWL:.3}
      이보다작으면배팅: {1.0/float(uwbettingupperboound):.4}""")
      if udpconsecutiveWL < 1.0/float(uwbettingupperboound):
        if pokemon["usjustbeforeWL"] == "W":
          st.text("V전략1 일시 L에 배팅")
        else:
          st.text("V전략1 일시 W에 배팅")
          


uidnextbettingmachine = st.session_state.ot.Mw_choose()
st.text(f'전략2일 것 같은데 적당히 이익극대화를 하고 싶다면 다음에 배팅할 기계는(If you want to maximize your profits with Strategy 2, the next machine to bet on is): machine {uidnextbettingmachine}')
st.text('어느 기계에 더 많이 베팅했지(Which machine has been used)?')
df1 = Pmf.from_seq(st.session_state.ot.vanalysis_machine)
df1.columns = ['machineid','W per machine']
st.table(df1)
st.text('내가 전반적으로 잘하고 있나(Am I doing well in general)?')
df2 = Pmf.from_seq(st.session_state.ot.vanalysis_WL)
df2.columns = ['WL','Total ratio']
st.table(df2)

#with st.expander(label='검증해 보기', expanded=True):
#  st.subheader('검증')

