HASH_LETTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62encode(num_to_encode):
    code = []
    while (num_to_encode > 0):
        # base62 encoding stuff
        remainder = num_to_encode % 62
        num_to_encode = num_to_encode // 62
        code.append(remainder)

    return reduce(lambda accum, num: accum + HASH_LETTERS[num], code, "")
