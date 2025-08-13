import streamlit as st
import pandas as pd
import random
from datetime import date

# -----------------------------
# Page Config & Theming
# -----------------------------
st.set_page_config(
    page_title="일본어 · 일본문화 안내", 
    page_icon="🇯🇵", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Subtle CSS for a friendlier look
st.markdown(
    """
    <style>
        .main > div {
            padding-top: 1.5rem;
        }
        .hero {
            padding: 2rem 2rem;
            background: linear-gradient(135deg, rgba(255,99,132,0.08), rgba(54,162,235,0.08));
            border-radius: 18px;
            border: 1px solid rgba(120,120,120,0.15);
        }
        .tag {
            display: inline-block; padding: 0.25rem 0.6rem; border-radius: 999px; font-size: 0.8rem;
            background: rgba(255,255,255,0.6); border: 1px solid rgba(120,120,120,0.25); margin-right: .4rem;
        }
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
st.sidebar.title("📚 일본어·일본문화")
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
    "수준": ["초급", "중급", "심화"],
    "학습 목표": [
        "히라가나·가타카나 습득, 기초 인사·자기소개",
        "기본 문형 확장, 상황별 회화(가게, 길찾기 등)",
        "프로젝트형 과제, JLPT·말하기 대회 준비"
    ],
    "평가": [
        "퀴즈·말하기(쇼텔), 포트폴리오",
        "역할극·듣기, 수행평가",
        "프로젝트 발표, 포트폴리오·성찰일지"
    ]
})

culture_df = pd.DataFrame({
    "테마": [
        "사계절 문화", "전통·예술", "생활·요리", "대중문화"
    ],
    "예시 활동": [
        "봄 사쿠라·단오/여름 우치와·풍령·테루테루보즈/가을 단풍·달맞이/겨울 신년문화",
        "종이접기·서예·와가시 색칠·전통놀이(켄다마)",
        "오니기리 모형·젓가락 매너·빈티지 포장 디자인",
        "애니·J-POP 가사 읽기·지역 PR 영상 제작"
    ],
})

calendar_df = pd.DataFrame({
    "월": [f"{m}월" for m in range(3, 13)],
    "핵심 주제": [
        "학기 OT·히라가나",
        "가타카나·인사말",
        "자기소개·취미",
        "학교생활·동아리",
        "가게·주문·가격",
        "길찾기·교통",
        "일본 축제·여름 문화(풍령·테루테루보즈)",
        "가정·초대·선물",
        "계절과 날씨·단풍",
        "연말 정리·프로젝트 발표",
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
    "정중 표현": ["お願いします", "すみません"]
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
            <h1>🇯🇵 일본어 & 일본문화 과목 안내</h1>
            <p class='big'>한 번 배워두면 평생 쓰는 언어, 그리고 재미있는 문화 체험까지!<br> 
            모든 학생이 <b>쉽고 즐겁게</b> 시작할 수 있도록 준비했습니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric'><div class='emoji'>🗣️</div><b>회화 중심</b><br><span class='small-muted'>롤플레이·실전 표현</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='metric'><div class='emoji'>🎎</div><b>문화 체험</b><br><span class='small-muted'>만들기·프로젝트</span></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric'><div class='emoji'>🧭</div><b>진로 연계</b><br><span class='small-muted'>관광·콘텐츠·통번역</span></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric'><div class='emoji'>🏆</div><b>성취 지원</b><br><span class='small-muted'>JLPT·말하기 대회</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("오늘의 한 마디 · 今日のひとこと")
    day_phrases = [
        ("よろしくお願いします", "잘 부탁드립니다"),
        ("はじめまして", "처음 뵙겠습니다"),
        ("ありがとうございます", "감사합니다"),
        ("がんばって！", "힘내!"),
    ]
    # Rotate by date
    idx = date.today().toordinal() % len(day_phrases)
    jp, kr = day_phrases[idx]
    st.markdown(f"### {jp}  ")
    st.caption(f"{kr}")


def page_why():
    st.header("왜 일본어를 배울까요?")
    st.write(
        "일본어는 한국어와 어순이 비슷하고 한자를 공유해 **초반 진입 장벽이 낮은 언어**입니다.\n"
        "콘텐츠·관광·비즈니스 분야에서 활용도가 높고, 교류 활동으로 **국제 감각**을 기를 수 있습니다."
    )
    a,b = st.columns(2)
    with a:
        st.markdown(
            """
            <div class='card'>
            <h4>학습 장점</h4>
            <ul>
              <li>한글과 어순 유사 → 문장 만들기 쉬움</li>
              <li>말하기·듣기 위주 수업 → 실전 즉시 활용</li>
              <li>짧은 기간에도 성취 체감 ↑</li>
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
                - 인사·소개: おはよう / こんにちは / わたしはOOです
                - 가게·주문: これをください / いくらですか
                - 길찾기: 駅はどこですか / 右・左・まっすぐ
                - 취미: 音楽が好きです / サッカーをします
                """
            )
        st.info("평가: 수행 중심(역할극·프로젝트)과 성찰 포트폴리오 비중을 높입니다.")

    with t2:
        st.subheader("일본문화")
        st.dataframe(culture_df, use_container_width=True)
        st.markdown(
            "- 대표 활동 예시: 풍령 만들기, 테루테루보즈, 와시츠(다다미) 모형, 젓가락 매너, 지역 PR 영상 제작 등"
        )
        st.success("문화 과목은 협업 프로젝트로 마무리합니다: ‘우리 동네 일본문화 전시’ or ‘한·일 문화카드 아카이브’.")


def _new_quiz_question():
    k, v = random.choice(list(hiragana.items()))
    # Create 3 wrong options
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
            if intent == "인사" and name:
                out = f"{item}、{name}さん！"
            else:
                out = item
            st.success(out)
            st.caption("복사해서 친구에게 사용해 보세요!")

    with t3:
        st.subheader("미니 단어장")
        words = pd.DataFrame({
            "日本語": ["ありがとう", "ごめんなさい", "ください", "いくら", "たのしい"],
            "한국어": ["고마워", "미안해", "주세요", "얼마", "즐겁다"],
            "발음": ["arigatou", "gomen nasai", "kudasai", "ikura", "tanoshii"],
        })
        st.dataframe(words, hide_index=True, use_container_width=True)


def page_activities():
    st.header("수업 활동")
    st.markdown(
        """
        - **롤플레이**: 가게 주문, 길 묻기, 소개하기 등 실전 대화 연습
        - **문화 만들기**: 풍령·테루테루보즈·와시츠 모형 등 만들기 활동
        - **프로젝트**: 일본 지역 PR, 한·일 문화 비교 카드, 학교생활 브이로그(스크립트 일본어)
        - **교류 활동**: 온라인 국제교류(자기소개·학교소개·문화 소개)
        - **평가**: 과정 중심 평가(참여도·협업·발표)와 포트폴리오
        """
    )

    st.info("교류 학교와 연계하여 ‘공민(사회)’ 주제를 접목한 토론 활동도 설계합니다: 지역 문제, 환경, 문화 다양성 등.")


def page_calendar():
    st.header("행사·캘린더")
    st.dataframe(calendar_df, hide_index=True, use_container_width=True)
    st.markdown(
        """
        **주요 행사**
        - 5월: 일본어 말하기 챌린지(클래스 영상 릴레이)
        - 7월: 여름 문화 주간(풍령·우치와)
        - 9~10월: 온라인 국제교류(학교·지역 소개)
        - 12월: 종합 프로젝트 전시회
        """
    )


def page_faq():
    st.header("FAQ & 문의")
    with st.expander("일본어가 처음인데 따라갈 수 있나요?"):
        st.write("네. 히라가나부터 단계적으로 배우며, 말하기 활동으로 자신감을 키웁니다.")
    with st.expander("일본문화 과목은 어떤가요?"):
        st.write("만들기·체험 중심으로 즐겁게 배우며, 결과물을 전시·공유합니다.")
    with st.expander("평가가 부담스럽진 않나요?"):
        st.write("과정 중심으로 참여·협업·발표를 중시합니다. 작은 성취를 꾸준히 쌓아요.")
    with st.expander("진로에 도움이 되나요?"):
        st.write("콘텐츠·관광·국제교류 등 다양한 진로와 연결됩니다.")

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
st.caption("© 일본어·일본문화 과목 안내 — 모두가 즐겁게 배우는 수업을 지향합니다.")
