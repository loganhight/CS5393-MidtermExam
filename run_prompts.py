import os           # Provides file and directory handling
import subprocess   # Used to execute model prompts via command line
import time         # Enables response timing collection
import psutil       # Allows monitoring of system resources like CPU and memory

# List of models to evaluate
models = ["tinyllama", "mistral", "llama2:13b"]

# List of task types for basic evaluation
tasks = ["question_answering", "summarization", "code_generation", "creative_writing"]  # Common NLP tasks

# Function to get current system CPU and memory usage
def get_resource_usage():
    cpu_percent = psutil.cpu_percent(interval=1)    # Measure CPU usage over a 1-second interval
    mem = psutil.virtual_memory()                   # Get memory statistics from the OS
    return {
        "cpu_percent": cpu_percent,                                             # CPU usage as a percentage
        "mem_used_mb": round((mem.total - mem.available) / (1024 * 1024), 2),   # Convert memory usage to MB
        "mem_total_mb": round(mem.total / (1024 * 1024), 2),                    # Convert total memory to MB
        "mem_percent": mem.percent                                              # Memory usage as a percentage
    }

# Function to send a prompt to the model and capture the output, response time, and resource usage
def run_prompt_and_capture(model: str, prompt: str) -> tuple[str, float, dict]:
    # Start time
    start = time.time()
    try:
        # Call the model using the Ollama CLI
        result = subprocess.run(
            ["ollama", "run", model],       # Command to execute the model
            input=prompt.encode("utf-8"),   # Encode prompt string to bytes for subprocess input
            stdout=subprocess.PIPE,         # Capture normal output
            stderr=subprocess.PIPE,         # Capture any error output
            timeout=600                     # Timeout if response takes longer than 10 minutes
        )
        output = result.stdout.decode("utf-8")  # Decode the model's response from bytes to string
    except subprocess.TimeoutExpired:
        output = "[ERROR] Model response timed out."  # Error message if timeout

    # Calculate response time
    duration = round(time.time() - start, 2)
    resource_usage = get_resource_usage()  # Record resource usage after model runs
    return output.strip(), duration, resource_usage  # Return the model's response, timing, and system stats

# Run all basic tasks for a given model and record results
def process_basic_tasks(model: str):
    # Store original model string for actual execution (i.e., "llama2:13b" instead of "llama2")
    model_actual = model

    # Fix model name for use in file paths ("llama2:13b" is not a valid directory name)
    if model == "llama2:13b":
        model = "llama2"

    for task in tasks:
        prompt_file = f"prompts/basic_tasks/{task}.md"                  # Path to markdown file with prompts
        output_file = f"experiments/{model}/basic_tasks/{task}.txt"     # Where outputs will be recorded

        # Create necessary directories
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Open input and output files with UTF-8 encoding
        with open(prompt_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(f"=== TASK: {task.upper()} for {model} ===\n")  # Header for task
            lines = f_in.readlines()                                    # Read all lines from the input prompt file

            # Reset prompt
            current_prompt = None
            
            for line in lines:
                if line.startswith("## Prompt"):
                    f_out.write(f"\n\n{line.strip()}\n")  # Section header
                    current_prompt = ""                   # New prompt
                elif current_prompt is not None and line.strip():
                    current_prompt = line.strip()                           # Actual prompt text
                    f_out.write(f"> Prompt: {current_prompt}\n")            # Write prompt to output file
                    print(f"Running: {model} — {task} — {current_prompt}")  # Log progress
                    output, duration, resources = run_prompt_and_capture(model_actual, current_prompt)  # Execute prompt
                    f_out.write(f"(Response time: {duration} seconds)\n")   # Record timing
                    f_out.write(f"(CPU Usage: {resources['cpu_percent']}%, Memory Used: {resources['mem_used_mb']} MB / {resources['mem_total_mb']} MB ({resources['mem_percent']}%))\n")  # Record resource usage
                    f_out.write(">>> MODEL OUTPUT:\n")
                    f_out.write(output + "\n")  # Write model response
                    f_out.write("===\n")
                    current_prompt = None       # Reset for next prompt

# Run focused experimentation (ethical consideration) for a given model and record results
def process_focused_experimentation(model: str):
    # Store original model string for actual execution (i.e., "llama2:13b" instead of "llama2")
    model_actual = model

    # Fix model name for use in file paths ("llama2:13b" is not a valid directory name)
    if model == "llama2:13b":
        model = "llama2"

    prompt_file = "prompts/focused_experimentation/ethical_considerations.md"                           # Path to markdown file with prompts
    output_file = f"experiments/{model}/focused_experimentation/focused_experimentation_results.txt"    # Where outputs will be recorded

    # Create necessary directories
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Open input and output files with UTF-8 encoding
    with open(prompt_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
        lines = f_in.readlines()  # Read all lines from the input prompt file

        # Reset prompt
        current_prompt = None
        
        for line in lines:
            if line.startswith("## Prompt"):
                f_out.write(f"\n\n{line.strip()}\n")    # Section header
                current_prompt = ""                     # New prompt
            elif current_prompt is not None and line.strip():
                current_prompt = line.strip()                   # Actual prompt text
                f_out.write(f"> Prompt: {current_prompt}\n")    # write prompt to file
                print(f"Running Focused Experimentation (Ethical Considerations): {model} — {current_prompt}")  # Log progress
                output, duration, resources = run_prompt_and_capture(model_actual, current_prompt)              # Execute prompt
                f_out.write(f"(Response time: {duration} seconds)\n")  # Record timing
                f_out.write(f"(CPU Usage: {resources['cpu_percent']}%, Memory Used: {resources['mem_used_mb']} MB / {resources['mem_total_mb']} MB ({resources['mem_percent']}%))\n")  # Record resource usage
                f_out.write(">>> MODEL OUTPUT:\n")
                f_out.write(output + "\n")  # Write model response
                f_out.write("===\n")
                current_prompt = None       # Reset prompt

# Main function to iterate through all models and run all basic tasks and focused experimentation
def main():
    for model in models:
        print(f"Processing Model: {model}")     # Progress update
        process_basic_tasks(model)              # Run and log basic tasks
        process_focused_experimentation(model)  # Run and log focused experimentation (ethical considerations)
        print(f"Completed {model}\n")           # Progress update

# Script entry point
if __name__ == "__main__":
    main()
