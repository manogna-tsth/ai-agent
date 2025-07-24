from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Configuration
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Or use "gemini-pro"

# FastAPI setup

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict it to ['http://localhost:5500'] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request body format
class QuestionRequest(BaseModel):
    question: str

# Get column names from a table
def get_table_schema(table_name):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cursor.fetchall()]
    conn.close()
    return cols

# Ask Gemini to generate SQL
def generate_sql_from_question(question, schemas):
    prompt = f"""
You are an expert data analyst. Convert the user question into a clean, executable **SQLite SQL query**.

Use ONLY the following tables and columns:

🔹 ad_sales_metrics ({', '.join(schemas['ad_sales_metrics'])})  
🔹 total_sales_metrics ({', '.join(schemas['total_sales_metrics'])})

Never use a table named 'sales'.  
Never wrap your SQL inside ``` or add the word 'sql'.  
Return ONLY the query.

User question: {question}
"""
    print("Prompt sent to Gemini:\n", prompt)

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        print("Gemini Response:\n", raw)
        # Remove any accidental markdown formatting
        cleaned = raw.replace("```sql", "").replace("```", "").strip()
        return cleaned
    except Exception as e:
        print("Gemini Error:", str(e))
        return f"ERROR: Gemini failed - {str(e)}"

# Execute the generated SQL
def execute_query(sql):
    print("SQL to execute:\n", sql)
    try:
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print("SQL Execution Error:", str(e))
        return f"ERROR: Query failed - {str(e)}"

# Main API endpoint
@app.post("/ask")
def ask_question(request: QuestionRequest):
    # Fetch table schemas
    schemas = {
        "ad_sales_metrics": get_table_schema("ad_sales_metrics"),
        "total_sales_metrics": get_table_schema("total_sales_metrics")
    }

    # Ask Gemini to generate SQL
    sql = generate_sql_from_question(request.question, schemas)
    if sql.startswith("ERROR"):
        raise HTTPException(status_code=500, detail=sql)

    # Run SQL
    result = execute_query(sql)
    if isinstance(result, str) and result.startswith("ERROR"):
        raise HTTPException(status_code=500, detail=result)

    return {
        "question": request.question,
        "generated_sql": sql,
        "answer": result
    }
