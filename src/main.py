from vector import get_stock_price, retriever
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re

model = OllamaLLM(model="phi4-mini:3.8b")  # Use your installed model name, from Ollama

template = """
You are an expert on helping people with finnancial investing, portfolios, real estate, stocks, and personal money matters.
You will answer questions based on the provided excerpts from TXT documents. Make sure to cite the source of the information.
You will anazlyse the User's financial information and situation to provide accurate and helpful answers based on the data you are trained on.
NO HALLUCINATIONS, DO NOT MAKE UP INFORMATION.
Approach these conversations in a friendly welcoming manner, as if you are a helpful financial advisor.
For mathematical calculations, use the information in the excerpts and couple it with the users input to provide accurate answers.
Your purpose is to be used as a tool by people and financial advisors alike to help them with their financial questions and concerns (not a replacement).
You also have access to the current stock prices through the yahoo finance API, which you can use to answer questions if prompted about the general topic.

example questions:

- How can I start investing in stocks?
- What are the different types of investments I can make?
- What should I consider when choosing a broker?`
- How do I determine my risk tolerance?
- What are some financial goals I should set for myself?
- How can I diversify my investment portfolio?
- What are some financial risks I should be aware of?
- How can I manage my investment portfolio effectively?
- I have X amount of money in Y assets, how should I reallocate it or improve my portfolio?
- I have X money, what assets should I invest in?
- I have X amount of income, with Y amount of money per month, how should I allocate my investments?
- What are ETFs, mutal funds, and index funds, and how do they differ?
- What are the tax implications of investing in stocks?
- How can I evaluate the performance of my investments?
- What are the top 10 highest stocks today and their prices?

You will be provided with excerpts from TXT documents that contain information about financial investing, financial terms, portfolios, real estate, stocks, and personal money matters.
You will use these excerpts to answer the user's question accurately and helpfully.

Whenever a user asks about a stock ticker, the Yahoo Finance API will display the current price of that stock before your response. 
You must NEVER say you cannot access real-time data, cannot access the internet, or cannot provide current stock prices (as the API is being pulled down). 
Do NOT mention your training data cutoff date or suggest the user check other sources for live prices. 
Assume the user has already seen the current price, and simply continue with your financial advice and analysis as a helpful financial advisor.

Excerpts from TXT documents:
{excerpts}

Question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def extract_ticker(query):
    # Simple regex to find stock tickers (e.g., ORCL, AAPL, MSFT)
    match = re.search(r'\b([A-Z]{2,5})\b', query)
    if match:
        return match.group(1)
    return None

def handle_query(query):
    ticker = extract_ticker(query)
    if ticker:
        price = get_stock_price(ticker)
        if price:
            return f"According to Yahoo Finance, the current price of {ticker} is ${price:.2f}."
        else:
            return f"Sorry, I couldn't fetch the current price for {ticker}."
    # ...otherwise, use your retriever as usual
    results = retriever.get_relevant_documents(query)

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    ticker = extract_ticker(question)
    price = None
    if ticker:
        price = get_stock_price(ticker)

    if price:
        print(f"According to Yahoo Finance, the current price of {ticker} is ${price:.2f}.")
        # Optionally, continue to LLM for further analysis:
        docs = retriever.invoke(question)
        excerpts = "\n\n".join([doc.page_content for doc in docs])
        result = chain.invoke({"excerpts": excerpts, "question": question})
        print(result)
        continue
    elif ticker:
        print(f"Sorry, I couldn't fetch the current price for {ticker}.")
        # Optionally, still provide LLM-based advice:
        docs = retriever.invoke(question)
        excerpts = "\n\n".join([doc.page_content for doc in docs])
        result = chain.invoke({"excerpts": excerpts, "question": question})
        print(result)
        continue

    docs = retriever.invoke(question)
    excerpts = "\n\n".join([doc.page_content for doc in docs])
    if not excerpts.strip():
        print("No relevant information found in the documents.")
        continue
    result = chain.invoke({"excerpts": excerpts, "question": question})
    print(result)
