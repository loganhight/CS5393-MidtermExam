import os
import re
import matplotlib.pyplot as plt

models = ["tinyllama", "mistral", "llama2"]
tasks = ["question_answering", "summarization", "code_generation", "creative_writing"]

def extract_timings(model, task_file):
    times = []
    with open(task_file, "r") as f:
        for line in f:
            match = re.search(r"Response time: (\d+\.?\d*) seconds", line)
            if match:
                times.append(float(match.group(1)))
    return times

def main():
    os.makedirs("graphs", exist_ok=True)
    data = {model: [] for model in models}

    for model in models:
        for task in tasks:
            path = f"experiments/{model}/basic_tasks/{task}.txt"
            if os.path.exists(path):
                times = extract_timings(model, path)
                avg_time = sum(times) / len(times) if times else 0
                data[model].append(avg_time)
            else:
                data[model].append(0)

    x = range(len(tasks))
    width = 0.25

    fig, ax = plt.subplots()
    for i, model in enumerate(models):
        bars = ax.bar([p + i * width for p in x], data[model], width=width, label=model)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.2f}', ha='center', va='bottom')

    ax.set_xlabel("Task Type")
    ax.set_ylabel("Avg Response Time (s)")
    ax.set_title("Average Response Time per Task by Model")
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(tasks, rotation=15)
    ax.legend()
    plt.tight_layout()
    plt.savefig("graphs/response_time_comparison.png")
    plt.close()

if __name__ == "__main__":
    main()
