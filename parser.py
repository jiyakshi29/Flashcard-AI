def parse_flashcards(raw_text):
    flashcards = []
    lines = raw_text.strip().split("\n")
    question = None
    for line in lines:
        line = line.strip()
        if line.startswith("Q:"):
            question = line[2:].strip()
        elif line.startswith("A:") and question:
            answer = line[2:].strip()
            flashcards.append({"question": question, "answer": answer})
            question = None
    return flashcards
