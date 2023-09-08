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
        return ' '.join(txt) if len(self.__value)<=5 else ' '.join(txt)+'...'
class Tag:
    def __init__(self, tag: str):
        self.__value = None
        self.tag = tag

    @property
    def tag(self):
        return self.__value

    @tag.setter
    def tag(self, tag):
        if isinstance(tag, str) or len(tag.split(' '))>1:
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

if __name__ == '__main__':
    pass
    # #можливий варіант виклику класів
    # txt = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    # n = Note(txt)
    # t1 = Tag('dummy')
    # t2 = Tag('bummy')
    # t3 = Tag('gummy')
    # r = Record(n, t1, t2, t3)
    # print(r)