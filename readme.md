English Fluency Builder
A beginner-friendly English learning app built with Python, Streamlit, and the Groq API.
Features
- Daily Vocabulary: Learn words, read example sentences, and check your understanding.
- Grammar Correction: Submit a sentence and receive an AI correction with an explanation.
- Grammar Quiz: Practise common grammar patterns even without an API key.
- Sentence Builder: Rearrange words to build a sentence and get feedback on your writing.
- Vocabulary Revision: Test your memory with a random vocabulary question.
- AI Writing Feedback: Get a corrected version of your writing and practical improvement tips.
The vocabulary and quiz activities work without an API key. Groq is required for AI grammar correction and writing feedback.
1. Create the GitHub repository
Create a new repository on GitHub, for example:

english-fluency-builder

Upload these files to the repository root:
- app.py
- requirements.txt
- README.md
2. Get a Groq API key
1. Open the Groq Console: https://console.groq.com/
2. Sign in and create an API key.
3. Keep the key private. Do not paste it directly into app.py or commit it to GitHub.
3. Deploy on Streamlit Community Cloud
1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Select Create app and choose your repository.
3. Set the main file path to app.py.
4. Open the app's Advanced settings / Secrets section.
5. Add this secret, replacing the placeholder with your actual key:
GROQ_API_KEY = "your_actual_groq_api_key"
6. Deploy the app.
If the app is already deployed, open its app settings and add the secret there, then reboot the app.
4. Run locally (optional)
Install Python 3.10 or newer. In a terminal, run:
python -m venv .venv
Activate the environment:

Windows
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate
Install dependencies and start Streamlit:
pip install -r requirements.txt
streamlit run app.py
For local AI features, create .streamlit/secrets.toml with:
GROQ_API_KEY = "your_actual_groq_api_key"
Do not upload secrets.toml to GitHub. Add it to .gitignore.
Optional model setting
The app defaults to llama-3.3-70b-versatile. If that model is not available to your Groq account, set GROQ_MODEL to a currently supported chat model in your deployment environment.
Troubleshooting
- AI feedback says the key is missing: Check that GROQ_API_KEY is set in Streamlit Secrets and restart/reboot the app.
- Groq request failed: Check your internet connection, API key, account limits, and whether the configured model is currently supported.
- App fails during deployment: Check that app.py and requirements.txt are in the repository root and review the Streamlit deployment logs.
- Keep the API key secret: If you accidentally publish it, revoke it in the Groq Console and create a new one.
Project structure
english-fluency-builder/
├── app.py
├── requirements.txt
└── README.md
Note
This is an educational practice tool. AI suggestions can occasionally be incorrect, so learners should compare explanations with trusted learning resources when needed.
