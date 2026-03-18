from langchain_ollama import OllamaLLM
import re
import math

llm = OllamaLLM(model="llama3.2:latest")  # Changed to a better model for extraction tasks


# 🔥 DECISION (IMPROVED LOGIC)
def decide_with_context(query, context):
    # Check for math keywords
    math_keywords = ["calculate", "math", "square", "root", "plus", "minus", "multiply", "divide", "sum", "average", "equation"]
    if any(word in query.lower() for word in math_keywords):
        return "calculator"

    # If context is available and not empty, use it
    if context.strip():
        return "use_context"

    # Else, general
    return "general"


# 🔥 STRICT RAG
def generate_answer(query, context):

    prompt = f"""
Extract and list all relevant HR interview questions and answers mentioned in the provided context.

If the context does not contain any HR interview questions or relevant information, say "Not found in knowledge base".

Do not use external knowledge. Base your response only on the context.

Context:
{context}

Query: {query}

Response:
"""

    response = llm.invoke(prompt)
    print(f"🔍 LLM Response: {response}")  # Debug print
    return response


# 🔥 GENERAL
def general_answer(query):
    return llm.invoke(query)


# 🔥 MATH FIX
def solve_math(query):

    prompt = f"""
Convert to Python expression.

Examples:
square root of 64 → math.sqrt(64)
square of 5 → 5**2

ONLY return expression.

Query:
{query}
"""

    expression = llm.invoke(prompt)

    # 🔥 CLEAN HARD
    expression = re.sub(r"```.*?```", "", expression, flags=re.DOTALL)
    expression = expression.replace("```python", "").replace("```", "").strip()

    print(f"🧮 Expression: {expression}")

    try:
        return str(eval(expression, {"__builtins__": None}, {"math": math}))
    except Exception as e:
        print("❌ Eval error:", e)
        return "Calculation error"