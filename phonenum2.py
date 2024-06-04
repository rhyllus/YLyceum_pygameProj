class NumberError(Exception):
    pass


class StartsOrEndsWrong(NumberError):
    pass


class StackedHyphens(NumberError):
    pass


class ForbiddenSymbol(NumberError):
    pass


class WrongParentheses(NumberError):
    pass


class LengthError(NumberError):
    pass


class UnknownOperator(NumberError):
    pass


def process(number):
    number = number.strip()
    hyphens = 0
    allowed = '\t1234567890+()- '
    operators = [i for i in range(910, 920)] + [i for i in range(980, 990)] + \
                [i for i in range(920, 940)] + [i for i in range(902, 907)] + \
                [i for i in range(950, 970)]
    parentheses = 0
    try:
        for i in number:
            if i.isdigit():
                hyphens = 0
            elif i == '-':
                hyphens += 1
                if hyphens == 2:
                    raise StackedHyphens
            elif i == ')':
                if parentheses == 0:
                    raise WrongParentheses
                else:
                    parentheses -= 1
            elif i == '(':
                if parentheses != 0:
                    raise WrongParentheses
                else:
                    parentheses += 1
            elif i not in allowed:
                raise ForbiddenSymbol
        if parentheses != 0:
            raise WrongParentheses
    except NumberError:
        print('неверный формат')
    try:
        if not number.startswith('+7', '8', '+359') or not number.startswith('+55', '+1'):
            raise StartsOrEndsWrong
        if number[0] == '-' or number[-1] == '-':
            raise StartsOrEndsWrong
    except StartsOrEndsWrong:
        print('не определяется код страны')
    else:
        if number[0] == '8':
            number = '+7' + number[1::]
        number = number.translate({ord(c): None for c in '\t()- '})
        try:
            if int(number[2:5]) not in operators:
                raise UnknownOperator
            if len(number) == 12:
                print(number)
            else:
                raise LengthError
        except LengthError:
            print('неверное количество цифр')
        except UnknownOperator:
            print('не определяется оператор сотовой связи')


process(input())
