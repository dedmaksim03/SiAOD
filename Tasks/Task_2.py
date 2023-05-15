def is_palindrome(s):
    for i in range(0, len(s)//2):
        if s[i] != s[-i-1]:
            return False
    return True


def max_palindrome(s):
    for i in range(len(s), 1, -1):
        for j in range(0, len(s)-i+1):
            if is_palindrome(s[j:i+j]):
                return s[j:i+j]
    return "Палиндрома нет"


def is_concatenation(s):
    if len(s) % 2 != 0:
        return False
    if len(s) == 2:
        return s[0] == s[1]
    return s[0:len(s)//2-1] == s[len(s)//2:-1]


def concatenation(s):
    count = 0
    strings = []
    for i in range(len(s), 1, -1):
        for j in range(0, len(s) - i + 1):
            if is_concatenation(s[j:i + j]) and s[j:i+j] not in strings:
                count += 1
                strings.append(s[j:i+j])
                print(s[j:i + j])
    return count


print(concatenation("abcabcabc"))
