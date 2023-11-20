import pandas as pd
import pprint

path_to_search = "C:\\Users\\kszmydki001\\Desktop\\"

class StudentsDataException(Exception):
    pass


class BadLine(StudentsDataException):
    def __init__(self, message):
        self.message = message
        print(message)


class FileEmpty(StudentsDataException):
    def __init__(self, message):
        self.message = message
        return message



action = 1


try:
    # file_name = input("Prof. Jekyll's file name: ")

    while action != 0:
        action = int(input('''
        [1]. See points summary.
        [2]. Add record to the table. 
        [0]. End the program.
        Select action: '''))

        if action == 0:
            print('Ending program')
        else:

            file_name = 'f_jekyll.txt'
            f_jekyll = pd.read_table(path_to_search+file_name)
            f_jekyll.columns = ['name','surname','points']

            if len(f_jekyll) == 0:
                raise FileEmpty('File is empty!')
            else:
                # print(f_jekyll.head())

                if action == 2:
                    f_jekyll_dict = f_jekyll.to_dict("list")
                    pprint.pprint(f_jekyll_dict)

                    print('Add new record to the table.'.center(50,"*"))
                    name = input('Name: ')
                    surname = input('Surname: ')
                    points = input('Points: ')

                    if any([len(name) == 0, len(surname) == 0, len(points) == 0]):
                        print("Incorrect data! Can't add the record to the table! Try once again.")
                        action = 2
                    else:
                        f_jekyll_dict["name"].append(name)
                        f_jekyll_dict["surname"].append(surname)
                        f_jekyll_dict["points"].append(points)

                        # new_record_df = pd.DataFrame(new_record, index=False)
                        pprint.pprint(f_jekyll_dict)
                        f_jekyll_df = pd.DataFrame(f_jekyll_dict)
                        f_jekyll_df.to_csv(path_to_search+file_name, sep='\t', index=False)

                else:
                    print('Points summary:'.center(30,"*"))
                    print(f_jekyll.groupby(['name','surname']).sum('points'))


except FileNotFoundError:
    print('File not in directory')
except ValueError:
    print('ValueError')
except:
    print('File not correct.')
else:
    print('Finished!')




# ================================================================================

if __name__ == "__main__":
    pass