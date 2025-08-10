import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# ------------------------------
# Load environment & persona
# ------------------------------
load_dotenv()

persona_path = Path("ferro.txt")
if persona_path.exists():
    with open(persona_path, "r", encoding="utf-8") as f:
        ferro_persona = f.read()
else:
    ferro_persona = "I am Ferro, your friendly beagle assistant."

model = init_chat_model("groq:llama-3.1-8b-instant")

# ------------------------------
# Page config
# ------------------------------
st.set_page_config(
    page_title="FerroForever",
    page_icon="1bb97fa1-af63-43bd-bc68-836ccb203d8b.png",
    layout="centered"
)

# ------------------------------
# Custom CSS (Beagle Theme)
# ------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: #5c3a21;
    font-family: 'Poppins', sans-serif;
}}
.logo-container {{
    display: flex;
    justify-content: center;
    margin-bottom: 0.5rem;
}}
.logo-container img {{
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    width: 120px;
    height: 120px;
    object-fit: cover;
}}
h1 {{
    text-align: center;
    color: #ffb347;
    margin-bottom: 2rem;
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Logo & Title
# ------------------------------
with open("1bb97fa1-af63-43bd-bc68-836ccb203d8b.png", "rb") as img_file:
    img_data = img_file.read()
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image(img_data)
st.markdown('</div>', unsafe_allow_html=True)
st.title("Forever")

# ------------------------------
# Chat memory
# ------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ------------------------------
# Chat input
# ------------------------------
prompt = st.chat_input("Say something to Ferro...")

if prompt:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Generate Ferro's reply
    response = model.invoke(f"{ferro_persona}\nUser: {prompt}\nFerro:")
    reply = response.content

    # Append assistant message
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# ------------------------------
# Render all messages (custom)
# ------------------------------
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="background-color:#f4e1c1; padding:10px 15px; border-radius:20px;
                    box-shadow:0 3px 6px rgba(0,0,0,0.2); margin-bottom:10px; color:#5c3a21;">
            🐾 {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#ffe5b4; padding:10px 15px; border-radius:20px;
                    box-shadow:0 3px 6px rgba(0,0,0,0.2); margin-bottom:10px; color:#4b2e19;">
            🐶 {msg['content']}
        </div>
        """, unsafe_allow_html=True)
