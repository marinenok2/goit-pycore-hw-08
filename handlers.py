"""Функції, які виконують команди користувача."""

from functools import wraps
from address_book import Record


def input_error(func):
    # Декоратор перехоплює помилки введення, щоб бот продовжував працювати.
    # wraps зберігає назву й опис початкової функції.
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Передаємо у функцію всі отримані аргументи.
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError) as error:
            return str(error)
    return wrapper


def require_args(args, count, usage):
    # Перевіряємо кількість аргументів і підказуємо правильний запис команди.
    if len(args) != count:
        raise ValueError(f"Usage: {usage}")
    return args


def get_record(book, name):
    # Спільний пошук контакту для команд, яким потрібен наявний запис.
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    return record


@input_error
def add_contact(args, book):
    # Додаємо новий контакт або ще один телефон до наявного.
    name, phone = require_args(args, 2, "add <name> <phone>")
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    # Для заміни потрібні ім'я, старий номер і новий номер.
    name, old, new = require_args(args, 3, "change <name> <old_phone> <new_phone>")
    get_record(book, name).edit_phone(old, new)
    return "Contact updated."


@input_error
def show_phone(args, book):
    # Кома після name означає розпакування списку з одного елемента.
    name, = require_args(args, 1, "phone <name>")
    record = get_record(book, name)
    phones = []
    for phone in record.phones:
        phones.append(phone.value)
    if not phones:
        return "No phones."
    return "; ".join(phones)


@input_error
def show_all(args, book):
    # Команда не потребує аргументів. Кожен контакт виводимо з нового рядка.
    require_args(args, 0, "all")
    if not book:
        return "Address book is empty."
    contacts = []
    for record in book.values():
        contacts.append(str(record))
    return "\n".join(contacts)


@input_error
def add_birthday(args, book):
    # Record.add_birthday перевірить дату через клас Birthday.
    name, birthday = require_args(args, 2, "add-birthday <name> DD.MM.YYYY")
    get_record(book, name).add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    # Окремо повідомляємо, якщо контакт є, але дату ще не додано.
    name, = require_args(args, 1, "show-birthday <name>")
    birthday = get_record(book, name).birthday
    if birthday is None:
        return "Birthday is not set."
    return str(birthday)


@input_error
def birthdays(args, book):
    # Отримуємо список привітань і перетворюємо його на текст для консолі.
    require_args(args, 0, "birthdays")
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    result = []
    for contact in upcoming:
        result.append(f"{contact['birthday']}: {contact['name']}")
    return "\n".join(result)
