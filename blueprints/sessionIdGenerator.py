import random
import string

def randomID(pwlen = 24, seed = 10):
	chars = string.ascii_letters + string.digits
	random.seed(seed)
	return ''.join(random.choice(chars) for i in range(pwlen))
