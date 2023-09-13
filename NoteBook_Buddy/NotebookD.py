from collections import UserList
import pickle

class Note:
    def __init__(self, note: str):
        self.__value = None
        self.note = note
        self.tags = []

    @property
    def note(self):
        return self.__value

    @note.setter
    def note(self, note):
        if isinstance(note, str):
            self.__value = note
        else:
            raise ValueError('Note must be a string type')

    def add_tag(self, tag):
        if isinstance(tag, Tag):
            self.tags.append(tag)
        else:
            raise ValueError('Tag must be an instance of the Tag class')

    def __repr__(self):
        txt = self.__value.split(' ')[:5]
        return ' '.join(txt) if len(self.__value) <= 5 else ' '.join(txt) + '...'

class Tag:
    def __init__(self, tag: str):
        self.__value = None
        self.tag = tag

    @property
    def tag(self):
        return self.__value

    @tag.setter
    def tag(self, tag):
        if isinstance(tag, str):
            self.__value = tag
        else:
            raise ValueError('Tag must be a string type')

    def __repr__(self):
        return self.tag

class Record:
    def __init__(self, note: Note, *tags: Tag):
        self.note = note
        self.note.tags.extend(tags)

    def __repr__(self):
        return f'Note: {self.note}\ntags: {self.note.tags}'

class Notebook(UserList):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        self.data.append(record)

    def remove_record(self, record: Record):
        if record in self.data:
            self.data.remove(record)
        else:
            print("Запис не знайдено в блокноті.")

    def edit_record(self, old_record: Record, new_record: Record):
        if old_record in self.data:
            index = self.data.index(old_record)
            self.data[index] = new_record
        else:
            print("Запис не знайдено в блокноті.")

    def search_by_tag(self, tag: Tag):
        matching_records = [record for record in self.data if tag in record.note.tags]
        return matching_records if matching_records else []

    def list_records(self):
        for record in self.data:
            print(record)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("Файл не знайдено.")
        except Exception as e:
            print(f"Помилка при завантаженні файлу: {str(e)}")

if __name__ == '__main__':
    notebook = Notebook()

    txt1 = "Це перша нотатка."
    txt2 = "Це друга нотатка."

    n1 = Note(txt1)
    n2 = Note(txt2)

    t1 = Tag('Hello world!')
    t2 = Tag('Hi friends!')

    r1 = Record(n1, t1)
    r2 = Record(n2, t2)

    # Додавання записів до блокноту
    notebook.add_record(r1)
    notebook.add_record(r2)

    # Додавання тегів до записів
    n1.add_tag(t2)
    n2.add_tag(t1)

    # Виведення всіх записів
    print("Всі записи в блокноті:")
    notebook.list_records()

    # Пошук за тегом
    print("\nЗаписи з тегом 'Hello world!':")
    matching_records = notebook.search_by_tag(t1)
    for record in matching_records:
        print(record)

    # Видалення запису
    print("\nВидаляємо запис з тегом 'Hello world!':")
    notebook.remove_record(r2)
    notebook.list_records()

    # Зберігання та завантаження з файлу
    notebook.save_to_file("notebook_data.pickle")
    notebook2 = Notebook()
    notebook2.load_from_file("notebook_data.pickle")
    print("\nЗавантажені записи з файлу:")
    notebook2.list_records()
