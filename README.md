# 🤖 SME AI Agent Pipeline

A production-ready, cost-optimized AI Agent backend designed specifically for Small and Medium Enterprises (SMEs). This pipeline serves as an API Gateway to handle multi-tenant chatbot interactions, enforce usage quotas, and drastically reduce LLM costs through advanced caching strategies.

## ✨ Key Features

* **Multi-Tenant Architecture:** Secure isolation of SME data and settings using `X-Shop-ID` and JWT Authentication.
* **Cost Optimization Engine:** Achieves a high gross margin via Google Gemini's Context Caching (Layer 2), reducing input token costs by up to 90% for repetitive knowledge base queries.
* **Token & Quota Management:** Real-time token usage tracking and monthly quota enforcement backed by Supabase.
* **LLM Observability:** Integrated with Langfuse to trace latency, monitor token consumption, and calculate costs per message.
* **Graceful Fallbacks:** Built-in error handling for rate limits and free-tier exhaustions, ensuring uninterrupted service.

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **LLM Orchestration:** [LangChain](https://www.langchain.com/)
* **AI Models:** Google Gemini 2.5 Flash / Flash-Lite
* **Database & Auth:** [Supabase](https://supabase.com/) (PostgreSQL)
* **Observability:** [Langfuse](https://langfuse.com/)
* **Deployment:** Railway (Template available)

## 🏗️ System Architecture

1.  **API Gateway:** FastAPI intercepts incoming chat requests (e.g., from LINE OA or Web Frontend).
2.  **Auth & Quota Layer:** Verifies JWT and checks Supabase for the shop's remaining token quota (`shop_quota` table).
3.  **Cache Wrapper (Layer 2):** Evaluates if the shop's Knowledge Base (KB) exceeds 1,024 tokens to utilize Gemini Prompt Caching.
4.  **Agent Execution:** LangChain processes the user query using the optimized context.
5.  **Background Logging:** Traces are sent to Langfuse, and `token_usage` is updated asynchronously in Supabase without blocking the API response.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Google AI Studio API Key
* Supabase Project URL & Service Key
* Langfuse API Keys

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/UWillC-How/SME-AI-Agent.git
   cd sme-ai-agent
