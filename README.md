[README.md](https://github.com/user-attachments/files/21403444/README.md)
# 🧠 Anarix.AI Agent

Anarix.AI is an intelligent e-commerce data agent that converts natural language questions into SQL queries and visual answers using Gemini API, FastAPI, SQLite, and Plotly.js.

---

## 💡 What It Does

- Takes questions like:
  - “Top 5 products by sales”
  - “Which campaign had the highest ad spend?”
  - “Compare impressions vs clicks”
- Uses **Gemini 1.5 Flash** to generate SQL queries
- Runs SQL on local **SQLite database**
- Returns:
  - Text answer with typing animation 💬
  - Interactive chart using **Plotly.js** 📊

---

## 🚀 Tech Stack

| Layer     | Tools Used                |
|-----------|---------------------------|
| Frontend  | HTML, CSS, JavaScript     |
| Backend   | FastAPI                   |
| Database  | SQLite                    |
| AI Model  | Gemini API (Google)       |
| Charts    | Plotly.js                 |

---

## 🧪 How to Run the Project

1. Clone or download this repository

2. Add your Gemini API key inside a `.env` file:
   ```
   GEMINI_API_KEY=your_google_gemini_key
   ```

3. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

5. Open `index.html` in your browser (from `frontend/`)

---

## 📁 Project Structure

```
anarix-ai-agent/
├── backend/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── ecommerce.db
├── README.md
├── .gitignore
```

---

## 👩‍💻 Built By

Created with love by **Manogna**  
Feel free to fork, star, or give feedback!
