# Adhikar Setu

### A Multilingual AI Assistant for Government Scheme Awareness and Discovery

Adhikar Setu is a final-year project that aims to develop a multilingual AI-powered platform to help citizens discover and understand relevant government welfare schemes.

The platform will provide information about government schemes, including eligibility criteria, benefits, required documents, and application-related information through a user-friendly interface and an AI-powered conversational assistant.

---

## Problem Statement

Citizens often face difficulties in finding suitable government welfare schemes because information is distributed across different portals and sources. Complex eligibility criteria, large amounts of information, and language barriers can make it difficult for users to identify schemes that are relevant to them.

Adhikar Setu aims to address these challenges by bringing scheme information into a unified platform and providing AI-assisted, multilingual access to the information.

---

## Objectives

* Provide a centralized platform for discovering government welfare schemes.
* Help users find schemes based on their requirements and eligibility.
* Provide clear information about scheme benefits, eligibility, and required documents.
* Develop an AI-powered conversational assistant for scheme-related queries.
* Support multilingual access to improve accessibility.
* Use Retrieval-Augmented Generation (RAG) to provide responses based on verified scheme information.
* Reduce irrelevant or unsupported AI-generated responses through retrieval-based answering.

---

## Key Features

The planned system will include:

* 🔍 Government Scheme Search
* 🤖 AI-powered Scheme Assistant
* 📋 Eligibility Information
* 📄 Required Documents
* 🎁 Scheme Benefits
* 🌐 Multilingual Support
* 🔎 Semantic and Hybrid Retrieval
* 📚 Retrieval-Augmented Generation (RAG)
* 💬 Conversational Query Interface
* 🔗 Links to Official Scheme Sources

> Features will be implemented and updated progressively during the development process.

---

## Proposed System Architecture

```text
                 User
                  │
                  ▼
          ┌───────────────┐
          │   Frontend    │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │   Backend API │
          └───────┬───────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌────────────────┐
│ Scheme        │   │ RAG Pipeline   │
│ Database      │   │                │
└───────────────┘   └───────┬────────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
              Vector Database       LLM
                    │                │
                    └───────┬────────┘
                            ▼
                     AI-generated
                        Response
```

---

## Technology Stack

### Frontend

* HTML / CSS / JavaScript
* React.js *(planned)*

### Backend

* Python
* FastAPI

### Artificial Intelligence

* Retrieval-Augmented Generation (RAG)
* Large Language Model (LLM)
* Hugging Face models
* Text Embeddings
* Semantic Search

### Database

* MongoDB *(planned)*
* Vector Database *(to be finalized during development)*

### Data Processing

* Python
* Pandas
* NumPy

### Development Tools

* Git
* GitHub
* VS Code
* Jupyter Notebook

---

## Project Structure

```text
Adhikar-Setu/
│
├── data/              # Government scheme data
├── backend/           # Backend APIs and services
├── frontend/          # User interface
├── rag/               # RAG and retrieval pipeline
├── database/          # Database-related components
├── models/            # AI/ML models
├── utils/             # Utility functions
├── tests/             # Testing
├── docs/              # Project documentation
├── weekly_reports/    # Development progress reports
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Development Approach

The project will be developed incrementally through multiple development stages:

1. Requirement analysis
2. Government scheme data collection
3. Data cleaning and structuring
4. Database development
5. Document processing and embeddings
6. Vector search and retrieval
7. RAG pipeline development
8. Backend API development
9. Multilingual support
10. Frontend development
11. System integration
12. Testing and evaluation
13. Deployment and documentation

---

## Team Development

The project will be developed collaboratively using Git and GitHub.

Each team member will work on separate development branches for their assigned modules. Completed changes will be reviewed and merged into the `main` branch.

```text
main
 │
 ├── rag-development
 ├── database-development
 ├── backend-development
 ├── frontend-development
 └── multilingual-development
```

---

## Project Status

🚧 **Under Development**

The project is currently in the initial development stage. Features, architecture, technologies, and implementation details may be updated as development progresses.

---

## Future Scope

* Support for additional Indian languages.
* Voice-based interaction.
* Personalized scheme recommendations.
* Improved eligibility matching.
* Integration with additional verified government data sources.
* Accessibility improvements for users with limited digital literacy.
* Deployment as a scalable web application.

---

## Disclaimer

Adhikar Setu is an academic project intended to improve access to government scheme information. Users should verify eligibility, application procedures, and other official requirements through the respective official government sources before applying.

---

## License

This project is developed for academic and educational purposes.
