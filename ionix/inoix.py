"""
s = '((1 +3 * [8 -5])'
s = '(1 +3 * [8 -5])}'
s = ' '
s = ' '

"""
def is_valid(s: str) -> bool:
    stack = []
    brackets = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    if not s:
        return True
    
    for char in s:
        if char in brackets.values():
            stack.append(char)

        elif char in brackets.keys():
            if not stack or brackets[char] != stack.pop():
                return False

    return not stack

