from collections import UserDict


class Field:
    """Базове поле запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Обов'язкове ім'я контакту."""

    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name is a required field.")
        super().__init__(value.strip())


class Phone(Field):
    """Номер телефону з 10 цифр."""

    def __init__(self, value):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    """Контакт: ім'я та список телефонів."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Додає номер. Некоректний номер завершує метод помилкою ValueError."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видаляє номер. Якщо його немає в записі, видає помилку ValueError."""
        found = self.find_phone(phone)
        if found is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone, new_phone):
        """Замінює старий номер на новий. Якщо дані некоректні, видає помилку ValueError."""
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError("Phone number not found.")
        self.phones[self.phones.index(found)] = Phone(new_phone)

    def find_phone(self, phone):
        """Повертає об'єкт Phone або None, якщо номера немає."""
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Книга контактів."""

    def add_record(self, record):
        """Додає запис до self.data."""
        self.data[record.name.value] = record

    def find(self, name):
        """Повертає Record за ім'ям або None, якщо запису немає."""
        return self.data.get(name)

    def delete(self, name):
        """Видаляє запис за ім'ям."""
        del self.data[name]

    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print(book)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    book.delete("Jane")
