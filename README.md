# **CS 5393: Advanced Python Midterm Exam**

# Exploring Open-Source LLMs with Ollama

- **Author:** Logan Hight
- **Date:** April x, 2025

## **Overview**

This project explores the performance, capabilities, and ethical behavior of three open-source large language models (LLMs) using [Ollama](https://ollama.ai). The assignment includes:

- Installing and running LLMs locally
- Performing basic tasks (QA, summarization, code generation, creative writing)
- Conducting focused experimentation on ethical considerations
- Analyzing results and writing a report

---

## **Models Used**

- `tinyllama`: Lightweight, efficient transformer for quick responses
- `mistral`: Balanced model with high-quality outputs
- `llama2:13b`: Larger model with deeper contextual understanding

---

## **Project Structure**

```
CS5393-MidtermExam/
├── prompts/                  # Basic tasks and focused experimentation prompts
├── experiments/              # Model outputs, timing, and resource usage logs
├── graphs/                   # Output analysis graphs as .png files
├── report/                   # Final report PDF
├── presentation/             # Class presentation PPTX
├── run_prompts.py            # Main script (run each prompt for all 3 models; collect output, save generation time, and log resource usage)
├── compare_timing.py         # Visualize response timing
├── compare_resource_usage.py # Visualize CPU and memory usage
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
python3 run_prompts.py
```

- Runs each prompt for all 3 models
- Automatically logs outputs, response time, and resource usage (CPU, memory)
- Outputs saved to `experiments/<model>/<task>.txt`

---

## **Output Analysis**

### 1. Compare Timing

```bash
python3 compare_timing.py
```

Generates average response time per task/model.

### 2. Compare Resource Usage

```bash
python3 compare_resource_usage.py
```

Generates charts for:

- Average CPU usage
- Average Memory usage (MB)

---

## **Final Deliverables**

- `report/CS5393_Midterm_Report.pdf`
- `presentation/CS5393_Midterm_Presentation.pptx`
- This complete GitHub repository

---

## **References**

- [Ollama Docs](https://ollama.ai/docs)
- [Hugging Face Model Hub](https://huggingface.co/models)
