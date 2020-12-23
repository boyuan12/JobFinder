import random
import string

def random_str(n=20):
    return "".join([random.choice(string.ascii_letters) for s in range(n)])