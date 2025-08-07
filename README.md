# 🤖 AI Tools Finder Chatbot

A simple chatbot that helps users discover useful AI tools based on their input. It uses OpenAI's GPT model in the backend with FastAPI, and a user interface built using Streamlit.

---

## 📌 Features

- Chat interface to ask for AI tools
- Backend built using FastAPI
- Frontend built using Streamlit
- Uses OpenAI API for generating responses

---

## 🖼️ Screenshots

Add your screenshots inside a folder named `screenshots` and reference them here like:

- `./screenshots/ui.png`
- `./screenshots/chat_response.png`

---

## 🧰 Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT

---

## 🚀 How to Run Locally

### 1. Clone the Repo
```bash
git clone https://github.com/anaszia60/AI_tools_finder.git
cd AI_tools_finder
```

### 2. Create Virtual Environment and Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate      # On Linux/macOS
# .venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

### 3. Run Backend
```bash
cd backend
uvicorn main:app --reload
```

### 4. Run Frontend
Open a new terminal:
```bash
cd frontend
streamlit run streamlit_app.py
```

---

## 📁 Folder Structure

```
AI_tools_finder/
├── backend/
│   └── main.py
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## 📌 Notes

- Don’t forget to add your OpenAI API key to use the chatbot properly.
- Screenshots help demonstrate your UI in the README.

---