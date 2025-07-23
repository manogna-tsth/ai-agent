from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ Load Gemini API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ FastAPI app
app = FastAPI()

# ✅ APPLY CORS BEFORE ANY ROUTE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Data model
class QuestionRequest(BaseModel):
    question: str

# ✅ Helper to get table schema
def get_table_schema(table_name):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cursor.fetchall()]
    conn.close()
    return cols

# ✅ Gemini SQL generation
def generate_sql_from_question(question, schemas):
    prompt = f"""
You are an expert data analyst. Convert the user question into a clean, executable SQLite SQL query.

Use ONLY the following tables and columns:

🔹 ad_sales_metrics ({', '.join(schemas['ad_sales_metrics'])})  
🔹 total_sales_metrics ({', '.join(schemas['total_sales_metrics'])})

⚠️ Never use a table named 'sales'.  
⚠️ Never wrap your SQL inside ``` or add the word 'sql'.  
⚠️ Return ONLY the query.

User question: {question}
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        return raw.replace("```sql", "").replace("```", "").strip()
    except Exception as e:
        return f"ERROR: Gemini failed - {str(e)}"

# ✅ Query executor
def execute_query(sql):
    try:
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return f"ERROR: Query failed - {str(e)}"

# ✅ Main route
@app.post("/ask")
def ask_question(request: QuestionRequest):
    schemas = {
        "ad_sales_metrics": get_table_schema("ad_sales_metrics"),
        "total_sales_metrics": get_table_schema("total_sales_metrics")
    }

    sql = generate_sql_from_question(request.question, schemas)
    if sql.startswith("ERROR"):
        raise HTTPException(status_code=500, detail=sql)

    result = execute_query(sql)
    if isinstance(result, str) and result.startswith("ERROR"):
        raise HTTPException(status_code=500, detail=result)

    return {
        "question": request.question,
        "generated_sql": sql,
        "answer": result
    }




from fastapi.responses import JSONResponse

@app.post("/ask")
def ask_question(request: QuestionRequest):
    print(f"Received question: {request.question}")  # 🔍 Debug

    schemas = {
        "ad_sales_metrics": get_table_schema("ad_sales_metrics"),
        "total_sales_metrics": get_table_schema("total_sales_metrics")
    }
    print("Schema fetched:", schemas)  # 🔍 Debug

    sql = generate_sql_from_question(request.question, schemas)
    print("Generated SQL:", sql)  # 🔍 Debug

    if sql.startswith("ERROR"):
        raise HTTPException(status_code=500, detail=sql)

    result = execute_query(sql)
    print("Query result:", result)  # 🔍 Debug

    if isinstance(result, str) and result.startswith("ERROR"):
        raise HTTPException(status_code=500, detail=result)

    return {
        "question": request.question,
        "generated_sql": sql,
        "answer": result
    }

