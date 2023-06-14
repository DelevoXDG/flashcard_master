from collections import deque

from . import (
    Deck,
    Flashcard,
    get_scoped_session,
)

class Playlist:
    # Define difficulty levels
    difficulties = {
        "Easy": [1, 2, 3],
        "Medium": [2, 1, 3],
        "Hard": [3, 2, 1],
    }

    def __init__(self, deck_ids, difficulty=None, study_type=None):
        self.flashcard_queue = deque()
        session = get_scoped_session()

        # Get flashcards from database
        flashcards = session.query(Flashcard).filter(Flashcard.deck_id.in_(deck_ids)).all()

        # Sort flashcards by given difficulty level
        if difficulty in self.difficulties:
            order = self.difficulties[difficulty]
            flashcards.sort(key=lambda x: order.index(x.difficulty))

        self.flashcard_queue.extend(flashcards)
        self.cur_card = None

    def next(self):
        if self.has_next():
            self.cur_card = self.flashcard_queue.popleft()
            return self.cur_card
        else:
            return None

    def has_next(self):
        return len(self) > 0

    def handle_cur(self, is_correct):
        if self.cur_card is None:
            return
        if not is_correct:
            self.flashcard_queue.append(self.cur_card)
        self.cur_card = None

    def __len__(self):
        return len(self.flashcard_queue)
