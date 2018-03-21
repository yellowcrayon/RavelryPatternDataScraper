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
        patternDict['downloadable'] = te(patternData.get('downloadable'), bool)         # Bool; whether the pattern can be downloaded (on Ravelry or on another site)
        patternDict['ravelry_download'] = te(patternData.get('ravelry_download'), bool) # Bool; whether the pattern is available as a download from Ravelry (free or for money)
        patternDict['free'] = te(patternData.get('free'), bool)                         # Bool; whether the pattern is available for no cost

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
        tempData = patternData.get('photos', {}) # If the 'photos' key doesn't exist, return an empty list so that the following line can still run
        patternDict['num_photos'] = len(tempData) # Int; the number of photos the pattern has

        # Items from 'pattern_type'
        tempData = patternData.get('pattern_type', {})
        patternDict['pattern_type_permalink'] = te(tempData.get('permalink'), str) # String; a word that describes the type of pattern, e.g. 'pullover'
        patternDict['pattern_type_name'] = te(tempData.get('name'), str)           # String; another descriptive word
        patternDict['pattern_type_clothing'] = te(tempData.get('clothing'), bool)  # Bool; whether or not the pattern is considered clothing

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
        patternDict['pattern_attribute_permalinks'] = te(makeAttrList(tempData, 'permalink'),str) # String; the list of attribute descriptors

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
