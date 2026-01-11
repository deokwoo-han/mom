import streamlit as st
import pandas as pd
from datetime import datetime

# --- 페이지 설정 및 디자인 ---
st.set_page_config(page_title="LAMP: 마음 관찰 앱", layout="wide")

# CSS를 이용해 다중 선택 박스를 버튼(태그)처럼 보이게 최적화
st.markdown("""
    <style>
    .stMultiSelect div div div div div {
        background-color: #A3B18A !important;
        color: white !important;
        border-radius: 15px !important;
    }
    .main {
        background-color: #FDFCF8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 베이스 (확장된 리스트) ---
EMOTION_CHIPS = {
    "불안/공포": ["초조함", "안절부절못함", "막연한 불안", "공포", "식은땀 나는 긴장", "압박감", "질식할 것 같음"],
    "분노/짜증": ["욱함", "신경질", "억울함", "냉소적임", "부글부글함", "답답함", "짜증"],
    "슬픔/무력": ["낙담", "허무함", "막막함", "외로움", "우울함", "자괴감", "의욕 없음"],
    "자기비난/수치": ["후회", "죄책감", "민망함", "열등감", "부끄러움", "창피함"]
}

SENSATION_CHIPS = {
    "머리/얼굴": ["두통", "머리가 멍함", "얼굴 화끈거림", "눈의 피로", "턱 근육 긴장"],
    "상체/호흡": ["가슴 답답함", "숨이 가쁨", "심장 두근거림", "목에 이물감", "명치 끝 통증"],
    "근육/사지": ["어깨 결림", "손발 차가움", "손 떨림", "등 근육 긴장", "다리에 힘이 풀림"],
    "소화기계": ["위가 뒤틀림", "복부 팽만감", "메스꺼움", "속쓰림"]
}

if 'journal' not in st.session_state:
    st.session_state.journal = []

# --- 앱 메인 UI ---
st.title("🕯️ LAMP: 내 마음의 이름표")
st.caption("문서 1-2부 기반: 걱정을 객관적으로 분류하고 신체 반응을 기록하세요.")

with st.container():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📍 1. 생각 포착하기")
        thought = st.text_input("지금 머릿속을 스쳐간 생각/단어는?", placeholder="예: 어제 했던 실수...")

        st.subheader("🎭 2. 감정 골라 담기")
        all_selected_emotions = []
        for category, emotions in EMOTION_CHIPS.items():
            selected = st.multiselect(f"[{category}]", emotions)
            all_selected_emotions.extend(selected)
        
        intensity = st.slider("감정의 총 농도 (%)", 0, 100, 50)

    with col2:
        st.subheader("⚡ 3. 신체 감각 체크")
        all_selected_sensations = []
        for category, sensations in SENSATION_CHIPS.items():
            selected = st.multiselect(f"[{category}]", sensations)
            all_selected_sensations.extend(selected)

        st.subheader("🏷️ 4. 이름표 & 관찰")
        label = st.selectbox("생각의 성격 (문서 기반 분류)", ["소모적인 걱정", "과거 반추(되새김)", "실행 가능한 계획", "단순 사실"])
        observer_log = st.text_area("제3자의 시선 (예: 그녀는 지금 과거를 후회 중이다)", height=100)

if st.button("✨ 오늘의 마음 저장하기", use_container_width=True):
    if thought and all_selected_emotions:
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "thought": thought,
            "emotions": all_selected_emotions,
            "intensity": intensity,
            "sensations": all_selected_sensations,
            "label": label,
            "observer": observer_log
        }
        st.session_state.journal.append(entry)
        st.success("걱정 모니터링 일지에 추가되었습니다!")
    else:
        st.error("생각과 감정을 최소 하나 이상 선택해주세요.")

# --- 종합 리스트 확인 (사용자 요청사항) ---
st.divider()
st.subheader("📖 나의 걱정 모니터링 히스토리")
if not st.session_state.journal:
    st.info("아직 기록이 없습니다. 위에서 첫 마음을 기록해보세요.")
else:
    for i, log in enumerate(reversed(st.session_state.journal)):
        # 리스트 중 하나를 누르면 상세 내용이 보이는 Expander 기능
        with st.expander(f"📌 [{log['label']}] {log['thought']} | 농도: {log['intensity']}%"):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**🎭 느낀 감정:**")
                st.write(", ".join(log['emotions']))
                st.write("**⚡ 신체 반응:**")
                st.write(", ".join(log['sensations']) if log['sensations'] else "특이사항 없음")
            with c2:
                st.write("**🕵️ 관찰자 기록 (제3자의 시선):**")
                st.info(log['observer'] if log['observer'] else "기록 없음")