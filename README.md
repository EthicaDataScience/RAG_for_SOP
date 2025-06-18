# Clinical SOP AI Assistant (Hybrid CAG + RAG on Azure)

This project implements a secure, production-grade **AI Assistant** for Clinical SOPs using a **hybrid Cache-Augmented Generation (CAG)** and **Retrieval-Augmented Generation (RAG)** approach. It is designed to answer employee questions with traceable, citation-backed responses.

---

## **Key Features**

- 🔍 **RAG Pipeline:** Retrieve SOP context from a vector store.
- 🗂️ **CAG Layer:** Embed static policies and instructions as cached context.
- 🤖 **Azure OpenAI:** Use GPT-4 or GPT-3.5 for final response generation.
- 🔐 **Secure Auth:** Azure AD B2C for user authentication.
- 🌐 **Web-based UI:** Frontend via React, Streamlit, or Copilot Studio.
- 📊 **Monitoring:** Azure Monitor & App Insights for usage and performance.

---
## **Project Roadmap**

The full roadmap, step-by-step plan, and technical details are included [here](./SOP%20RAG%20Generation%20Roadmap.md).

**Phases:**
- Ideation & Scoping
- Data Preprocessing & CAG Setup
- RAG Pipeline Development
- Web App & Azure Deployment
- Testing & QA
- Production Integration & Maintenance
---


