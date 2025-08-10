import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# ------------------------------
# Load Ferro's persona
# ------------------------------
persona_path = Path("ferro.txt")
if persona_path.exists():
    with open(persona_path, "r", encoding="utf-8") as f:
        ferro_persona = f.read()
else:
    ferro_persona = "I am Ferro, your friendly beagle assistant."

# ------------------------------
# LangChain + Groq setup
# ------------------------------
load_dotenv()
model = init_chat_model("groq:llama-3.1-8b-instant")

# ------------------------------
# Page config
# ------------------------------
st.set_page_config(
    page_title="Forever",
    page_icon="1bb97fa1-af63-43bd-bc68-836ccb203d8b.png",
    layout="centered"
)

# ------------------------------
# Custom CSS
# ------------------------------
st.markdown("""
<style>
body {
    background-color: #5c3625;
}
[data-testid="stChatMessage"][class*="user"] {
    background-color: #a35d40 !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px;
}
[data-testid="stChatMessage"][class*="assistant"] {
    background-color: transparent !important;
    color: #ff9933 !important; /* Beagle orange */
    font-weight: 500;
    padding: 10px 0;
}
div[data-baseweb="textarea"] {
    background-color: white !important;
    color: black !important;
    border-radius: 8px;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# Logo and title
st.image("1bb97fa1-af63-43bd-bc68-836ccb203d8b.png", width=120)
st.markdown("<h1 style='color:#ff9933;text-align:center;'>Ferro Forever</h1>", unsafe_allow_html=True)

# ------------------------------
# Session state
# ------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [SystemMessage(content=ferro_persona)]

# ------------------------------
# Display chat history
# ------------------------------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").markdown(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").markdown(msg.content)

# ------------------------------
# Chat input
# ------------------------------
if prompt := st.chat_input("Say something to Ferro..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Generate reply using Groq model
    reply = model.invoke(st.session_state.messages)
    
    st.chat_message("assistant").markdown(reply.content)
    st.session_state.messages.append(AIMessage(content=reply.content))
