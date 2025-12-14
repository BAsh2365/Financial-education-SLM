from flask import Flask, request, jsonify, send_from_directory
import re
import os
from vector import get_stock_price, retriever
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__, static_folder="static", static_url_path="")

template = """
You are an expert on helping people with finnancial investing, portfolios, real estate, stocks, and personal money matters.
You will answer questions based on the provided excerpts from TXT documents. Make sure to cite the source of the information.
You will anazlyse the User's financial information and situation to provide accurate and helpful answers based on the data you are trained on.
NO HALLUCINATIONS, DO NOT MAKE UP INFORMATION.
Approach these conversations in a friendly welcoming manner, as if you are a helpful financial advisor.
For mathematical calculations, use the information in the excerpts and couple it with the users input to provide accurate answers.
Your purpose is to be used as a tool by people and financial advisors alike to help them with their financial questions and concerns (not a replacement).
You also have access to the current stock prices through the yahoo finance API, which you can use to answer questions if prompted about the general topic.

Excerpts from TXT documents:
{excerpts}

Question:
{question}
"""

model = OllamaLLM(model="phi4-mini:3.8b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def extract_ticker(query):
    match = re.search(r"\b([A-Z]{2,5})\b", query)
    if match:
        return match.group(1)
    return None

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "missing message"}), 400

    question = data["message"]
    ticker = extract_ticker(question)
    price_text = None
    if ticker:
        try:
            price = get_stock_price(ticker)
            if price is not None:
                price_text = f"According to Yahoo Finance, the current price of {ticker} is ${price:.2f}."
            else:
                price_text = f"Sorry, I couldn't fetch the current price for {ticker}."
        except Exception:
            price_text = f"Sorry, I couldn't fetch the current price for {ticker}."

    docs = retriever.get_relevant_documents(question)
    excerpts = "\n\n".join([doc.page_content for doc in docs])

    try:
        result = chain.invoke({"excerpts": excerpts, "question": question})
        response_text = result
    except Exception as e:
        response_text = f"Error invoking model: {e}"

    payload = {"reply": response_text}
    if price_text:
        payload["stock_price_info"] = price_text

    return jsonify(payload)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_dir = app.static_folder
    target = os.path.join(static_dir, path)
    if path and os.path.exists(target):
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
