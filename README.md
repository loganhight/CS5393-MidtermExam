# **CS 5393: Advanced Python Midterm Exam**

# Exploring Open-Source LLMs with Ollama

- **Author:** Logan Hight
- **Date:** April 9, 2025

## **Overview**

This project explores the performance, capabilities, and ethical considerations of three open-source LLMs using [Ollama](https://ollama.ai). The assignment includes:

- Installing and running LLMs locally
- Performing basic tasks (QA, summarization, code generation, creative writing)
- Conducting focused experimentation on ethical considerations
- Analyzing results and writing a  comprehensive report
- Delivery of a 10 minute in-class presentation

---

## **Models Used**

- `tinyllama`: Lightweight, efficient transformer for quick responses
- `mistral`: Balanced model with high-quality outputs
- `llama2:13b`: Larger model with deeper contextual understanding

---

## **Project Structure**

```
CS5393-MidtermExam/
├── prompts/                            # Basic tasks and focused experimentation prompts in markdown files
│   ├── basic_tasks/
│   │   ├── question_answering.md
│   │   ├── summarization.md
│   │   ├── code_generation.md
│   │   └── creative_writing.md
│   └── focused_experimentation/
│       └── ethical_considerations.md
├── experiments/                        # Model outputs, timing, and resource usage logs
│   └── [model]/
│       ├── basic_tasks/
│       │   ├── question_answering.txt
│       │   ├── summarization.txt
│       │   ├── code_generation.txt
│       │   └── creative_writing.txt
│       └── focused_experimentation/
|           └── ethical_considerations.txt
├── graphs/
│   ├── response_time_comparison.png               # Average response time graph
│   ├── cpu_usage_comparison.png                   # Average CPU usage graph
│   └── memory_usage_comparison.png                # Average memory usage graph
├── report/                   # Final report in PDF formate
├── presentation/             # Class presentation PPTX
├── run_prompts.py            # Main script (runs each prompt for all 3 models and record output)
├── compare_timing.py         # Generates average response time graph
├── compare_resource_usage.py # Generates average CPU and memory usage graphs
├── README.md                 
```

---

## **Setup & Usage**

### 1. Clone GitHub Repository & Install Ollama

Install Ollama as per: [https://ollama.ai/download](https://ollama.ai/download)

### 2. Download Models

```bash
ollama run tinyllama
ollama run mistral
ollama run llama2:13b
```

### 3. Run Script to Collect Results

```bash
python run_prompts.py
```

- Runs each prompt for all 3 models
- Automatically logs outputs, response time, and resource usage (CPU, memory)
- Outputs saved to text file as seen above in project structure

---

## **Output Analysis**

### 1. Compare Timing

```bash
python compare_timing.py
```

Generates average response time per task/model.

### 2. Compare Resource Usage

```bash
python compare_resource_usage.py
```

Generates charts for:

- Average CPU usage per task/model
- Average Memory usage (MB) per task/model

---

## **Final Deliverables**

1. This GitHub repository which contains all code used to run the models and experiments
2. Comprehensive report in pdf format: `report/Report.pdf`
3. Presentation slides: `presentation/Presentation.pptx`
