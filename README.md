# Groq Chatbot with Gradio

This is a simple chatbot application using the Groq API and Gradio for the UI.

## Features
- Uses Groq API for chat completions
- Gradio web interface
- API key loaded from `.env` file

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Add your Groq API key to a `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Run the chatbot:
   ```sh
   python chatbot.py
   ```

## Files
- `chatbot.py`: Main application
- `.env`: Store your Groq API key
- `requirements.txt`: Python dependencies
