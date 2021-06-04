"""
A script for counting the range of hashtags in a data. To be run after the hashtag-bootstrapping.py script on the output of
that script and the full corpus.
"""

import csv
import re
import json

list_of_hashtags = []

clean_message_csv_location = r"far-right-data-new.csv"

output_file = open("output-hashtags.txt", "r", encoding="utf8")
for hastag in output_file.readlines():
    list_of_hashtags.append(hastag.strip("\n"))
output_file.close()

dict_of_hashtag_count = {}

used_hastags = []

collected_hashtags = {}

length_of_file = 0

messages = []

with open(clean_message_csv_location, newline='', encoding="utf8") as csvfile:
    row_reader = csv.reader(csvfile)
    # Get length of csv
    print("Retrieving data from CSV file: {}".format(clean_message_csv_location))
    for row in row_reader:
        length_of_file = length_of_file + 1
        messages.append(row[3])

collected_hashtags = {}

with open(clean_message_csv_location, newline='', encoding="utf8") as csvfile:
    search_hastag_count = 0

    # Loops through all hastags to be searched for
    for search_hashtag in list_of_hashtags:

        # Write to file as we go
        sorted(dict_of_hashtag_count, key=dict_of_hashtag_count.get, reverse=True)
        output_file = open("hashtag-count.txt", "w", encoding="utf8")
        json.dump(dict_of_hashtag_count, output_file)
        output_file.close()

        search_hastag_count = search_hastag_count+ 1
        # Loop through all rows of messages looking for the hastag that's being searched for
        message_count = 0

        # Loops through all messages
        for message in messages:
            message_count = message_count + 1
            print("Hashtag '{}' of Hashtags '{}', searched in message '{}' of messages '{}'".format(
                search_hastag_count, len(list_of_hashtags), message_count, len(messages)))

            if search_hashtag.lower() in message.lower():

                if search_hashtag.lower() in dict_of_hashtag_count.keys():
                    dict_of_hashtag_count[search_hashtag.lower()] = dict_of_hashtag_count[search_hashtag.lower()] + 1
                else:
                    dict_of_hashtag_count[search_hashtag.lower()] = 1

# Write to file when completed
sorted(dict_of_hashtag_count, key=dict_of_hashtag_count.get, reverse=True)
output_file = open("hashtag-count.txt", "w", encoding="utf8")
json.dump(dict_of_hashtag_count, output_file)