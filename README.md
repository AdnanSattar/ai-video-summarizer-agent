# Phidata x Gemini Video Summarizer Agent

An AI-powered video summarizer built using Streamlit, Google Gemini 2.0 Flash Exp, and Phidata AI Agent. This application enables users to upload videos, analyze their content, and generate insights or summaries in different styles (Executive Summary, Bullet Points, In-depth Narrative). It also features dynamic API key handling, making it flexible and user-friendly.

---

## Features

### **Dynamic API Key Handling**
- Users can choose to:
  - Provide their API key during runtime via the app interface.
  - Load the API key from a `.env` file in the project directory.
- Provides flexibility for developers and users managing API keys.
- Includes debugging support by displaying the first four characters of the API key being used (optional).

### **Video Upload and Display**
- Users can upload videos in MP4, MOV, or AVI formats.
- The uploaded video is displayed in the app for reference.

### **Customizable Summaries**
- Generate video summaries in three different styles:
  - **Executive Summary**: A concise, single-paragraph overview.
  - **Bullet Points**: Key takeaways in a list format.
  - **In-depth Narrative**: A detailed, contextual summary.

### **Query-Based Analysis**
- Users can input custom queries about the video content.
- The AI generates actionable insights based on the video and the user query.

### **Interactive User Interface**
- Built with Streamlit for an intuitive, web-based experience.

---

## Prerequisites

- Python 3.8 or higher
- A valid `GOOGLE_API_KEY` (can be provided via the app interface or a `.env` file).
- Required Python libraries (install via `pip`):
  - `streamlit`
  - `google-generativeai`
  - `phidata`
  - `python-dotenv`

---

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
###
.
├── app.py             # Main application script
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies
├── .env               # API key (not included in the repo)`
###

## Contributing
Feel free to open an issue or submit a pull request for any enhancements or bug fixes. Contributions are welcome!


