import json

# Path to your input .txt file
input_file = "Filled_Farming_Questions_and_Answers.txt"
output_file = "Farming_QA.json"

# Initialize variables
qa_pairs = []
question = ""
answer = ""

# Read and parse the file
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith("Q"):
            if question and answer:
                qa_pairs.append({"Question": question, "Answer": answer})
            question = line[3:].strip()  # Remove "QX. "
            answer = ""
        elif line.startswith("A:"):
            answer = line[2:].strip()
        elif line:
            answer += " " + line  # Multi-line answer

    # Add the last Q&A pair
    if question and answer:
        qa_pairs.append({"Question": question, "Answer": answer})

# Write to JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(qa_pairs, f, indent=2, ensure_ascii=False)

print(f"Saved {len(qa_pairs)} Q&A pairs to {output_file}")
