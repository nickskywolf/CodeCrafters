import os
from pathlib import Path
import shutil
import re


class Sorted:

    user_folder = ""
    all_files_list = list()

    filters = { 
                'image'   : ['JPEG', 'PNG', 'JPG', 'SVG'],
                'video'   : ['AVI', 'MP4', 'MOV', 'MKV'],
                'docs': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                'music'   : ['MP3', 'OGG', 'WAV', 'AMR'],
                'archive' : ['ZIP', 'GZ', 'TAR']  
            }

  

    def __init__(self):
       pass

    def create_directory(self):

        while True:

            self.user_folder = Path(input(r'Input directory: '))
            
            if self.user_folder.is_dir():

                a = re.findall("/", str(self.user_folder))
                if len(a) >= 3:
                    print(self.user_folder)
                    break
            else:
                print("Your input is not a correct directory. Try again.")
            
                
            print(self.user_folder)
        return self.user_folder


    def get_list_of_files(self, dir_name):

        list_of_files = os.listdir(dir_name)
        
        allFiles = list()


        for entry in list_of_files:
            fullPath = os.path.join(dir_name, entry)
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.get_list_of_files(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles


    def create_folder(self, folders_dictionary):

        for df_k, df_v in folders_dictionary.items():
            if not os.path.exists(df_v):
                os.makedirs(df_v, exist_ok=True)
                print(f"Folder created {df_v}")

        return True



    def check_extension(self, file_):

        for key_f, val_f in self.filters.items():
            for v in val_f:
                if file_.upper().find('.' + v) > 0:
                    
                    return key_f
                
        return "unknown"



    def sort_file(self, files_, folders_dictionary):
        
        for f in files_:

            ext = ''
            ext = self.check_extension(f)

            for type, dest_folder in folders_dictionary.items():
                if type == ext:
                    # what to do with exisiting file - the same name
                    dest_path = dest_folder + '/' + f.split('/')[-1] 

                    print(f, dest_path) # + r'\' + f.split())
                    shutil.move(f, dest_path)
                else:
                    dest_path = folders_dictionary['unknown'] + '/' + f.split('/')[-1] 



    def create_list_of_sorted_files(self, folders_dictionary):
        
        list_of_sorted_files = []

        for dk, dv in folders_dictionary.items():
            for a in self.get_list_of_files(dv):
                #print(a)
                list_of_sorted_files.append(a)
        

        return list_of_sorted_files



    def get_list_of_ext(self, folders_dictionary):

        list_extensions = []
    
        for key_, val in folders_dictionary.items():
            if key_ != "unknown":
                
                list_files = (self.get_list_of_files(val))
            
                for el in list_files:
                    
                    list_extensions.append(el.split("/")[-1].split(".")[-1])
                    
        return list(set(list_extensions))
                    


    def get_list_unknown_ext(self, folders_dictionary):
    
        list_unknown_ext = []
        for key_, val in folders_dictionary.items():
            if key_ == "unknown":
                list_files = (self.get_list_of_files(val))
            
                for el in list_files:
                    
                    list_unknown_ext.append(el.split("/")[-1].split(".")[-1])

                
        return list(set(list_unknown_ext))   



    def normalize(name: str)-> str:

        CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

        TRANS = {}

        for c, l in zip(CYRILLIC, LATIN):
        
            TRANS[ord(c)] = l
            #TRANS.update({ord(CYRILLIC_SYMBOLS[i]):LATIN[i]})
            TRANS[ord(c.upper())] = l.upper()

            translated = name.translate(TRANS)
            translated = re.sub(r'\W','_', translated)
        
        return translated



    def rename_files_in_folder(self, folder):

        result = self.get_list_of_files(folder)
        
        for path in result:

            file_path_source = path
            l = path.split("/")
            lista = l[-1].split(".")
            lista[0] = self.normalize(lista[0])
            l[-1] = ".".join(lista)
            file_path_dest = "/".join(l)
            os.rename(file_path_source, file_path_dest)
        
        return True



    def rename_all_files_in_all_folders(self, folders_dictionary):

        for k_dest,v_dest in folders_dictionary.items():
            self.rename_files_in_folder(v_dest)
        return True 


        

    def run(self):

        while True:
            print("\nMenu:")
            print("1. Create directory")
            print("2. Sort files")
            print("3. Go back to the main menu")
            
            choice = input("Choose an option: ")
            directory = ""

            if choice == "1":

                directory = self.create_directory()
                dest_folders = {
                        'image'    : str(directory) + '/sort/image/',
                        'video'    : str(directory) + '/sort/video/',
                        'docs'     : str(directory) + '/sort/docs/',
                        'music'    : str(directory) + '/sort/music/',
                        'archive'  : str(directory) + '/sort/archive/',
                        'unknown'  : str(directory) + '/sort/unknown/'
                    }
                
                self.create_folder(dest_folders)

                
                #sorted_object.add_contact(contact)
                print("Directory created!")

            elif choice == "2": 

                print(f"Directory : {directory}")
                if directory != "":


                
                    all_files_list = self.get_list_of_files(directory) 

                    self.sort_file(all_files_list, dest_folders)

                    for el in self.create_list_of_sorted_files(dest_folders):

                        print(el)
                
                    print(self.get_list_unknown_ext(dest_folders))

                    
                    print(self.get_list_of_ext(dest_folders))
                    
                    self.rename_all_files_in_all_folders(dest_folders)
                    print("Адресну книгу збережено!")
                else:
                    print("The directory has not been provided. Choose option 1 to create directory.")

            # elif choice == "3":
            #     filename = input("Введіть ім'я файлу для відновлення: ")
            #     sorted_object.load_from_file(filename)
            #     print("Адресну книгу відновлено!")

            # elif choice == "4":
            #     search_str = input("Введіть рядок для пошуку: ")
            #     matching_contacts = sorted_object.search_contacts(search_str)

            #     if matching_contacts:
            #         print("Знайдено контакти:")
            #         for contact in matching_contacts:
            #             print(f"Ім'я: {contact.name}, Номер телефону: {contact.phone}")
            #     else:
            #         print("Контакти не знайдено!")
            # elif choice == "5":
            #     break 

            # directory = self.create_directory()

            # 
            
            

            # self.create_folder(dest_folders)

            

    @staticmethod
    def main():
        sorted_object = Sorted()
        sorted_object.run()
        
if __name__ == "__main__":

    Sorted.main()
   
#/Users/marinavakulenko/Documents/to_sort_copy_2  
         

