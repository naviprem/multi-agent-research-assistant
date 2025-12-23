# Project Setup

## Prerequisites

```bash
# Install Ollama
brew install ollama

# Verify installation
ollama --version

# Start the Ollama service: 
ollama serve

# Pull a model: 
ollama pull llama2

# Run a model: 
ollama run llama2

# List installed models: 
ollama list

# To start ollama now and restart at login:
brew services start ollama
```

## Download Models

```bash
# Primary model (8B parameters, good balance)
ollama pull llama3.1

# Alternative smaller model (faster, less accurate)
ollama pull mistral

# Test the model
ollama run llama3.1
# Type: "Hello, explain what you are in one sentence"
# Press Ctrl+D to exit
```

## Create Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

# Test

```bash
python3 -m notebooks.test_loader
python3 -m notebooks.test_chunking
python3 -m notebooks.build_vector_db
python3 -m notebooks.query_system
python3 -m notebooks.evaluate_rag
python3 -m notebooks.test_langgraph
python3 -m notebooks.test_router
python3 -m notebooks.test_research_agent
python3 -m notebooks.create_sample_db
python3 -m notebooks.test_sql_agent
python3 -m notebooks.test_code_agent
python3 -m notebooks.run_multi_agent
python3 -m notebooks.evaluate_multi_agent
python3 -m notebooks.test_evaluation_deps
python3 -m notebooks.run_ragas_evaluation
python3 -m notebooks.run_llm_judge
python3 -m notebooks.test_guardrails
python3 -m notebooks.run_with_phoenix.py
# Visit http://localhost:6006 to see traces
python3 -m notebooks.run_regression_tests
python3 -m notebooks.generate_dashboard
```