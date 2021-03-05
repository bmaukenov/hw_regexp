import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    # pprint(contacts_list)

names_list = []
for contact in contacts_list:
    if contact[0] == "lastname":
        continue
    full_name_united = contact[0] + contact[1] + contact[2]
    pattern = re.compile(r"([А-Я][а-я]*)\s?([А-Я][а-я]*)\s?([А-Я][а-я]*)?")
    full_name_divided = pattern.sub(r"\1 \2 \3", full_name_united).split()
    contact[0] = full_name_divided[0]
    contact[1] = full_name_divided[1]
    if len(full_name_divided) > 2:
        contact[2] = full_name_divided[2]
    else:
        contact[2] = ""
    first_last_name = contact[0] + contact[1]
    names_list.append(first_last_name)
    pattern2 = re.compile(r"\+?\d{1}\s?\(*(\d{3})\)*\s?\-?(\d{3})\-?(\d{2})\-?(\d{2})\s?\(?(доб.)?\s?(\d{4})?\)?")
    contact[5] = pattern2.sub(r"+7(\1)\2-\3-\4\5\6", contact[5])

new_contacts_list = [contacts_list[0]]
for index1, contact in enumerate(contacts_list):
    if index1 == 0:
        continue
    for index2, contact_new_list in enumerate(new_contacts_list):
        if contact[0] == contact_new_list[0] and contact[1] == contact_new_list[1]:
            for index3 in [2, 3, 4, 5, 6]:
                if len(contact[index3]) > len(contact_new_list[index3]):
                    contact_new_list[index3] = contact[index3]
            break
        else:
            if index2 == len(new_contacts_list) - 1:
                new_contacts_list.append(contact)


pprint(new_contacts_list)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)
