# Financial-education-SLM
Financial SLM chatbot using Model and architecture from Ollama, ChromaDB, and Langchain


Understanding the Power of Local Language Models ( SLM financial chatbot)
From Information and Tutorials gathered online, using Python, Ollama, Langchain, the Yahoo Finance API, and various compiled, trusted financial sources (such as Investopedia, Fidelity, BlackRock, etc. through GPT Deep research, I built a local financial assistant that helps users enter personal financial information (which is not shared with anyone) on their local machine. The SLM (using Microsoft's Phi-4-mini model found on Ollama) answers any quick questions related to investments, retirement, and other financial topics. The goal of the SLM is to serve as a tool that educates people on finances through specific use cases. 
(Note: This is not a replacement for a Financial Advisor, but rather an educational tool for understanding finances.) 
When used correctly, local language models can be a powerful tool that works with people to achieve solutions, while learning throughout the process, and can be scaled to work with developers, analysts, etc. 
In a sustainable way.

Sources:

- Tech With Tim: https://youtu.be/E4l91XKQSgw?si=SF3J4wYa_O5tijCE

- https://python-yahoofinance.readthedocs.io/en/latest/api.html

- https://youtu.be/5RIOQuHOihY?si=RYPOCxGaE28SK04r

- https://python.langchain.com/docs/introduction/

- https://aws.amazon.com/what-is/retrieval-augmented-generation/

- https://openai.com/index/introducing-deep-research/

- https://techcommunity.microsoft.com/blog/educatordeveloperblog/welcome-to-the-new-phi-4-models---microsoft-phi-4-mini--phi-4-multimodal/4386037

- https://ollama.com/

Presentation (Prezi Link):

https://prezi.com/view/126TGN0eCgijBZXVbWJF/



## Quick start (local)

Requirements:
- Python 3.10+
- Ollama running locally with `phi4-mini:3.8b` (or adjust model names in code)
- Install Python dependencies: `flask`, `yfinance`, `langchain_ollama`, `langchain_chroma`, `langchain_core`

Run the app (from repository root):

```bash
python -m src.app
```
Then open it in your browser. The simple web UI will send messages to `/api/chat` and display the bot replies. The backend uses the existing `retriever` and `get_stock_price` functions in `src/vector.py`.

