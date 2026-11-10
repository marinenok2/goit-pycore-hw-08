"""Запуск консольного бота: python main.py."""

import pickle
from handlers import (add_contact, change_contact, show_phone, show_all,
                      add_birthday, show_birthday, birthdays)
from storage import load_data, save_data
from views import ConsoleView


def parse_input(user_input):
    # Розділяємо введений рядок на команду та її аргументи за пробілами.
    parts = user_input.split()
    if not parts:
        return "", []
    # Регістр команди не має значення, але імена залишаються без змін.
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def main(view=None):
    # Головний цикл використовує методи подання, а не print/input напряму.
    # Для іншого інтерфейсу можна передати іншу реалізацію UserView.
    if view is None:
        view = ConsoleView()
    try:
        # На початку відновлюємо контакти з попереднього сеансу.
        book = load_data()
    except (OSError, pickle.UnpicklingError, EOFError, ValueError, AttributeError,
            ImportError) as error:
        view.show_message(f"Could not load address book: {error}")
        # Не продовжуємо роботу, щоб випадково не перезаписати пошкоджений файл.
        return
    view.show_message("Welcome to the assistant bot! Type help to see commands.")
    try:
        while True:
            # Читаємо команди, доки користувач не завершить роботу.
            command, args = parse_input(view.read_command())
            if command in ("close", "exit"):
                view.show_message("Good bye!")
                # break завершує цикл, після чого виконається блок finally.
                break
            # Для кожної команди викликаємо відповідну функцію з handlers.py.
            if command == "hello":
                view.show_message("How can I help you?")
            elif command == "help":
                if args:
                    view.show_message("Usage: help")
                else:
                    view.show_help()
            elif command == "add":
                view.show_message(add_contact(args, book))
            elif command == "change":
                view.show_message(change_contact(args, book))
            elif command == "phone":
                view.show_phones(show_phone(args, book))
            elif command == "all":
                view.show_contacts(show_all(args, book))
            elif command == "add-birthday":
                view.show_message(add_birthday(args, book))
            elif command == "show-birthday":
                view.show_message(show_birthday(args, book))
            elif command == "birthdays":
                view.show_birthdays(birthdays(args, book))
            elif command:
                view.show_message("Invalid command. Type help to see commands.")
    except (EOFError, KeyboardInterrupt):
        # Завершення введення або Ctrl+C також коректно закривають програму.
        view.show_message("\nGood bye!")
    finally:
        # Цей блок зберігає книгу і після exit/close, і після Ctrl+C або EOF.
        try:
            save_data(book)
        except OSError as error:
            view.show_message(f"Could not save address book: {error}")


if __name__ == "__main__":
    # Запускаємо бота лише при прямому запуску файла, а не при його імпорті.
    main()
