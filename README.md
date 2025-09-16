# Groq Chatbot with Gradio

This is a simple chatbot application using the Groq API and Gradio for the UI.

## Features
- Uses Groq API for chat completions
- Gradio web interface
- API key loaded from `.env` file
   Beautiful **Gradio web UI** with animated headers and gradient styles  
-  Predefined **Maharashtrian menu** with prices  
-  **Interactive ordering system** with name input, checkboxes & order summary  
-  **AI-powered chat** (Groq Llama 3.1 model) for recommendations & help  
-  Styled HTML responses with emojis and tables  
-  Graceful handling of **rate-limit errors**  


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

🍽️ Gourmet Bistro – AI Restaurant Ordering Chatbot

This project is an **AI-powered restaurant ordering chatbot** built using [Gradio](https://gradio.app/), [Groq API](https://groq.com/), and Python.  
It simulates a **Maharashtrian cuisine restaurant** where users can browse dishes, place orders, and chat with a friendly AI waiter.

## restaurant-chatbot
┣ 📜 app.py # Main chatbot code
┣ 📜 .env # Stores API key securely (ignored by Git)
┣ 📜 requirements.txt # Dependencies
┣ 📜 setup_notes.txt # Original setup instructions
┣ 📜 README.md # Documentation (this file)
┣ 📜 .gitignore # Ensures .env & temp files aren’t uploaded

## Code Explanation

1️ Imports & API Setup

os → Access environment variables
requests → Send API requests to Groq
gradio → Build the chatbot’s web interface
dotenv → Load API key securely from .env

2 The Groq API key is read from .env:
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

3 Menu Data

A list of Maharashtrian dishes with their prices.
menu_to_string() → formats the menu into a text block with dish count.

4 System Prompt

Defines how the AI assistant behaves:
Greets customers
Shows menu
Suggests items
Confirms orders & total price
Uses emojis and engaging tone

5 Order Functions

get_item_by_name(name) → Finds dish details by name
order_summary(items) → Builds an HTML table with dish list + total price
place_order(items, user) → Confirms order and thanks customer
These functions power the order placement system.

6 Chat with Groq

Builds a conversation with system + history + user message
Sends request to Groq API → gets AI reply
If user mentions dishes, adds highlight cards with names & prices
Handles errors (e.g., 429 Too Many Requests) with styled messages

7 Custom Styling (CSS)

The UI uses rainbow gradient headers, animated borders, and colorful text:
.rainbow-heading → animated restaurant name
.welcome-heading → gradient welcome message
Chatbox with gradient borders

8 Gradio Interface

The main UI is built with gr.Blocks:
Header Section → Styled restaurant name & welcome text
Order Section → Name input + checkboxes for dishes + “Place Order” button
Chat Section → ChatInterface for AI conversation

9 App Launch

Starts the Gradio app
Opens a local web server (and optionally a shareable public link)