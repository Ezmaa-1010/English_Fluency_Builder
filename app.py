import os
import random
import streamlit as st

try:
    from groq import Groq
except ImportError:
    Groq = None

st.set_page_config(page_title="English Fluency Builder", page_icon="📘", layout="wide")

# ---------- Design ----------
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1150px;}
.hero {padding: 1.6rem 1.8rem; border-radius: 18px; background: linear-gradient(120deg,#183b56,#287271); color: white; margin-bottom: 1.2rem;}
.hero h1 {color: white; margin: 0 0 .35rem 0; font-size: 2.2rem;}
.hero p {color: #e8f5f2; margin: 0; font-size: 1.05rem;}
.metric-card {padding: 1rem; border: 1px solid rgba(128,128,128,.25); border-radius: 14px; min-height: 100px;}
.word-card {padding: 1.2rem; border-radius: 16px; border: 1px solid rgba(128,128,128,.25); margin: .5rem 0 1rem 0;}
.small-muted {opacity: .75; font-size: .9rem;}
div.stButton > button {border-radius: 10px; min-height: 2.7rem;}
</style>
""", unsafe_allow_html=True)

WORDS = [
    {"word":"Curious","meaning":"Eager to learn or know about something.","example":"I am curious about how languages work.","options":["Eager to learn","Very tired","Angry"],"answer":"Eager to learn"},
    {"word":"Reliable","meaning":"Able to be trusted or depended on.","example":"A reliable teammate keeps their promises.","options":["Easy to break","Able to be trusted","Always late"],"answer":"Able to be trusted"},
    {"word":"Improve","meaning":"To make or become better.","example":"Ten minutes of practice can improve your English.","options":["Make better","Hide something","Make noisier"],"answer":"Make better"},
    {"word":"Confident","meaning":"Feeling sure about yourself or your abilities.","example":"She felt confident while speaking in class.","options":["Sure of yourself","Sleepy","Confused"],"answer":"Sure of yourself"},
    {"word":"Brief","meaning":"Short in time or length.","example":"We had a brief conversation after class.","options":["Very long","Short in time or length","Very expensive"],"answer":"Short in time or length"},
    {"word":"Consider","meaning":"To think carefully about something.","example":"Consider each answer before choosing.","options":["Think carefully about","Forget completely","Copy quickly"],"answer":"Think carefully about"},
    {"word":"Essential","meaning":"Very important or necessary.","example":"Practice is essential for progress.","options":["Unnecessary","Necessary or very important","Unusual"],"answer":"Necessary or very important"},
    {"word":"Achieve","meaning":"To succeed in reaching a goal.","example":"She worked hard to achieve her goal.","options":["Reach successfully","Give away","Put off"],"answer":"Reach successfully"},
    {"word":"Polite","meaning":"Showing respect and good manners.","example":"It is polite to listen without interrupting.","options":["Rude","Showing good manners","Impatient"],"answer":"Showing good manners"},
    {"word":"Expand","meaning":"To make or become larger.","example":"Reading helps expand your vocabulary.","options":["Make smaller","Make larger","Repeat"],"answer":"Make larger"},
    {"word":"Hesitate","meaning":"To pause before doing or saying something because you are unsure.","example":"Do not hesitate to ask questions.","options":["Pause because you are unsure","Celebrate loudly","Finish quickly"],"answer":"Pause because you are unsure"},
    {"word":"Accurate","meaning":"Correct and without mistakes.","example":"Please provide accurate information.","options":["Correct and without mistakes","Hard to read","Very fast"],"answer":"Correct and without mistakes"},
]
GRAMMAR = [
    {"q":"She ___ to school every day.","options":["go","goes","going"],"answer":"goes","why":"With he, she, or it in the simple present, most verbs take -s or -es: she goes."},
    {"q":"I have lived here ___ 2020.","options":["for","since","during"],"answer":"since","why":"Use since with a starting point (since 2020). Use for with a duration (for three years)."},
    {"q":"They ___ watching a film right now.","options":["is","are","was"],"answer":"are","why":"Use are with they in the present continuous: they are watching."},
    {"q":"If I ___ more time, I would learn French.","options":["have","had","will have"],"answer":"had","why":"The second conditional uses if + past simple, then would + base verb."},
    {"q":"This is the ___ book I have ever read.","options":["more interesting","most interesting","interesting"],"answer":"most interesting","why":"Use the superlative when comparing one item with the whole group: the most interesting."},
    {"q":"He is good ___ mathematics.","options":["at","in","on"],"answer":"at","why":"The usual expression is good at something: good at mathematics."},
    {"q":"We ___ dinner when the phone rang.","options":["had","were having","are having"],"answer":"were having","why":"Use past continuous for an action in progress when another past event happened."},
]

def api_key():
    try:
        value = st.secrets.get("GROQ_API_KEY", "")
        if value:
            return value
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")

def ai_reply(system, prompt):
    key = api_key()
    if not key:
        return None, "Groq API key is missing. Add GROQ_API_KEY in Streamlit → Manage app → Settings → Secrets."
    if Groq is None:
        return None, "Groq package is not installed. Check that requirements.txt contains groq, then reboot the app."
    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            temperature=0.25,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip(), None
    except Exception as exc:
        return None, f"Groq could not answer: {exc}"

def set_default(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

set_default("word_index", 0)
set_default("word_order", list(range(len(WORDS))))
set_default("word_results", {})
set_default("grammar_index", 0)
set_default("grammar_results", {})
set_default("revision_word", random.randrange(len(WORDS)))
set_default("sentence_order", ["because", "I", "practise", "English", "every day"])
set_default("writing_feedback", None)

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <h1>📘 English Fluency Builder</h1>
  <p>Small daily practice. Stronger English. More confidence.</p>
</div>
""", unsafe_allow_html=True)
