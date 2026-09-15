import streamlit as st
import tempfile
import os

from main import build_flashcards
from database import (
    create_database,
    save_deck,
    get_decks,
    load_deck,
    delete_deck
)


# Create database
create_database()


# -----------------------------
# Page Settings
# -----------------------------

st.set_page_config(
    page_title="Flashcard AI",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Flashcard AI")
st.write("Turn your study notes into smart flashcards!")


# -----------------------------
# Upload PDF
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success("PDF uploaded successfully! ✅")

    if st.button("🚀 Generate Flashcards"):

        with st.spinner("Generating your flashcards... 🤖"):

            try:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    temp_pdf_path = temp_file.name

                cards = build_flashcards(
                    temp_pdf_path
                )

                os.remove(temp_pdf_path)

                if cards:

                    st.session_state.cards = cards
                    st.session_state.current_card = 0

                    st.success(
                        f"Generated {len(cards)} flashcards! 🎉"
                    )

                else:

                    st.warning(
                        "No flashcards were generated."
                    )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# -----------------------------
# Display Flashcards
# -----------------------------

if "cards" in st.session_state:

    cards = st.session_state.cards
    current = st.session_state.current_card
    card = cards[current]

    st.divider()

    st.subheader(
        f"🧠 Flashcard {current + 1} of {len(cards)}"
    )

    # Flashcard box

    st.markdown(
        """
        <div style="
            border: 2px solid #ddd;
            border-radius: 15px;
            padding: 30px;
            margin: 15px 0;
            text-align: center;
        ">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"## ❓ {card['question']}"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # Show Answer

    if st.button("👁️ Show Answer"):

        st.success(
            f"💡 {card['answer']}"
        )


    # Navigation

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⬅️ Previous"):

            if current > 0:

                st.session_state.current_card -= 1

                st.rerun()


    with col2:

        if st.button("Next ➡️"):

            if current < len(cards) - 1:

                st.session_state.current_card += 1

                st.rerun()


    # -----------------------------
    # Save Deck
    # -----------------------------

    st.divider()

    st.subheader("💾 Save This Deck")

    deck_name = st.text_input(
        "Enter a name for your deck",
        placeholder="Example: Python Basics"
    )


    if st.button("💾 Save Deck"):

        if deck_name.strip():

            save_deck(
                deck_name,
                cards
            )

            st.success(
                f"Deck '{deck_name}' saved successfully! 🎉"
            )

        else:

            st.warning(
                "Please enter a deck name."
            )


# -----------------------------
# Saved Decks
# -----------------------------

st.divider()

st.subheader("📚 Saved Decks")

decks = get_decks()


if decks:

    for deck_id, deck_name in decks:

        col1, col2, col3 = st.columns(
            [3, 1, 1]
        )


        with col1:

            st.write(
                f"📖 {deck_name}"
            )


        with col2:

            if st.button(
                "Load",
                key=f"load_{deck_id}"
            ):

                name, cards = load_deck(
                    deck_id
                )

                st.session_state.cards = cards
                st.session_state.current_card = 0

                st.rerun()


        with col3:

            if st.button(
                "Delete",
                key=f"delete_{deck_id}"
            ):

                delete_deck(deck_id)

                st.success(
                    f"Deck '{deck_name}' deleted!"
                )

                st.rerun()


else:

    st.write(
        "No saved decks yet."
    )