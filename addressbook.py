import calendar
import csv
import json
import os
import string
from collections import UserDict
from datetime import datetime
import re

class PhoneError(Exception):
    #print('Wrong phone number')
    pass

class NameError(Exception):
    pass

class BirthdayError(Exception):
    pass

class AddressError(Exception):
    pass

class EmailError(Exception):
    pass

class Field:
    pass
class Phone(Field):
    def __init__(self, phone: str):
        self.__value = None
        self.phone = phone

    @property
    def phone(self):
        return self.__value

    @phone.setter
    def phone(self, new_phone):
        if len(new_phone) == 10 and new_phone.isdigit():
            self.__value = new_phone
        else:
            raise ValueError
            #raise ValueError("Incorrect phone number! It must contain exactly 10 numbers.")

    def __repr__(self):
        return self.phone
class Name(Field):
    def __init__(self, name: str):
        self.__value = None
        self.name = name.capitalize()

    @property
    def name(self):
        return self.__value

    @name.setter
    def name(self, new_name):
        if new_name.isalpha():
            self.__value = new_name.capitalize()
        else:
            raise ValueError('Name can contain only letters!')

    def __repr__(self):
        return self.name
class Birthday(Field):
    def __init__(self, birthday: str):
        self.__value = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__value

    @birthday.setter
    def birthday(self, new_bday: str):
        try:
            bday = datetime.strptime(new_bday, '%d.%m.%Y')
        except:
            raise ValueError('Wrong date format! Please provide correct form dd.mm.yyyy')

        # Перевірка реальності дати
        if bday.date() > datetime.now().date() or bday.year <= datetime.now().year - 120:
            raise ValueError('Unrealistic date! Provide the real one.')
        else:
            self.__value = new_bday

    def __repr__(self):
        return self.birthday
class Address(Field):
    def __init__(self, town: str, street: str, building: str, apartment: int = None):
        self.__town_value = None
        self.town = town
        self.__street_value = None
        self.street = street
        self.__building_value = None
        self.building = building
        self.__apartment_value = None
        self.apartment = apartment

    @property
    def town(self):
        return self.__town_value

    @town.setter
    def town(self, town: str):
        if isinstance(town, str) and string.digits not in town:
            self.__town_value = town.capitalize()
        else:
            raise ValueError('Town should be a string type without numbers')

    @property
    def street(self):
        return self.__street_value

    @street.setter
    def street(self, street: str):
        if isinstance(street, str) and string.digits not in street:
            self.__street_value = street.capitalize()
        else:
            raise ValueError('Street should be a string type')

    @property
    def building(self):
        return self.__building_value

    @building.setter
    def building(self, building):
        if isinstance(building, str) and re.match(r'^\d*[A-Za-z]?$',building):
            self.__building_value = building
        else:
            raise ValueError('Building number must be a string type')

    @property
    def apartment(self):
        return self.__apartment_value

    @apartment.setter
    def apartment(self, apartment):
        if isinstance(apartment, int) or apartment is None:
            self.__apartment_value = apartment
        else:
            raise ValueError('Apartment number must be an int type')

    def __repr__(self):
        address = f'{self.town}, {self.street} {self.building}'
        return address if self.apartment is None else f'{address}/{self.apartment}'
class Email(Field):
    def __init__(self, email):
        self.__value = None
        self.email = email

    @property
    def email(self):
        return self.__value
    @email.setter
    def email(self, email: str):
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.match(pat, email):
            self.__value = email
        else:
            raise ValueError

    def __repr__(self):
        return self.email

    def __str__(self):
        return f'{self.email}'
class Record:
    def __init__(self, name: Name, address: Address, email: Email, phones: list[Phone], birthday=None):
        if len(phones) == 0:
            phones = []
        self.name = name
        self.phones = list(phones)
        self.birthday = birthday
        self.address = address
        self.email = email

    # функція додавання телефону
    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    # функція вилучення телефону
    def remove_phone(self, phone: Phone):
        for ph in self.phones:
            if ph.phone == phone.phone:
                self.phones.remove(ph)

    # функція зміни телефону
    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if old_phone == phone.phone:
                phone.phone = new_phone

    # функіця, яка рахує кількість днів до наступного дня народження даного контакту
    def days_to_birthday(self): #функція повертає int або None
        if self.birthday is not None:
            bday = self.birthday.birthday[:-4] + str(datetime.now().year)
            bday = datetime.strptime(bday, '%d.%m.%Y')
            now = datetime.now()
            result = bday.toordinal() - now.toordinal()  # обчислення різниці днів між двома датами у поточному році
            if result < 0:
                result += 366 if calendar.isleap(now.year) else 365
            return result
        else:
            return None

    def __repr__(self):
        s = f'Name: {self.name}, Address: {self.address}, email: {self.email}, phones: {self.phones}'
        return s if self.birthday is None else f'{s}, birthday: {self.birthday}'


class AddressBook(UserDict):
    def __init__(self, N=1):
        super().__init__()
        self.N = N  # Кількість записів, які повертаються за одну ітерацію

    def list_contacts(self):
        return [contact for contact in self.data.values()]

    # до списку контактів додає об'єкт Record
    def add_record(self, record: Record):
        self.data.update({record.name.name.capitalize(): record})

    # повертає список об'єктів phone
    def get_contact(self, name: str) -> list:
        return self.data.get(name.capitalize()).phones

    # видаляє контакт
    def remove_contact(self, name: str):
        self.data.pop(name.capitalize())

    def __iter__(self, n=None):
        if n:
            self.N = n
        iter_list = list(self.data.items())
        grouped = [iter_list[n:n + self.N] for n in range(0, len(iter_list), self.N)]
        for group in grouped:
            yield group

    """"функція завантажує до вказаного файлу дані, 
        які знаходяться в об'єкті AddressBook на момент її виклику"""

    def save_to_file(self, filename):
        data = {
            "records": {
                name: {
                    "name": record.name.name,
                    'address': str(record.address),
                    'email': str(record.email),
                    "phones": [phone.phone for phone in record.phones],
                    "birthday": record.birthday.birthday if record.birthday else None
                }
                for name, record in self.data.items()
            }
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    """"функція, яка зі вказаного файлу завантажує дані до об'єкту AddressBook"""
    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for name, record_data in data.get("records", {}).items():
                    name_field = Name(record_data["name"])
                    email = Email(record_data['email'])
                    town, street = record_data['address'].split(',')
                    street, building = street.strip().split(' ')
                    if '/' in building:
                        address = Address(town, street, building.split('/')[0], apartment=int(building.split('/')[1]))
                    else:
                        address = Address(town, street, building)


                    phones = [Phone(phone) for phone in record_data["phones"]]
                    birthday = Birthday(record_data["birthday"]) if record_data["birthday"] else None
                    rec = Record(name_field,address,email, phones, birthday=birthday)
                    self.add_record(rec)
        except FileNotFoundError:
            pass

    """"функція, яка повертає список записів у об'єкті AddressBook,
        номери яких, співпадають із поданим, як параметр, фрагментом номеру"""
    def search_by_number(self, number: str) -> list[Record]:
        return [record for record in self.data.values() for phone in record.phones if number in phone.phone]

    """"функція, яка повертає список записів у об'єкті AddressBook,
        імена яких, співпадають із поданим, як параметр, фрагментом імені"""
    def search_by_name(self, name: str) -> list[Record]:
        return [self.data[n] for n in self.data.keys() if name.upper() in n.upper()]

    """функція виводить контакти усіх, хто має день народження протягом наступних н днів"""
    def birthday_contacts(self, number_of_days: int) -> object:
        contacts_list = [contact for contact in self.data.values() if
                         contact.birthday and contact.days_to_birthday() <= number_of_days]
        return contacts_list



if __name__ == "__main__":
    ab = AddressBook()
    while True:
        print('1. Load data from json file')
        print("2. Add Record")
        print('3. Edit record')
        print('4. Remove record')
        print("5. Search")
        print("6. Show all contacts")
        print('7. Show all contacts with the birthday within next n days')
        print("7. Save")
        print("8. Save and Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                os.system('cls')
                full_path = input('Provide full path to the desired json file: ')
                if os.path.isfile(full_path):
                    ab.load_from_file(full_path)
                    if len(ab) == 0:
                        print('Nothing to load')
                    else:
                        print('Successfully loaded\n')
                        break
                else:
                    print('Wrong file path. Please try again.\n')
        elif choice == "2":
                while True:
                    os.system('cls')
                    name = input("Enter name: ")
                    try:
                        name = Name(name)
                        break
                    except ValueError:
                        print('Name can contain only letters!')
                while True:
                    number = input('Enter phone: ')
                    try:
                        phones = [Phone(number)]
                        while True:
                            print('Enter another phone?')
                            choice = input('1. Yes\n2. No\nChoice: ')
                            if choice == '1':
                                number = input('Enter phone: ')
                                if number in [phone.phone for phone in phones]:
                                    print("This phone number has already been added!")
                                else:
                                    phones.append(Phone(number))
                            elif choice == '2':
                                break
                            else:
                                print('Wrong option!\n')
                        break
                    except ValueError:
                        print("Incorrect phone number! It must contain exactly 10 numbers.")
                while True:
                    email = input('Enter email: ')
                    try:
                        email = Email(email)
                        break
                    except ValueError:
                        print('Wrong email provided')
                while True:
                    town = input('Town: ')
                    street = input('Street: ')
                    building = input('Building: ')
                    try:
                        apartment = int(input('Apartment (optional): '))
                    except ValueError:
                        apartment = None
                    try:
                        address = Address(town,street,building,apartment)
                        break
                    except ValueError:
                        print('Wrong address!')

                while True:
                    birthday = input('Birthday (dd.mm.yyyy):')
                    try:
                        birthday = Birthday(birthday)
                        break
                    except ValueError:
                        print('Wrong date!')
                rec = Record(name,address,email, phones, birthday=birthday)
                ab.add_record(rec)
                os.system('cls')
                print('Record successfully added.\n')
        elif choice == "3":
            while True:
                os.system('cls')
                print("1.Search by number")
                print("2.Search by name")
                search_term = input("Option: ")
                if search_term == '1':
                    number = input('Enter the number or a part of it to search: ')
                    results = ab.search_by_number(number)
                    break
                elif search_term == '2':
                    name = input('Enter the name or a part of it to search: ')
                    results = ab.search_by_name(name)
                    break
                else:
                    print('Wrong option! Please try again')
            if results:
                for result in results:
                    print("Name:", result.name.name)
                    print("Phone:", ", ".join(phone.phone for phone in result.phones))
                    print("Email: ", result.email.email)
                    print("Address: ", result.address)
                    if result.birthday:
                        print("Birthday:", result.birthday.birthday)
                    print("-" * 20)
            else:
                print("No results found.")
        elif choice == '4':
            os.system('cls')
            for contact in ab.list_contacts():
                print(contact)
            print('\n')
        elif choice == "5":
            os.system('cls')
            while True:
                full_path = input('Provide full path to the desired json file: ')
                if os.path.isfile(full_path):
                    ab.save_to_file(full_path)
                    if len(ab) == 0:
                        print('Nothing to save')
                    else:
                        print('Data has been successfully saved')
                    break
                else:
                    os.system('cls')
                    print('Wrong file path. Please try again.')
        elif choice == "6":
            os.system('cls')
            full_path = input('Provide full path to the desired json file: ')
            if os.path.isfile(full_path):
                ab.save_to_file(full_path)
                if len(ab) == 0:
                    print('Nothing to save')
                else:
                    print('Data has been successfully saved')
                break
            else:
                print('Wrong file path. Please try again.')
        else:
            print('Wrong choice. Please try again.')

