
import json
import os

FLASHCARDS_FILE = "flashcards.json"


def load_flashcards():
    """Load flashcards from JSON"""
    if not os.path.exists(FLASHCARDS_FILE):
        with open(FLASHCARDS_FILE, "w") as f:
            json.dump([], f)
        return []

    with open(FLASHCARDS_FILE, "r") as f:
        return json.load(f)


def save_flashcards(flashcards):
    """Save flashcards list to JSON file."""
    with open(FLASHCARDS_FILE, "w") as f:
        json.dump(flashcards, f, indent=4)


def add_flashcard(front,back):
    flashcards = load_flashcards()
    flashcards.append({"front": front, "back": back})
    save_flashcards(flashcards)

def delete_all_flashcards():
    save_flashcards([])   



