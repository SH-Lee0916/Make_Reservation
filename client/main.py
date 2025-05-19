import streamlit as st
from datetime import date, timedelta

st.title("📅 예약 관리 캘린더")

# 오늘 날짜를 기본값으로 설정
today = date.today()
selected_date = st.date_input("날짜를 선택하세요", today)

st.subheader(f"{selected_date.year}년 {selected_date.month}월 {selected_date.day}일 예약 현황")

# 선택된 날짜에 대한 예약 정보를 보여주는 로직 (API 연동 후 데이터베이스에서 가져올 예정)
# 임시 데이터
reservations = {
    today: ["오전 10시 - 회의", "오후 2시 - 발표 준비"],
    today + timedelta(days=1): ["오후 3시 - 팀 미팅"],
}

if selected_date in reservations:
    for reservation in reservations[selected_date]:
        st.info(f"⏰ {reservation}")
else:
    st.info("선택하신 날짜에는 예약이 없습니다.")

st.subheader("📝 예약 또는 취소")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🗓️ 예약")
    reservation_time = st.time_input("시간 선택", value=None, key="reserve_time")
    reservation_content = st.text_input("예약 내용", key="reserve_content")
    if st.button("예약하기"):
        if reservation_time and reservation_content:
            # 실제 API 호출 로직 필요 (예: requests 라이브러리 사용)
            st.success(f"{selected_date} {reservation_time.strftime('%H:%M')} - {reservation_content} 예약 완료!")
        else:
            st.warning("시간과 내용을 모두 입력해주세요.")

with col2:
    st.subheader("❌ 취소")
    # 해당 날짜의 예약 목록을 보여주고 선택할 수 있도록 (API 연동 후 데이터베이스에서 가져올 예정)
    if selected_date in reservations and reservations[selected_date]:
        reservation_to_cancel = st.selectbox("취소할 예약을 선택하세요", reservations[selected_date], key="cancel_select")
        if st.button("취소하기"):
            # 실제 API 호출 로직 필요 (예: requests 라이브러리 사용)
            st.warning(f"{selected_date} {reservation_to_cancel} 예약이 취소되었습니다.")
    else:
        st.info("취소할 예약이 없습니다.")