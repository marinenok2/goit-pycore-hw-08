"""Класи для контактів, адресної книги та роботи з днями народження."""

from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    # Спільний клас для полів контакту: зберігає значення та виводить його як рядок.
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        # Ім'я не може бути порожнім або складатися лише з пробілів.
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        # Дозволяємо рівно 10 звичайних цифр від 0 до 9.
        if len(value) != 10 or not value.isascii() or not value.isdigit():
            raise ValueError("Phone must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            # Перетворюємо рядок на datetime. Неіснуюча дата викличе ValueError.
            parsed = datetime.strptime(value, "%d.%m.%Y")
            # Перевіряємо, що день і місяць введені саме двома цифрами.
            if parsed.strftime("%d.%m.%Y") != value:
                raise ValueError
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from None
        super().__init__(parsed)

    def __str__(self):
        # Під час виведення повертаємо дату у звичному форматі.
        return self.value.strftime("%d.%m.%Y")


class Record:
    # Один контакт має ім'я, список телефонів і необов'язковий день народження.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        # Спочатку перевіряємо номер, а потім додаємо, якщо такого ще немає.
        validated = Phone(phone)
        if self.find_phone(phone) is None:
            self.phones.append(validated)

    def find_phone(self, phone):
        # Повертаємо об'єкт Phone, а якщо номер не знайдено — None.
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def remove_phone(self, phone):
        existing = self.find_phone(phone)
        if existing is None:
            raise ValueError("Phone not found.")
        self.phones.remove(existing)

    def edit_phone(self, old_phone, new_phone):
        # Новий номер перевіряємо до заміни, щоб не втратити старий при помилці.
        validated = Phone(new_phone)
        existing = self.find_phone(old_phone)
        if existing is None:
            raise ValueError("Phone not found.")
        if new_phone != old_phone and self.find_phone(new_phone):
            raise ValueError("This phone already exists.")
        self.phones[self.phones.index(existing)] = validated

    def add_birthday(self, birthday):
        # Зберігаємо одну дату. Повторний виклик замінить попередню.
        self.birthday = Birthday(birthday)

    def __str__(self):
        # Збираємо дані контакту в один рядок для команди all.
        phone_numbers = []
        for phone in self.phones:
            phone_numbers.append(phone.value)
        phones = "; ".join(phone_numbers)
        if not phones:
            phones = "not set"
        birthday = "not set"
        if self.birthday is not None:
            birthday = str(self.birthday)
        return f"Contact name: {self.name}, phones: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    # UserDict дозволяє працювати з книгою як зі словником.
    def add_record(self, record):
        # Ключ — ім'я контакту, значення — об'єкт Record.
        self.data[record.name.value] = record

    def find(self, name):
        # get поверне None, якщо контакту з таким ім'ям немає.
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, today=None):
        # today можна передати в тестах, а під час роботи беремо поточну дату.
        if today is None:
            today = date.today()
        upcoming = []
        for record in self.data.values():
            # Контакти без дня народження пропускаємо.
            if record.birthday is None:
                continue
            born = record.birthday.value.date()
            # Перевіряємо і наступний рік, бо тиждень може починатися в грудні.
            for year in (today.year, today.year + 1):
                try:
                    birthday = born.replace(year=year)
                except ValueError:
                    # У невисокосний рік вітаємо народжених 29 лютого 28 числа.
                    birthday = date(year, 2, 28)
                # Беремо сьогодні та наступні 6 днів — разом 7 днів.
                if 0 <= (birthday - today).days < 7:
                    congratulation = birthday
                    # weekday(): понеділок — 0, субота — 5, неділя — 6.
                    # Із суботи додаємо 2 дні, з неділі — 1, щоб отримати понеділок.
                    if birthday.weekday() >= 5:
                        congratulation += timedelta(days=7 - birthday.weekday())
                    upcoming.append({"name": record.name.value,
                                     "birthday": congratulation.strftime("%d.%m.%Y")})
                    # Цей контакт уже доданий, тому інший рік не перевіряємо.
                    break
        # Сортуємо за датою привітання, а за однакової дати — за ім'ям.
        # Дату перетворюємо на datetime, щоб порівнювати дати, а не рядки.
        return sorted(upcoming, key=lambda item: (
            datetime.strptime(item["birthday"], "%d.%m.%Y"), item["name"]))
