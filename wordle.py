"""
def wordle(secret: str, guess: str):
   ....
   print(result)


> wordle("horse", "human")
> gbbbb

> wordle("horse", "hello")
> gybby


> wordle("hello", "hhhhh")
> gbbbb

>wordle("hello hi", "oooooooo")
>bbbbgbbb

>wordle("hello hi", "hhhhhhhh")
>gbbbbbgb
"""

# def wordle(secret: str, guess: str):
#     """ return b if not exist in secret, y if exist in secret but in different position and didn't get g, otherwise return b """
#     result = []
#     for i in range(len(secret)):
#         if secret[i] == guess[i]:
#             result.append('g')
#         elif secret[i] in guess:
#             result.append('y')
#         else:
#             result.append('b')
#
#     print(''.join(result))
#     return ''.join(result)


from collections import Counter


def wordle(secret: str, guess: str):
    """
    Return 'g' if the letter is in the correct position,
    'y' if the letter is in the secret but in a different position and not already marked as 'g',
    otherwise return 'b'.
    """
    result = ['b'] * len(secret)
    # secret_counter = Counter(secret)  # Counter have the ability to do `secret_counter[un_existing_key]` without raising an exception
    secret_counter = {c: secret.count(c) for c in secret}


    # Single loop to handle both 'g' and 'y'
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            result[i] = 'g'
            secret_counter[guess[i]] = secret_counter.get(guess[i], 0) - 1  # Exact match, decrement count immediately
    for i in range(len(secret)):
        if result[i] == 'b' and secret_counter.get(guess[i]) and secret_counter[guess[i]] > 0:
            result[i] = 'y'
            secret_counter[guess[i]] = secret_counter.get(guess[i], 0) - 1  # Potential yellow, decrement only if still available
    print(''.join(result))
    return ''.join(result)


assert wordle("horse", "human") == 'gbbbb'
assert wordle("horse", "hello") == 'gybby'
assert wordle("hello", "hhhhh") == 'gbbbb'
assert wordle("hello hi", "oooooooo") == 'bbbbgbbb'
assert wordle("hello hi", "hhhhhhhh") == 'gbbbbbgb'
assert wordle("hhhhhhhh", "hello hi") == 'gbbbbbgb'

print('success')