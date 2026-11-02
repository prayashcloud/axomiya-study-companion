import json
import os
import re

from openai import OpenAI

BASE_URL = "https://bharatcode.ai/api/model/v1"
MODEL = "qwen-3.8-27b"

SYSTEM = (
    "You are a patient tutor for school students in Assam following the SEBA / AHSEC "
    "syllabus. Use simple words, short sentences, and everyday examples from Assam "
    "(rivers, tea gardens, paddy fields, Bihu). Never invent facts. "
    "When replying in Assamese, use standard Assamese (Axomiya) spelling and vocabulary, "
    "not Bengali. For example, write 'হৈ', not 'হে'."
)


def _chat(prompt):
    client = OpenAI(api_key=os.environ["BHARATCODE_API_KEY"], base_url=BASE_URL)
    reply = client.chat.completions.create(
        model=MODEL,
        max_tokens=8000,
        extra_body={"reasoning_effort": "none"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
    )
    choice = reply.choices[0]
    text = choice.message.content or ""
    if not text:
        raise RuntimeError(
            f"The model sent an empty answer (finish_reason: {choice.finish_reason}). Please try again."
        )
    return text


def explain(topic, subject, language):
    text = _chat(
        f"Subject: {subject}. Topic: {topic}. Reply in {language}. "
        "Explain in 3 parts: (1) the idea in 3-4 simple sentences, "
        "(2) one local Assam example, (3) the 3 most important points for exams."
    )
    return text or "(No answer came back. Please try again.)"


def make_quiz(topic, subject, language, n=3):
    raw = _chat(
        f"Subject: {subject}. Topic: {topic}. Write {n} multiple-choice questions in {language}. "
        "Return ONLY a JSON array with no other text. Each item must look like: "
        '{"question": "...", "options": ["...", "...", "...", "..."], '
        '"answer_index": 0, "why": "one short sentence"}.'
    )
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        raise ValueError("The quiz came back in the wrong format. Please click Quiz me again.")
    quiz = json.loads(match.group(0))
    good = [
        q for q in quiz
        if len(q.get("options", [])) == 4 and q.get("answer_index") in (0, 1, 2, 3)
    ]
    if not good:
        raise ValueError("No usable questions came back. Please click Quiz me again.")
    return good


def grade(quiz, answers):
    """Plain code, no AI. Scores are exact."""
    details = []
    for q, a in zip(quiz, answers):
        right = q["options"][q["answer_index"]]
        details.append({"correct": a == right, "right": right, "why": q.get("why", "")})
    return {
        "score": sum(d["correct"] for d in details),
        "total": len(quiz),
        "details": details,
    }