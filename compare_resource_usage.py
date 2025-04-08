import os
import re
import matplotlib.pyplot as plt

models = ["tinyllama", "mistral", "llama2"]
tasks = ["question_answering", "summarization", "code_generation", "creative_writing"]

def extract_resources(model, task_file):
    cpu_usages = []
    mem_usages = []

    with open(task_file, "r", encoding="utf-8") as f:
        for line in f:
            cpu_match = re.search(r"CPU Usage: ([\d.]+)%", line)
            mem_match = re.search(r"Memory Used: ([\d.]+) MB", line)
            if cpu_match and mem_match:
                cpu_usages.append(float(cpu_match.group(1)))
                mem_usages.append(float(mem_match.group(1)))

    avg_cpu = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0
    avg_mem = sum(mem_usages) / len(mem_usages) if mem_usages else 0
    return avg_cpu, avg_mem

def main():
    os.makedirs("graphs", exist_ok=True)
    cpu_data = {model: [] for model in models}
    mem_data = {model: [] for model in models}

    for model in models:
        for task in tasks:
            path = f"experiments/{model}/basic_tasks/{task}.txt"
            if os.path.exists(path):
                avg_cpu, avg_mem = extract_resources(model, path)
                cpu_data[model].append(avg_cpu)
                mem_data[model].append(avg_mem)
            else:
                cpu_data[model].append(0)
                mem_data[model].append(0)

    x = range(len(tasks))
    width = 0.25

    # CPU Usage Plot
    fig, ax = plt.subplots()
    for i, model in enumerate(models):
        bars = ax.bar([p + i * width for p in x], cpu_data[model], width=width, label=model)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:.1f}%', ha='center', va='bottom')

    ax.set_xlabel("Task Type")
    ax.set_ylabel("Avg CPU Usage (%)")
    ax.set_title("Average CPU Usage per Task by Model")
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(tasks, rotation=15)
    ax.legend()
    plt.tight_layout()
    plt.savefig("graphs/cpu_usage_comparison.png")
    plt.close()

    # Memory Usage Plot
    fig, ax = plt.subplots()
    for i, model in enumerate(models):
        bars = ax.bar([p + i * width for p in x], mem_data[model], width=width, label=model)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 10, f'{height:.0f} MB', ha='center', va='bottom')

    ax.set_xlabel("Task Type")
    ax.set_ylabel("Avg Memory Usage (MB)")
    ax.set_title("Average Memory Usage per Task by Model")
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(tasks, rotation=15)
    ax.legend()
    plt.tight_layout()
    plt.savefig("graphs/memory_usage_comparison.png")
    plt.close()

if __name__ == "__main__":
    main()
