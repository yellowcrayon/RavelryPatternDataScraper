import time
import requests as rq
import math
import logging


def getNestedAttributes(Dict, attrList, levelKey, attrKey):
    # Take a dictionary of nested dictionaries,
    # go down each level of the nested dictionary and construct a list of all the values (attributes) that correspond to attrKey.
    # Dict is the dictionary of data.
    # attrList is the list of attributes associated with attrKey.
    # levelKey is the dictionary key that contains another dictionary within it.
    # attrKey is the dictionary key that contains the data we want from each level of the nested dictionaries.
    # This function adds onto the existing list, attrList, and simply returns True when it reaches the end of the nested dictionaries.
    # This function assumes that there are only a handful of nested dictionaries inside Dict, so recursion is appropriate.
    #
    # Example:
    # myDict = [{'permalink': 'shawl-wrap', 'id': 350, 'parent': {'permalink': 'neck-torso', 'id': 338, 'parent': {'permalink': 'accessories', 'id': 337, 'parent': {'permalink': 'categories', 'id': 301, 'name': 'Categories'}, 'name': 'Accessories'}, 'name': 'Neck / Torso'}, 'name': 'Shawl / Wrap'}]
    # myList = []
    # getNestedAttribute(myDict,myList,'parent','name')

    try:
        tempDict = Dict.get(levelKey)  # Look for the next level of dictionaries.
        # This will return the value if there is another level, and None if there is not.

        tempVal = Dict.get(attrKey)  # Look for the attribute of interest at this dictionary level.
        # If the attribute is not available, we'll get a None in its place.

        if tempDict is None:  # If we've reached the inner-most dictionary.
            attrList.append(tempVal)  # Simply append the final attribute at this level.
            return True  # Return True (attrList is modified in place, and doesn't need to be returned).

        else:  # If there are more levels within the nested dictionary.
            attrList.append(tempVal)  # Append the value associated with attrKey from this level of the dictionary.
            return getNestedAttributes(tempDict, attrList, levelKey,
                                       attrKey)  # Go down one level in the nested dictionary and look for more data.

    except:  # If anything goes wrong, return False
        return False


def makeAttrList(dictList, attr):
    # dictList is a list of dictionaries.
    # attr is the dictionary key whose values you want to pick out and put in a list.
    # attrList is the final list of all attributes associated with the attr key.
    try:
        attrList = []
        for el in dictList:
            attrList.append(el.get(attr))  # Appends None if that key is not found
        return attrList

    except:  # If anything goes wrong, return None
        return None


def te(codeChunk, func):
    # This function tries to apply a function to an input.
    # If it is unsuccessful, it returns None.
    try:
        return func(codeChunk)
    except:
        return None


def parsePatData(patternData):
    # This function will take in the json data from a single pattern ID,
    # and return a dictionary with the pattern attributes I want to store.

    try:

        patternDict = {}  # Initialize an empty dictionary--this is where we'll store all of the data

        # Single item bools
        patternDict['downloadable'] = te(patternData.get('downloadable'), int)         # Bool; whether the pattern can be downloaded (on Ravelry or on another site)
        patternDict['ravelry_download'] = te(patternData.get('ravelry_download'), int) # Bool; whether the pattern is available as a download from Ravelry (free or for money)
        patternDict['free'] = te(patternData.get('free'), int)                         # Bool; whether the pattern is available for no cost

        # Single item ints
        patternDict['queued_projects_count'] = te(patternData.get('queued_projects_count'), int) # Int; number of user queues the pattern is in
        patternDict['rating_count'] = te(patternData.get('rating_count'), int)                   # Int; number of times the pattern has been rated
        patternDict['id'] = te(patternData.get('id'), int) # Int; pattern ID
        patternDict['favorites_count'] = te(patternData.get('favorites_count'), int)             # Int; number of times the pattern has been favorited
        patternDict['difficulty_count'] = te(patternData.get('difficulty_count'), int)           # Int; number of difficulty ratings the pattern has received
        patternDict['projects_count'] = te(patternData.get('projects_count'), int)               # Int; number of projects made from this pattern
        patternDict['comments_count'] = te(patternData.get('comments_count'), int)               # Int; number of comments that have been made on this pattern

        # Single item floats
        patternDict['rating_average'] = te(patternData.get('rating_average'), float) # Float; the pattern's average rating on a scale from 0 to 5 stars
        patternDict['yardage_max'] = te(patternData.get('yardage_max'), float)       # Float; a number describing the estimated maximum yarn yardage a patter will take to make
        patternDict['yardage'] = te(patternData.get('yardage'), float)               # Float; estimated yarn yardage the patter will use
        patternDict['gauge'] = te(patternData.get('gauge'), float)                   # Float; e.g. 16.0
        patternDict['price'] = te(patternData.get('price'), float)                   # Float; the pattern price, currency is given by 'currency'

        # Single item strings
        patternDict['sizes_available'] = te(patternData.get('sizes_available'), str)               # String; description of sizes the pattern can be made to
        patternDict['row_gauge'] = te(patternData.get('row_gauge'), str)                           # String; the pattern's row gauge (not sure what the range of values are)
        patternDict['permalink'] = te(patternData.get('permalink'), str)                           # String; the pattern's url--add to 'https://www.ravelry.com/patterns/library/'
        patternDict['gauge_pattern'] = te(patternData.get('gauge_pattern'), str)                   # String; e.g. 'Stockinette Stitch with yarn held double'
        patternDict['gauge_description'] = te(patternData.get('gauge_description'), str)           # String; e.g. 16 stitches and 24 rows = 4 inches in Stockinette Stitch with yarn held double
        patternDict['yarn_weight_description'] = te(patternData.get('yarnWeightDescription'), str) # String, e.g. 'Fingering (14 wpi)'
        patternDict['yardage_description'] = te(patternData.get('yardage_description'), str)       # String; string describing yardage
        patternDict['currency_symbol'] = te(patternData.get('currency_symbol'), str)               # String; currency symbol, e.g. $
        patternDict['currency'] = te(patternData.get('currency'), str)                             # String; a string describing the currency, e.g. USD
        patternDict['name'] = te(patternData.get('name'), str)  # String; the pattern name
        patternDict['difficulty_average'] = te(patternData.get('difficulty_average'), str)         # String; the average difficulty rating of the pattern, on a scale from 0 to 10, with ? as unknown

        # Items from 'pattern_author'
        tempData = patternData.get('pattern_author', {})  # Data on the pattern's author
        patternDict['author_patterns_count'] = te(tempData.get('patterns_count'), int)      # Int; number of patterns by the author
        patternDict['author_favorites_count'] = te(tempData.get('favorites_count'), int)    # Int; number of times the author has been favorited
        patternDict['author_id'] = te(tempData.get('id'), int)                              # Int; author ID
        patternDict['author_name'] = te(tempData.get('name'), str)                          # String; author name
        patternDict['author_permalink'] = te(tempData.get('permalink'), str)                # String; permalink to the pattern author's Ravelry page (/designers/{permalink})
        tempData = tempData.get('users',[]) # Pattern author site user info, a list of dictionaries; if the 'users' key is not found, return an empty list so that the following lines can still run
        patternDict['author_users_usernames'] = te(makeAttrList(tempData, 'username'), str) # String; list of author usernames
        patternDict['author_users_ids'] = te(makeAttrList(tempData, 'id'), str)             # String; list of author usernames

        # Items from 'photos'
        tempData = patternData.get('photos', {})  # If the 'photos' key doesn't exist, return an empty list so that the following line can still run
        patternDict['num_photos'] = len(tempData) # Int; the number of photos the pattern has

        # Items from 'pattern_type'
        tempData = patternData.get('pattern_type', {})
        patternDict['pattern_type_permalink'] = te(tempData.get('permalink'), str) # String; a word that describes the type of pattern, e.g. 'pullover'
        patternDict['pattern_type_name'] = te(tempData.get('name'), str)           # String; another descriptive word
        patternDict['pattern_type_clothing'] = te(tempData.get('clothing'), int)  # Bool; whether or not the pattern is considered clothing

        # Items from 'craft'
        tempData = patternData.get('craft', {})
        patternDict['craft_permalink'] = te(tempData.get('permalink'), str) # String; a word describing the craft
        patternDict['craft_name'] = te(tempData.get('name'), str)           # String; also a word describing the craft

        # Items from 'pattern_categories'
        tempData = patternData.get('pattern_categories', {})
        tempList = []  # Start a temporary, empty list
        for el in tempData: # Each element of tempData is a nested dictionary (dictionary of dictionaries)
            getNestedAttributes(el, tempList, 'parent', 'name') # This function appends all the names of the pattern categories onto tempList
        patternDict['pattern_categories_names'] = te(tempList, str) # String; the list of category names

        # Items from 'notes'
        tempData = patternData.get('notes','') # if the 'notes' key is not found, return an empty string so the following lines can still run
        patternDict['notes_length'] = len(tempData) # Int; the number of characters in the pattern notes

        # Items from 'pattern_attributes'
        tempData = patternData.get('pattern_attributes', []) # tempData will be a list of dictionaries
        patternDict['pattern_attribute_permalinks'] = te(makeAttrList(tempData, 'permalink'), str) # String; the list of attribute descriptors

        # Items from 'packs'
        tempData = patternData.get('packs', [])  # A list of data about the suggested yarn for the pattern
        patternDict['packs_colorways'] = te(makeAttrList(tempData, 'colorway'), str)   # String; list of colorways of suggested yarns
        patternDict['packs_yarn_names'] = te(makeAttrList(tempData, 'yarn_name'), str) # String; list of yarn names
        patternDict['packs_yarn_ids'] = te(makeAttrList(tempData, 'yarn_id'), str)     # String; list of yarn company names

        # If everything goes to plan, return the dictionary of data that we made!
        return patternDict

    except:

        return None

    # Ravelry pattern data that I DIDN'T use:
    # Don't use 'url', 'pdf_url', 'volumes_in_library', 'printings', 'product_id', 'personal_attributes',
    # 'pattern_needle_sizes' (going to leave it off for now because it's complicated. Could add it in a later version.)
    # 'download_location' (leaving it off because we already have whether the pattern is available for free and whether it's a ravelry download)
    # 'packs': there is more info in packs, but I chose to save 'colorway', 'yarn_weight', 'yarn_name', and 'yarn_company_name'

    # It turns out it was unnecessary to use te to convert everything to the correct data type, because python already
    # recognized the data as their correct data types. However, I have chosen to keep all the te wrappings because it is
    # a failsafe that will return None if the data is somehow not the expected type, and this will prevent the function from crashing.

#     patternDict['author_usernames']       = []                               #A list of author names
#     patternDict['author_userids']         = []                               #A list of author user IDs
#     for el in tempData['users']:
#         patternDict['author_users_username'].append(el['username'])
#         patternDict['author_users_ids'].append(el['id'])
#     str(patternDict['author_users_username'])                                #String; list of author usernames
#     str(patternDict['author_users_ids'])                                     #String; list of author user IDs

#         truthList = ['true','True'] #List of strings to compare to when converting a string to a bool
#         Turns out that python already recognized these variables as bools, so we don't need a truthList


def importPatternIDs(filePath):
    # Function that imports the patterin IDs from a file
    mode = 'r'
    IDsList = []
    with open(filePath, mode) as f:  # Open the file.
        for line in f:
            IDsList.append(line.rstrip())

    return IDsList  # A list of strings--each element is one pattern ID


def makePatternQueryString(IDsList):
    # Function that constructs a pattern query string
    # IDsList should be a list of strings
    s = '+'
    baseString = 'https://api.ravelry.com/patterns.json?ids='
    queryString = baseString + s.join(IDsList)  # Concatenate all elements in patIDs using s as a separator

    return queryString


def constructPatternTuple(pD):
    """This function takes in a dictionary of parsed pattern data and returns an ordered list of pattern data"""

    patternTuple = (pD['id'], pD['name'], pD['permalink'],
                   pD['downloadable'], pD['ravelry_download'],
                   pD['free'], pD['price'], pD['currency'], pD['currency_symbol'],
                   pD['projects_count'], pD['queued_projects_count'], pD['favorites_count'], pD['comments_count'],
                   pD['rating_count'], pD['rating_average'], pD['difficulty_count'], pD['difficulty_average'],
                   pD['yardage_max'], pD['yardage'], pD['gauge'], pD['row_gauge'], pD['sizes_available'],
                   pD['author_id'], pD['author_name'], pD['author_permalink'],
                   pD['author_patterns_count'], pD['author_favorites_count'],
                   pD['author_users_usernames'], pD['author_users_ids'],
                   pD['num_photos'], pD['notes_length'],
                   pD['pattern_type_permalink'], pD['pattern_type_name'], pD['pattern_type_clothing'],
                   pD['craft_permalink'], pD['craft_name'],
                   pD['pattern_categories_names'], pD['pattern_attribute_permalinks'],
                   pD['gauge_pattern'], pD['gauge_description'],
                   pD['yarn_weight_description'], pD['yardage_description'],
                   pD['packs_yarn_ids'], pD['packs_yarn_names'], pD['packs_colorways'])

    return patternTuple


# Configure the scraper's log file
logging.basicConfig(filename='scrapeRavelryPatternData.log', level=logging.INFO)
# ??? Check patternIDs for null values in the main function
# ??? Check that logging works when I run a scraping test

def scrapeRavelryPatternData(c, conn, tableName, patternIDs, batchSize, waitTime, user, pswd, storedIDsList, failedIDsList):
    """"""  # TODO: Write doc string
    # batchSize is assumed to be an integer.
    # batchIDs is assumed to b a non-empty list of integers.
    # storedIDsList should be [] in the initial function call.
    # failedIDsList should be [] in the initial function call.
    # Wrap this whole function in a try/except?

    if batchSize < 1:  # Recursion stop condition.

        failedIDsList.append(patternIDs)  # Add this ID to the list of failed IDs.
        logging.info('batchSize decreased to < 1, skipped ID ' + str(patternIDs) + '.')
        # If batchSize < 1, then there must be only 1 ID in patternIDs
        return True  # Return True to go back up the recursion chain.

    for i in range(0, len(patternIDs), batchSize):  # Split the patternIDs into batches of length batchSize.
        batchIDs = patternIDs[i:i+batchSize]  # Take the desired portion of patternIDs.
        # If batchSize is greater than the len(batchIDs), then the final batch will be the remaining patternIDs--
        # all pattern IDs will be covered, and no error will be thrown.
        queryString = makePatternQueryString(batchIDs)  # Construct the api query string.
        logging.info('Making API query with batchSize = ' + str(batchSize) + ', using ' + str(len(batchIDs))
                     + ' IDs from ID ' + str(batchIDs[0]) + ' to ' + str(batchIDs[-1]) + '.')

        response_time_start = time.clock()
        response = rq.get(queryString, auth=(user, pswd))  # Ask Ravelry for the pattern data.
        response_time_stop = time.clock()

        responseStr = str(response)  # responseStr is the API's response code, e.g. 404, 500, etc.
        logging.info('Received response code ' + responseStr + ' from the API; request took ' +
                     str(response_time_stop - response_time_start) + ' s to complete.')

        time.sleep(waitTime)  # Wait a moment to avoid spooking the API.

        if responseStr == '<Response [200]>':  # If the response is successful, parse and save the data to the database.

            data = response.json()['patterns']

            storage_time_start = time.clock()
            for ID in batchIDs:  # Store the data corresponding to each pattern ID one by one.
                patternData = data[ID]
                patternDict = parsePatData(patternData)

                if not patternDict:  # If patternDict returns None, then skip this pattern ID.
                    # This means that something serious has gone wrong for this particular pattern ID.
                    failedIDsList.append(ID)  # Add this ID to the list of failed IDs
                    logging.info('Error parsing pattern data, skipping pattern ID ' + str(ID) + '.')

                else:
                    patternTuple = constructPatternTuple(patternDict)  # Parse our pattern data into an ordered tuple.

                    # Insert data from this pattern into the table.
                    tableString = ''' INSERT OR IGNORE INTO patternData1 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''  # Ignores entries with a repeated primary key (the pattern ID)
                    c.execute(tableString, patternTuple)
                    # ??? Write a function to generate the tableString

                    storedIDsList.append(ID)  # Add this ID to the list of IDs whose data were stored in the table.

            conn.commit()  # Save the changes to the table
            storage_time_stop = time.clock()
            logging.info('It took ' + str(storage_time_stop - storage_time_start) + ' seconds to store data for '
                         + str(len(batchIDs)) + ' IDs.')

        elif responseStr in ['<Response [404]>', '<Response [500]>', '<Response [504]>']:
            # If we get a data error, reduce the batch size and recursively call this function.
            # We will query the API with smaller and smaller batches of IDs until we find and skip the IDs that were
            # causing problems.
            # We will break the IDs into smaller batches until the batch size gets below 1. This function checks
            # whether batchSize is < 1 at the top, and returns True if so. Therefore, batch sizes down to batchSize = 1
            # will be tried before we simply skip that pattern ID.
            # 404 means that one or more of the patterns in the batch were not found (the corresponding pattern page
            # may have been deleted, or maybe we somehow input a pattern ID that never existed).
            # 500 indicates a server error. I have found that sometimes an particular ID will consistently return a 500
            # response even though my ID scraper found it to be a valid ID--I don't know why this happens, but a
            # reasonable solution is to just skip these patterns, which is what reducing the batch size will do.
            # 504 indicates a Gateway Time-out: the request was canceled because it took more than 10 s to generate a
            # response. Breaking the IDs into smaller batches should fix this problem.

            if len(batchIDs) < batchSize:
                # From the way we created batchIDs, batchIDs should always have at least 1 element. However, batchIDs
                # could end up with far fewer elements than batchSize. For example, let's say we input an initial
                # patternIDs list with 3 elements, and a batchSize of 100. If one of those IDs gives an error, then
                # this function will make several API requests with all 3 IDs before batchSize redues to 1.
                # So if the number of IDs in this batch is less than the current batch size, we'll calculate the new
                # batch size based on the number of IDs instead of on the previous batchSize.
                # This condition will also occur on the tail end of a set of batches, e.g. if we have 4021 IDs initially
                # that get broken into batches of 100 IDs, then the final batch will have only 21 elements.

                tempBatchSize = len(batchIDs)  # Set a temporary batch size equal to the number of IDs in this batch.
                newBatchSize = 10 ** math.floor(math.log10(tempBatchSize - 1))  # Nearest power of 10 < number of IDs.

            else:
                newBatchSize = 10**math.floor(math.log10(batchSize-1))  # Nearest power of 10 that is < than batchSize.
                # e.g. if batchSize = 4291, then newBatchSize = 1000; if batchSize = 100, then newBatchSize = 10.

            # Recursively call this function with a smaller batchSize on the current range of batchIDs.
            # I assume that the original batchSize is something fairly small, like 100 or 1000 patterns per request,
            # which makes recursion appropriate. In my tests so far I have found an initial batch size of 100 or 200
            # to be best.
            logging.info(responseStr + ' in pattern IDs ' + str(batchIDs[0]) + ' to '
                         + str(batchIDs[-1]) + '; reducing batchSize to ' + str(newBatchSize) + '.')

            scrapeRavelryPatternData(c, conn, tableName, batchIDs, newBatchSize, waitTime, user, pswd, storedIDsList, failedIDsList)

        else:
            # If we get another kind of API response code, STOP THE FUNCTION.
            # Other possible response codes are:
            # 400 Bad Request: API call is not valid.
            # 401 Unauthorized: OAuth token has expired or the user has revoked access.
            # 403 Forbidden: Oauth token is not valid, API keys are not valid, or the user is not permitted to use the
            # requested method.
            # 405 Method Not Allowed: you attempted to POST to a GET API method or vice-versa.
            # 413 Request Entity Too Large: your POST was too large; this function uses a GET API method, so this error
            # should not come up.
            # 429 Too Many Requests: If the API says we've sent too many requests, then we should stop sending requests.
            # I haven't found any documentation that specifies the request limits.
            # 503 Service Unavailable: returned if the Ravelry API is down / not avaiable. If we get this error, then
            # we should stop and manually check on the server, and start the function again when the server is back up.
            msg = responseStr + ' in pattern IDs ' + str(batchIDs[0]) + ' to ' + str(batchIDs[-1]) + '; STOPPING THE FUNCTION.'
            logging.info(msg)
            logging.critical(msg)

            raise SystemExit(msg)

    return True  # If the function's largest for loop finishes, this will return True and either go back up the
    # recursion chain, or end the function.

