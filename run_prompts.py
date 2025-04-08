import os
import subprocess
import time
import psutil

models = ["tinyllama", "mistral", "llama2"]
tasks = ["question_answering", "summarization", "code_generation", "creative_writing"]

def get_resource_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    return {
        "cpu_percent": cpu_percent,
        "mem_used_mb": round((mem.total - mem.available) / (1024 * 1024), 2),
        "mem_total_mb": round(mem.total / (1024 * 1024), 2),
        "mem_percent": mem.percent
    }

def run_prompt_and_capture(model: str, prompt: str) -> tuple[str, float, dict]:
    start = time.time()
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=600
        )
        output = result.stdout.decode("utf-8")
    except subprocess.TimeoutExpired:
        output = "[ERROR] Model response timed out."
    duration = round(time.time() - start, 2)
    resource_usage = get_resource_usage()
    return output.strip(), duration, resource_usage

def process_basic_tasks(model: str):
    for task in tasks:
        prompt_file = f"prompts/basic_tasks/{task}.md"
        output_file = f"experiments/{model}/basic_tasks/{task}.txt"

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(prompt_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(f"=== TASK: {task.upper()} for {model} ===\n")
            lines = f_in.readlines()

            current_prompt = None
            for line in lines:
                if line.startswith("## Prompt"):
                    f_out.write(f"\n\n{line.strip()}\n")
                    current_prompt = ""
                elif current_prompt is not None and line.strip():
                    current_prompt = line.strip()
                    f_out.write(f"> Prompt: {current_prompt}\n")
                    print(f"Running: {model} — {task} — {current_prompt}")
                    output, duration, resources = run_prompt_and_capture(model, current_prompt)
                    f_out.write(f"(Response time: {duration} seconds)\n")
                    f_out.write(f"(CPU Usage: {resources['cpu_percent']}%, Memory Used: {resources['mem_used_mb']} MB / {resources['mem_total_mb']} MB ({resources['mem_percent']}%))\n")
                    f_out.write(">>> MODEL OUTPUT:\n")
                    f_out.write(output + "\n")
                    f_out.write("===\n")
                    current_prompt = None

def process_focused_experimentation(model: str):
    prompt_file = "prompts/focused_experimentation/ethical_considerations.md"
    output_file = f"experiments/{model}/focused_experimentation/focused_experimentation_results.txt"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(prompt_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
        lines = f_in.readlines()

        current_prompt = None
        for line in lines:
            if line.startswith("## Prompt"):
                f_out.write(f"\n\n{line.strip()}\n")
                current_prompt = ""
            elif current_prompt is not None and line.strip():
                current_prompt = line.strip()
                f_out.write(f"> Prompt: {current_prompt}\n")
                print(f"Running Focused Experimentation (Ethical Considerations): {model} — {current_prompt}")
                output, duration, resources = run_prompt_and_capture(model, current_prompt)
                f_out.write(f"(Response time: {duration} seconds)\n")
                f_out.write(f"(CPU Usage: {resources['cpu_percent']}%, Memory Used: {resources['mem_used_mb']} MB / {resources['mem_total_mb']} MB ({resources['mem_percent']}%))\n")
                f_out.write(">>> MODEL OUTPUT:\n")
                f_out.write(output + "\n")
                f_out.write("===\n")
                current_prompt = None

def main():
    for model in models:
        print(f"Processing Model: {model}")
        process_basic_tasks(model)
        process_focused_experimentation(model)
        print(f"Completed {model}\n")

if __name__ == "__main__":
    main()
