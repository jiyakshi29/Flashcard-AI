from extract import extract_text_from_pdf
from chunker import chunk_text
from generate import generate_flashcards
from parser import parse_flashcards

def build_flashcards(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    all_cards = []
    for chunk in chunks:
        raw = generate_flashcards(chunk)
        cards = parse_flashcards(raw)
        all_cards.extend(cards)
    return all_cards

if __name__ == "__main__":
    cards = build_flashcards("sample.pdf")
    print(f"Generated {len(cards)} flashcards!\n")
    for i, card in enumerate(cards, 1):
        print(f"{i}. Q: {card['question']}")
        print(f"   A: {card['answer']}\n")
    