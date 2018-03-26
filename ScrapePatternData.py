import time as time
import RavelryFunctions as rav
import sqlite3 as sq

# Open my Ravelry authentication values
# Path to the file that holds my keys--the username and password given to me by Ravelry for my Basic Auth, read only app
path = 'C:/Users/Jamie/Desktop/RavelrySecret.txt'
mode = 'r'  # read mode--I'll only need to read the username and password from the file

keys = []  # The list where I'll store my username and password
with open(path, mode) as f:  # Open the file
    for line in f:
        keys.append(line)  # The first line is the username, and the second line is the
        # password--add each of these lines to the keys list

user = keys[0].rstrip()  # The username is held in the first element of the keys list
pswd = keys[1].rstrip()  # The password is the second element of the keys list

# Pull in valid pattern IDs from their file
root = 'C:/Users/Jamie/Desktop/'
fileName = 'AllUniqueSortedPatternIDs'
extension = '.txt'
filePath = root + fileName + extension
patternIDs = rav.importPatternIDs(filePath)

# Set up database
conn = sq.connect('C:/Users/Jamie/Desktop/ravelryData2.db')  # Opens or creates the database
c = conn.cursor()

# Create a table in the database -- ONLY RUN THIS ONCE, COMMENT THIS LINE OUT IF YOU NEED TO ADD TO THE TABLE
# c.execute("CREATE TABLE patternData1 (id int PRIMARY KEY, name text, permalink text, "
#           + "published text, downloadable integer, "
#           + "ravelry_download integer, free integer, price real, currency text, currency_symbol text, "
#           + "projects_count integer, queued_projects_count integer, favorites_count integer, comments_count integer, "
#           + "rating_count integer, rating_average real, difficulty_count integer, difficulty_average text, "
#           + "yardage_max real, yardage real, gauge real, row_gauge text, sizes_available text, author_id integer, "
#           + "author_name text, author_permalink text, author_patterns_count integer, author_favorites_count integer, "
#           + "author_users_usernames text, author_users_ids text, num_photos integer, notes_length integer, "
#           + "pattern_type_permalink text, pattern_type_name text, pattern_type_clothing text, craft_permalink text, "
#           + "craft_name text, pattern_categories_name text, pattern_attributes_permalinks text, gauge_pattern text, "
#           + "gauge_description text, yarn_weight_description text, yardage_description text, packs_yarn_ids text, "
#           + "packs_yarn_names text, packs_colorways text)")

time_start = time.clock()

# # Scraping parameters
# # Scraping test run -- first 5000 pattern IDs
# batchSize = 400  # I'm intentionally using a larger batch size than I feel I ought to for the test, to see if my code
# # for catching timeouts and decreasing batch size works
# patIDs = patternIDs[0:5000:]  # Test the scraping on just the first 5000 pattern IDs
# waitTime = 5  # Time to wait between API requests. I might decrease this if I see in the log files that it takes
# # a few seconds just to parse the data and insert it into the table.
# tableName = 'patternData1'  # ??? Function doesn't use this yet but might in the future.
# authTuple = (user, pswd)  # API authentication parameters
# storedIDsList = []  # List of IDs whose data the function was able to store in the table; should initialize with []
# failedIDsList = []  # List of IDs whose data the function could not store in the table; should initialize with []
# # storedIDsList and failedIDsList will end up as lists of strings

# Scraping parameters--full run
batchSize = 200
# patIDs = patternIDs[0:100000:]  # Scraping the first 100 000 pattern IDs
# patIDs = patternIDs[100000:300001:]  # Scraping the next 200 000 pattern
# patIDs = patternIDs[300000:500001:]  # Scraping the next 200 000 pattern IDs
patIDs = patternIDs[500000:]  # Scraping the rest of the pattern IDs, should be about 250 000 IDs
waitTime = 5  # Time to wait between API requests.
tableName = 'patternData1'  # ??? Function doesn't use this yet but might in the future.
authTuple = (user, pswd)  # API authentication parameters
storedIDsList = []  # List of IDs whose data the function was able to store in the table; should initialize with []
failedIDsList = []  # List of IDs whose data the function could not store in the table; should initialize with []
# storedIDsList and failedIDsList will end up as lists of strings

# Perform the scraping
rav.scrapeRavelryPatternData(c, conn, tableName, patIDs, batchSize, waitTime, authTuple, storedIDsList, failedIDsList)

# Close the database connection
conn.close()

# Save the stored and failed IDs lists to files
mode = 'a'

path = 'C:/Users/Jamie/Desktop/storedIDs2.txt'
storedIDsList = map(lambda x: x + '\n', storedIDsList)  # Add a newline character after each ID in the list
with open(path, mode) as out:
    out.writelines(map(str, storedIDsList))  # Using map is a quick and dirty way to turn storedIDsList into an iterator
    # storedIDsList is already a list of strings, so there's probably a better way to do this.

path = 'C:/Users/Jamie/Desktop/failedIDs2.txt'
failedIDsList = map(lambda x: x + '\n', failedIDsList)  # Add a newline character after each ID in the list
with open(path, mode) as out:
    out.writelines(map(str, failedIDsList))

time_elapsed = (time.clock() - time_start)
print('It took ', time_elapsed/60/60, ' hours to scrape ', len(patIDs), ' IDs from', patIDs[0], ' to ', patIDs[-1], '.')
