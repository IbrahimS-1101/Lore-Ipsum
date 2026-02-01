import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETUP & CONFIG ---
st.set_page_config(
    page_title="Lore Ipsum",
    page_icon="🎲",
    layout="centered"
)

# Invisible Auth
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif os.getenv("GEMINI_API_KEY"):
        api_key = os.getenv("GEMINI_API_KEY")
except:
    pass

# --- 2. HEADER ---
st.title("🎲 Lore Ipsum")
st.caption("The Lorem Ipsum for Game Developers.")

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ NPC Config")
    
    if api_key:
        st.success("✅ System Online")
    else:
        api_key = st.text_input("API Key", type="password")

    st.markdown("---")
    
    genre = st.selectbox(
        "Genre:",
        ["High Fantasy", "Cyberpunk", "Cosmic Horror", "Space Opera", "Modern Noir"]
    )
    
    archetype = st.selectbox(
        "Archetype:",
        ["Shopkeeper", "City Guard", "Quest Giver", "Drunk Patron", "Corrupt Official", "Cultist"]
    )
    
    # NEW: Gender Selector
    gender = st.radio(
        "Gender Identity:",
        ["Any/Random", "Male", "Female", "Non-Binary"]
    )
    
    mood = st.select_slider(
        "Personality:",
        options=["Friendly", "Neutral", "Suspicious", "Hostile", "Terrified"]
    )

# --- 4. THE LOGIC ---
def generate_lore(genre, archetype, gender, mood, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        prompt = f"""
        You are a Game Design Assistant.
        Generate a JSON-style character card for a generic NPC.
        
        Context:
        - Genre: {genre}
        - Role: {archetype}
        - Gender: {gender}
        - Mood: {mood}
        
        Output Requirements:
        1. Name: A generic name fitting the genre and gender.
        2. Bio: A 1-sentence background.
        3. Barks: 3 short lines of dialogue (under 10 words) they shout if clicked.
        4. Quest_Hook: 1 sentence hinting at a task.
        
        Format the output as clean text, not code blocks, but labeled clearly.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 5. MAIN UI ---
st.markdown(f"### Generate Placeholder: **{mood} {archetype}**")

generate_btn = st.button("🎲 Roll NPC", type="primary", use_container_width=True)

if generate_btn and api_key:
    with st.spinner("Rolling stats..."):
        result = generate_lore(genre, archetype, gender, mood, api_key)
        
        # Display as Code Block
        st.code(result, language="yaml")
        st.caption("👆 Copy this block and paste it into your Unity/Godot Inspector.")

elif generate_btn and not api_key:
    st.error("Missing API Key.")

# --- 6. FOOTER & DISCLAIMER ---
st.markdown("---")

# Disclaimer moved to bottom
st.warning(
    """
    **⚠️ Developer Note:** This tool generates **placeholder text** for prototyping, UI testing, and gray-boxing. 
    It is NOT a replacement for professional narrative design. 
    Please support human writers for your final game scripts!
    """,
    icon="🛑"
)

st.markdown("Made with a lot of ☕ by Ibrahim Samir")