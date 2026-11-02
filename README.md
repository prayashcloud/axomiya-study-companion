# 📘 Axomiya Study Companion

An AI study companion for SEBA / AHSEC students in Assam, built for the BharatCode Build League.

Most AI study tools answer in English with generic examples. Axomiya Study Companion explains topics in simple Assamese, with local examples, and turns learning into a loop:

1. **Explain:** simple explanation, one Assam example, 3 key exam points
2. **Quiz:** 3 multiple-choice questions on the topic
3. **Grade:** answers are marked in plain Python code (not by the AI), so scores are always exact
4. **Track:** low-scoring topics are flagged as "topics to revise"

## How it uses BharatCode
All explanations and quiz questions come from BharatCode's `qwen-3.8-27b` model through its OpenAI-compatible API.

## Run it yourself
1. Install the packages: `pip install -r requirements.txt`
2. Get a key from https://bharatcode.ai/account and set it (PowerShell): `$env:BHARATCODE_API_KEY="your-key"`
3. Start the app: `streamlit run app.py`

## Files
- `app.py`: the Streamlit interface
- `harness.py`: prompts, quiz generation and grading
- `BharatCode.txt`: hackathon entry file

Built with Python, Streamlit and the BharatCode API.