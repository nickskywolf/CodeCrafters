if __name__ == '__main__':
    notebook = Notebook()

    for i in range(1, 16):
        note_text = f"This is note {i}"
        tag_text = f"Tag {i}"

        note = Note(note_text)
        tag = Tag(tag_text)

        record = Record(note, tag)
        notebook.add_record(record)

    print("All records in the notebook:")
    notebook.list_records()

    search_tag = Tag("Tag 5")
    print("\nRecords with the tag 'Tag 5':")
    matching_records = notebook.search_by_tag(search_tag)
    for record in matching_records:
        print(record)

    record_to_remove = matching_records[0]
    print("\nRemoving a record:")
    notebook.remove_record(record_to_remove)
    notebook.list_records()

    notebook.save_to_file("notebook_data.pickle")

    notebook2 = Notebook()
    notebook2.load_from_file("notebook_data.pickle")
    print("\nLoaded records from the file:")
    notebook2.list_records()
