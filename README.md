# Gemini Chatbot with Streamlit

A multi-turn chatbot powered by **Google Gemini (via LangChain)** with a Streamlit web interface.
Supports typing animation, chat history, and PDF export of conversations.

---

## Features

* **Sidebar setup**: Enter Gemini API key securely (hidden password field)
* **Setup button**: Chat is only available after proper setup
* **Multi-turn conversation**: Maintains conversation using `HumanMessage` / `AIMessage`
* **Typing animation**: Assistant responses display with a typewriter effect
* **Chat history**: Stored in session state for full conversation retention
* **Export to PDF**: Download the conversation history directly from the sidebar
* **System messages skipped** in display for cleaner chat view

---

## Screenshots

<img width="1914" height="939" alt="image" src="https://github.com/user-attachments/assets/e8b3e83e-2b3e-41d8-a4b6-8dc54a4f1f2d" />

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gemini-chatbot.git
cd gemini-chatbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Open the sidebar to:

   * Enter your **Gemini API key**
   * Select model (`gemini-pro` or `gemini-2.0-flash`)
   * Set **temperature** for creativity

3. Click **Setup** to initialize the chatbot.

4. Start chatting in the main chat window.

5. When the conversation is complete, click **Download Chat History as PDF** in the sidebar to save the conversation.

---

## File Structure

```
gemini-chatbot/
│── app.py                  # Main Streamlit app
│── requirements.txt        # Dependencies
│── README.md               # Project documentation
```

---

## Dependencies

* `streamlit` – Web app UI
* `langchain` – LLM integration with Gemini
* `google-generativeai` – Gemini API client
* `fpdf` – PDF generation

---

## License

This project is licensed under the MIT License.

---

If you want, I can **also add a “Usage GIF + Typing Animation Example” section** in the README that makes it look very professional for GitHub.

Do you want me to do that?
