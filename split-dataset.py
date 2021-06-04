"""
A script to be used on the full corpus and a list of far-right hashtags, provided by the output of hashtag-bootstrapping.py.
This script will create two sub-corpuses, one which only includes posts containing the far-right hashtags and one of no
posts of far-right hashtags.
"""

import csv
import random
clean_message_csv_location  = r"far-right-data-new.csv"
keywords_location = r"C:\Projects\Clean Pareler Data\output-hashtags.txt"

list_of_extreamist_messages = []
list_of_non_extreamist_messages = []

# Read keywords from keywords file
keywords_file = open(keywords_location, "r")
extreamist_keywords = keywords_file.read().splitlines()
keywords_file.close()

number_of_entries = 0

print("Counting rows in CSV file")
with open(clean_message_csv_location, newline='', encoding="utf8") as csvfile:
    row_reader = csv.reader(csvfile)
    for row in row_reader:
        number_of_entries = number_of_entries + 1

count = 0
with open(clean_message_csv_location, newline='', encoding="utf8") as csvfile:
    row_reader = csv.reader(csvfile)

    is_header = True

    for row in row_reader:
        count = count + 1
        # Skip the csv header
        if is_header:
            is_header = False
            continue

        is_extreamist = False
        name = row[0]
        user_name = row[1]
        date = row[2]
        message = row[3]

        found_keyword = ''
        random.shuffle(extreamist_keywords)
        for key_word in extreamist_keywords:
            if key_word.lower() in message.lower():
                found_keyword = key_word
                is_extreamist = True
                break

        if is_extreamist:
            print("Found extreamist message - {} of {}. Via keyword {}".format(count, number_of_entries, found_keyword))
            list_of_extreamist_messages.append({"name": name, "username": user_name, "timestamp": date, "message": message})
        else:
            list_of_non_extreamist_messages.append({"name": name, "username": user_name, "timestamp": date, "message": message})

print("Finished with total number {} extreamist messages and {} non-extreamist, with total of {}".format(
    len(list_of_extreamist_messages), len(list_of_non_extreamist_messages),  len(list_of_extreamist_messages)+ len(list_of_non_extreamist_messages)
))

# Write extreamist data
with open('extreamist-messages-with-violent.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file,
                        fieldnames=list_of_extreamist_messages[0].keys(),
                        )
    fc.writeheader()
    fc.writerows(list_of_extreamist_messages)

# Write non-extreamist data
with open('non-extreamist-messages-with-violent.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file,
                        fieldnames=list_of_non_extreamist_messages[0].keys(),
                        )
    fc.writeheader()
    fc.writerows(list_of_non_extreamist_messages)