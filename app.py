import os
import time
import tempfile
from pathlib import Path

import streamlit as st
import google.generativeai as genai
from google.generativeai import upload_file, get_file
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

########################################
# Streamlit Sidebar for Key Selection
########################################
st.sidebar.title("API Key Configuration")

# User selects whether to use their own key or .env
key_source = st.sidebar.radio(
    "Choose API Key Source:",
    options=["Use my own key", "Load key from .env"],
    index=0
)

# Initialize API_KEY variable
API_KEY = None

# If user chooses to provide their own key
if key_source == "Use my own key":
    user_provided_key = st.sidebar.text_input(
        "Enter your GOOGLE_API_KEY:",
        value="",
        help="Provide your Google API Key for accessing Gemini services."
    )
    API_KEY = user_provided_key.strip() if user_provided_key.strip() else None

# If user chooses to load from .env
elif key_source == "Load key from .env":
    load_dotenv()  # Load .env file
    API_KEY = os.getenv("GOOGLE_API_KEY")

# Validate API Key
if not API_KEY:
    st.sidebar.error("No valid API key found! Please provide a key or add it to the .env file.")
    st.stop()

# Debugging Info (Optional)
st.sidebar.text(f"DEBUG: Using API Key: {API_KEY[:4]}...")  # Show the first 4 characters only

########################################
# Configure Google Generative AI
########################################
try:
    genai.configure(api_key=API_KEY)
    st.sidebar.success("API Key successfully configured!")
except Exception as e:
    st.sidebar.error(f"Failed to configure API key: {e}")
    st.stop()

########################################
# Initialize AI Agent
########################################
@st.cache_resource
def create_ai_agent(api_key):
    try:
        # Pass the dynamically configured API key
        genai.configure(api_key=api_key)
        return Agent(
            name="Phidata Video Analyzer",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo()],
            markdown=True
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize AI Agent: {e}")

video_analyzer = create_ai_agent(API_KEY)

########################################
# Video Upload and Processing
########################################
def upload_and_process_video():
    """
    Handles video upload and returns the local path for processing.
    Displays the uploaded video in the main interface.
    """
    with st.sidebar:
        st.subheader("Upload Your Video")
        uploaded_video = st.file_uploader(
            label="(MP4/MOV/AVI)",
            type=["mp4", "mov", "avi"],
            help="Upload your video file to summarize or analyze"
        )

    if not uploaded_video:
        st.info("Please upload a video file to proceed.")
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_video.read())
        local_video_path = temp_file.name

    st.video(local_video_path, format="video/mp4", start_time=0)
    return local_video_path

########################################
# Perform Video Analysis
########################################
def perform_video_analysis(local_video_path, query, summary_style):
    try:
        with st.spinner("Uploading video to AI service..."):
            processed_file = upload_file(local_video_path)
            while processed_file.state.name == "PROCESSING":
                time.sleep(1)
                processed_file = get_file(processed_file.name)

        if summary_style == "Executive Summary":
            style_instruction = "Provide a concise, single-paragraph executive overview."
        elif summary_style == "Bullet Points":
            style_instruction = "Provide a list of bullet points highlighting the key takeaways."
        else:  # "In-depth Narrative"
            style_instruction = "Provide a more detailed, narrative-style summary with contextual insights."

        analysis_prompt = (
            "You are a helpful AI model. Analyze the provided video carefully. "
            f"{style_instruction}\n\n"
            f"User Query: {query}\n\n"
            "Use any context from the video. Present your findings in user-friendly language."
        )

        response = video_analyzer.run(analysis_prompt, videos=[processed_file])
        return response.content

    except Exception as e:
        raise RuntimeError(f"Video analysis failed: {e}")
    finally:
        Path(local_video_path).unlink(missing_ok=True)

########################################
# Main Streamlit App
########################################
def main():
    st.sidebar.title("Video Summarizer Options")

    # Sidebar: Choose summary style
    summary_style = st.sidebar.radio(
        "Choose your summary style:",
        ["Executive Summary", "Bullet Points", "In-depth Narrative"],
        index=0
    )

    video_path = upload_and_process_video()

    if video_path:
        user_prompt = st.text_area(
            label="Enter a query or request:",
            placeholder="Example: 'Summarize the main topic' or 'List key points.'"
        )

        if st.button("Analyze & Respond"):
            if not user_prompt.strip():
                st.warning("Please enter a query before clicking the button.")
            else:
                try:
                    with st.spinner("Analyzing video..."):
                        answer = perform_video_analysis(video_path, user_prompt, summary_style)
                    st.subheader("Video Analysis Result")
                    st.markdown(answer)
                except Exception as err:
                    st.error(str(err))

if __name__ == "__main__":
    main()

    # Optional: Adjust text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )