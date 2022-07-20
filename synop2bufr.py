#!/usr/bin/env python3

"""
synop2bufr.py is the main program which converts synop data to bufr message (edition 4).
Run program by command: python3 synop2bufr.py name_of_the_synop_file.dat
"""
import sys
import traceback
from eccodes import *
import subset_arrays as subA
import separate_keys_and_values

VERBOSE = 1

def print_error_message(x, text):
    """
    This function prints out an error message and stops the program.
        If x = 0: Error is with naming the bufr file according to the first row of
        the synop data file.
        If x = 1: Error is in the data structure of the synop file.
        Function gets the argument text, which adds information to the error text.
    """
    print('\nError in synop data:\n')
    if x == 0:
        print('Error with naming the bufr file.')
        print('The first row of synop data should be: ')
        print('FILENAME: /path/to/file/TTAAII_year-month-day_hour:minute_something.dat')
        print(text)
    elif x == 1:
        print('Row in synop data with n data values should be: ')
        print('keyname1=value1;keyname2=value2;keyname3=value3;...;keynamen=valuen*')
        print(text)
    sys.exit(1)

def check_name(data):
    """
    This function check if the first row in synop data (data) is written correctly.
    """
    try:
        test = data[0]
    except IndexError:
        print_error_message(0, 'Synop file is empty!\n')

    if 'FILENAME: ' not in data[0]:
        print_error_message(0, '"Filename:  " is missing!\n')
    elif '.dat' not in data[0]:
        print_error_message(0, '".dat" is missing!\n')
    elif '_' not in data[0]:
        print_error_message(0, '"_" are missing!\n')

    test = data[0].split('/')
    test = test[len(test) - 1].split('_')
    if len(test) < 4:
        print_error_message(0, 'Amount of "_" is less than 3!\n')
    elif '-' not in test[1]:
        print_error_message(0, '"-" or "_" in a wrong place!\n')
    elif ':' not in test[2]:
        print_error_message(0, '":" not in a right place!\n')

    day = test[1].split('-')
    time = test[2].split(':')

    if len(day) != 3:
        print_error_message(0, '"year-month-day" is wrong!\n')
    elif len(time) !=2:
        print_error_message(0, '"hour:minute" is wrong!\n')
    try:
        int(day[0])
        int(day[1])
        int(day[2])
        int(time[0])
        int(time[1])
    except ValueError:
        print_error_message(0, 'year, month, day, hour and minute should be integers!\n')

    return data

def check_data(data):
    """
    This function checks if the data section in the synop file is written correctly.
    Argument data is the data in the synop file.
    """
    try:
        data[1]
    except IndexError:
        print_error_message(1, 'Synop file seems not to have any data.\n')

    for i in range(1, len(data)):
        if ';' not in data[i] or '=' not in data[i] or '*' not in data[i]:
            message = 'Synop file has wrongly written data in row ' + str(i) + '.\n'
            print_error_message(1, message)
    for i in range(1, len(data)):
        if ';=' in data[i] or '=;' in data[i]:
            message = 'Synop file has wrongly written data in row ' + str(i) + '.\n'
            print_error_message(1, message)
        elif ';*' in data[i] or '*;' in data[i]:
            message = 'Synop file has wrongly written data in row ' + str(i) + '.\n'
            print_error_message(1, message)
        elif '=*' in data[i] or '*=' in data[i]:
            message = 'Synop file has wrongly written data in row ' + str(i) + '.\n'
            print_error_message(1, message)

    return data

def read_filename(row):
    """
    Separates the 1st row (row) of data to get the parts needed to name the output file.
        1. Splits the first row from ":" -> [some text, file path]
        2. Splits the path -> [path, to, the, file] and selects the last part (file).
        3. Splits filename from "_" and selects the right parts to name the file.
        4. The second value (year-month-day) is split from "-" and the day is selected.
        5. The 3rd value (hour:minute) is also split from ":".
    """
    # 1.
    first_row = row.split(': ')

    # 2.
    filepath = first_row[1].split('/')
    for i in range (0, len(filepath)):
        if i == len(filepath) - 1:
            filename = filepath[i]

    # 3.
    parts = filename.split('_')

    # 4.
    output = []
    for i in range (0, len(parts)):
        if i in (0, 2):
            output.append(parts[i])
        elif i == 1:
            day = parts[i].split('-')
            output.append(day[2])

    # 5.
    time = output[2].split(':')
    output[2] = time[0]
    output.append(time[1])
    return output

def read_synop(rows):
    """
    Separates the synop data to key and value arrays:
        1. Splits rows from ";", -> [ [key=value], [key=value], ...]
        2. Splits: [key=value] in each row to [key, value] and the last value from "*".
    """
    # 1.
    split_rows = []
    for row in rows:
        split_rows.append(row.split(';'))

    number_of_rows =  len(split_rows)

    # 2.
    rows_with_key_value_pairs = []
    for i in range(0, number_of_rows):
        key_value_array = []
        row = split_rows[i]
        number_of_arguments = len(row)
        for j in range(0, number_of_arguments):
            key_value_pair = row[j]
            split_key_value = key_value_pair.split('=')
            if j == number_of_arguments - 1:
                last_value = split_key_value[1]
                only_value = last_value.split('*')
                split_key_value[1] = only_value[0]
            key_value_array.append(split_key_value)
        rows_with_key_value_pairs.append(key_value_array)
    return rows_with_key_value_pairs

def message_encoding(input_file):
    """
    Main sends the input file here.
    1. Reads the lines from the input_file and checks (check_name) if the file's first row
    contains the right parts for naming the output file. After that it checks (check_data)
    if the synop data in the input_file contains the right parts for fetching the data.
    2. Sends the first row of the input file to read_filename to get the name for the
    output file. After that it checks if the output has a right number of values for naming
    the file.
    3. Calls read_synop to get the keys and the values from the input file.
    4. Separates the keys and the values to their own arrays and makes subset array objects.
    The keys and the values are separated by separate_keys_and_values module.
    The subset object has all the values from different subsets in the same array
    according to the key-name.
    5. separate_keys_and_values module's longest_row function is used to choose the key
    row from keys_in_each_row, which has the biggest number of key names.
    6. The bufr message skeleton is made from a sample (edition 4).
    7. Sends the bufr skeleton and the subset_array to bufr_encode to fill the bufr message.
    8. The output filename is named by the parts of the first row of the data (output) and
    the name of the centre.
    9. The output file is opened, the bufr message is written to it, and the output filename is
    returned to the main function.
    """

    # 1.
    rows_in_input_file = input_file.readlines()
    rows_in_input_file = check_name(rows_in_input_file)
    rows_in_input_file = check_data(rows_in_input_file)

    # 2.
    output = read_filename(rows_in_input_file[0])
    if len(output) != 4:
        print_error_message(0, '\n')
    # 3.
    data_in = read_synop(rows_in_input_file[1:])

    # 4.
    keys_in_each_row = []
    sub_array = []

    for i in range(0,len(data_in[0])):
        sub_array.append([])

    for i in range(0, len(data_in)):
        keys_in_each_row.append(separate_keys_and_values.get_keys(data_in[i]))
        values = separate_keys_and_values.get_values(data_in[i])

        for j in range(0,len(values)):
            sub_array[j].append(values[j])

    # 5.
    longest = separate_keys_and_values.longest_row(keys_in_each_row)
    subset_array = subA.Subset(keys_in_each_row[longest], sub_array)

    # 6.
    bufr = codes_bufr_new_from_samples('BUFR4')

    # 7.
    try:
        bufr = bufr_encode(bufr, subset_array)
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')
        codes_release(bufr)
        sys.exit(1)

    # 8.
    centre = codes_get_string(bufr, 'bufrHeaderCentre')
    output_filename = output[0] + '_' + str(centre.upper()) + '_' + output[1] + output[2]
    output_filename = output_filename + output[3] + '.bufr'

    # 9.
    with open(output_filename, 'wb') as fout:
        codes_write(bufr, fout)
        fout.close()

    codes_release(bufr)
    return output_filename

def bufr_encode(ibufr, subs):
    """
    Encodes a bufr message (ibufr) by the subset_array object (subs).
    The subser_array object includes all the values in each subset.
    """
    codes_set(ibufr, 'edition', 4)
    codes_set(ibufr, 'masterTableNumber', 0)
    codes_set(ibufr, 'bufrHeaderCentre', 86)
    codes_set(ibufr, 'bufrHeaderSubCentre', 0)
    codes_set(ibufr, 'updateSequenceNumber', 1)
    codes_set(ibufr, 'dataCategory', 0)
    codes_set(ibufr, 'internationalDataSubCategory', 0)
    codes_set(ibufr, 'dataSubCategory', 1)
    codes_set(ibufr, 'masterTablesVersionNumber', 14)
    codes_set(ibufr, 'localTablesVersionNumber', 0)
    codes_set(ibufr, 'observedData', 1)
    codes_set(ibufr, 'numberOfSubsets', subs.NSUB)
    codes_set(ibufr, 'compressedData', 0)
    codes_set(ibufr, 'typicalYear', max(set(subs.YYYY), key = subs.YYYY.count))
    codes_set(ibufr, 'typicalMonth', max(set(subs.MM), key = subs.MM.count))
    codes_set(ibufr, 'typicalDay', max(set(subs.DD), key = subs.DD.count))
    codes_set(ibufr, 'typicalHour', max(set(subs.HH24), key = subs.HH24.count))
    codes_set(ibufr, 'typicalMinute', max(set(subs.MI), key = subs.MI.count))
    codes_set(ibufr, 'typicalSecond', 0)
    codes_set_array(ibufr, 'inputDelayedDescriptorReplicationFactor', subs.DEL)
    codes_set(ibufr, 'unexpandedDescriptors', 307080)

    # Surface station identification; time, horizontal and vertical coordinates
        # 301090: 301004, 301011, 301012, 301021, 7030, 7031
            # 301004: 1001, 1002, 1015, 2001:
                #    block number, station number, station name, station type
            # 301011: 4001, 4002, 4003: year, moth, day
            # 301012: 4004, 4005: hour, minute
            # 301021: 5001, 6001: latitude, longitude
            # 7030: height of station ground above mean sea level
            # 7031: height of barometer above mean sea level

    codes_set_array(ibufr, 'blockNumber', subs.BLOCK_NUMBER)
    codes_set_array(ibufr, 'stationNumber', subs.STATION_NUMBER)

    # codes_set_array is not for string values:
        # These should work: codes_set_string_array, codes_get_string_array
    for i in range(0, len(subs.STATION_NAME)):
        key = '#'+str(i+1)+'#stationOrSiteName'
        codes_set(ibufr, key, subs.STATION_NAME[i])

    codes_set_array(ibufr, 'stationType', subs.STATION_TYPE)
    codes_set_array(ibufr, 'year', subs.YYYY)
    codes_set_array(ibufr, 'month', subs.MM)
    codes_set_array(ibufr, 'day', subs.DD)
    codes_set_array(ibufr, 'hour', subs.HH24)
    codes_set_array(ibufr, 'minute', subs.MI)
    codes_set_array(ibufr, 'latitude', subs.LAT)
    codes_set_array(ibufr, 'longitude', subs.LON)
    codes_set_array(ibufr, 'heightOfStationGroundAboveMeanSeaLevel', subs.ELSTAT)
    codes_set_array(ibufr, 'heightOfBarometerAboveMeanSeaLevel', subs.ELBARO)

    # Pressure information
    # 302031: 302001, 10062, 7004, 10009
        # 302001: 10004, 10051, 10061, 10063
            #   non coordinate pressure, 3 hour pressure change,
            #   pressure reduced to mean sea level, characteristic of pressure tendency
        # 10062: 24 hour pressure change (Not included in the data)
        # 7004: pressure (Not included in the data)
        # 10009: non coordinate geopotential height (Not included in the data)

    codes_set_array(ibufr, 'nonCoordinatePressure', subs.P_ST)
    codes_set_array(ibufr, '3HourPressureChange', subs.P_PPP)
    codes_set_array(ibufr, 'pressureReducedToMeanSeaLevel', subs.P_SEA)
    codes_set_array(ibufr, 'characteristicOfPressureTendency', subs.P_A)

    # Basic synoptic “instantaneous” data
    # 302035: 302032, 302033, 302034, 7032, 302004, 101000, 31001, 302005
        # 302032: 7032, 12101, 12103, 13003
        # 302033: 7032, 2001
        # 302034: 7032, 13023
        # 302004: 20010, 8002, 20011, 20013, 20012, 20012, 20011
        # 302005: 8002, 20011, 20012, 20013

        # Temperature and humidity data
        # 302032: 7032, 12101, 12103, 13003
            # Height of sensor above local ground
            # Temperature/air temperature
            # Dewpoint temperature
            # Relative humidity

    codes_set_array(ibufr, 'heightOfSensorAboveLocalGroundOrDeckOfMarinePlatform', subs.SENSOR)
    codes_set_array(ibufr, 'airTemperature', subs.T)
    codes_set_array(ibufr, 'dewpointTemperature', subs.TD)
    codes_set_array(ibufr, 'relativeHumidity', subs.RH)

        # Visibility data
        # 302033: 7032, 2001
            # Height of sensor above local ground
            # Horizontal visibility

    codes_set_array(ibufr, 'horizontalVisibility', subs.VIS)

        # Precipitation past 24 hours
        # 302034: 7032, 13023
            # Height of sensor above local ground
            # Total precipitation past 24 hours

    codes_set_array(ibufr, 'totalPrecipitationPast24Hours', subs.R_24H_TOTAL)

        # 7032:
            # Height of sensor above local ground

        # General cloud information
        # 302004: 20010, 8002, 20011, 20013, 20012, 20012, 20012
            # cloud cover
            # vertical significance
            # cloud amount
            # height of base of cloud
            # cloud type
        # 101000, 31001
        # 302005: 8002, 20011, 20012, 20013
            # vertical significance
            # cloud amount
            # cloud type
            # height of base of cloud

    codes_set_array(ibufr, 'cloudCoverTotal', subs.N_CALC)
    codes_set_array(ibufr, 'verticalSignificanceSurfaceObservations', subs.VS_TOTAL)
    codes_set_array(ibufr, 'cloudAmount', subs.CLA_TOTAL)
    codes_set_array(ibufr, 'heightOfBaseOfCloud', subs.HB)
    codes_set_array(ibufr, 'cloudType', subs.CLOUD_TYPE)

    # Clouds with bases below station level
    # Replication for this is 0 (number of cloud layers)
        # The number of cloud layers with bases below station level shall be
        # always set to zero in reports from a station at which observations of
        # clouds with bases below station level are not executed.
    # 302036: 105000, 31001, 8002, 20011, 20012, 20014, 20017 (Not included in the data)
        # Delayed replication of 5 descriptors
        # Vertical significance
        # Cloud amount
        # Cloud type
        # Height of top of cloud
        # Cloud top description

    # Direction of cloud drift
    # 302047: 102003, 8002, 20054
        # Replicate 2 descriptors 3 times
        # Vertical significance (surface observations)
        # True direction from which a phenomenon or clouds are moving or in which
            # they are observed. (Not included in the data)

    # 8002:
        # Vertical significance (surface observations)(set to missing to cancel the
        # previous value)

    # Direction and elevation of cloud
    # 302048: 5021, 7021, 20012, 5021, 7021 (Not included in the data)
        # Bearing or azimuth
        # Elevation
        # Cloud type
        # Bearing or azimuth (set to missing to cancel the previous value)
        # Elevation (set to missing to cancel the previous value)

    # State of ground, snow depth, ground minimum temperature
    # 302037: 20062, 13013, 12113
        # State of the ground (with or without snow)
        # Total snow depth [m]
        # Ground minimum temperature, past 12 hours [K]

    codes_set_array(ibufr, 'stateOfGround', subs.GR)
    codes_set_array(ibufr, 'totalSnowDepth', subs.SNOW_TOTAL)
    codes_set_array(ibufr, 'groundMinimumTemperaturePast12Hours', subs.TGMIN06)

    # Basic synoptic “period” data
    # 302043: 302038, 101002, 302039, 302040, 302041, 302042, 7032

        # Present and past weather
        # 302038: 20003, 4024, 20004, 20005
            # Present weather
            # Time period or displacement (in hours)
            # Past weather (1)
            # Past weather (2)

    codes_set_array(ibufr, 'presentWeather', subs.WW)
    codes_set_array(ibufr, 'timePeriod', subs.TP)
    codes_set_array(ibufr, 'pastWeather1', subs.W1)
    codes_set_array(ibufr, 'pastWeather2', subs.W2)

        # 101002:
            # Replicate 1 descriptor 2 times

        # Sunshine data (from 1 hour and 24-hour period)
        # 302039: 4024, 14031 (Not included in the data)
            # Time period or displacement (in hours)
            # Total sunshine

        # Precipitation measurement
        # 302040: 7032, 102002, 4024, 13011
            # Height of sensor above local ground (for precipitation measurement)
            # Replicate 2 descriptors 2 times
            # Time period or displacement (in hours)
            # Total precipitation/total water equivalent

    codes_set_array(ibufr, 'totalPrecipitationOrTotalWaterEquivalent', subs.PRECIPITATION)

        # Extreme temperature data
        # 302041: 7032, 4024, 4024, 12111, 4024, 4024, 12112
            # Height of sensor above local ground
            # Time period or displacement
            # Time period or displacement
            # Maximum temperature, at height and over period specified
            # Time period or displacement
            # Time period or displacement
            # Minimum temperature, at height and over period specified

    codes_set_array(ibufr, 'maximumTemperatureAtHeightAndOverPeriodSpecified', subs.TMAX)
    codes_set_array(ibufr, 'minimumTemperatureAtHeightAndOverPeriodSpecified', subs.TMIN)

        # Wind data
        # 302042: 7032, 2002, 8021, 4025, 11001, 11002, 8021, 103002, 4025, 11043, 11041
            # Height of sensor above local ground
            # Type of instrumentation for wind measurement
            # Time significance = 2 Time averaged
            # Time period or displacement = –10 minutes,
                # or number of minutes after a significant change
                # of wind (same name but different descriptor 4024)
            # Wind direction
            # Wind speed
            # Time significance = missing value
            # Replicate 3 descriptors 2 times
            # Time period or displacement (in minutes)
            # Maximum wind gust direction
            # Maximum wind gust speed

    codes_set_array(ibufr, 'instrumentationForWindMeasurement', subs.INSTRUMENT)
    codes_set_array(ibufr, 'timeSignificance', subs.TIME_SIGNIFICANCE)
    codes_set_array(ibufr, 'windDirection', subs.WD_10MIN)
    codes_set_array(ibufr, 'windSpeed', subs.WS_10MIN)
    codes_set_array(ibufr, 'maximumWindGustDirection', subs.WGD_MAX)
    codes_set_array(ibufr, 'maximumWindGustSpeed', subs.WGS_MAX)

        # 7032: Height of sensor above local ground
            # (set to missing to cancel the previous value)

    # Evaporation data
    # 302044: 4024, 2004, 13033 (Not included in the data)
        # Time period or displacement (in hours)
        # Type of instrumentation for evaporation measurement or type of
            # crop for which evapotranspiration is reported
        # Evaporation/evapotranspiration

    # 101002: Replicate 1 descriptor 2 times

    # Radiation data (from 1 hour and 24-hour period)
    # 302045: 4024, 14002, 14004, 14016, 14028, 14029, 14030 (Not included in the data)
        # Time period or displacement (in hours)
        # Long-wave radiation, integrated over period specified
        # Short-wave radiation, integrated over period specified
        # Net radiation, integrated over period specified
        # Global solar radiation (high accuracy), integrated over period specified
        # Diffuse solar radiation (high accuracy), integrated over period specified
        # Direct solar radiation (high accuracy), integrated over period specified

    # Temperature change
    # 302046: 4024, 4024, 12049 (Not included in the data)
        # Time period or displacement
        # Time period or displacement (see Note 3)
        # Temperature change over specified period

    codes_set(ibufr, 'pack', 1)  # Required to encode the keys back in the data section
    return ibufr

def main():
    """
    The main function gets the input file from command line and sends it to message_encode
    function which writes the bufr into the output file named by the input file information.
    """
    if len(sys.argv) < 2:
        print('Usage: ', sys.argv[0], ' synop_filename', file=sys.stderr)
        sys.exit(1)
    synop_filename = sys.argv[1]

    try:
        with open(synop_filename, 'r', encoding="utf8") as synop_file:
            print('synop data from file: ', synop_filename)
            try:
                bufr_filename = message_encoding(synop_file)
            except CodesInternalError as err:
                if VERBOSE:
                    traceback.print_exc(file=sys.stderr)
                else:
                    sys.stderr.write(err.msg + '\n')
                return 1
            except Exception as err:
                if VERBOSE:
                    traceback.print_exc(file=sys.stderr)
                else:
                    print(err)
                return 1
            finally:
                synop_file.close()
    except FileNotFoundError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')
        return 1

    print('bufr data in file: ', bufr_filename)
    return None

if __name__ == '__main__':
    sys.exit(main())
