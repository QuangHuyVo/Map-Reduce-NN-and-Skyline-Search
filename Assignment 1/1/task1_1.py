import pymongo

import os
default_directory = r"C:\Users\ADMIN\Desktop\Macquarie\Semester 2\COMP 6210\Assignment 1"
os.chdir(default_directory)

connection = pymongo.MongoClient("mongodb://localhost:27017/")
db = connection['Assignment1']  
collection = db['Song']  

with open('task1_1_output.txt', 'w', encoding='utf-8') as output_file:
    for song in collection.find():
        artist = song.get('Artist')
        year = song.get('Year')
        sales = song.get('Sales')
        
        # Create a triplet <artist, year, sales>
        triplet = f"{artist}; {year}; {sales}\n"
        
        # Write the triplet
        output_file.write(triplet)








