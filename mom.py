import streamlit as st
import pandas as pd
from datetime import datetime

# --- 디자인 커스텀 (CSS) ---
st.markdown("""
    <style>
    /* 전체 폰트 및 배경 부드럽게 */
    .stApp {
        background-color: #F8F9FA;
    }
    /* 버튼 디자인 변경 */
    div.stButton > button:first-child {
        background-color: #76BA99;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
    }
    /* 입력창 테두리 둥글게 */
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_ Harris=True)


# --- 데이터 소스: 문서 기반 리스트 ---
EMOTIONS = ["불안함", "초조함", "두려움", "죄책감", "무력감", "짜증남", "막막함", "슬픔", "후회", "창피함"]
SENSATIONS = ["가슴 답답함", "심장 두근거림", "목에 이물감", "어깨/목 긴장", "배아픔/소화불량", "손발 차가움", "머리 무거움", "얕은 호흡"]
CATEGORIES = ["소모적인 걱정 (통제 불가)", "과거 반추 (후회)", "생산적인 계획 (해결 가능)", "단순한 사실"]

# 데이터 저장소
if 'worry_db' not in st.session_state:
    st.session_state.worry_db = []

st.title("🕯️ LAMP 마음 치유 일기")

# --- 1단계: 생각 포착 ---
st.subheader("1. 지금 잡힌 단어")
word = st.text_input("머릿속에 떠오른 그 단어는?", placeholder="예: 어제 했던 말, 내일 발표...")

# --- 2단계: 감정 고르기 (멀티 선택) ---
st.subheader("2. 어떤 감정들이 묻어있나요?")
selected_emotions = st.multiselect("리스트에서 모두 골라주세요", EMOTIONS)

# 감정 농도 (슬라이더)
intensity = st.select_slider("감정의 총 농도", options=range(0, 101, 10), value=50)

# --- 3단계: 신체 감각 고르기 ---
st.subheader("3. 몸의 어디가 반응하나요?")
selected_sensations = st.multiselect("느껴지는 신체 감각을 골라주세요", SENSATIONS)

# --- 4단계: 이름표 및 관찰 ---
st.subheader("4. 이름표 붙이기 & 관찰자 기록")
category = st.selectbox("생각의 이름표", CATEGORIES)
observer_text = st.text_area("제3자의 시선으로 기록 (그/그녀는~)", placeholder="그는 지금 불안을 관찰하고 있다...")

if st.button("일지에 저장하기"):
    if word and selected_emotions:
        new_log = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "word": word,
            "emotions": ", ".join(selected_emotions),
            "intensity": f"{intensity}%",
            "sensations": ", ".join(selected_sensations),
            "category": category,
            "observer": observer_text
        }
        st.session_state.worry_db.append(new_log)
        st.success("오늘의 마음을 저장했습니다.")
    else:
        st.error("단어와 감정을 최소 하나 이상 선택해주세요.")

st.divider()

# --- 5단계: 리스트 확인 (사용자 요청사항) ---
st.subheader("📂 나의 걱정 모니터링 기록")
if not st.session_state.worry_db:
    st.caption("저장된 기록이 없습니다.")
else:
    for i, log in enumerate(reversed(st.session_state.worry_db)):
        # 클릭하면 상세 내용이 나오는 구조
        with st.expander(f"📌 {log['date']} | {log['word']} ({log['intensity']})"):
            st.write(f"**🏷️ 이름표:** {log['category']}")
            st.write(f"**🎭 담긴 감정:** {log['emotions']}")
            st.write(f"**⚡ 신체 감각:** {log['sensations']}")
            st.info(f"**🕵️ 관찰 기록:** {log['observer']}")