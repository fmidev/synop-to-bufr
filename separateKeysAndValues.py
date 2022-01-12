# This funktion gets the keys and sets them in a array
# row is one observation, which includes key/value pairs.
from eccodes import *

def getKeys(row_with_key_value_pairs):
    number_of_pairs = len(row_with_key_value_pairs)
    keys =[]
    for k in range(0, number_of_pairs):
        keyValue = row_with_key_value_pairs[k]
        key = keyValue[0]
        keys.append(key)

    return keys

def getValues(row_with_key_value_pairs):
    number_of_pairs = len(row_with_key_value_pairs)
    values =[]
    for v in range(0, number_of_pairs):
        keyValue = row_with_key_value_pairs[v]
        value = keyValue[1]
        if(value == '/'):
            value = str(CODES_MISSING_DOUBLE)
        values.append(value)

    return values   


# This function checks if all the rows are the same

def areAllTheRowsSimilar(rows):
    numberOfRows = len(rows)
    different = True
    for r in range(0,numberOfRows - 1):
        row_a = rows[r]
        row_b = rows[r+1]
        if (row_a != row_b):
            different = False

    return different

 