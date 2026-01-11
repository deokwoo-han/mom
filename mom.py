import streamlit as st
import pandas as pd
from datetime import datetime

# --- 페이지 설정 ---
st.set_page_config(page_title="LAMP: 마음 관찰 일기", layout="wide")

# --- 주황색 테마 커스텀 CSS ---
st.markdown("""
    <style>
    /* 멀티셀렉트 칩 색상 변경 */
    .stMultiSelect div div div div div {
        background-color: #FF8C42 !important;
        color: white !important;
        border-radius: 15px !important;
    }
    /* 버튼 둥글게 */
    div.stButton > button:first-child {
        background-color: #FF8C42;
        color: white;
        border-radius: 20px;
        border: none;
    }
    /* 배경색 부드럽게 */
    .stApp {
        background-color: #FFFBF0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 베이스 (확장된 리스트) ---
EMOTION_CHIPS = {
    "🔥 불안과 공포": ["초조함", "안절부절못함", "막연한 불안", "공포", "식은땀 나는 긴장", "압박감", "질식할 것 같음", "도망치고 싶음", "얼어붙음"],
    "💢 분노와 짜증": ["욱함", "신경질", "억울함", "부글부글함", "답답함", "짜증", "원망", "분개심", "적개심"],
    "🌧️ 슬픔과 무력": ["낙담", "허무함", "막막함", "외로움", "우울함", "자괴감", "의욕 없음", "비참함", "절망감"],
    "🥀 수치와 죄책": ["후회", "죄책감", "민망함", "열등감", "부끄러움", "창피함", "자책", "비굴함"]
}

SENSATION_CHIPS = {
    "🧠 머리와 얼굴": ["두통", "멍함", "얼굴 화끈거림", "눈의 피로", "턱 긴장", "어지러움", "뒷목 당김"],
    "🫁 호흡과 가슴": ["가슴 답답함", "숨 가쁨", "심장 두근거림", "목 이물감", "가슴 통증", "옥죄는 느낌"],
    "💪 근육과 신경": ["어깨 결림", "손발 차가움", "손 떨림", "등 근육 긴장", "다리 힘 풀림", "몸의 떨림", "식은땀"],
    "🤢 위장과 기타": ["위 뒤틀림", "복부 팽만감", "메스꺼움", "속쓰림", "목마름", "입 마름"]
}

if 'journal' not in st.session_state:
    st.session_state.journal = []

# --- 메인 화면 ---
st.title("🍊 LAMP: 마음 이름표 붙이기")
st.info("문서 1-2부 기반: 걱정을 포착하고, 감정의 농도를 측정하며, 제3자의 눈으로 관찰하세요.")

with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 생각 포착 (Catch)")
        thought = st.text_input("지금 머릿속을 지나가는 한 문장/단어는?", placeholder="예: 내가 그때 왜 그런 말을 했을까?")

        st.subheader("2️⃣ 감정 농도 (Intensity)")
        intensity = st.select_slider("지금 느껴지는 감정의 '진하기'는?", options=range(0, 101, 10), value=50)
        
        st.subheader("3️⃣ 감정 고르기 (Feelings)")
        st.caption("해당하는 감정 버튼을 모두 선택하세요.")
        all_selected_emotions = []
        for category, emotions in EMOTION_CHIPS.items():
            selected = st.multiselect(category, emotions)
            all_selected_emotions.extend(selected)

    with col2:
        st.subheader("4️⃣ 신체 감각 (Sensations)")
        st.caption("몸 어디에서 반응이 오나요?")
        all_selected_sensations = []
        for category, sensations in SENSATION_CHIPS.items():
            selected = st.multiselect(category, sensations)
            all_selected_sensations.extend(selected)

        st.subheader("5️⃣ 이름표 & 관찰 (Labeling)")
        label = st.selectbox("이 걱정의 '이름표'를 붙여주세요", ["소모적인 걱정", "과거 반추(되새김)", "실행 가능한 계획", "단순 사실"])
        observer_log = st.text_area("🕵️ 제3자의 시선 (관찰 일기)", 
                                     placeholder="그녀는 지금 상사의 말을 곱씹으며 불안해하고 있다. 하지만 이건 생각일 뿐이다.", height=100)

if st.button("✨ 오늘의 마음 종합 저장하기", use_container_width=True):
    if thought and all_selected_emotions:
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "thought": thought,
            "emotions": all_selected_emotions,
            "intensity": f"{intensity}%",
            "sensations": all_selected_sensations,
            "label": label,
            "observer": observer_log
        }
        st.session_state.journal.append(entry)
        st.success("걱정 모니터링 일지에 성공적으로 저장되었습니다!")
    else:
        st.error("생각과 감정을 최소 하나 이상 선택해주세요.")

# --- 종합 히스토리 ---
st.divider()
st.subheader("📂 나의 마음 관찰 기록")

if not st.session_state.journal:
    st.write("아직 기록이 없습니다.")
else:
    for i, log in enumerate(reversed(st.session_state.journal)):
        # 리스트 중 하나를 클릭하면 상세 내용이 나옴
        with st.expander(f"📌 {log['time']} | {log['thought']} ({log['intensity']})"):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**🏷️ 분류:** {log['label']}")
                st.write("**🎭 선택한 감정들:**")
                st.write(", ".join(log['emotions']))
            with c2:
                st.write("**⚡ 신체 반응:**")
                st.write(", ".join(log['sensations']) if log['sensations'] else "특이사항 없음")
                st.info(f"**🕵️ 관찰자 기록:**\n{log['observer']}")