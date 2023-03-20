import io
import shlex
import time

from deque import Deque
from stack import Stack


def sort_books(name_file):
    def _sort_books(_first: Deque, _second: Deque):
        min_name = chr(126)  # Максимально возможный символ

        while not _second.is_empty():
            name = _second.remove_left()
            for i in range(len(min_name)):
                if name[i] < min_name[i]:
                    _first.add_left(name)
                    min_name = name
                    break
                elif name[i] > min_name[i]:
                    _first.add_right(name)
                    break

        return _first.remove_left()

    first = Deque()
    second = Deque()
    sorted_books = []
    file = io.open(name_file, encoding='utf-8')
    books = file.read().split('\n')
    for name in books:
        second.add_right(name)
    switch = True
    while not second.is_empty() or not first.is_empty():
        if switch:
            sorted_books.append(_sort_books(first, second))
            switch = False
        else:
            sorted_books.append(_sort_books(second, first))
            switch = True
    return sorted_books


def decoder():
    alf = "абвгдеёжзиклмнопрстуфхцчшщъыьэюя"

    def encrypt(n, word):
        new_word = ""
        k = -1
        deque = Deque()
        for i in alf:
            deque.add_right(i)
        while len(word) > 0:
            change_char = deque.remove_left()
            if k >= 1 and k != n:
                k += 1
            elif k >= 1 and k == n:
                new_word += change_char
                word = word[1:]
                k = -1
            if len(word) > 0 and word[0] == change_char:
                k = 1

            deque.add_right(change_char)
        return new_word

    def decrypt(n, word):
        new_word = ""
        k = -1
        deque = Deque()
        for i in alf:
            deque.add_right(i)
        while len(word) > 0:
            change_char = deque.remove_right()
            if k >= 1 and k != n:
                k += 1
            elif k >= 1 and k == n:
                new_word += change_char
                word = word[1:]
                k = -1
            if len(word) > 0 and word[0] == change_char:
                k = 1

            deque.add_left(change_char)
        return new_word

    print(encrypt(6, "цезарь"))
    print(decrypt(6, "ьлоёцв"))


def towers_of_hanoi():
    a, b, c = Stack(), Stack(), Stack()

    def hanoi(n, start, temp, end):
        if n <= 1:
            return
        elif n == 2:
            temp.push(start.pop())
            end.push(start.pop())
            end.push(temp.pop())
        else:
            hanoi(n - 1, start, end, temp)
            end.push(start.pop())
            hanoi(n - 1, temp, start, end)

    with open("text_files/towers_of_hanoi.txt", 'r') as f:
        for line in f:
            word = line.strip().split(" ")[::-1]
            print(word)
            n = len(word)
            for i in word:
                a.push(int(i))
            hanoi(n, a, b, c)
            while not c.is_empty():
                print("c: ", c.pop())


def check_balance_stack(name_file):
    """
    Принимает текстовый файл на алгоритмическом языке и с помощью стека проверяет баланс
    квадратных скобок в тексте
    """
    file = io.open(name_file, encoding='utf-8')
    stack = Stack()
    words = shlex.split(file.read())  # Записываем в спомогательный массив содержимое файла
    for item in words:  # Заполняем стек
        stack.push(item)
    op, close = 0, 0  # Количество открытых и закрытых скобок
    for i in range(0, stack.size(), 1):
        item = stack.pop()
        if item == '[':
            op += 1
        if item == ']':
            close += 1
    if op == close:
        return "Баланс сошелся"
    return "Баланс не сошелся"


def check_balance_deque(name_file):
    """
    Принимает текстовый файл на алгоритмическом языке и с помощью дека проверяет баланс
    круглых скобок в тексте.
    """
    file = io.open(name_file, encoding='utf-8')
    deque = Deque()
    string = file.read()
    for symbol in string:
        if symbol == "(":  # Если открытая, то добавляем в дек
            deque.add_right(symbol)
        elif symbol == ")":  # Если закрытая, то, если дек не пустой, убираем одну открытую из дека
            if deque.is_empty():
                return "Баланс не сошелся"
            deque.remove_right()
    if deque.size() % 2 == 0:
        return "Баланс сошелся"
    return "Баланс не сошелся"


def print_symbols(name_file):
    """
    Принимает файл с последовательностью символов. Выводит на экран сначала числа, затем
    буквы, а затем все остальное в том же порядке, в каком они были в файле
    """
    file = io.open(name_file, encoding='utf-8')
    numbers = Stack()
    symbols = Stack()
    etc = Stack()
    string = file.read()
    for i in range(len(string) - 1, -1, -1):
        if string[i].isdigit():
            numbers.push(string[i])
        elif string[i].isalpha():
            symbols.push(string[i])
        else:
            etc.push(string[i])
    out = []
    while not numbers.is_empty():
        out.append(numbers.pop())
    while not symbols.is_empty():
        out.append(symbols.pop())
    while not etc.is_empty():
        out.append(etc.pop())
    print(*out)


def print_numbers(name_file):
    """
    Принимает файл с последовательностью целых чисел. Выводит на экран сначала отрицательные числа, затем
    положительные в том же порядке, в каком они были в файле
    """
    file = io.open(name_file, encoding='utf-8')
    s = file.read().split(" ")
    numbers = Deque()
    for number in s:
        if int(number) < 0:
            print(number, end=" ")
        else:
            numbers.add_right(int(number))
    for i in range(numbers.size()):
        print(numbers.remove_left(), end=" ")


def reverse_strings(name_file):
    """
    Принимает файл с несколькими строками. Выводит на экран эти строки в обратном порядке с помощью стека
    """
    file = io.open(name_file, encoding='utf-8')
    strings = file.read().split("\n")
    stack = Stack()
    for string in strings:
        stack.push(string)
    out = ""
    while not stack.is_empty():
        out += stack.pop() + "\n"
    return out


if __name__ == '__main__':
    # print_numbers("text_files/numbers.txt")
    # print(check_balance_deque('text_files/algorithm_language.txt'))
    # print_symbols("text_files/symbols.txt")
    # print(sort_books("text_files/books.txt"))
    decoder()
