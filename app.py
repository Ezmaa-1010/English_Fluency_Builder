import os
import random
import streamlit as st

try:
    from groq import Groq
except ImportError:
    Groq = None

st.set_page_config(
    page_title="English Fluency Builder",
    page_icon="📘",
    layout="wide",
)

VOCABULARY = [
    {"word": "Curious", "meaning": "Eager to learn or know about something.", "example": "She was curious about how the machine worked.", "options": ["Eager to learn", "Very tired", "Angry with someone"], "answer": "Eager to learn"},
    {"word": "Reliable", "meaning": "Able to be trusted or depended on.", "example": "He is a reliable friend who always keeps his promises.", "options": ["Difficult to understand", "Able to be trusted", "Quick to forget"], "answer": "Able to be trusted"},
    {"word": "Improve", "meaning": "To make or become better.", "example": "Reading every day can improve your vocabulary.", "options": ["Make better", "Make smaller", "Hide something"], "answer": "Make better"},
    {"word": "Confident", "meaning": "Feeling sure about your abilities or yourself.", "example": "Practice helped her feel confident when speaking English.", "options": ["Feeling sure of yourself", "Feeling confused", "Feeling sleepy"], "answer": "Feeling sure of yourself"},
    {"word": "Brief", "meaning": "Short in time or length.", "example": "We had a brief meeting before class.", "options": ["Very noisy", "Short in time or length", "Extremely expensive"], "answer": "Short in time or length"},
    {"word": "Consider", "meaning": "To think carefully about something.", "example": "Please consider all the options before deciding.", "options": ["Think carefully about", "Forget completely", "Speak loudly"], "answer": "Think carefully about"},
    {"word": "Essential", "meaning": "Completely necessary or very important.", "example": "Regular practice is essential for progress.", "options": ["Unusual", "Not needed", "Necessary or very important"], "answer": "Necessary or very important"},
    {"word": "Achieve", "meaning": "To succeed in doing or reaching something.", "example": "She worked hard to achieve her goal.", "options": ["Reach successfully", "Give away", "Delay until later"], "answer": "Reach successfully"},
    {"word": "Polite", "meaning": "Showing respect and good manners.", "example": "It is polite to listen when another person is speaking.", "options": ["Showing good manners", "Very impatient", "Hard to find"], "answer": "Showing good manners"},
    {"word": "Expand", "meaning": "To become larger or make something larger.", "example": "Try to expand your vocabulary by learning five words a day.", "options": ["Make smaller", "Make larger", "Repeat exactly"], "answer": "Make larger"},
]

GRAMMAR_QUESTIONS = [
    {"question": "She ___ to school every day.", "options": ["go", "goes", "going"], "answer": "goes", "explanation": "Use 'goes' with he, she, or it in the simple present tense."},
    {"question": "I have lived here ___ 2020.", "options": ["for", "since", "from"], "answer": "since", "explanation": "Use 'since' with a starting point in time, such as 2020. Use 'for' with a duration, such as three years."},
    {"question": "They ___ watching a movie right now.", "options": ["is", "are", "was"], "answer": "are", "explanation": "Use 'are' with the plural subject 'they' in the present continuous tense."},
    {"question": "If I ___ more time, I would learn another language.", "options": ["have", "had", "will have"], "answer": "had", "explanation": "In this second conditional pattern, use 'if + past simple' followed by 'would + base verb'."},
    {"question": "This is the ___ book I have ever read.", "options": ["more interesting", "most interesting", "interesting"], "answer": "most interesting", "explanation": "Use the superlative 'most interesting' when comparing one thing with all others in a group."},
]

def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")

def ask_groq(system_prompt, user_prompt):
    api_key = get_api_key()
    if not api_key:
        return None, "Add your Groq API key in Streamlit Secrets or as the GROQ_API_KEY environment variable."
    if Groq is None:
        return None, "The Groq package is not installed. Add groq to requirements.txt and redeploy."
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=900,
        )
        return response.choices[0].message.content.strip(), None
    except Exception as exc:
        return None, f"Groq request failed: {exc}"

def init_state():
    defaults = {
        "vocab_index": 0,
        "vocab_order": list(range(len(VOCABULARY))),
        "vocab_answered": {},
        "grammar_index": 0,
        "grammar_answers": {},
        "sentence_words": ["because", "practice", "I", "every day", "improve", "my English"],
        "sentence_feedback": "",
        "daily_seed": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

st.title("📘 English Fluency Builder")
st.write("Build your English skills with short vocabulary, grammar, and writing activities.")
st.caption("You can use the practice activities without an API key. Groq AI is used for personalized grammar correction and writing feedback.")

with st.sidebar:
    st.header("Your practice plan")
    st.write("Try a short activity each day.")
    st.markdown("- 📚 Learn a new word")
    st.markdown("- ✍️ Correct a sentence")
    st.markdown("- 🧩 Build a sentence")
    st.markdown("- 🧠 Revise vocabulary")
    st.divider()
    if get_api_key():
