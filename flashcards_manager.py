
import json
import os

FLASHCARDS_FILE = "flashcards.json"


def load_flashcards():
    """Load flashcards from JSON or create file if it doesn't exist."""
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
    #front = input("Front of card: ")
    #back = input("Back of card: ")

    flashcards = load_flashcards()
    flashcards.append({"front": front, "back": back})
    save_flashcards(flashcards)

    #print("Flashcard saved!\n")


def delete_all_flashcards():
    save_flashcards([])   # overwrite with empty list
    #print("All flashcards have been deleted!\n")


