import streamlit as st
from google import genai
import tempfile
import time
from textblob import TextBlob

# ------------------------
# 🔑 API KEY
# ------------------------
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))  
models = client.models.list()
for m in models:
    print("Model name:", m.name)
    print("Supported actions:", m.supported_actions)
    print("---")
# ------------------------
# 🎤 Transcribe Audio
# ------------------------

import time

def transcribe_audio(file, retries=3):
    for i in range(retries):
        try:
            file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(file.read())
                temp_path = temp_audio.name

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=["Generate a transcript of the speech.", client.files.upload(file=temp_path)]
            )
            return response.text

        except Exception as e:
            if i < retries - 1 and "503" in str(e):
                time.sleep(5)  # wait and retry
            else:
                return f"❌ Transcription Error: {e}"


# ------------------------
# 🧠 Analyze Interview
# ------------------------
def analyze_interview(text):
    # Simple local analysis: sentiment + summary
    blob = TextBlob(text)
    sentiment = blob.sentiment
    word_count = len(blob.words)
    return f"Sentiment: {sentiment}\nWord count: {word_count}"

# ------------------------
# 🎨 STREAMLIT UI
# ------------------------
st.title("🎤 AI Interview Analyzer (Simplified)")

st.write("Upload an audio clip to transcribe and analyze your interview.")

audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a", "mpeg"])

if audio_file:
    st.audio(audio_file)

    if "transcript" not in st.session_state:
        st.session_state.transcript = ""

    if st.button("Transcribe Audio"):
        st.info("⏳ Transcribing...")
        st.session_state.transcript = transcribe_audio(audio_file)
        st.success("✅ Transcription Complete")

        if st.session_state.transcript:
           st.subheader("📝 Transcript")
           st.write(st.session_state.transcript)

      


