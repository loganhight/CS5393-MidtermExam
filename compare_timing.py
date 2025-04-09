import os                           # Provides file and directory handling
import re                           # Regular expressions for parsing timing info
import matplotlib.pyplot as plt     # For creating plots

# List of models
models = ["tinyllama", "mistral", "llama2"]

# List of task types for basic evaluation
tasks = ["question_answering", "summarization", "code_generation", "creative_writing"]

# Extract response times from a model output file
def extract_timings(model, task_file):
    # List to store times
    times = []
    
    # Open output file with UTF-8 encoding
    with open(task_file, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"Response time: (\d+\.?\d*) seconds", line)  # Locate timing pattern
            if match:
                times.append(float(match.group(1)))                         # Add time as float to times[]
                
    # Return list of times
    return times

# Main plotting logic
def main():
    # Create the output directory
    os.makedirs("graphs", exist_ok=True)

    # Initialize dictionary to store average model response time per task type
    data = {model: [] for model in models}

    # Iterate through each model and task
    for model in models:
        for task in tasks:
            path = f"experiments/{model}/basic_tasks/{task}.txt"    # Path to the experiment log
            if os.path.exists(path):
                times = extract_timings(model, path)                # Get response times
                avg_time = sum(times) / len(times) if times else 0  # Compute average response time for task type
                data[model].append(avg_time)                        # Add average time to data{}
            else:
                data[model].append(0)

    # Bar chart setup
    x = range(len(tasks))   # Position for each task type
    width = 0.25            # Bar width

    # --- Response Time Plot --- #
    fig, ax = plt.subplots()
    for i, model in enumerate(models):
        # Plot each model
        bars = ax.bar([p + i * width for p in x], data[model], width=width, label=model)
        
        # Add values to bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,     # Center of the bar
                height + 0.1,                           # Slightly above the bar
                f'{height:.2f}',                        # Show average time
                ha='center', va='bottom'                # Centered text
            )

    # Set chart labels and title
    ax.set_xlabel("Task Type")
    ax.set_ylabel("Avg Response Time (s)")
    ax.set_title("Average Response Time per Task by Model")
    ax.set_xticks([p + width for p in x])   # Position x-ticks
    ax.set_xticklabels(tasks, rotation=15)  # Task labels slightly tilted for readability
    ax.legend()                             # Show legend

    plt.tight_layout()                      # Adjust spacing
    plt.savefig("graphs/response_time_comparison.png")  # Save chart as .png file
    plt.close()                             # Close the plot

# Script entry point
if __name__ == "__main__":
    main()
