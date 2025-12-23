# Winter Break GenAI Project: Multi-Agent Research Assistant with Evaluation Pipeline

## Project Overview
Build a **production-grade, multi-agent research system** that can analyze technical documentation, answer complex queries, and self-evaluate its responses — all using open-source tools running locally.

## Why This Project?
- **Multi-agent orchestration** is where GenAI is heading (not simple chatbots)
- Combines **RAG + Agents + Evaluation** (the holy trinity of production GenAI)
- Leverages your **data engineering skills** (ETL pipelines, data quality, monitoring)
- Entirely **local and open-source** (no API costs)
- Portfolio-worthy project that demonstrates senior-level thinking

## Tech Stack (100% Free & Open Source)

### Core LLM
- **Ollama** - Run LLMs locally (Llama 3.1, Mistral, Phi-3)
- **llama.cpp** - Efficient inference

### Frameworks
- **LangGraph** - Multi-agent orchestration (successor to LangChain agents)
- **LlamaIndex** - Document processing and RAG

### Vector Database
- **ChromaDB** (open-source)

### Evaluation
- **Ragas** - RAG evaluation framework
- **DeepEval** - LLM output evaluation

### Monitoring & UI
- **Streamlit** - Web interface
- **MLflow** - Experiment tracking
- **Phoenix (Arize AI)** - LLM observability

## Implementation Phases

### Phase 1: Foundation
**Goal:** Set up local LLM infrastructure and basic RAG

1. Install Ollama and download 2-3 models (Llama 3.1 8B, Mistral 7B)
2. Build document ingestion pipeline:
   - Support PDF, Markdown, code files
   - Implement advanced chunking (semantic chunking, not just fixed-size)
   - Generate embeddings using local models
3. Set up ChromaDB with metadata filtering
4. Create basic RAG query system
5. Integrate MLflow for experiment tracking

**Deliverables:**
- Working local LLM setup
- Document processing pipeline handling 100+ documents
- Basic RAG Q&A system

### Phase 2: Multi-Agent System
**Goal:** Build agent orchestration with LangGraph

1. **Router Agent:** Classifies query type and routes to appropriate specialist
2. **Research Agent:** RAG-based agent for document retrieval
3. **SQL Agent:** Queries structured data (use sample DB like Chinook)
4. **Code Agent:** Analyzes code repositories using AST parsing + RAG
5. **Synthesis Agent:** Combines outputs from multiple agents into coherent answer

**Challenge:** Implement agent memory and state management using LangGraph's graph-based approach

**Deliverables:**
- 5 working agents with clear responsibilities
- Routing logic with confidence thresholds
- Agent conversation history and context management

### Phase 3: Evaluation & Guardrails 
**Goal:** Make it production-grade with evaluation and safety

1. **Build Evaluation Pipeline:**
   - Implement Ragas metrics (faithfulness, answer relevancy, context precision)
   - Create custom evaluation metrics for your domain
   - Use "LLM-as-Judge" for quality scoring
   - Build regression test suite with 50+ query-answer pairs

2. **Add Guardrails:**
   - Input validation (PII detection, prompt injection blocking)
   - Output filtering (hallucination detection)
   - Implement NeMo Guardrails or Guardrails AI

3. **Observability:**
   - Integrate Phoenix for tracing agent decisions
   - Log all agent interactions and decisions
   - Build dashboards showing system performance

**Deliverables:**
- Automated evaluation suite
- Guardrails preventing common attacks
- Observable system with tracing

## Success Metrics
Build evaluation around:
- **Accuracy:** % of factually correct answers (evaluated by LLM-as-Judge)
- **Latency:** Response time per query
- **Context Relevance:** Are retrieved chunks relevant?
- **Agent Efficiency:** Are agents routed correctly?
- **Hallucination Rate:** % of responses with fabricated information