__author__ = "Afanasin Egor"
__version__ = "1.1"

from operator import and_, or_, xor, eq, ne, not_

ALLOWED_NAMES = {
    "NOT": lambda x: int(not_(x)),
    "AND": and_,
    "OR": or_,
    "XOR": xor,
    "EQ": lambda x, y: int(eq(x, y)),
    "ANTIEQ": lambda x, y: int(ne(x, y)),
    "IMP": lambda x, y: or_(not_(x), y),
}


PS1 = "variables >>> "  # Приглашение на ввод переменных.
PS2 = "Bool_Exp >>> "  # Приглашение на ввод выражения.


WELCOME = f"""
Author: {__author__}.
Bool_Expression {__version__} - создание таблицы значений для логического выражения на Python!
Введите переменные через пробел после приглашения "{PS1}"
Введите логическое выражение со скобочками после приглашения "{PS2}".
Чтобы обновить переменные, используйте команду variables.
Для дополнительной информации используйте команду help.
Чтобы выйти, используйте команды quit или exit.
"""

USAGE = f"""
Соберите логическое выражение из переменных и операторов.
Программа "Bool_Expression" выведет результат всего логического выражения для значений 1 или 0 каждой переменной.
Можно использовать любые из следующих функций: {', '.join(ALLOWED_NAMES.keys())}.
Можно использовать любые буквенные переменные.

Пример использования:
{PS1}a b
{PS2}AND(NOT(a), b)
Вывод:
a:0, b:0 --> 0
a:0, b:1 --> 1
a:1, b:0 --> 0
a:1, b:1 --> 0
"""


def change_variables():
    # Читаем пользовательский ввод переменных.
    try:
        variables = input(f"{PS1}")
    except (KeyboardInterrupt, EOFError):
        raise SystemExit()

    # Поддержка специальных команд.
    low_case = variables.lower()
    if low_case == "help":
        print(USAGE)
    elif low_case in {"quit", "exit"}:
        raise SystemExit()
    elif low_case == "variables":
        print("Ты тупой человек.")
        raise SystemExit()

    # Заносим имя каждой переменной в массив.
    variables = variables.split()
    # Проверка на корректность переменных.
    for variable in variables:
        if not variable.isalpha():
            raise NameError(f"Использование '{variable}' не разрешено.")
    # Обновление главного словаря доступных имён.
    ALLOWED_NAMES.update({key: True for key in variables})

    return variables


def validation(expression):
    """Вычисляет математическое выражение."""
    # Компиляция выражения в байт-код.
    code = compile(expression, "<string>", "eval")
    # Если не может скомпилировать - SyntaxError.

    # Валидация доступных имен.
    for name in code.co_names:
        if name not in ALLOWED_NAMES:
            raise NameError(f"Использование '{name}' не разрешено.")
    return code


def main():
    """Читает и рассчитывает введенное выражение."""
    print(WELCOME)

    while True:
        try:
            variables = change_variables()
        except NameError as err:
            # Если пользователь попытался использовать неразрешенное имя переменной.
            print(err)
            continue
        break

    while True:
        # ПРОВЕРКА ВВОДА:
        # Читаем пользовательский ввод выражения.
        try:
            expression = input(f"{PS2}")
        except (KeyboardInterrupt, EOFError):
            raise SystemExit()

        # Поддержка специальных команд.
        low_case = expression.lower()
        if low_case == "help":
            print(USAGE)
            continue
        elif low_case in {"quit", "exit"}:
            raise SystemExit()
        elif low_case == "variables":
            while True:
                try:
                    variables = change_variables()
                except NameError as err:
                    # Если пользователь попытался использовать неразрешенное имя переменной.
                    print(err)
                    continue
                break
            continue

        # Обработка ошибок.
        try:
            code = validation(expression)
        except SyntaxError:
            # Некорректное выражение.
            print("Вы ввели некорректное выражение.")
            continue
        except NameError as err:
            # Если пользователь попытался использовать неразрешенное имя функции.
            print(err)
            continue

        # ВЫВОД ТАБЛИЦЫ ИСТИННОСТИ:
        n = len(variables)
        stack = [0] * n
        last = n - 1

        for _ in range(2 ** n):
            # Обновляем значение каждой переменной.
            values = {key: value for key, value in zip(variables, stack)}

            if stack[last]:
                for i in range(last, -1, -1):
                    if stack[i]:
                        stack[i] = 0
                    else:
                        stack[i] += 1
                        break
            else:
                stack[last] += 1
            # Обновляем главный словарь.
            ALLOWED_NAMES.update(values)
            # Выполняем выражение.
            result = eval(code, {}, ALLOWED_NAMES)  # FIX? {"__builtins__": {}}
            # Печатаем строку таблицы.
            print(", ".join([f"{key}:{value}" for key, value in zip(values.keys(), values.values())])
                  + " --> " + str(result))


main()
