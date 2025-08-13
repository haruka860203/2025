import streamlit as st
import pandas as pd
import random
from datetime import date

# -----------------------------
# Page Config & Theming
# -----------------------------
st.set_page_config(
    page_title="고2 일본어 · 일본문화 안내",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Subtle CSS for a friendlier look
st.markdown(
    """
    <style>
        .main > div { padding-top: 1.5rem; }
        .hero {
            padding: 2rem 2rem;
            background: linear-gradient(135deg, rgba(255,99,132,0.08), rgba(54,162,235,0.08));
            border-radius: 18px;
            border: 1px solid rgba(120,120,120,0.15);
        }
        .tag { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 999px; font-size: 0.8rem;
               background: rgba(255,255,255,0.6); border: 1px solid rgba(120,120,120,0.25); margin-right: .4rem; }
        .card {border:1px solid rgba(120,120,120,0.2); border-radius: 16px; padding: 1rem; background: rgba(255,255,255,0.65)}
        .metric {text-align:center; border:1px solid rgba(120,120,120,0.2); border-radius: 16px; padding: 1rem; background: white}
        .emoji {font-size: 1.9rem}
        .small-muted {color:#666; font-size:0.9rem}
        .center {text-align:center}
        .big {font-size:1.2rem}
        footer {visibility: hidden;}
        .quiz-correct{background:#ecfdf5;border:1px solid #10b981;color:#065f46;padding:.6rem;border-radius:10px}
        .quiz-wrong{background:#fef2f2;border:1px solid #ef4444;color:#7f1d1d;padding:.6rem;border-radius:10px}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📚 고2 일본어·일본문화")
nav = st.sidebar.radio(
    "빠르게 이동",
    (
        "홈 Home",
        "왜 일본어?",
        "과목 소개",
        "수업 활동",
        "미니 학습도구",
        "행사·캘린더",
        "FAQ & 문의",
    ),
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("교사: 일본어과 / 문의: teacher@example.com")

# -----------------------------
# Helper Data
# -----------------------------
levels_df = pd.DataFrame({
    "수준": ["기초 다지기(고2)", "실전 회화·문형 확장(고2)", "심화·진로 연계(고2)"],
    "학습 목표": [
        "히라가나·가타카나 완성, 기초 회화 리마인드, 자기소개·학교소개 업그레이드",
        "경어(존경·겸양) 기초, 면접·전화·이메일 표현, 상황별 문제 해결 대화",
        "프로젝트 프레젠테이션, 공민 이슈 토론 일본어, JLPT N3~N2 대비"
    ],
    "평가": [
        "퀴즈·말하기, 성찰 포트폴리오",
        "역할극·면접 시뮬, 협업 과제",
        "프로젝트 발표·리서치 보고서·포트폴리오"
    ]
})

culture_df = pd.DataFrame({
    "테마": [
        "사계절 문화", "전통·예술", "생활·요리", "현대사회·대중문화"
    ],
    "예시 활동": [
        "봄 사쿠라·여름 축제·가을 단풍·겨울 신년문화 심화 리서치",
        "종이접기·서예·와가시 디자인 + 전시 큐레이션",
        "오니기리·벤토 문화 분석, 젓가락 매너 캠페인 영상",
        "애니·J-POP 가사 읽기, 일본 미디어 리터러시, 지역 PR 영상 제작"
    ],
})

calendar_df = pd.DataFrame({
    "월": [f"{m}월" for m in range(3, 13)],
    "핵심 주제": [
        "학기 OT·목표 설정·자기소개(리더십)",
        "경어 기초·정중 표현(면접·전화)",
        "학교생활·동아리 PR 스피치",
        "가게·알바 표현·가격·전화 주문",
        "진로 탐색·이메일·자기소개서 문형",
        "공민 연계 토론: SDGs·지역 문제",
        "여름 문화 주간·국제교류 준비",
        "지역 조사·인터뷰 기획(온라인 교류)",
        "프레젠테이션 스킬·데이터 시각화",
        "포트폴리오·말하기 종합 평가",
    ],
})

# Kana quiz data (small, extendable)
hiragana = {
    "あ":"a","い":"i","う":"u","え":"e","お":"o",
    "か":"ka","き":"ki","く":"ku","け":"ke","こ":"ko",
    "さ":"sa","し":"shi","す":"su","せ":"se","そ":"so",
    "た":"ta","ち":"chi","つ":"tsu","て":"te","と":"to",
    "な":"na","に":"ni","ぬ":"nu","ね":"ne","の":"no",
}

phrases = {
    "인사": ["おはよう", "こんにちは", "こんばんは"],
    "감사": ["ありがとう", "ありがとうございます"],
    "정중 표현": ["お願いします", "すみません"],
    "경어": ["よろしくお願いいたします", "失礼いたします", "お世話になっております"],
}

if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = {
        "current": None,
        "options": [],
        "score": 0,
        "count": 0,
        "history": []
    }

# -----------------------------
# Page Components
# -----------------------------

def page_home():
    st.markdown(
        f"""
        <div class='hero'>
            <div class='tag'>제2외국어</div>
            <div class='tag'>일본어</div>
            <div class='tag'>일본문화</div>
            <div class='tag'>고2 맞춤</div>
            <h1>🇯🇵 고2 일본어 & 일본문화 과목 안내</h1>
            <p class='big'>대학·진로를 준비하는 시기에 맞춰 <b>실전 회화와 프로젝트</b>를 강화했어요.<br>
            모두가 <b>자신 있게 말하고 발표</b>할 수 있도록 설계했습니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric'><div class='emoji'>🗣️</div><b>실전 회화</b><br><span class='small-muted'>면접·전화·이메일</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric'><div class='emoji'>🎎</div><b>문화·연구</b><br><span class='small-muted'>리서치·전시</span></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric'><div class='emoji'>🧭</div><b>진로 연계</b><br><span class='small-muted'>콘텐츠·관광·통번역</span></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric'><div class='emoji'>🏆</div><b>성취 지원</b><br><span class='small-muted'>JLPT N3~N2</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("오늘의 한 마디 · 今日のひとこと")
    day_phrases = [
        ("よろしくお願いいたします", "잘 부탁드립니다(경어)"),
        ("お世話になっております", "늘 신세지고 있습니다(비즈니스)"),
        ("失礼いたします", "실례하겠습니다(격식)"),
        ("ありがとうございます", "감사합니다"),
    ]
    idx = date.today().toordinal() % len(day_phrases)
    jp, kr = day_phrases[idx]
    st.markdown(f"### {jp}  ")
    st.caption(f"{kr}")


def page_why():
    st.header("왜 일본어를 배울까요?")
    st.write(
        "고2는 진로를 구체화하는 시기입니다. 일본어는 한국어와 어순이 비슷해 **단기간 성취**를 느끼기 쉽고,\n"
        "콘텐츠·관광·비즈니스까지 활용도가 높아 **대학·취업 포트폴리오**에 강점이 됩니다."
    )
    a,b = st.columns(2)
    with a:
        st.markdown(
            """
            <div class='card'>
            <h4>학습 장점</h4>
            <ul>
              <li>한글과 어순 유사 → 문장 생성이 쉬움</li>
              <li>면접·전화·이메일 등 실제 상황 훈련</li>
              <li>프로젝트 결과물을 포트폴리오로 전환</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            """
            <div class='card'>
            <h4>진로 연계</h4>
            <ul>
              <li>관광·항공 서비스, 무역·유통</li>
              <li>게임·애니·음악 등 콘텐츠 산업</li>
              <li>통번역·국제교류·해외대학 진학</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_courses():
    st.header("과목 소개")
    t1, t2 = st.tabs(["일본어(제2외국어)", "일본문화"])
    with t1:
        st.subheader("일본어(제2외국어)")
        st.dataframe(levels_df, use_container_width=True)
        with st.expander("단원별 핵심 표현 예시 보기"):
            st.markdown(
                """
                - 인사·경어: お世話になっております / よろしくお願いいたします
                - 면접: 志望動機は〜です / 強みは〜です
                - 전화·가게: 〜をお願いします / いくらですか / 予約できますか
                - 이메일: いつもお世話になっております。〜についてお問い合わせいたします。
                """
            )
        st.info("평가: 수행 중심(면접 롤플레이·프로젝트)과 성찰 포트폴리오 비중을 높입니다.")

    with t2:
        st.subheader("일본문화")
        st.dataframe(culture_df, use_container_width=True)
        st.markdown(
            "- 대표 활동 예시: 풍령 만들기, 테루테루보즈, 와시츠 모형, 젓가락 매너 캠페인, 지역 PR 영상 제작 등"
        )
        st.success("문화 과목은 협업 프로젝트로 마무리: ‘우리 학교·지역 일본문화 전시’ 또는 ‘공민 이슈 일본어 카드뉴스’.")


def _new_quiz_question():
    k, v = random.choice(list(hiragana.items()))
    wrong = random.sample([x for x in hiragana.values() if x != v], 3)
    options = wrong + [v]
    random.shuffle(options)
    st.session_state.quiz_state.update({
        "current": k,
        "options": options,
    })


def page_tools():
    st.header("미니 학습도구")
    t1, t2, t3 = st.tabs(["히라가나 퀴즈", "표현 조합기", "미니 단어장"])

    with t1:
        st.subheader("히라가나 → 로마자")
        if st.session_state.quiz_state["current"] is None:
            _new_quiz_question()
        q = st.session_state.quiz_state["current"]
        options = st.session_state.quiz_state["options"]
        st.markdown(f"### 글자: **{q}**")
        choice = st.radio("발음을 고르세요", options, index=None, horizontal=True)
        if st.button("정답 확인/제출", use_container_width=True):
            if choice is None:
                st.warning("선택지를 골라 주세요!")
            else:
                st.session_state.quiz_state["count"] += 1
                correct = hiragana[q]
                if choice == correct:
                    st.session_state.quiz_state["score"] += 1
                    st.markdown("<div class='quiz-correct'>✅ 정답! 잘했어요!</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='quiz-wrong'>❌ 아쉬워요. 정답은 <b>{correct}</b> 입니다.</div>", unsafe_allow_html=True)
                st.session_state.quiz_state["history"].append((q, choice, correct))
                _new_quiz_question()
        st.caption(f"점수: {st.session_state.quiz_state['score']} / 시도: {st.session_state.quiz_state['count']}")
        if st.session_state.quiz_state["history"]:
            with st.expander("풀이 기록 보기"):
                for i, (k, c, ans) in enumerate(st.session_state.quiz_state["history"], 1):
                    st.write(f"{i}. {k} → {ans} (선택: {c})")

    with t2:
        st.subheader("상황별 표현 조합기")
        col1, col2 = st.columns(2)
        with col1:
            intent = st.selectbox("상황", list(phrases.keys()))
        with col2:
            item = st.selectbox("표현", phrases[intent])
        name = st.text_input("이름을 입력(선택):", "")
        if st.button("문장 만들기"):
            if intent in ("인사", "경어") and name:
                out = f"{item}、{name}さん！"
            else:
                out = item
            st.success(out)
            st.caption("복사해서 친구에게 사용해 보세요!")

    with t3:
        st.subheader("미니 단어장")
        words = pd.DataFrame({
            "日本語": ["ありがとう", "ごめんなさい", "ください", "いくら", "たのしい", "面接", "予約", "履歴書"],
            "한국어": ["고마워", "미안해", "주세요", "얼마", "즐겁다", "면접", "예약", "이력서"],
            "발음": ["arigatou", "gomen nasai", "kudasai", "ikura", "tanoshii", "mensetsu", "yoyaku", "rirekisho"],
        })
        st.dataframe(words, hide_index=True, use_container_width=True)


def page_activities():
    st.header("수업 활동")
    st.markdown(
        """
        - **롤플레이**: 알바 면접, 전화 문의, 가게 주문, 길 안내 등 실전 대화
        - **문화 만들기**: 풍령·테루테루보즈·와시츠 모형 + 전시 기획
        - **프로젝트**: 일본 지역/기업 PR, 공민 이슈(환경·고령화·관광) 인포그래픽 제작
        - **교류 활동**: 온라인 국제교류(학교·지역 소개, 공동 토론, 인터뷰)
        - **평가**: 과정 중심(참여·협업·문제해결) + 프레젠테이션·포트폴리오
        """
    )

    st.info("고2 수준에 맞춰 공민(사회) 주제를 심화 연결합니다: 지역 문제·환경·다양성·디지털 시민성 등으로 토론·발표를 진행합니다.")


def page_calendar():
    st.header("행사·캘린더")
    st.dataframe(calendar_df, hide_index=True, use_container_width=True)
    st.markdown(
        """
        **주요 행사**
        - 5월: 일본어 면접·스피치 챌린지
        - 7월: 여름 문화 주간(풍령·우치와) + 교류 준비
        - 9~10월: 온라인 국제교류(지역·공민 주제 토론)
        - 12월: 종합 프로젝트 전시·포트폴리오 리뷰
        """
    )


def page_faq():
    st.header("FAQ & 문의")
    with st.expander("일본어가 처음인데 따라갈 수 있나요?"):
        st.write("네. 기초 리마인드 후 고2 수준 표현·경어로 확장합니다. 개별 보충도 제공해요.")
    with st.expander("일본문화 과목은 어떤가요?"):
        st.write("만들기·리서치·전시까지 이어지는 프로젝트형 수업으로 심화 학습이 가능합니다.")
    with st.expander("평가가 부담스럽진 않나요?"):
        st.write("과정 중심 평가로 성장 과정을 기록합니다. 발표·협업 능력도 반영해요.")
    with st.expander("진로에 도움이 되나요?"):
        st.write("콘텐츠·관광·서비스·국제교류·통번역 등 다양한 진로와 연결되며 JLPT N3~N2 대비에도 도움이 됩니다.")

    st.markdown("---")
    st.subheader("문의")
    with st.form("contact"):
        name = st.text_input("이름")
        q = st.text_area("질문/하고 싶은 말")
        submitted = st.form_submit_button("보내기")
        if submitted:
            st.success("문의가 임시로 제출되었습니다. (데모) 수업 시간에 교사에게 직접 문의해 주세요!")

# -----------------------------
# Router
# -----------------------------
if nav == "홈 Home":
    page_home()
elif nav == "왜 일본어?":
    page_why()
elif nav == "과목 소개":
    page_courses()
elif nav == "수업 활동":
    page_activities()
elif nav == "미니 학습도구":
    page_tools()
elif nav == "행사·캘린더":
    page_calendar()
else:
    page_faq()

# Footer note
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("© 고2 일본어·일본문화 과목 안내 — 실전 회화·프로젝트로 자신감을 키웁니다.")
