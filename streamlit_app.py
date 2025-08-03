import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

st.set_page_config(page_title="AI Tools Finder", layout="wide")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_tfb3estd.json")

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
        transition: transform 0.4s ease, box-shadow 0.4s ease, opacity 0.5s ease;
        opacity: 0;
    }
    .glass-card.show {
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

# Animation of title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st_lottie(lottie_ai, height=200, key="ai_animation")

title_placeholder = st.empty()
title_text = "AI Tools Finder"
typed = ""
for char in title_text:
    typed += char
    title_placeholder.markdown(f"<h1 style='text-align:center'>{typed}</h1>", unsafe_allow_html=True)
    time.sleep(0.05)

# Input field
query = st.text_input(
    "What do you need help with? (e.g. remove background, video editing, coding assistant)",
    key="query",
)

search_clicked = st.button("Find Tools")

if query and not search_clicked:
    # If user presses Enter instead of button
    search_clicked = True

if search_clicked and query:
    with st.spinner("Finding the best tools for you..."):
        time.sleep(0.3)
        try:
            response = requests.post(
                "http://127.0.0.1:8000/recommend",
                json={"query": query},
                timeout=20
            )
            if response.status_code == 200:
                tools = response.json().get("tools", [])
                if tools:
                    cols = st.columns(3)
                    for idx, tool in enumerate(tools):
                        with cols[idx % 3]:
                            card_html = f"""
                                <div class="glass-card show">
                                    <h3>{tool['name']}</h3>
                                    <p><b>Year:</b> {tool['year']}</p>
                                    <p>{tool['strengths']}</p>
                                    <a href="{tool['website']}" target="_blank">Visit</a>
                                </div>
                            """
                            st.markdown(card_html, unsafe_allow_html=True)
                            time.sleep(0.2)  # small delay for fade-in effect
                else:
                    st.warning("No tools found for this topic.")
            else:
                st.error("Backend error. Please try again.")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
