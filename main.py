import csv
import re


def fix_fio(contact):
    correct_name_list = [' '.join(employee[0:3]).split(' ')[0:3] + employee[3:7] for employee in contact]
    return correct_name_list


def remove_duplicates(correct_name_list):
    clean_list = correct_name_list.copy()
    for num, row in enumerate(correct_name_list):
        for i in range(num+1, len(correct_name_list)):
            if row[0] == correct_name_list[i][0]:
                clean_list.remove(row)
                clean_list.remove(correct_name_list[i])
                zipped = zip(row, correct_name_list[i])
                uniq = []
                for j in zipped:
                    if j[0] == j[1]:
                        uniq.append(j[0])
                    elif j[0] == '':
                        uniq.append(j[1])
                    elif j[1] == '':
                        uniq.append(j[0])
                clean_list.append(uniq)
    return clean_list


def fix_phones(clean_list):
    pattern = r"(\+?[78])(\s?\(?)?(\d{3})(\)?\s?)-?(\d{3})-?(\d{2})-?(\d{2})(\s?)(\(?(доб\.)\s(\d{4}))?\)?"
    new_pattern = r'+7(\3)\5-\6-\7\8\10\11'
    for row in clean_list:
        result = re.sub(pattern, new_pattern, row[5])
        row[5] = result
    return clean_list


with open('phonebook_raw.csv', encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    contacts = list(reader)

correct_fio = fix_fio(contacts)

fixed_duplicates = remove_duplicates(correct_fio)

final_list = fix_phones(fixed_duplicates)


with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_list)

