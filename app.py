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

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.warning("No valid GOOGLE_API_KEY found. Please add it to your .env.")

# Streamlit page configuration
st.set_page_config(
    page_title="AI Video Summarizer (Phidata/Gemini)",
    page_icon="🎥",
    layout="wide"
)

st.title("Phidata x Gemini Video Summarizer")
st.write(
    """
    Leverage Google Gemini 2.0 Flash Exp and Phidata's AI Agent to analyze video content, 
    answer queries, and produce meaningful insights.
    """
)

# Initialize AI Agent
@st.cache_resource
def create_ai_agent() -> Agent:
    return Agent(
        name="Phidata Video Analyzer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True
    )

video_analyzer = create_ai_agent()

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

def perform_video_analysis(local_video_path, query, summary_style):
    """
    Uploads the video, waits for processing, and performs AI analysis based on the query and summary style.
    Returns the AI's response or raises an error if processing fails.
    """
    try:
        with st.spinner("Uploading video to AI service..."):
            processed_file = upload_file(local_video_path)
            while processed_file.state.name == "PROCESSING":
                time.sleep(1)
                processed_file = get_file(processed_file.name)

        # Prompt customization based on the selected summary style
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

    # Adjust text area height for better UI
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