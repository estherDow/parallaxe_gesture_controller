import unittest

from src.domain.BookKeeper import BookKeeper
from src.domain.Labels import HandSignLabel


class MyTestCase(unittest.TestCase):
    book_keeper = BookKeeper()

    def test_should_store_hand_signs_popping_off_the_oldest_entries(self):
        self.book_keeper.push_hand_sign(HandSignLabel.OPEN)
        for i in range(1, 17):
            self.book_keeper.push_hand_sign(HandSignLabel.CLOSE)

        self.assertEqual(self.book_keeper.hand_sign_history[0], HandSignLabel.CLOSE)




if __name__ == '__main__':
    unittest.main()
