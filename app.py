import streamlit as st
from harness import explain, make_quiz, grade

st.title("📘 Axomiya Study Companion")

ss = st.session_state
for k, v in [("explanation", None), ("quiz", None), ("result", None), ("topic", ""), ("weak", [])]:
    ss.setdefault(k, v)

subject = st.text_input("Subject", "General Science")
language = st.radio("Language", ["Assamese", "English"])
topic = st.text_input("What do you want to learn?", placeholder="e.g. Photosynthesis")

try:
    if st.button("Explain it") and topic:
        with st.spinner("Thinking..."):
            ss.explanation = explain(topic, subject, language)
        ss.topic, ss.quiz, ss.result = topic, None, None

    if ss.explanation:
        st.markdown(ss.explanation)
        if st.button("Quiz me"):
            with st.spinner("Writing questions..."):
                ss.quiz = make_quiz(ss.topic, subject, language)
            ss.result = None

    if ss.quiz:
        st.subheader("Quick quiz")
        answers = [
            st.radio(f"Q{i + 1}. {q['question']}", q["options"], index=None, key=f"q{i}_{ss.topic}")
            for i, q in enumerate(ss.quiz)
        ]
        if st.button("Submit answers"):
            ss.result = grade(ss.quiz, answers)
            if ss.result["score"] < ss.result["total"] * 0.67:
                if ss.topic not in ss.weak:
                    ss.weak.append(ss.topic)
            elif ss.topic in ss.weak:
                ss.weak.remove(ss.topic)

    if ss.result:
        r = ss.result
        st.success(f"Score: {r['score']} / {r['total']}")
        for i, d in enumerate(r["details"]):
            st.write(f"{'✅' if d['correct'] else '❌'} Q{i + 1}: {d['right']}. {d['why']}")

    if ss.weak:
        st.warning("Topics to revise: " + ", ".join(ss.weak))
except Exception as e:
    st.error(f"Something went wrong: {e}")