
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="머니핏 | 금융생활 진단",
    page_icon="💰",
    layout="wide"
)

st.title("💰 MONEYFIT")
st.caption("나의 금융 습관을 진단하고 저축 목표를 세워보세요.")

st.subheader("1. 나의 월간 금융 정보")

col1, col2, col3 = st.columns(3)

with col1:
    income = st.number_input(
        "월 소득 (만원)",
        min_value=0, value=250, step=10
    )

with col2:
    fixed = st.number_input(
        "월 고정지출 (만원)",
        min_value=0, value=70, step=5
    )

with col3:
    variable = st.number_input(
        "월 변동지출 (만원)",
        min_value=0, value=80, step=5
    )

monthly_saving = st.number_input(
    "현재 월 저축액 (만원)",
    min_value=0, value=50, step=5
)

st.subheader("2. 나의 저축 목표")

col4, col5 = st.columns(2)

with col4:
    target = st.number_input(
        "목표 금액 (만원)",
        min_value=1, value=600, step=50
    )

with col5:
    current = st.number_input(
        "현재 모은 금액 (만원)",
        min_value=0, value=300, step=10
    )

# 금융 현황 계산
total_expense = fixed + variable
remaining = income - total_expense - monthly_saving
saving_rate = (
    monthly_saving / income * 100 if income > 0 else 0
)

# 목표 달성 기간 계산
needed = max(target - current, 0)

if needed == 0:
    months = 0
elif monthly_saving > 0:
    months = -(-needed // monthly_saving)
else:
    months = None

st.divider()
st.subheader("3. 금융생활 진단 결과")

a, b, c, d = st.columns(4)

a.metric("월 총지출", f"{total_expense:,.0f}만 원")
b.metric("월 저축률", f"{saving_rate:.1f}%")
c.metric("월 잔여금액", f"{remaining:,.0f}만 원")
d.metric("목표까지 남은 금액", f"{needed:,.0f}만 원")

if remaining < 0:
    st.warning("현재 입력 기준으로 지출과 저축액이 소득을 초과합니다.")
elif income == 0:
    st.info("월 소득을 입력하면 금융 현황을 분석할 수 있습니다.")
else:
    st.success("입력한 금융 정보를 바탕으로 분석했습니다.")

st.subheader("4. 월간 자금 배분")

if income > 0:
    chart_data = pd.DataFrame({
        "항목": ["고정지출", "변동지출", "저축", "잔여금액"],
        "금액": [
            fixed,
            variable,
            monthly_saving,
            max(remaining, 0)
        ]
    })

    st.bar_chart(
        chart_data.set_index("항목"),
        y="금액"
    )

st.subheader("5. 저축 목표 분석")

if needed == 0:
    st.success("축하합니다! 목표 금액을 달성했습니다.")
elif months is None:
    st.info("월 저축액을 입력하면 목표 달성 기간을 계산합니다.")
else:
    st.write(f"현재 저축액을 유지하면 약 **{int(months)}개월** 후 목표에 도달합니다.")
    st.write(
        f"목표 달성을 위해 필요한 월평균 저축액: "
        f"**{needed / 12:,.1f}만 원** (12개월 기준)"
    )

st.caption(
    "본 서비스는 사용자가 입력한 예시 정보를 바탕으로 계산합니다. "
    "투자·대출·예금 가입에 관한 확정적인 금융 자문은 제공하지 않습니다."
)
