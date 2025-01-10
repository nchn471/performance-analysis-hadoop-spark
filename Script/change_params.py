import argparse
import re

def change_params(input_split, parallelism, buffer, max_size_in_flight, file_path="env.py"):
    with open(file_path, 'r') as file:
        content = file.read()

    params = {
        "input_split": input_split,
        "parallelism": parallelism,
        "buffer": buffer,
        "max_size_in_flight": max_size_in_flight
    }

    for param, value in params.items():
        pattern = rf"^{param}\s*=\s*.*$"
        replacement = f"{param} = {repr(value)}"
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Parameters updated in {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_split", type=int, help="Set input_split value")
    parser.add_argument("--parallelism", type=int, help="Set parallelism value")
    parser.add_argument("--buffer", type=str, help="Set buffer value")
    parser.add_argument("--max_size_in_flight", type=str, help="Set max_size_in_flight value")
    
    args = parser.parse_args()

    change_params(
        input_split=args.input_split,
        parallelism=args.parallelism,
        buffer=args.buffer,
        max_size_in_flight=args.max_size_in_flight
    )
