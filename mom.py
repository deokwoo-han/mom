import streamlit as st
import pandas as pd
from datetime import datetime

# 데이터 저장 구조 (문서의 '걱정 모니터링 연습' 일지 양식 반영)
if 'worry_logs' not in st.session_state:
    st.session_state.worry_logs = []

st.title("🧠 심리학 수업: 걱정 치유 프로토타입")
st.markdown("---")

# 1. 머릿속 지나가는 단어 잡기 (훈련 1)
st.subheader("1. 생각 캡처 (Capture)")
keyword = st.text_input("지금 머릿속을 스쳐 지나가는 '단어' 하나를 잡으세요", placeholder="예: 프로젝트, 말실수, 미래")

# 2. 감정 농도 및 신체 감각 (훈련 6, 7)
col1, col2 = st.columns(2)
with col1:
    intensity = st.select_slider("이 생각에 묻어있는 '감정 농도'", options=range(0, 101, 10), value=50)
with col2:
    sensation = st.text_input("느껴지는 신체 감각은?", placeholder="예: 심장 두근거림, 어깨 뭉침")

# 3. 이름표 붙이기 (훈련 3, 4, 5)
st.subheader("2. 이름표 붙이기 (Labeling)")
category = st.radio(
    "이 생각의 정체는 무엇입니까?",
    ["단순한 사실 (Sample A)", "소모적인 걱정 (Sample B)", "과거에 대한 후회/반추", "생산적인 계획"],
    horizontal=True
)

# 4. 제3자의 시선으로 기록 (종합 일지 작성)
st.subheader("3. 관찰자 시점 기록 (Observer View)")
st.caption("거리 두기를 위해 '그(그녀)는 ~라고 생각 중이다'라고 기록하세요.")
observer_log = st.text_area("제3자의 눈으로 현재 상황을 묘사하세요.")

if st.button("걱정 일지에 저장"):
    if keyword and observer_log:
        log_entry = {
            "일시": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "키워드": keyword,
            "농도": f"{intensity}%",
            "신체감각": sensation,
            "분류": category,
            "관찰내용": observer_log
        }
        st.session_state.worry_logs.append(log_entry)
        st.success("일지가 저장되었습니다.")
    else:
        st.warning("키워드와 관찰 내용을 입력해주세요.")

# 5. 걱정 리스트 (종합된 내용 확인)
st.markdown("---")
st.subheader("📂 나의 걱정 모니터링 일지")
if st.session_state.worry_logs:
    for i, log in enumerate(reversed(st.session_state.worry_logs)):
        # 리스트 형식으로 보여주며, 클릭(Expander) 시 상세 내용 출력
        with st.expander(f"📌 {log['일시']} | {log['키워드']} ({log['분류']})"):
            st.write(f"**감정 농도:** {log['농도']}")
            st.write(f"**신체 반응:** {log['신체감각']}")
            st.info(f"**관찰 기록:** {log['관찰내용']}")
else:
    st.write("아직 저장된 일지가 없습니다.")