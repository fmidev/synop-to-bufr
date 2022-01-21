import sys
from datetime import datetime
import traceback
import numpy as np
import subsetArrays as subA
import separateKeysAndValues

from eccodes import *

VERBOSE = 1

#####################################################
# Separates parts from the first row of synop data  #
# to get the parts needed in naming the output file #
#####################################################
def read_filename(input_filename):
    Fin = open(input_filename, 'r')
    rows_in_Fin = Fin.readlines()
    Fin.close()

    # Splits the first row from ":" -> [some text, filepath]
    first_row = rows_in_Fin[0].split(': ')
    
    # Splits the path from file -> [path, to, the, file]
    # and selects only the last part (file).
    filepath = first_row[1].split('/')
    for i in range (0, len(filepath)):
        if (i == len(filepath) - 1):
            filename = filepath[i]

    # Splits filename fro, "_" and selects the right parts to name the file.
    # The second value (year-month-day) is also split from "-" and only the
    # day is selected.
    # The 3rd value (hour:minute) is also split from ":".
    parts = filename.split('_')
    output = []
    for i in range (0, len(parts)):
        if (i == 0 or i == 2):
            output.append(parts[i])
        elif (i == 1):
            day = parts[i].split('-')
            output.append(day[2])
    time = output[2].split(':')
    output[2] = time[0]
    output.append(time[1])

    return output

################################################
# Separates synop data to key and value arrays #
################################################
def read_synop(input_filename):

    Fin = open(input_filename, 'r')
    rows_in_Fin = Fin.readlines()
    Fin.close()

   # Splits the first row from ":" -> [some text, filepath]
   # and all the other rows from ";", -> [ [key=value], [key=value], ...]

    count = 0
    split_rows = []
    for row in rows_in_Fin:
        if(count == 0):
            parts = row.split(': ')
            split_rows.append(parts)
        else:
            parts = row.split(';')
            split_rows.append(parts)
        count = count + 1

    number_of_rows =  len(split_rows)

    # Splits [key=value] -values in each row -> [key, value]
    # Loop ignores the first row, since it doesn't have any key=value arguments

    rows_with_key_value_pairs = []
    for nr in range(1, number_of_rows):
        key_value_array = []
        row = split_rows[nr]
        number_of_arguments = len(row)
        for arg in range(0, number_of_arguments):
            key_value_pair = row[arg]
            split_key_value = key_value_pair.split('=')
            if (arg == number_of_arguments-1):
                last_value = split_key_value[1]
                only_value = last_value.split('*')  # plists the last value from "*"
                split_key_value[1] = only_value[0]  # Only the value is collected
            key_value_array.append(split_key_value)
        rows_with_key_value_pairs.append(key_value_array)

    return rows_with_key_value_pairs
    
#############################################################################
# Main sends input and output files here.                                   #
# 1. Calls read_synop to get keys and values                                #
# 2. Separates keys and values to their own arrays and makes subset array   #
#    objects.                                                               #
#    Subset object has all the values from different subsets in an array    #
#    acording to key-name.                                                  #
# 3. Sends the subset array objects to bufr_encode to give values to        #
#    bufr message.                                                          #
#############################################################################

def message_encoding(input_filename):
    output = read_filename(input_filename)
    # 1. 
    dataIn = read_synop(input_filename)

    # 2.
       #* This for loop uses separateKeysAndValues module to get the keys and values
       #  in separate arrays.
       #* After all the values and keys are separated to their own
       #  arrays, the array that contents values are used to make
       #  subset_array objects.

    keys_in_each_row = []
    values_in_each_row = []
    sub_array = []
    
    for i in range(0,len(dataIn[0])):
        array = []
        sub_array.append(array)

    for nr in range(0, len(dataIn)):
        keys = separateKeysAndValues.getKeys(dataIn[nr])
        keys_in_each_row.append(keys)

        values = separateKeysAndValues.getValues(dataIn[nr])
        values_in_each_row.append(values)

        for s in range(0,len(values)):
            sub_array[s].append(values[s])

    subset_array = subA.Subset(keys_in_each_row[0], sub_array)

    # 3.
       #* Bufr message made from sample. (If many messages loop needs to be added.)
       #* Output file is oppened.
       #* bufr message and subset_array objects are send to bufr_encode.
       #* bufr message is written to the output file. 

    bufr = codes_bufr_new_from_samples('BUFR4')
    

    bufr_encode(bufr, subset_array)

    # Output filename is named by:
    #   - the parts from the first row of the data (output array)
    #   - and by the name of the centre
    # If centre's string name is not found, the integer name is used.

    centre = codes_get(bufr, 'bufrHeaderCentre', s)
    if (str(centre) == 'None'):
        centre = codes_get(bufr, 'bufrHeaderCentre')
    output_filename = output[0] + '_' + str(centre) + '_' + output[1] + output[2] + output[3] + '.bufr'
    
    fout = open(output_filename, 'wb')
    codes_write(bufr, fout)
    codes_release(bufr)
    fout.close()

    
    return output_filename

#####################################################################################
# Encodes a bufr message from subset_array object.                                  #
# Subser_array object is used to get all the values in each subset                  #
#####################################################################################

def bufr_encode(ibufr, subs):
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
    codes_set(ibufr, 'typicalYear', subs.YYYY[0])  
    codes_set(ibufr, 'typicalMonth', subs.MM[0])    
    codes_set(ibufr, 'typicalDay', subs.DD[0])      
    codes_set(ibufr, 'typicalHour', subs.HH24[0])   
    codes_set(ibufr, 'typicalMinute', subs.MI[0])   
    codes_set(ibufr, 'typicalSecond', 0)                  
    
    codes_set_array(ibufr, 'inputDelayedDescriptorReplicationFactor', subs.DELAYED)
    codes_set(ibufr, 'unexpandedDescriptors', 307080)

    # 307080: 301090, 302031, 302035, 302036, 302047, 8002, 302048,
    #         302037, 302043, 302044, 101002, 302045, 302046
        # 302035: 302032, 302033, 302034, 7032, 302004, 101000, 31001, 302005
        # 302036: 105000, 31001, 8002, 20011, 20012, 20014, 20017
        # 302043: 302038, 101002, 302039, 302040, 302041, 302042, 7032
    # If 301001 doesn't work:
        # codes_set_array(ibufr, 'inputExtendedDelayedDescriptorReplicationFactor', subs.EXDESC)
        #ivalues = (301090, 302031,
        #    302032, 302033, 302034, 7032, 302004, 101000, 31001, 302005,
        #    105000, 31001, 8002, 20011, 20012, 20014, 20017,
        #    302047, 8002, 302048, 302037,
        #    302038, 101002, 302039, 302040, 302041, 302042, 7032,
        #    302044, 101002, 302045,
        #    302046)
        #codes_set_array(ibufr, 'unexpandedDescriptors', ivalues)

    # Surface station identification; time, horizontal and vertical coordinates
    # 301090: 301004, 301011, 301012, 301021, 7030, 7031
        # 301004: 1001, 1002, 1015
        # 301011: 4001, 4002, 4003
        # 301012: 4004, 4005
        # 301021: 5001, 6001

    codes_set_array(ibufr, 'year', subs.YYYY)       # 4001
    codes_set_array(ibufr, 'month', subs.MM)        # 4002
    codes_set_array(ibufr, 'day', subs.DD)          # 4003
    codes_set_array(ibufr, 'hour', subs.HH24)       # 4004
    codes_set_array(ibufr, 'minute', subs.MI)       # 4005

    # The WMO block number defines the area in which a station is located:
        # For example, in the 5-digit station index number 10962,
        # 10 is the block number for Germany and
        # 962 is the station number for Hohenpeissenberg.
        # WMON esim 02735 tarkoittaa, etta:
        # block number  = 02 is for Finland and Sweden
    
    codes_set_array(ibufr, 'blockNumber', subs.BLOCK_NUMBER)        # 1001
    codes_set_array(ibufr, 'stationNumber', subs.STATION_NUMBER)    # 1002
    
    # codes_set_array is not for string values:
        # These should work:
        # codes_set_string_array, codes_get_string_array
    for n in range(1, len(subs.STATION_NAME)+1):
        key = '#'+str(n)+'#stationOrSiteName'
        codes_set(ibufr, key, subs.STATION_NAME[n-1])               # 1015

    codes_set_array(ibufr, 'stationType', subs.STATION_TYPE)        # 2001
    codes_set_array(ibufr, 'latitude', subs.LAT)                    # 5001
    codes_set_array(ibufr, 'longitude', subs.LON)                   # 6001

    codes_set_array(ibufr, 'heightOfStationGroundAboveMeanSeaLevel', subs.ELSTAT)  # 7030
    codes_set_array(ibufr, 'heightOfBarometerAboveMeanSeaLevel', subs.ELBARO)      # 7031
 
    # Pressure information
    # 302031: 302001, 10062, 7004, 10009
        # 302001: 10004, 10051, 10061, 10063

    codes_set_array(ibufr, 'nonCoordinatePressure', subs.P_ST)              # 10004
    codes_set_array(ibufr, '3HourPressureChange', subs.P_PPP)               # 10051
    codes_set_array(ibufr, 'pressureReducedToMeanSeaLevel', subs.P_SEA)     # 10061
    codes_set_array(ibufr, 'characteristicOfPressureTendency', subs.P_A)    # 10063

    # Not included in the data:
        # '24HourPressureChange'                 # 10062
        # 'pressure'                             # 7004    
        # 'nonCoordinateGeopotentialHeight'      # 10009

    # Basic synoptic “instantaneous” data       (31001 -> 31002)
    # 302035: 302032, 302033, 302034, 7032, 302004, 101000, 31001, 302005
        # 302032: 7032, 12101, 12103, 13003
        # 302033: 7032, 2001
        # 302034: 7032, 13023
        # 302004: 20010, 8002, 20011, 20013, 20012, 20012, 20011
        # 302005: 8002, 20011, 20012, 20013

        # Temperature and humidity data
        # 302032: 7032, 12101, 12103, 13003
            # Height of sensor above local ground F77 -> 2.0
            # Temperature/air temperature
            # Dewpoint temperature
            # Relative humidity
    
    codes_set_array(ibufr, 'heightOfSensorAboveLocalGroundOrDeckOfMarinePlatform', subs.HEIGHT_OF_SENSOR) # 7032
    codes_set_array(ibufr, 'airTemperature', subs.T)            # 12101
    codes_set_array(ibufr, 'dewpointTemperature', subs.TD)      # 12103
    codes_set_array(ibufr, 'relativeHumidity', subs.RH)         # 13003

        # Visibility data
        # 302033: 7032, 2001
            # Height of sensor above local ground
            # Horizontal visibility

    codes_set_array(ibufr, 'horizontalVisibility', subs.VIS)        # 2001

        # Precipitation past 24 hours
        # 302034: 7032, 13023
            # Height of sensor above local ground
            # Total precipitation past 24 hours

    codes_set_array(ibufr, 'totalPrecipitationPast24Hours', subs.R_24H_TOTAL)

        # 7032:
            # Height of sensor above local ground

        # General cloud information         (31001 -> 31002)
        # 302004: 20010, 8002, 20011, 20013, 20012, 20012, 20012
            # cloud cover
            # vertical significance
            # cloud amounth
            # height of base of cloud
            # cloud type
        # 101000, 31001     
        # 302005: 8002, 20011, 20012, 20013
            # vertical significance 
            # cloud amounth  
            # cloud type   
            # height of base of cloud  

    codes_set_array(ibufr, 'cloudCoverTotal', subs.N_CALC)  # 20010
    codes_set_array(ibufr, 'verticalSignificanceSurfaceObservations', subs.VS_TOTAL)
    codes_set_array(ibufr, 'cloudAmount', subs.CLA_TOTAL)
    codes_set_array(ibufr, 'heightOfBaseOfCloud', subs.HB_TOTAL)
    codes_set_array(ibufr, 'cloudType', subs.CLOUD_TYPE_TOTAL)

    # Clouds with bases below station level     (31001 -> 31002)
    # Replication for this is 0 (number of cloud layers)
        # The number of cloud layers with bases below station level shall be
        # always set to zero in reports from a station at which observations of
        # clouds with bases below station level are not executed.
    # 302036: 105000, 31001, 8002, 20011, 20012, 20014, 20017
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
            # = 7 (low cloud)
            # = 8 (middle cloud)
            # = 9 (high cloud)
        # True direction from which a phenomenon or clouds are moving or in which they are observed
  
    # 8002:
        # Vertical significance (surface observations)(set to missing to cancel the previous value)
        # -> set missing

    # Direction and elevation of cloud   
    # 302048: 5021, 7021, 20012, 5021, 7021
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

    # If there were aws and manual values:
        # when station type == 0 -> use aws values: (WW_AWS, W1_AWS, W2_AWS )
        # when station type is something else -> use manual values
    codes_set_array(ibufr, 'presentWeather', subs.WW)
    codes_set_array(ibufr, 'pastWeather1', subs.W1)
    codes_set_array(ibufr, 'pastWeather2', subs.W2)    

        # 101002:    
            # Replicate 1 descriptor 2 times

        # Sunshine data (from 1 hour and 24-hour period)
        # 302039: 4024, 14031  
            # Time period or displacement (in hours)        data(54)
            # Total sunshine                                data(55)

        # Precipitation measurement
        # 302040: 7032, 102002, 4024, 13011
            # Height of sensor above local ground (for precipitation measurement) 
            # Replicate 2 descriptors 2 times              
            # Time period or displacement (in hours)        
            # Total precipitation/total water equivalent    
 
    codes_set_array(ibufr, 'timePeriod', subs.TIME_PERIOD)
    codes_set_array(ibufr, 'totalPrecipitationOrTotalWaterEquivalent', subs.PRECIPITATION)

        # Extreme temperature data
        # 302041: 7032, 4024, 4024, 12111, 4024, 4024, 12112
            # Height of sensor above local ground       
            # Time period or displacement                  
            # Time period or displacement (see Notes 1 and 2)    
            # Maximum temperature, at height and over periodspecified       
            # Time period or displacement                  
            # Time period or displacement (see Note 2)     
            # Minimum temperature, at height and over period specified         
    codes_set_array(ibufr, 'maximumTemperatureAtHeightAndOverPeriodSpecified', subs.TMAX)
    codes_set_array(ibufr, 'minimumTemperatureAtHeightAndOverPeriodSpecified', subs.TMIN)

        # Wind data
        # 302042: 7032, 2002, 8021, 4025, 11001, 11002, 8021, 103002, 4025, 11043, 11041
            # Height of sensor above local ground               # F77 -> elenem 
            # Type of instrumentation for wind measurement      # F77 -> 8
            # Time significance = 2 Time averaged               # F77 -> 2 
            # Time period or displacement = –10 minutes, or number of minutes after a significant change of wind 
            #     # F77 -> -10.
            #     # same name but different descriptor 4024
            # Wind direction                              
            # Wind speed                                        
            # Time significance = missing value                 # F77 -> missing 
            # Replicate 3 descriptors 2 times
            # Time period or displacement (in minutes)          # F77 -> -10 and -60
            # Maximum wind gust direction                    
            # Maximum wind gust speed                   
    codes_set_array(ibufr, 'instrumentationForWindMeasurement', subs.INSTRUMENT)
    codes_set_array(ibufr, 'timeSignificance', subs.TIME_SIGNIFICANCE)
    codes_set_array(ibufr, 'windDirection', subs.WD_10MIN)
    codes_set_array(ibufr, 'windSpeed', subs.WS_10MIN)
    # WS_MAX_3H # WS_MAX_3H_T ??
    codes_set_array(ibufr, 'maximumWindGustDirection', subs.WGD_MAX)
    codes_set_array(ibufr, 'maximumWindGustSpeed', subs.WGS_MAX)
    
        # 7032:     # hs8
            # Height of sensor above local ground (set to missing to cancel the previous value)

    # Evaporation data
    # 302044: 4024, 2004, 13033 
        # Time period or displacement (in hours)
        # Type of instrumentation for evaporation measurement or type of crop for which evapotranspiration is reported
        # Evaporation/evapotranspiration
    
    # 101002: Replicate 1 descriptor 2 times
    
    # Radiation data (from 1 hour and 24-hour period)
    # 302045: 4024, 14002, 14004, 14016, 14028, 14029, 14030 
        # Time period or displacement (in hours)
        # Long-wave radiation, integrated over period specified
        # Short-wave radiation, integrated over period specified
        # Net radiation, integrated over period specified
        # Global solar radiation (high accuracy), integrated over period specified
        # Diffuse solar radiation (high accuracy), integrated over period specified
        # Direct solar radiation (high accuracy), integrated over period specified

    # Temperature change 
    # 302046: 4024, 4024, 12049 
        # Time period or displacement
        # Time period or displacement (see Note 3)
        # Temperature change over specified period

    codes_set(ibufr, 'pack', 1)  # Required to encode the keys back in the data section

#############################################################################
# Main gets input and output files from command line and sends them to      # 
# message_encode funtion which writes the bufr into the output file.        #
#############################################################################

def main():
    if len(sys.argv) < 2:
        print('Usage: ', sys.argv[0], ' synop_filename', file=sys.stderr)
        sys.exit(1)

    synop_filename = sys.argv[1]
    print('synop data from file: ', synop_filename)

    try:
        bufr_filename = message_encoding(synop_filename)
        print('bufr data in file: ', bufr_filename)
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')

        return 1


if __name__ == '__main__':
    sys.exit(main())