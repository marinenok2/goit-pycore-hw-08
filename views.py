"""Подання відповідає за введення та вигляд інформації для користувача."""

from abc import ABC, abstractmethod


class UserView(ABC):
    # Абстрактний клас задає правила для всіх майбутніх інтерфейсів.
    # Створити його напряму не можна: потрібно реалізувати всі ці методи.
    @abstractmethod
    def read_command(self):
        pass

    @abstractmethod
    def show_message(self, message):
        pass

    @abstractmethod
    def show_contacts(self, contacts):
        pass

    @abstractmethod
    def show_phones(self, phones):
        pass

    @abstractmethod
    def show_birthdays(self, birthdays):
        pass

    @abstractmethod
    def show_help(self):
        pass


class ConsoleView(UserView):
    # Конкретне подання: читає команди й показує результат у консолі.
    def read_command(self):
        return input("Enter a command: ")

    def show_message(self, message):
        print(message)

    def show_contacts(self, contacts):
        # Рядок означає повідомлення про помилку від обробника.
        if isinstance(contacts, str):
            self.show_message(contacts)
            return
        if not contacts:
            self.show_message("Address book is empty.")
            return
        for record in contacts:
            print("-" * 32)
            print(f"Name: {record.name.value}")
            phones = []
            for phone in record.phones:
                phones.append(phone.value)
            print("Phones: " + ("; ".join(phones) or "not set"))
            birthday = "not set"
            if record.birthday is not None:
                birthday = record.birthday.value.strftime("%d.%m.%Y")
            print(f"Birthday: {birthday}")
        print("-" * 32)

    def show_phones(self, phones):
        if isinstance(phones, str):
            self.show_message(phones)
        elif not phones:
            self.show_message("No phones.")
        else:
            self.show_message("; ".join(phones))

    def show_birthdays(self, birthdays):
        if isinstance(birthdays, str):
            self.show_message(birthdays)
        elif not birthdays:
            self.show_message("No upcoming birthdays.")
        else:
            for contact in birthdays:
                print(f"{contact['birthday']}: {contact['name']}")

    def show_help(self):
        # Щоб змінити вигляд довідки, достатньо відредагувати цей метод.
        print("Available commands:")
        print("hello                                  - greeting")
        print("add <name> <phone>                     - add contact or phone")
        print("change <name> <old_phone> <new_phone>   - replace phone")
        print("phone <name>                           - show phones")
        print("all                                    - show contact cards")
        print("add-birthday <name> DD.MM.YYYY          - set birthday")
        print("show-birthday <name>                   - show birthday")
        print("birthdays                              - upcoming congratulations")
        print("help                                   - show this help")
        print("close / exit                           - save and quit")
