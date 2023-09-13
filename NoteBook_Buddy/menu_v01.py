import calendar
import csv
import json
import os
import string
from collections import UserDict
from datetime import datetime
import re

from addressbook import AddressBook, Name, Phone, Email, Address, Birthday, Record
from addressbook import run as run_adressbook

from NotebookD import Note, Tag, Record, Notebook
from file_sorter import Sorted

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистити екран, в залежності від операційної системи

        print("**********************************************")
        print("Main Menu:")
        print("1. Launch Address Book")
        print("2. Launch Notepad")
        print("3. Launch File Sorter")
        print("4. Exit")
        print("**********************************************")

        choice = input("Enter your choice: ")

        if choice == '1':
            launch_address_book()
        elif choice == '2':
            launch_notepad()
        elif choice == '3':
            launch_file_sorter()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def launch_address_book():
    print("Launching Address Book...")
    return_to_main_menu = run_adressbook()
    if return_to_main_menu:
        input("Press Enter to return to the main menu...")

def launch_notepad():
    print("Launching Notepad...")

    notebook = Notebook()

    while True:
        print("**********************************************")
        print("Notepad Menu:")
        print("1. Add Note")
        print("2. Edit Note")
        print("3. Delete Note")
        print("4. List Notes")
        print("5. Search Notes by Tag")
        print("6. Save to File")
        print("7. Load from File")
        print("8. Back to Main Menu")
        print("**********************************************")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Додати нотатку
            note_text = input("Enter the note text: ")
            note = Note(note_text)
            notebook.add_record(Record(note))
            print("Note added successfully.")
        elif choice == '2':
            # Редагувати нотатку
            print("List of Notes:")
            notebook.list_records()
            note_index = int(input("Enter the index of the note to edit: "))
            if 0 <= note_index < len(notebook):
                new_note_text = input("Enter the new note text: ")
                notebook[note_index].note = new_note_text
                print("Note edited successfully.")
            else:
                print("Invalid note index. Please try again.")
        elif choice == '3':
            # Видалити нотатку
            print("List of Notes:")
            notebook.list_records()
            note_index = int(input("Enter the index of the note to delete: "))
            if 0 <= note_index < len(notebook):
                notebook.pop(note_index)
                print("Note deleted successfully.")
            else:
                print("Invalid note index. Please try again.")
        elif choice == '4':
            # Вивести список нотаток
            print("List of Notes:")
            notebook.list_records()
        elif choice == '5':
            # Пошук нотаток за тегом
            tag_to_search = input("Enter the tag to search for: ")
            matching_records = notebook.search_by_tag(Tag(tag_to_search))
            if matching_records:
                print("Matching Notes:")
                for i, record in enumerate(matching_records):
                    print(f"{i + 1}. {record.note}")
            else:
                print("No matching notes found.")
        elif choice == '6':
            # Зберегти нотатки в файл
            file_name = input("Enter the file name to save to: ")
            notebook.save_to_file(file_name)
            print("Notes saved to file.")
        elif choice == '7':
            # Завантажити нотатки з файлу
            file_name = input("Enter the file name to load from: ")
            notebook.load_from_file(file_name)
            print("Notes loaded from file.")
        elif choice == '8':
            # Повернутися до головного меню
            break
        else:
            print("Invalid choice. Please try again.")


def launch_file_sorter():
    print("Launching File Sorter...")
    sorted_object = Sorted()
    sorted_object.run()


if __name__ == "__main__":
    main_menu()
