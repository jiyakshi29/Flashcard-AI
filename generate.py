from google import genai
import os


def generate_flashcards(chunk):

    if not chunk or not chunk.strip():
        return ""

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    prompt = f"""
You are an expert AI study assistant.

Read the study material below and create high-quality flashcards.

Rules:
1. Create 3 to 5 flashcards.
2. Focus on the most important concepts.
3. Use different question types:
   - What is...?
   - Why...?
   - How...?
   - What are...?
   - Difference between...?
   - Example/application questions when possible.
4. Do not repeat similar questions.
5. Answers must be accurate and based ONLY on the study material.
6. Keep answers clear, short and useful for exam revision.
7. Use simple English suitable for a college student.
8. Do not add information that is not present in the material.
9. Output ONLY this format:

Q: question
A: answer

Q: question
A: answer

Q: question
A: answer

Study material:
{chunk}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text