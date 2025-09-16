import os
import requests
import gradio as gr
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# --- Restaurant Orders Chatbot ---

# Popular Maharashtrian Dishes Menu
RESTAURANT_MENU = [
    {"name": "Vada Pav", "price": 3},
    {"name": "Misal Pav", "price": 4},
    {"name": "Pav Bhaji", "price": 5},
    {"name": "Puran Poli", "price": 6},
    {"name": "Poha", "price": 3},
    {"name": "Sabudana Khichdi", "price": 4},
    {"name": "Thalipeeth", "price": 5},
    {"name": "Kothimbir Vadi", "price": 4},
    {"name": "Rassa", "price": 8},
    {"name": "Sol Kadhi", "price": 2},
    {"name": "Bhakri", "price": 2},
    {"name": "Zunka Bhakar", "price": 5},
    {"name": "Modak", "price": 4},
    {"name": "Sheera", "price": 3},
    {"name": "Shengdana Chutney", "price": 2},
    {"name": "Alu Vadi", "price": 4},
    {"name": "Batata Bhaji", "price": 3},
    {"name": "Matki Usal", "price": 4},
    {"name": "Kanda Poha", "price": 3},
    {"name": "Sreekhand", "price": 5},
    {"name": "Basundi", "price": 5},
    {"name": "Ukadiche Modak", "price": 5},
    {"name": "Chakli", "price": 2},
    {"name": "Bhakarwadi", "price": 3},
    {"name": "Dhokla", "price": 3},
    {"name": "Kharvas", "price": 4},
    {"name": "Pithla Bhakri", "price": 5},
    {"name": "Kolhapuri Mutton", "price": 12},
    {"name": "Bombil Fry", "price": 10},
    {"name": "Sabudana Vada", "price": 4}
]

def menu_to_string():
    return "\n".join([f"- {item['name']} (${item['price']})" for item in RESTAURANT_MENU]) + f"\n\n<b>Total number of dishes: {len(RESTAURANT_MENU)}</b>"

SYSTEM_PROMPT = (
    '<div style="font-family:Quicksand,sans-serif;">'
    '<h2 style="color:#d7263d;font-size:1.6rem;margin-bottom:0.5em;">🍽️ Welcome to Gourmet Bistro!</h2>'
    '<p style="font-size:1.1rem;margin-bottom:0.5em;">'
    'I am your <span style="color:#fbb13c;font-weight:bold;">friendly, helpful, and creative</span> restaurant ordering assistant.<br>'
    '🥗 <b>Greet the customer</b> and make them feel welcome.<br>'
    '📜 <b>Show the menu</b> and help them place an order.<br>'
    '🌟 <b>Suggest popular items</b> if they ask for recommendations.<br>'
    '✅ <b>Confirm the order and total price</b> before checkout.<br>'
    '😃 <b>Be engaging</b> and use emojis where appropriate!'
    '</p>'
    '<div style="margin-top:1em;">'
    '<span style="color:#d7263d;font-size:1.2rem;font-weight:bold;">Menu:</span><br>'
    f'{menu_to_string()}'
    '</div>'
    '</div>'
)

def get_menu_options():
    return [f"{item['name']} (${item['price']})" for item in RESTAURANT_MENU]

def get_item_by_name(name):
    for item in RESTAURANT_MENU:
        if item['name'] == name:
            return item
    return None

def order_summary(selected_items):
    if not selected_items:
        return "<b>No items selected.</b>"
    total = 0
    rows = []
    for sel in selected_items:
        name = sel.split(' ($')[0]
        item = get_item_by_name(name)
        if item:
            rows.append(f"<tr><td>{item['name']}</td><td>${item['price']}</td></tr>")
            total += item['price']
    table = "<table style='width:100%;border-collapse:collapse;'>"
    table += "<tr style='background:#fbb13c22;'><th>Dish</th><th>Price</th></tr>"
    table += "".join(rows)
    table += f"<tr style='font-weight:bold;background:#fbb13c33;'><td>Total</td><td>${total}</td></tr></table>"
    return table

def place_order(selected_items, user_name):
    if not selected_items:
        return "<b>Please select at least one item to place an order.</b>"
    summary = order_summary(selected_items)
    return f"<div style='color:#d7263d;font-size:1.1rem;'><b>Thank you, {user_name or 'Guest'}! Your order has been placed.</b></div>" + summary

def chat_with_groq(message, history):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        if bot:
            messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": message})

    # ✅ FIXED JSON payload
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    found_dishes = []
    for item in RESTAURANT_MENU:
        if item["name"].lower() in message.lower():
            found_dishes.append(item)

    if response.status_code == 200:
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        if found_dishes:
            for dish in found_dishes:
                reply += f'<br><div style="margin:1em 0;padding:0.5em;border:1px solid #fbb13c;border-radius:8px;max-width:340px;">'
                reply += f'<div style="font-size:1.1rem;font-weight:bold;color:#d7263d;margin-top:0.5em;">{dish["name"]} - ${dish["price"]}</div></div>'
        return reply
    elif response.status_code == 429:
        return (
            '<div style="color:#d7263d;font-weight:bold;font-size:1.1rem;">'
            '🚦 <b>Rate limit reached!</b><br>'
            'The server is busy or you have sent too many requests.<br>'
            'Please wait a few seconds and try again.<br>'
            '<span style="font-size:0.95rem;color:#fbb13c;">(If you need higher limits, consider upgrading your Groq API plan.)</span>'
            '</div>'
        )
    else:
        return f"Error: {response.status_code} - {response.text}"

theme = gr.themes.Soft(
    primary_hue="red",
    secondary_hue="yellow",
    neutral_hue="gray",
    font=["Quicksand", "sans-serif"]
)

def main():
    with gr.Blocks(theme=theme) as demo:
        gr.HTML(
            '''
            <style>
            @keyframes rainbow-heading {
                0% { background-position: 0% 50%; }
                100% { background-position: 100% 50%; }
            }
            .rainbow-heading {
                font-family: Quicksand, sans-serif;
                font-size: 2.1rem;
                font-weight: bold;
                background: linear-gradient(90deg, #d7263d, #fbb13c, #2ec4b6, #3a86ff, #ff006e, #8338ec, #ffbe0b, #d7263d);
                background-size: 300% 300%;
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                -webkit-text-fill-color: transparent;
                text-fill-color: transparent;
                padding: 0.2em 1.2em;
                border-radius: 12px;
                letter-spacing: 1px;
                text-align: center;
                margin-bottom: 0.05em;
                animation: rainbow-heading 4s linear infinite;
            }
            .welcome-heading {
                font-family: Quicksand, sans-serif;
                font-size: 1.5rem;
                color: #d7263d;
                font-weight: bold;
                background: linear-gradient(90deg, #d7263d, #fbb13c, #2ec4b6, #3a86ff, #ff006e, #8338ec, #ffbe0b, #d7263d);
                background-clip: text;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-fill-color: transparent;
                padding: 0.2em 1.2em;
                border-radius: 12px;
                letter-spacing: 1px;
                text-align: center;
                margin-bottom: 0.1em;
                margin-top: 0.05em;
            }
            </style>
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin: 1.2em 0 1.2em 0;">
                <div class="rainbow-heading">Gourmet Bistro</div>
                <div class="welcome-heading">🍽️ Welcome to our restaurant!</div>
            </div>
            '''
        )
        gr.Markdown("Welcome to our restaurant!\n\nBrowse the menu, ask for recommendations, and place your order.")
        gr.Markdown("<b>Menu:</b> (Ask for any dish in chat to see its image and price!)")

        gr.Markdown("<hr><h3 style='color:#d7263d;'>Place Your Order</h3>")
        user_name = gr.Textbox(label="Your Name (optional)", placeholder="Enter your name", elem_id="username-box")
        selected_items = gr.CheckboxGroup(get_menu_options(), label="Select Dishes to Order")
        order_btn = gr.Button("Place Order", elem_id="order-btn", variant="primary")
        order_out = gr.HTML()

        def on_order(items, name):
            return place_order(items, name)

        order_btn.click(on_order, inputs=[selected_items, user_name], outputs=order_out)

        gr.HTML(
            """
<h3 style="text-align:center;font-size:28px;animation:rainbow 3s infinite;">💬 Chat with Assistant</h3>
<style>
@keyframes rainbow {
  0%   {color: red;}
  20%  {color: orange;}
  40%  {color: yellow;}
  60%  {color: green;}
  80%  {color: blue;}
  100% {color: purple;}
}
</style>
"""
        )

        gr.ChatInterface(
            fn=chat_with_groq,
            description=("Ask for recommendations, place your order, or inquire about any dish!\n\n"
                         "<details><summary><b>View Menu (text)</b></summary>" + menu_to_string() + "</details>"),
            examples=[
                ["What do you recommend?"],
                ["I want to order a Vada Pav and Poha."],
                ["Can I see the dessert options?"],
            ],
            textbox=gr.Textbox(placeholder="💬 Type a message", show_label=False, elem_id="chatbox-main"),
            submit_btn="📤"
        )

        gr.HTML(
            """
            <style>
            #chatbox-main textarea {
                border: 3px solid;
                border-image: linear-gradient(90deg,#d7263d,#fbb13c,#2ec4b6,#3a86ff,#ff006e,#8338ec,#ffbe0b,#d7263d) 1;
                animation: bordercycle 4s linear infinite;
                background: #fffbe6;
                color: #111 !important;
                transition: background 0.2s;
            }
            #chatbox-main textarea:focus {
                outline: none !important;
                background: #fff0f6;
                color: #111 !important;
            }
            @keyframes bordercycle {
                0% {border-image-source: linear-gradient(90deg,#d7263d,#fbb13c,#2ec4b6,#3a86ff,#ff006e,#8338ec,#ffbe0b,#d7263d);}
                100% {border-image-source: linear-gradient(450deg,#d7263d,#fbb13c,#2ec4b6,#3a86ff,#ff006e,#8338ec,#ffbe0b,#d7263d);}
            }
            </style>
            """
        )
    demo.launch()

if __name__ == "__main__":
    main()
