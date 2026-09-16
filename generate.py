from google import genai
import os


def generate_flashcards(chunk):

    if not chunk or not chunk.strip():
        return ""

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    prompt = f"""
You are an expert college-level study assistant.

Your task is to create high-quality study flashcards ONLY from the
study material provided below.

IMPORTANT:
The flashcards must test the ACTUAL ACADEMIC CONTENT, not the structure
of the document.

Create exactly 3 to 5 useful flashcards from this material.

STRICT RULES:

1. Focus on important academic concepts, definitions, explanations,
   processes, principles, differences, applications, and examples.

2. NEVER create questions about document structure, such as:
   - "What are the units mentioned in the material?"
   - "How many units are there?"
   - "What topics are covered?"
   - "What is the name of Unit 1?"
   - Page numbers
   - Chapter numbers
   - Section numbers
   - Headings or subheadings

3. Do NOT ask a question merely because a phrase appears in the
   material. The question must test meaningful knowledge.

4. Avoid repeated questions.
   Questions testing the same concept in different wording are
   considered DUPLICATES.

   For example, these are duplicates:
   - What is tokenization?
   - Define tokenization.
   - What does tokenization mean?

5. Every question must be logically answerable from the study material.

6. Every answer must be supported by the study material.
   DO NOT use outside knowledge.

7. Prefer a mixture of useful question types:
   - What is...?
   - Why is...?
   - How does...?
   - What are the important features of...?
   - What is the difference between...?
   - Explain...
   - Give an example/application mentioned in the material.

8. Avoid vague questions such as:
   - "What is important?"
   - "What is mentioned?"
   - "What are the units?"
   - "What topics are discussed?"

9. Questions should be clear and suitable for college exam revision.

10. Answers should be concise but complete. Do not give one-word
    answers unless the material genuinely requires one.

11. Before producing the final flashcards, internally check:
    - Is every question about an actual academic concept?
    - Is every answer supported by the material?
    - Are any two questions testing the same concept?
    - Is any question about Unit/chapter/page/document structure?
    Remove any question that fails these checks.

12. Output ONLY this format:

Q: question
A: answer

Q: question
A: answer

Q: question
A: answer

Do not add:
- numbering
- bullets
- explanations
- introductions
- conclusions
- markdown
- extra text

STUDY MATERIAL:
{chunk}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text