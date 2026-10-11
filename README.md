=
# Data Science Portfolio

A collection of practical projects in **data analytics, machine learning, AI engineering, and data visualisation**, demonstrating end-to-end problem-solving from data preparation and exploratory analysis to predictive modelling, application development, evaluation, and deployment.

Projects incorporate real-world analytical techniques, reproducible workflows, and software engineering practices, including Docker, automated testing, and CI/CD.

## Projects

### AI & LLM Engineering

#### [RAG Knowledge Assistant](rag-chatbot/)

A locally running **Retrieval-Augmented Generation (RAG) chatbot** that allows users to upload PDF documents and ask natural-language questions about their contents.

- Built an end-to-end RAG pipeline using LangChain, Sentence Transformers, ChromaDB, and Llama 3.2 through Ollama.
- Developed a FastAPI backend and interactive Streamlit frontend, supporting PDF uploads, document-specific retrieval, and source references.
- Containerised the application using Docker Compose and implemented automated testing with Pytest and GitHub Actions CI/CD.
- Evaluated retrieval and answer generation using a small synthetic dataset, achieving 100% on keyword-based retrieval (3/3) and answer/refusal checks (5/5), with an average response latency of 1.35 seconds.

**Technologies:** Python, LangChain, FastAPI, Streamlit, ChromaDB, Sentence Transformers, Ollama, Docker, Pytest, GitHub Actions.

[View Project Documentation](rag-chatbot/README.md)

### Machine Learning

#### [Daily Active Customer Forecasting](machine-learning/daily-active-customer-forecasting/)

Forecasting daily active banking customers using XGBoost and statistical baselines, with time-series feature engineering and chronological model evaluation.

**Technologies:** Python, Pandas, Scikit-learn, XGBoost.

### Data Analysis

#### [Respiratory Sound Analysis](data-analysis/respiratory-sound-analysis/)

Exploratory analysis of respiratory sound data, including patient demographics, diagnoses, and abnormal breathing sounds.

**Focus:** Data cleaning, exploratory data analysis, statistical exploration, and insight generation.

### Data Visualisation

#### [Chocolate Rating Dashboard](data-visualization/chocolate-rating-dashboard/)

An interactive dashboard exploring how cocoa origin, ingredients, cocoa percentage, and flavour characteristics relate to chocolate ratings.

**Technologies:** HTML, CSS, JavaScript.

[View Live Dashboard](https://areebak01.github.io/Data-Science-Portfolio/data-visualization/chocolate-rating-dashboard/)

## Tools and Technologies

**Programming & Data Analysis:** Python, SQL, Pandas, NumPy, Scikit-learn

**Machine Learning:** XGBoost, Time-Series Forecasting, Feature Engineering, Model Evaluation

**AI & LLM Engineering:** LangChain, Retrieval-Augmented Generation (RAG), Sentence Transformers, ChromaDB, Ollama

**Application Development:** FastAPI, Streamlit, HTML, CSS, JavaScript

**Software Engineering & MLOps:** Docker, Docker Compose, Pytest, GitHub Actions, CI/CD

## About This Portfolio

This portfolio demonstrates my interest in applying data analytics, machine learning, and AI to practical problems, with an emphasis on building reproducible solutions and communicating results clearly.

Projects range from exploratory data analysis and interactive visualisation to predictive modelling and end-to-end AI application development.

More projects will be added as the portfolio develops.
