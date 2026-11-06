"""Запуск консольного бота: python main.py."""

import pickle
from handlers import (add_contact, change_contact, show_phone, show_all,
                      add_birthday, show_birthday, birthdays)
from storage import load_data, save_data


def parse_input(user_input):
    # Розділяємо введений рядок на команду та її аргументи за пробілами.
    parts = user_input.split()
    if not parts:
        return "", []
    # Регістр команди не має значення, але імена залишаються без змін.
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def main():
    try:
        # На початку відновлюємо контакти з попереднього сеансу.
        book = load_data()
    except (OSError, pickle.UnpicklingError, EOFError, ValueError, AttributeError,
            ImportError) as error:
        print(f"Could not load address book: {error}")
        # Не продовжуємо роботу, щоб випадково не перезаписати пошкоджений файл.
        return
    print("Welcome to the assistant bot!")
    try:
        while True:
            # Читаємо команди, доки користувач не завершить роботу.
            command, args = parse_input(input("Enter a command: "))
            if command in ("close", "exit"):
                print("Good bye!")
                # break завершує цикл, після чого виконається блок finally.
                break
            # Для кожної команди викликаємо відповідну функцію з handlers.py.
            if command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))
            elif command:
                print("Invalid command.")
    except (EOFError, KeyboardInterrupt):
        # Завершення введення або Ctrl+C також коректно закривають програму.
        print("\nGood bye!")
    finally:
        # Цей блок зберігає книгу і після exit/close, і після Ctrl+C або EOF.
        try:
            save_data(book)
        except OSError as error:
            print(f"Could not save address book: {error}")


if __name__ == "__main__":
    # Запускаємо бота лише при прямому запуску файла, а не при його імпорті.
    main()
