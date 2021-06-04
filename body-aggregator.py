"""
This script is used on a a corpus of Json file Parler posts and users, extracting the body of the post and user information
(follow/ following ratio and post frequency). This script creates a single corpus (a CSV file) with one post per row. 

Download the posts and users into a folder named parler_data and parler_users respectively.
"""

import os
import json
import csv
from datetime import date
from datetime import datetime
import gc

cached_usernames = {}


folder_of_data = r"parler_data"
folder_of_usernames = r"parler_users"

def find_user_data(username):
    # per file look for username
    # if username found break
    # return dict data object

    all_username_files = get_all_files_in_a_folder(folder_of_usernames)
    found_row = ""

    if username in cached_usernames.keys():
        found_row = cached_usernames[username]
    else:

        for file in all_username_files:
            print("Looking for user {} in user Json files {}".format(username, file))
            with open(file, encoding='utf-8', newline='') as data_file:
                list_of_data = []
                for line in data_file:
                    list_of_data.append(json.loads(line))

                for entry in list_of_data:
                        try:
                            if username == entry["username"]:
                                found_row = entry
                                print("Found username {} in file {}".format(username, file))
                                cached_usernames[username] = found_row
                                break
                        except KeyError as e:
                            # an entry doesn't have a username
                            pass

            if found_row != "":
                break

    if found_row == "":
        raise Exception("Couldn't find a username entry for user {}".format(username))

    return found_row

def get_all_files_in_a_folder(directory):
    list_of_files = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json") or filename.endswith(".ndjson"):
            list_of_files.append(os.path.join(directory, filename))
    return list_of_files

def process_data():
    all_data_files = get_all_files_in_a_folder(folder_of_data)

    file_count = 0
    for file in all_data_files:
        file_count = file_count+1
        json_entry_count = 0
        print("Opening file {}".format(file))
        with open(file, encoding='utf8', newline='') as json_file:
            list_of_data = []
            for line in json_file:
                list_of_data.append(json.loads(line))

            for data in list_of_data:
                json_entry_count = json_entry_count + 1

                try:
                    body = data["body"]

                    if body == "":
                        print("No body, skipping")
                        continue

                    username = data["username"]

                    print("Processing user {}, in file {} of {}, json entry {} of {}".format(username, file_count, len(all_data_files),json_entry_count, len(list_of_data)))

                    username_dict = find_user_data(username)
                    being_followed_count = username_dict["user_followers"]
                    following_count = username_dict["user_following"]
                    joined_date = username_dict["joined"]
                    last_seen = username_dict["lastseents"]
                    # '2020-1114182509'
                    year = int(joined_date[0:4])
                    month = int(joined_date[4:6])
                    day = int(joined_date[6:8])
                    start_date  = date(year,month,day)
                    # "2020-12-23
                    last_seen_date = date(int(last_seen[0:4]),int(last_seen[5:7]),int(last_seen[8:10]))
                    delta = last_seen_date - start_date
                    total_active_days = delta.days
                    number_of_posts = username_dict["posts"]

                    post_frequency = number_of_posts/total_active_days
                    follow_ratio = being_followed_count/ following_count

                    fields = [username, post_frequency, follow_ratio, body]
                    with open(r'far-right-data-new.csv', 'a',encoding='utf8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(fields)
                        print("Added row to CSV {}".format(fields))
                except:
                    print("faild to find field")
                    pass

        gc.collect()

process_data()
