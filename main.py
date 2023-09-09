from collections import UserList

class Note:
    def __init__(self, note: str):
        self.__value = None
        self.note = note

    @property
    def note(self):
        return self.__value

    @note.setter
    def note(self, note):
        if isinstance(note, str):
            self.__value = note
        else:
            raise ValueError('Note must be a string type')

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
        if isinstance(tag, str) or len(tag.split(' ')) > 1:
            self.__value = tag
        else:
            raise ValueError('Tag must be a 1 word of str type')

    def __repr__(self):
        return self.tag

class Record:
    def __init__(self, note: Note, *tags: Tag):
        self.note = note
        self.tags = list(tags) if len(tags) else []

    def __repr__(self):
        return f'Note: {self.note}\ntags: {self.tags}'

class Notebook(UserList):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        """Додавання запису до блокноту."""
        self.data.append(record)

    def remove_record(self, record: Record):
        """Видалення запису з блокноту."""
        if record in self.data:
            self.data.remove(record)
        else:
            print("Запис не знайдено в блокноті.")

    def edit_record(self, old_record: Record, new_record: Record):
        """Редагування запису в блокноті."""
        if old_record in self.data:
            index = self.data.index(old_record)
            self.data[index] = new_record
        else:
            print("Запис не знайдено в блокноті.")

    def search_by_tag(self, tag: Tag):
        """Пошук записів за тегом."""
        matching_records = [record for record in self.data if tag in record.tags]
        return matching_records

    def list_records(self):
        """Виведення списку всіх записів в блокноті."""
        for record in self.data:
            print(record)

    def search_by_keyword(self, keyword: str):
        """Пошук записів за ключовим словом в тексті нотатки."""
        matching_records = [record for record in self.data if keyword in record.note.note]
        return matching_records

    def sort_by_keyword(self, keyword: str):
        """Сортування записів за ключовим словом в тексті нотатки."""
        self.data.sort(key=lambda record: record.note.note.count(keyword), reverse=True)
    

    def save_notes_to_file(self, filename):
        """Зберегти текст нотаток у файл."""
        with open(filename, 'w') as file:
            for record in self.data:
                file.write(f"Note: {record.note.note}\n")
                file.write(f"Tags: {', '.join(tag.tag for tag in record.tags)}\n\n")


if __name__ == '__main__':
    # Приклад використання класів і нових методів
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

    # Виведення всіх записів
    print("Всі записи в блокноті:")
    notebook.list_records()

    # Пошук за тегом
    print("\nЗаписи з тегом 'tag1':")
    matching_records = notebook.search_by_tag(t1)
    for record in matching_records:
        print(record)

    # Видалення запису
    print("\nВидаляємо запис з тегом 'tag1':")
    notebook.remove_record(r1)
    notebook.list_records()


    # #можливий варіант виклику класів
    # txt = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    # n = Note(txt)
    # t1 = Tag('dummy')
    # t2 = Tag('bummy')
    # t3 = Tag('gummy')
    # r = Record(n, t1, t2, t3)
    # print(r)