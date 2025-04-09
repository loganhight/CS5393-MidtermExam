import os                           # Provides file and directory handling
import re                           # Regular expressions for parsing timing info
import matplotlib.pyplot as plt     # For creating plots

# List of models
models = ["tinyllama", "mistral", "llama2"]

# List of task types for basic evaluation
tasks = ["question_answering", "summarization", "code_generation", "creative_writing"]

# Extract CPU and memory usage from a model outputfile
def extract_resources(model, task_file):
    cpu_usages = []  # List to store CPU usage
    mem_usages = []  # List to store memory usage

    # Open output file with UTF-8 encoding
    with open(task_file, "r", encoding="utf-8") as f:
        for line in f:
            cpu_match = re.search(r"CPU Usage: ([\d.]+)%", line)        # Locate CPU usage pattern
            mem_match = re.search(r"Memory Used: ([\d.]+) MB", line)    # Locate memory usage pattern
            if cpu_match and mem_match:
                cpu_usages.append(float(cpu_match.group(1)))            # Add CPU usage as float to cpu_usages[]
                mem_usages.append(float(mem_match.group(1)))            # Add memory usage as float to mem_usages[]

    # Calculate average CPU usage
    avg_cpu = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0
    
    # Calculate average memory usage
    avg_mem = sum(mem_usages) / len(mem_usages) if mem_usages else 0
    
    # Return average CPU usage and average memory usage as a tuple
    return avg_cpu, avg_mem

# Main plotting logic
def main():
    # Create the output directory
    os.makedirs("graphs", exist_ok=True)

    # Initialize dictionary to store average model CPU usage per task type
    cpu_data = {model: [] for model in models}
    
    # Initialize dictionary to store average model memory usage per task type
    mem_data = {model: [] for model in models}

    # Iterate through each model and task
    for model in models:
        for task in tasks:
            path = f"experiments/{model}/basic_tasks/{task}.txt"    # Path to the experiment log
            if os.path.exists(path):
                avg_cpu, avg_mem = extract_resources(model, path)   # Get average CPU and memory usage
                cpu_data[model].append(avg_cpu)                     # Add average CPU usage to avg_cpu{}
                mem_data[model].append(avg_mem)                     # Add average memory usage to avg_mem{}
            else:
                cpu_data[model].append(0)
                mem_data[model].append(0)

    # Bar chart set up
    x = range(len(tasks))   # Position for each task type
    width = 0.25            # Bar width

    # --- CPU Usage Plot --- #
    fig, ax = plt.subplots()
    for i, model in enumerate(models):
        # Plot each model
        bars = ax.bar([p + i * width for p in x], cpu_data[model], width=width, label=model)
        
        # Add values to bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,       # Center of the bar
                height + 0.5,                           # Slightly above the bar
                f'{height:.1f}%',                       # Show average CPU usage
                ha='center', va='bottom'                # Centered text
            )

    # Set chart labels and title
    ax.set_xlabel("Task Type")
    ax.set_ylabel("Avg CPU Usage (%)")
    ax.set_title("Average CPU Usage per Task by Model")
    ax.set_xticks([p + width for p in x])       # Position x-ticks
    ax.set_xticklabels(tasks, rotation=15)      # Task labels slightly tilted for readability
    ax.legend()                                 # Show legend
    
    plt.tight_layout()                          # Adjust spacing
    plt.savefig("graphs/cpu_usage_comparison.png")  # Save chart as .png file
    plt.close()                                 # Close the plot

    # --- Memory Usage Plot --- #
    fig, ax = plt.subplots()
    for i, model in enumerate(models):
        # Plot each model
        bars = ax.bar([p + i * width for p in x], mem_data[model], width=width, label=model)
        
        # Add values to bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,       # Center of the bar
                height + 10,                            # Slightly above the bar
                f'{height:.0f} MB',                     # Show average memory usaged
                ha='center', va='bottom'                # Centered text
            )

    # Set chart labels and title
    ax.set_xlabel("Task Type")
    ax.set_ylabel("Avg Memory Usage (MB)")
    ax.set_title("Average Memory Usage per Task by Model")
    ax.set_xticks([p + width for p in x])       # Position x-ticks
    ax.set_xticklabels(tasks, rotation=15)      # Task labels slightly tilted for readability
    ax.legend()                                 # Show legend
    
    plt.tight_layout()                          # Adjust spacing
    plt.savefig("graphs/memory_usage_comparison.png")  # Save the memory usage graph
    plt.close()                                 # Close the plot

# Script entry point
if __name__ == "__main__":
    main()
