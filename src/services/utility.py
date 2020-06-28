import string
import random

class Utility:
    @staticmethod
    def substring_generator(size=3, chars=string.ascii_uppercase + string.digits):
        """Generate random sequence of chars/nums"""
        return ''.join(random.choice(chars) for _ in range(size)).lower()
