# Phidata x Gemini Video Summarizer Agent

An AI-powered video summarizer built using Streamlit, Google Gemini 2.0 Flash Exp, and Phidata AI Agent. This application enables users to upload video, analyze their content, and generate insights or summaries in different styles (Executive Summary, Bullet Points, In-depth Narrative).

## Features

- **Video Upload:** Upload videos in MP4, MOV, or AVI format.
- **Customizable Summaries:** Generate video summaries in multiple styles:
  - Executive Summary
  - Bullet Points
  - In-depth Narrative
- **Query-Based Analysis:** Ask specific questions about the video content, and the AI provides actionable insights.
- **Interactive UI:** Built with Streamlit for an intuitive, web-based interface.

## Prerequisites

- Python 3.8 or higher
- A valid `GOOGLE_API_KEY` added to a `.env` file in the root directory.
- The following Python libraries (install with `pip`):
  - `streamlit`
  - `google-generativeai`
  - `phidata`
  - `python-dotenv`

## Installation and Setup

**1. Clone this repository:**
   git clone https://github.com/AdnanSattar/ai-video-summarizer-agent.git
   cd ai-video-summarizer-agent

**2. Install dependencies:**
pip install -r requirements.txt

**3. Add your Google API key to a .env file generate from Google AI Studio**
makefile `.env`
GOOGLE_API_KEY=<your-google-api-key>

**4. Run the Streamlit application:**
streamlit run app.py
Access the app in your browser at http://localhost:8501.

**File Structure**
.
├── app.py             # Main application script
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies
├── .env               # API key (not included in the repo)

## Contributing
Feel free to open an issue or submit a pull request for any enhancements or bug fixes. Contributions are welcome!


