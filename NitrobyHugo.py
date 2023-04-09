import random
import string
import requests
from multiprocessing import Pool

# Define the characters that can be used in the code
characters = string.ascii_uppercase + string.ascii_lowercase + string.digits

# Define the number of codes to generate
num_codes = 10

# Define the function to test a single code
def test_code(code):
    url = f'http://discord.gift/{code}'
    response = requests.get(url)
    if "This gift code may be expired or you might have the wrong" in response.text:
        return f'Code {code} is invalid: expired or incorrect'
    elif "You have claimed your gift!" in response.text:
        return f'Success! Code {code} is valid.'
    else:
        return f'Code {code} is invalid.'

# Generate the codes and test them in parallel
with Pool() as pool:
    codes = [''.join(random.choice(characters) for _ in range(16)) for _ in range(num_codes)]
    results = pool.map(test_code, codes)
    for result in results:
        print(result)
