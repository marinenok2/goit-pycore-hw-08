"""Збереження адресної книги у файл і відновлення з нього."""

import pickle
from address_book import AddressBook


def save_data(book, filename="addressbook.pkl"):
    # wb відкриває файл для запису байтів. with закриє його автоматично.
    with open(filename, "wb") as file:
        # pickle.dump записує всю книгу разом із контактами, телефонами й датами.
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        # rb відкриває файл для читання байтів.
        with open(filename, "rb") as file:
            # pickle.load відновлює збережений об'єкт AddressBook.
            book = pickle.load(file)
    except FileNotFoundError:
        # Під час першого запуску файла ще немає, тому створюємо порожню книгу.
        return AddressBook()
    # Переконуємося, що у файлі збережена саме адресна книга.
    if not isinstance(book, AddressBook):
        raise ValueError("The saved file does not contain an AddressBook.")
    return book
