import streamlit as st
import google.generativeai as genai

# 페이지 기본 설정
st.set_page_config(
    page_title="캠퍼스 리더십 튜터", 
    page_icon="👑", 
    layout="wide"
)

# 사이드바: API Key 입력 및 정보
st.sidebar.title("🔑 API 설정")
api_key = st.sidebar.text_input(
    "Google Gemini API Key 입력", 
    type="password", 
    help="https://aistudio.google.com/ 에서 발급받은 API 키를 입력하세요."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👑 캠퍼스 리더십 튜터")
st.sidebar.caption("대학생을 위한 맞춤형 리더십 학습 플랫폼")

# API 키 입력 안내 경고
if not api_key:
    st.warning("⚠️ 왼쪽 사이드바에 Google Gemini API Key를 입력하셔야 모든 AI 학습 기능을 이용하실 수 있습니다.")
    st.info("👉 API Key 발급 방법: [Google AI Studio](https://aistudio.google.com/)에서 무료로 발급받으실 수 있습니다.")

# Gemini API 설정 및 모델 초기화
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        # 요구사항에 명시된 exact model name 사용
        model = genai.GenerativeModel("gemini-3.5-flash-lite")
    except Exception as e:
        st.error(f"API 키 설정 중 오류가 발생했습니다: {e}")

# 탭 구성 (3가지 핵심 기능)
tab1, tab2, tab3 = st.tabs([
    "🎯 리더십 유형 자가 진단",
    "🎭 캠퍼스 리더십 시나리오 롤플레잉",
    "💬 1:1 리더십 AI 튜터"
])

# ---------------------------------------------------------
# Tab 1: 리더십 유형 자가 진단
# ---------------------------------------------------------
with tab1:
    st.header("🎯 리더십 유형 자가 진단")
    st.write("다음 5가지 문항에 답하고 자신의 주된 리더십 스타일과 Gemini AI의 맞춤형 분석 리포트를 확인해보세요!")
    
    with st.form("leadership_quiz"):
        q1 = st.radio("1. 팀 프로젝트 중 과제 방향성에 대해 의견 충돌이 발생했을 때 나는?", [
            "모든 팀원의 의견을 경청하고 다수결 또는 합의점을 찾는다. (민주적 리더)",
            "팀원들의 개별 성장을 돕고 동기를 부여하며 이끈다. (서번트 리더)",
            "명확한 비전을 제시하고 변화와 혁신을 주도한다. (변혁적 리더)",
            "빠르게 상황을 판단하여 유연하고 신속하게 의사결정을 내린다. (민첩한 리더)"
        ])
        
        q2 = st.radio("2. 무임승차 팀원이 발생했을 때 나의 대처 방식은?", [
            "팀 전체 회의에서 역할을 재조정하고 소통으로 해결한다. (민주적 리더)",
            "해당 팀원과 1:1 면담을 통해 개인적 어려움이 있는지 들어주고 도와준다. (서번트 리더)",
            "프로젝트의 목표와 의미를 재상기시키며 열정을 다시 불어넣는다. (변혁적 리더)",
            "체크리스트와 기한을 명확히 재설정하여 즉각적인 행동을 유도한다. (민첩한 리더)"
        ])
        
        q3 = st.radio("3. 팀 목표 달성을 위해 가장 중요하다고 생각하는 것은?", [
            "팀원 전체의 협력과 수평적인 소통 (민주적 리더)",
            "팀원 개개인의 역량 강화와 신뢰 관계 (서번트 리더)",
            "도전적인 목표 설정과 영감을 주는 리더십 (변혁적 리더)",
            "신속한 실행력과 상황 변화에 대한 적응력 (민첩한 리더)"
        ])
        
        q4 = st.radio("4. 의사결정을 내릴 때 주로 의존하는 기준은?", [
            "팀원들의 집단 지성과 투표 결과 (민주적 리더)",
            "팀원들이 유기적으로 일할 수 있는 환경과 필요사항 (서번트 리더)",
            "장기적인 비전과 혁신적인 가능성 (변혁적 리더)",
            "현재 피드백 데이터와 실시간 상황 변화 (민첩한 리더)"
        ])
        
        q5 = st.radio("5. 프로젝트 완료 후 팀원들에게 가장 듣고 싶은 말은?", [
            ""덕분에 모두의 의견이 반영된 멋진 결과를 만들었어요!" (민주적 리더)",
            ""팀장님 덕분에 많이 배우고 성장할 수 있었어요!" (서번트 리더)",
            ""선배/동기님의 열정과 비전에 큰 자극을 받았어요!" (변혁적 리더)",
            ""위기 상황에서도 빠르고 유연하게 대처해서 멋졌어요!" (민첩한 리더)"
        ])
        
        submitted = st.form_submit_button("진단 결과 및 AI 분석 받기", type="primary")

    if submitted:
        answers = [q1, q2, q3, q4, q5]
        scores = {"민주적 리더": 0, "서번트 리더": 0, "변혁적 리더": 0, "민첩한 리더": 0}
        
        for ans in answers:
            if "(민주적 리더)" in ans:
                scores["민주적 리더"] += 1
            elif "(서번트 리더)" in ans:
                scores["서번트 리더"] += 1
            elif "(변혁적 리더)" in ans:
                scores["변혁적 리더"] += 1
            elif "(민첩한 리더)" in ans:
                scores["민첩한 리더"] += 1

        dominant_style = max(scores, key=scores.get)
        
        st.markdown("---")
        st.success(f"🎉 당신의 주 리더십 유형은 **[{dominant_style}]** 입니다!")
        
        # 유형별 점수 시각화
        st.subheader("📊 리더십 성향 분석")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("민주적 리더", f"{scores['민주적 리더']}점")
        col2.metric("서번트 리더", f"{scores['서번트 리더']}점")
        col3.metric("변혁적 리더", f"{scores['변혁적 리더']}점")
        col4.metric("민첩한 리더", f"{scores['민첩한 리더']}점")

        st.markdown("---")
        st.subheader("🤖 Gemini API 맞춤형 리더십 리포트")
        
        if model:
            with st.spinner("Gemini API가 맞춤형 리더십 분석 리포트를 생성하고 있습니다..."):
                prompt = f"""
당신은 대학생 전문 리더십 교육 전문가입니다.
다음 학생의 리더십 자가 진단 결과를 분석하고 맞춤형 피드백 리포트를 작성해주세요.

- 주 리더십 유형: {dominant_style}
- 진단 세부 응답: {answers}

리포트 구성 요망 (마크다운 포맷):
1. 🌟 {dominant_style}의 핵심 강점과 가치
2. ⚠️ 대학 생활(조별 과제, 동아리 등)에서 경계해야 할 주의점
3. 🚀 리더십 역량을 한 단계 더 높이기 위한 3가지 실천 행동 팁
"""
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"AI 리포트 생성 중 오류가 발생했습니다: {e}")
        else:
            st.info("💡 사이드바에 API Key를 입력하시면 Gemini AI의 심층 분석 리포트를 받아보실 수 있습니다.")

# ---------------------------------------------------------
# Tab 2: 시나리오 롤플레잉
# ---------------------------------------------------------
with tab2:
    st.header("🎭 캠퍼스 리더십 시나리오 롤플레잉")
    st.write("대학 생활에서 흔히 겪는 리더십 갈등 상황에 어떻게 대처할지 작성해보고, AI의 맞춤형 코칭과 모의 점수를 받아보세요.")

    scenario = st.selectbox("실습할 상황 시나리오를 선택하세요:", [
        "1. 조별 과제에서 아무도 의견을 내지 않고 참여하지 않을 때",
        "2. 팀원이 정해진 기한을 계속 어기고 연락이 두절될 때",
        "3. 동아리 행사를 앞두고 두 팀원의 의견이 팽팽하게 대립할 때"
    ])

    if scenario.startswith("1."):
        st.info("📌 **상황**: 발표 일주일 전, 팀 카톡방에 질문을 올리고 의견을 요청해도 아무도 답하지 않고 읽기만 하는 상황입니다.")
    elif scenario.startswith("2."):
        st.info("📌 **상황**: 제출 마감이 당장 내일인데, 중요한 자료 조사를 맡은 팀원이 카톡을 읽지 않고 전화도 받지 않습니다.")
    else:
        st.info("📌 **상황**: 동아리 축제 메인 부스 컨셉을 두고 두 핵심 부원이 서로 양보 없이 대립하여 분위기가 매우 경색되었습니다.")

    user_response = st.text_area(
        "✍️ 당신이라면 이 상황에서 리더로서 어떻게 말하고 행동하시겠습니까?", 
        height=150, 
        placeholder="예: 단톡방에 다시 독촉하기보다는 개별 메시지로 1:1 연락을 취하여 부담을 덜어줄 수 있는 구체적인 선택지를 제시하겠습니다..."
    )

    if st.button("AI 코칭 및 평가 받기", type="primary"):
        if not user_response.strip():
            st.warning("대처 방안을 작성해주세요.")
        elif not model:
            st.error("AI 피드백을 받으시려면 사이드바에 Gemini API Key를 입력해주셔야 합니다.")
        else:
            with st.spinner("Gemini API가 대처 방안을 다각도로 분석 중입니다..."):
                eval_prompt = f"""
당신은 대학생을 위한 친절하고 날카로운 리더십 코치입니다.
선택된 캠퍼스 시나리오: {scenario}
학생의 대처 방안: {user_response}

다음 양식에 맞춰 한국어로 분석 피드백을 제공해주세요:

### 👏 칭찬할 점 (Strengths)
- 대처 방안에서 나타난 훌륭한 리더십 태도 및 접근법

### 💡 보완할 점 (Areas for Improvement)
- 놓쳤거나 더 명확히 개선하면 좋을 부분

### 🚀 추천 행동 팁 (Actionable Advice)
- 실제 캠퍼스 현장에서 적용 가능한 한 단계 더 발전된 구체적 대화법/행동 가이드

### 💯 리더십 지수 평가 (100점 만점)
- 점수: [점수]/100점
- 총평: [한 줄 피드백]
"""
                try:
                    res = model.generate_content(eval_prompt)
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"피드백 분석 중 오류가 발생했습니다: {e}")

# ---------------------------------------------------------
# Tab 3: 1:1 리더십 AI 튜터 (Chatbot)
# ---------------------------------------------------------
with tab3:
    st.header("💬 1:1 리더십 AI 튜터")
    st.write("조별 과제, 동아리 운영, 팀원과의 갈등 대화법 등 리더십과 관련된 고민을 자유롭게 나누세요.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 대학생을 위한 리더십 AI 튜터입니다. 👑
조별 과제 팀장 역할을 맡게 되었거나, 팀원들과의 소통에 어려움이 있다면 무엇이든 편하게 물어보세요!"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("리더십 관련 질문을 입력하세요 (예: 팀원이 약속한 기한을 어겼을 때 기분 나쁘지 않게 제촉하는 법)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not model:
            with st.chat_message("assistant"):
                st.error("대화를 이어가시려면 사이드바에 Gemini API Key를 입력해주셔야 합니다.")
        else:
            with st.chat_message("assistant"):
                with st.spinner("답변을 작성하고 있습니다..."):
                    system_prompt = """
당신은 대학생들을 유쾌하고 명확하게 지도하는 리더십 멘토입니다.
대학 생활의 맥락(조별과제, 동아리, 학생회, 대외활동)에 맞춰 실용적이고 공감대 높은 조언을 제공하세요.
답변은 읽기 쉽게 이모지와 불렛포인트, 마크다운 체계를 잘 활용하세요.
"""
                    full_prompt = f"{system_prompt}\n\n[학생 질문]: {prompt}"
                    try:
                        chat_res = model.generate_content(full_prompt)
                        reply = chat_res.text
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"답변 생성 중 오류가 발생했습니다: {e}")
