from eccodes import *

##############################################################################
# This Subset class makes keyname objects with keynames that are             #
# mostly used in synop data.                                                 #
# All the values with same keyname are placed into  same object as an array. #
# The values are modified in different functions according to Codes manual.  #
##############################################################################
class Subset:

    #########################################################
    # 1. At first Subset class makes all the values         #
    #    which are not dependent on any other objects       #
    #    to be missing. Only the number of subsets (NSUB)   #  
    #    is given.                                          #
    #########################################################
    def __init__(self, key_array, value_array):
        
        self.NSUB = len(value_array[0])
        miss_list = []
        for m in range(0, self.NSUB):
            miss_list.append('-1e+100')

        self.TTAAII = miss_list                                                                                             
        self.ELANEM = str2float(miss_list, 1)                              
        self.ELBARO = str2float(miss_list, 2)                                
        self.ELSTAT = str2float(miss_list, 3)                               
        self.ELTERM = str2float(miss_list, 4)                                 
        self.LAT = str2float(miss_list, 5)
        self.LON = str2float(miss_list, 6)
        self.STATION_NAME = miss_list
        self.STATION_TYPE = str2int(miss_list, 8)
        self.WMON = miss_list                                                           
        self.N_CALC = str2int(miss_list, 29)                                      
        self.HH_CALC = str2float(miss_list, 25)                             
        self.CLHB2 = str2float(miss_list, 16)                                 
        self.CLHB3 = str2float(miss_list, 17)    
        self.CLHB4 = str2float(miss_list, 18)
        self.CLHB5 = str2float(miss_list, 19)
        self.DD = str2int(miss_list, 21)
        self.GROUND = miss_list 
        self.GROUND06 = str2int(miss_list, 23)   
        self.HH24 = str2int(miss_list, 24)
        self.MI = str2int(miss_list, 26)
        self.MM = str2int(miss_list, 27)       
        self.OBSTIME = miss_list
        self.P_A = str2int(miss_list, 31)
        self.P_PPP = str2float(miss_list, 32)
        self.P_SEA = str2float(miss_list, 33)
        self.P_ST = str2float(miss_list, 34)
        self.RH = str2int(miss_list, 35)
        self.R_12H_AWS = str2float(miss_list, 36)
        self.R_12H_MAN = str2float(miss_list, 37)
        self.R_1H_AWS = str2float(miss_list, 38)
        self.R_1H_MAN = str2float(miss_list, 39)
        self.R_24H = str2float(miss_list, 40)
        self.SNOW06 = str2float(miss_list, 41)
        self.SNOW18 = str2float(miss_list, 42)
        self.SNOW_AWS = str2float(miss_list, 43)
        self.SYNOP = miss_list
        self.T = str2float(miss_list, 45)
        self.TD = str2float(miss_list, 46)
        self.TGMIN06 = str2float(miss_list, 47)
        self.TMAX06 = str2float(miss_list, 48)
        self.TMAX18 = str2float(miss_list, 49)
        self.TMIN06 = str2float(miss_list, 50)
        self.TMIN18 = str2float(miss_list, 51)
        self.VALUE_COUNT = miss_list
        self.VIS = str2int(miss_list, 53)
        self.W1_CALC = str2int(miss_list, 54)   
        self.W2_CALC = str2int(miss_list, 55)   
        self.WD_10MIN = str2float(miss_list, 56)  
        self.WG_10MIN = str2float(miss_list, 57)  
        self.WG_1H_MAX = str2float(miss_list, 58)  
        self.WS_10MIN = str2float(miss_list, 59)  
        self.WS_MAX_3H = miss_list
        self.WS_MAX_3H_T = miss_list                                       
        self.WW_CALC = str2int(miss_list, 62)   
        self.YYYY = str2int(miss_list, 63)
       
       ######################################################################
       # 2. The values are read form value_array, and value is              #
       #    placed in keyname object acording keyname's index position.     #
       #    Values that don't depend on any other objects are given first   #
       #    (as and exception, block number and sation number are given     #
       #    acording to WMO).                                               #
       ######################################################################  
        for key in key_array:
            if (key == 'TTAAII'):                                                
                self.TTAAII = value_array[key_array.index(key)]
            elif (key == 'ELANEM'):                                                 
                self.ELANEM = str2float(value_array[key_array.index(key)], 1)                             
            elif (key == 'ELBARO'):                                                 
                self.ELBARO = str2float(value_array[key_array.index(key)], 2)                                
            elif (key == 'ELSTAT'):                                                 
                self.ELSTAT = str2float(value_array[key_array.index(key)], 3)                               
            elif (key == 'ELTERM'):                                                 
                self.ELTERM = str2float(value_array[key_array.index(key)], 4)                                 
            elif (key == 'LAT'):                                                 
                self.LAT = str2float(value_array[key_array.index(key)], 5)
            elif (key == 'LON'):                                                 
                self.LON = str2float(value_array[key_array.index(key)], 6)
            elif (key == 'STATION_NAME'):                                                 
                self.STATION_NAME = value_array[key_array.index(key)]                                         
            elif (key == 'STATION_TYPE'):                                                 
                self.STATION_TYPE = str2int(value_array[key_array.index(key)], 8)
            elif (key == 'WMON'):                                                 
                self.WMON = value_array[key_array.index(key)]                                                                                              
                self.BLOCK_NUMBER = str2int(self.WMON, 64)                                                                               
                self.STATION_NUMBER = str2int(self.WMON, 65)                
            elif (key =='N_CALC'):                                                 
                self.N_CALC = str2int(value_array[key_array.index(key)], 29)               
            elif (key == 'HH_CALC'):                                                 
                self.HH_CALC = str2float(value_array[key_array.index(key)], 25) 
            elif (key == 'CLHB2'):                                                 
                self.CLHB2 = str2float(value_array[key_array.index(key)], 16)                               
            elif (key == 'CLHB3'):                                                 
                self.CLHB3 = str2float(value_array[key_array.index(key)], 17)   
            elif (key == 'CLHB4'):                                                 
                self.CLHB4 = str2float(value_array[key_array.index(key)], 18)
            elif (key == 'CLHB5'):                                                 
                self.CLHB5 = str2float(value_array[key_array.index(key)], 19)
            elif (key == 'DD'):                                                 
                self.DD = str2int(value_array[key_array.index(key)], 21)
            elif (key == 'GROUND'):                                                 
                self.GROUND = str2int(value_array[key_array.index(key)], 22)
            elif (key == 'GROUND06'):                                                 
                self.GROUND06 = str2int(value_array[key_array.index(key)], 23)   
            elif (key == 'HH24'):                                                 
                self.HH24 = str2int(value_array[key_array.index(key)], 24)
            elif (key == 'MI'):                                                 
                self.MI = str2int(value_array[key_array.index(key)], 26)
            elif (key == 'MM'):                                                 
                self.MM = str2int(value_array[key_array.index(key)], 27)       
            elif (key == 'OBSTIME'):                                                 
                self.OBSTIME = value_array[key_array.index(key)]                                         
            elif (key == 'P_A'):                                                 
                self.P_A = str2int(value_array[key_array.index(key)], 31)
            elif (key == 'P_PPP'):                                                 
                self.P_PPP = str2float(value_array[key_array.index(key)], 32)
            elif (key == 'P_SEA'):                                                 
                self.P_SEA = str2float(value_array[key_array.index(key)], 33)
            elif (key == 'P_ST'):                                                 
                self.P_ST = str2float(value_array[key_array.index(key)], 34)
            elif (key == 'RH'):                                                 
                self.RH = str2int(value_array[key_array.index(key)], 35)
            elif (key == 'R_12H_AWS'):                                                 
                self.R_12H_AWS = str2float(value_array[key_array.index(key)], 36)
            elif (key == 'R_12H_MAN'):                                                 
                self.R_12H_MAN = str2float(value_array[key_array.index(key)], 37)
            elif (key == 'R_1H_AWS'):                                                 
                self.R_1H_AWS = str2float(value_array[key_array.index(key)], 38)
            elif (key == 'R_1H_MAN'):                                                 
                self.R_1H_MAN = str2float(value_array[key_array.index(key)], 39)     
            elif (key == 'R_24H'):                                                 
                self.R_24H = str2float(value_array[key_array.index(key)], 40)
            elif (key == 'SNOW06'):                                                 
                self.SNOW06 = str2float(value_array[key_array.index(key)], 41)
            elif (key == 'SNOW18'):                                                 
                self.SNOW18 = str2float(value_array[key_array.index(key)], 42)
            elif (key == 'SNOW_AWS'):                                                 
                self.SNOW_AWS = str2float(value_array[key_array.index(key)], 43)   
            elif (key == 'SYNOP'):                                                 
                self.SYNOP = value_array[key_array.index(key)]                                         
            elif (key == 'T'):                                                 
                self.T = str2float(value_array[key_array.index(key)], 45)
            elif (key == 'TD'):                                                 
                self.TD = str2float(value_array[key_array.index(key)], 46)
            elif (key == 'TGMIN06'):                                                 
                self.TGMIN06 = str2float(value_array[key_array.index(key)], 47)
            elif (key == 'TMAX06'):                                                 
                self.TMAX06 = str2float(value_array[key_array.index(key)], 48)
            elif (key == 'TMAX18'):                                                 
                self.TMAX18 = str2float(value_array[key_array.index(key)], 49)
            elif (key == 'TMIN06'):                                                 
                self.TMIN06 = str2float(value_array[key_array.index(key)], 50)
            elif (key == 'TMIN18'):                                                 
                self.TMIN18 = str2float(value_array[key_array.index(key)], 51)
            elif (key == 'VALUE_COUNT'):                                                 
                self.VALUE_COUNT = value_array[key_array.index(key)]                                         
            elif (key == 'VIS'):                                                 
                self.VIS = str2int(value_array[key_array.index(key)], 53)
            elif (key == 'W1_CALC'):                                                 
                self.W1_CALC = str2int(value_array[key_array.index(key)], 54)   
            elif (key == 'W2_CALC'):                                                 
                self.W2_CALC = str2int(value_array[key_array.index(key)], 55)       
            elif (key == 'WD_10MIN'):                                                 
                self.WD_10MIN = str2float(value_array[key_array.index(key)], 56)  
            elif (key == 'WG_10MIN'):                                                 
                self.WG_10MIN = str2float(value_array[key_array.index(key)], 57)  
            elif (key == 'WG_1H_MAX'):                                                 
                self.WG_1H_MAX = str2float(value_array[key_array.index(key)], 58)  
            elif (key == 'WS_10MIN'):                                                 
                self.WS_10MIN = str2float(value_array[key_array.index(key)], 59)  
            elif (key == 'WS_MAX_3H'):                                                 
                self.WS_MAX_3H = value_array[key_array.index(key)]                                         
            elif (key == 'WS_MAX_3H_T'):                                                 
                self.WS_MAX_3H_T = value_array[key_array.index(key)]                                         
            elif (key == 'WW_CALC'):                                                 
                self.WW_CALC = str2int(value_array[key_array.index(key)], 62)   
            elif (key == 'YYYY'):                                                 
                self.YYYY = str2int(value_array[key_array.index(key)], 63)

        #######################################################################
        # 3. Values that depend only on N_CALC (cloud cover total) are given. #
        #######################################################################
        for key in key_array:    
            if (key == 'NH_CALC'):
                self.NH_CALC = str2intForCloudAmount(self.N_CALC, value_array[key_array.index(key)], 28) 
            elif (key == 'CH'):                                                 
                self.CH = typeOfcloud(self.N_CALC, value_array[key_array.index(key)], 10)                   
            elif (key == 'CL'):                                                 
                self.CL = typeOfcloud(self.N_CALC, value_array[key_array.index(key)], 11)              
            elif (key == 'CM'):                                                 
                self.CM = typeOfcloud(self.N_CALC, value_array[key_array.index(key)], 20) 
            elif (key == 'CLA2'):                                                 
                self.CLA2 = str2intForCloudAmount(self.N_CALC, value_array[key_array.index(key)], 12)   
            elif (key == 'CLA3'):                                                 
                self.CLA3 = str2intForCloudAmount(self.N_CALC, value_array[key_array.index(key)], 13)   
            elif (key == 'CLA4'):                                                 
                self.CLA4 = str2intForCloudAmount(self.N_CALC, value_array[key_array.index(key)], 14)
            elif (key == 'CLA5'):                                                 
                self.CLA5 = str2intForCloudAmount(self.N_CALC, value_array[key_array.index(key)], 15)
        
        ##################################################################
        # 4. The rest of the values are given to get all the values that # 
        #    bufr message (with descriptor 307080) needs.                #
        ##################################################################
        self.VS = verticalSignificance(self.N_CALC, self.NH_CALC, self.CL, self.CM)         
        self.NREP1 = numberOfRepetition(self.CLA2, self.CLA3, self.CLA4, self.CLA5)
        self.NREP2 = numberOfRepetition2(self.NSUB)
        self.DELAYED = replication(self.NSUB, self.NREP1, self.NREP2)
        self.CLOUD_TYPE_TOTAL = totalListOfCloudType(self.NREP1, self.NREP2, self.CL, self.CM, self.CH)
        self.HB_TOTAL = totalListOfHeightOfBase(self.N_CALC, self.CLA2, self.CLA3, self.CLA4, self.CLA5, self.NREP1, self.HH_CALC, self.CLHB2, self.CLHB3, self.CLHB4, self.CLHB5)
        self.CLA_TOTAL = totalListOfCloudAmount(self.NREP2, self.NH_CALC, self.CLA2, self.CLA3, self.CLA4, self.CLA5)
        self.VS_TOTAL = totalListOfVerticalSignificance(1, self.NREP1, self.NREP2, self.VS, self.CLA2, self.CLA3, self.CLA4, self.CLA5)
        self.PRECIPITATION = totalPrecipitation(self.STATION_TYPE, self.R_12H_MAN, self.R_1H_MAN, self.R_12H_AWS, self.R_1H_AWS)                                                
        self.PRECIPITATION_TIME_PERIOD = timePeriodForPrecipitation(self.PRECIPITATION)
        self.R_24H_TOTAL = totalListOfR24H(self.HH24, self.R_24H) 
        self.GR = chooseGroundData(key_array, self.GROUND, self.GROUND06)
        self.SNOW_TOTAL = totalListOfSnowDepth(self.HH24, key_array, self.GR, self.SNOW06, self.SNOW18, self.SNOW_AWS)
        self.TMAX = temperature(self.HH24, self.TMAX06, self.TMAX18)                                              
        self.TMIN = temperature(self.HH24, self.TMIN06, self.TMIN18)                                                
        self.HEIGHT_OF_SENSOR = totalListOfHeightOfSensor(self.ELANEM, self.ELTERM, self.TMAX, self.TMIN)                                                 
        self.INSTRUMENT = typeOfInstrument(self.NSUB)                                                 
        self.TIME_SIGNIFICANCE = timeSignificance(self.NSUB)
        self.TIME_PERIOD = timePeriod(self.NSUB, self.HH24, self.W1_CALC, self.PRECIPITATION_TIME_PERIOD, self.TMAX, self.TMIN) 
        self.WGD_MAX = windGustDirection(self.NSUB)                                                 
        self.WGS_MAX = windGustSpeed(self.WG_10MIN, self.WG_1H_MAX)

#####################################################
# Functions which are used to give the right values #
# to bufr message are placed below.                 #
#####################################################

def verticalSignificance(n_list, nh_list, CL_list, CM_list):
    # This function calculates vertical significance 8002 for sequence 302004.
        # Vertical significance depends on:
            # n_list = N_CALC = cloud cover total
            # nh_list = NH_CALC = cloud amount
            # CL_list = CL = cloud type (low clouds)
            # CM_list = CM = cloud type (middle clouds)
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(n_list)):
        if (n_list[i] == miss):
            int_list.append(miss)
        elif (n_list[i] == 0):
            int_list.append(62)
        elif (n_list[i] == 113):
            int_list.append(5)
        elif (CL_list[i] > 0):
            int_list.append(7)
        elif (CL_list[i] == 0 and CM_list[i] > 0):
            int_list.append(8)
        elif (nh_list[i] == 0 and n_list != 0):
            int_list.append(0)
        else:
            int_list.append(miss)
    return int_list

def totalListOfVerticalSignificance(aws, NREP1_list, NREP2_list, VS_list , c2list, c3list, c4list, c5list): 
    # This function makes a total list of vertical significance in 307080
        # 302004: These vertical significance values are made in 
        #         function verticalSignificance
        # 302005: Here vertical significance depens on:
            # NREP1_list = NREP1 = number of repetitions of sequance 302005
            # aws = is stations an automatic station or manual station
            # c2list = CLA2 = cloud amount in cloud layer 2
            # c3list = CLA3 = cloud amount in cloud layer 3
            # c4list = CLA4 = cloud amount in cloud layer 4
            # c5list = CLA5 = cloud amount in cloud layer 5
        # 302036: Number of vertical significance depends on the 
            # NREP2_list = NREP2 = number of cloud layers with bases
            # below station mlevel shall be always set to zero in
            # reports from a station at which observations of clouds
            # with bases below station level are not executed.
        # 302047: This information is required from land stations mainly
        #         in the tropics. 
        # 8002: set to missing to cancel the previous value.
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(VS_list)):
        w = 5 + NREP1_list[i] + NREP2_list[i]              
        for j in range(0, w):
            if (j == 0):                             # 302004
                int_list.append(VS_list[i])
            elif (j > 0 and j <= NREP1_list[i]):     # 302005               
                if (aws == 0):                       # manual station
                    int_list.append(j)
                else:                                # automatic station
                    if (NREP1_list[i] == 1 and c2list[i] == miss):
                        int_list.append(miss)
                    elif (NREP1_list[i] == 2 and c3list[i] == miss):
                        int_list.append(miss)
                    elif (NREP1_list[i] == 3 and c4list[i] == miss):
                        int_list.append(miss)
                    elif (NREP1_list[i] == 4 and c5list[i] == miss):
                        int_list.append(miss)
                    else:
                        int_list.append(20 + j)
            else:                                     # 302036, 302047 and 8002
                int_list.append(miss)                           
    return int_list

def totalListOfCloudAmount(NREP2_list, list1, list2, list3, list4, list5):
    # This funtion makes a total list of cloud amount:
        # 302004: depends on list1 = NH_CALC = cloud amount.
        # 302005: depends on:
            # list2 = CLA2 = cloud amount in cloud layer 2.
            # list3 = CLA3 = cloud amount in cloud layer 3.
            # list5 = CLA4 = cloud amount in cloud layer 4.
            # list5 = CLA5 = cloud amount in cloud layer 5.
        # 302036: Number of cloud amount depends on the 
            # NREP2_list = NREP2 = number of cloud layers with bases
            # below station mlevel shall be always set to zero in
            # reports from a station at which observations of clouds
            # with bases below station level are not executed.
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(list1)):
        for j in range (0, 5 + NREP2_list[i]):
            if (j == 0):                              # 302004
                int_list.append(list1[i])
            elif (j == 1):                            # 302005
                if (list2[i] == 0):
                    int_list.append(miss)
                else:
                    int_list.append(list2[i])
            elif (j == 2 and list3[i] != miss):       # 302005
                if (list3[i] == 0):
                    int_list.append(miss)
                else:
                    int_list.append(list3[i])
            elif (j == 3 and list4[i] != miss):       # 302005
                if (list4[i] == 0):
                    int_list.append(miss)
                else:
                    int_list.append(list4[i])
            elif (j == 4 and list5[i] != miss):       # 302005
                if (list5[i] == 0):
                    int_list.append(miss)
                else:
                    int_list.append(list5[i])
            elif (j > 5):                             # 302036
                int_list.append(miss)     
    return int_list

def typeOfcloud(n_list, str_list, x):
    # This function calculates cloud type 20012 for sequence 302004:
        # Cloud type (low clouds) CL :
        #   20012 = CL + 30,
        #   if N = 0, then 20012 = 30,
        #   if N = 9 or /, then 20012 = 62
        # Cloud type (middle clouds) CM :
        #   20012 = CM + 20,
        #   if N = 0, then 20012 = 20,
        #   if N = 9 or / or CM = /, then 20012 = 61
        # Cloud type (high clouds) CH :
        #   20012 = CH + 10,
        #   if N = 0, then 20012 = 10,
        #   if N = 9 or / or CH = /, then 20012 = 60    
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(str_list)):    
        if (n_list[i] == miss or str_list[i] == '-1e+100'):
            int_list.append(miss)
        elif (n_list[i] == 113):
            if (x == 11):
                int_list.append(62)
            elif (x == 20):
                int_list.append(61)
            else:
                int_list.append(60)      
        else:
            if (x == 11):
                cl = int(str_list[i]) + 30
                if (cl == 40):
                    int_list.append(63)
                else:
                    int_list.append(cl)
            elif (x == 20):
                cm = int(str_list[i]) + 20
                if (cm == 30):
                    int_list.append(63)
                else:
                    int_list.append(cm)
            else:
                ch = int(str_list[i]) + 10
                if (ch == 20):
                    int_list.append(63)
                else:
                    int_list.append(ch)             
    return int_list

def totalListOfCloudType(NREP1_list, NREP2_list, CL_list, CM_list, CH_list):
    # This function makes the whole list of cloud types:
        # 302004: depends on:
            # CL_list = CL = cloud type (low cloud)
            # CM_list = CM = cloud type (middle cloud)
            # CH_list = CH = cloud type (high cloud)
        # 302005: depens on:
            # NREP1_list = NREP1 = number of repetitions of sequance 302005
        # 302036: Number of cloud types depends on the 
            # NREP2_list = NREP2 = number of cloud layers with bases
            # below station mlevel shall be always set to zero in
            # reports from a station at which observations of clouds
            # with bases below station level are not executed.
        # 302048: given if value of cloud type is given for cloud elevation
    int_list = []
    for i in range(0, len(CL_list)):
        k = 4 + NREP1_list[i] + NREP2_list[i]   # If NREP2 == 0 then there is 0 repetition of sequance 302036
        for j in range(0, k):
            if (j == 0):         
                int_list.append(CL_list[i])       # 302004
            elif (j == 1): 
                int_list.append(CM_list[i])       # 302004
            elif (j == 2):
                int_list.append(CH_list[i])       # 302004 
            else:
                int_list.append(63)               # missing in other sequences
    return int_list

def numberOfRepetition(list2, list3, list4, list5):
    # Number of repetition in sequance 302005.
    # Depends on: given cloud amount values in each layer:
        # list2 = CLA2 = cloud amount in cloud layer 2.
        # list3 = CLA3 = cloud amount in cloud layer 3.
        # list4 = CLA4 = cloud amount in cloud layer 4.
        # list5 = CLA5 = cloud amount in cloud layer 5.

    int_list = []
    miss = CODES_MISSING_LONG
    for i in range(0, len(list2)):
        int_list.append(1)

    for i in range (0, len(list2)):
        if (list5[i] == miss or list5[i] == 0):
            if (list4[i] == miss or list4[i] == 0):
                if(list3[i] == miss or list3[i] == 0):
                    int_list[i] = 1
                else:
                    int_list[i] = 2
            else:
                int_list[i] = 3
        else:
            int_list[i] = 4    
    return int_list

def str2intForCloudAmount(n_list, str_list, x):
    # This function converts cloud amount data from string to integer
    # before the total list of cloud amount is made.
    # 302004: x = 28, the integer value depends on:
        # n_list = N_CALC = cloud cover total
        # values in data 
    # 302005: x >= 12 and x <= 15, the integer value depends on:
        # values in data
    # 302036: depends on values in data (there is none)

    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(str_list)):
        if (x >= 12 and x <= 15):    
            if (x == 12 and str_list[i] == '0'):
                int_list.append(0)
                    # this will get changed to a missing value later
            elif (x != 12 and str_list[i] == '0'):
                int_list.append(miss)
            elif (str_list[i] == '-1e+100'):
                int_list.append(miss)
            else:
                int_list.append(int(str_list[i]))
        elif (x == 28):
            if (n_list[i] == miss):
                int_list.append(miss)
            elif (n_list[i] == 0):
                int_list.append(0)
            elif (n_list[i] == 113):
                int_list.append(9)
            elif(str_list[i] == '-1e+100'):
                int_list.append(miss)
            else:
                int_list.append(int(str_list[i]))
        else:
            int_list.append(miss)
    return int_list

def totalListOfHeightOfBase(n_list, clist2, clist3, clist4, clist5, NREP1_list, HH_CALC_list, hlist2, hlist3, hlist4, hlist5):
    # This function makes total list of height of base from
    # sequances 302004 and 302005.
    # 302004: depends on:
        # n_list = N_CALC = cloud cover total
        # values in data
    # 302005: depends on:
        # NREP1_list = NREP1 = number of repetition of sequence 302005.
        # clist2 = CLA2 = cloud amount in cloud layer 2.
        # clist3 = CLA3 = cloud amount in cloud layer 3.
        # clist4 = CLA4 = cloud amount in cloud layer 4.
        # clist5 = CLA5 = cloud amount in cloud layer 5.
        # values of data.
    float_list = []
    miss = CODES_MISSING_LONG
    missd = CODES_MISSING_DOUBLE
    for i in range (0, len(HH_CALC_list)):
        d = NREP1_list[i] + 1
        for j in range (0, d):
            if (j == 0):                                        # 302004
                if (n_list[i] == miss):
                    float_list.append(missd)
                elif (n_list[i] == 0):
                    float_list.append(missd)
                else:
                    float_list.append(HH_CALC_list[i])
            else:    
                if (j == 1):                                    # 302005
                    if (clist2[i] == miss):
                        float_list.append(missd)
                    else:
                        float_list.append(hlist2[i])
                elif (j == 2):                                  # 302005
                    if (clist3[i] == miss):
                        float_list.append(missd)
                    else:
                        float_list.append(hlist3[i])
                elif (j == 3):                                  # 302005
                    if (clist4[i] == miss):
                        float_list.append(missd)
                    else:
                        float_list.append(hlist4[i])
                else:                                           # 302005
                    if (clist5[i] == miss):
                        float_list.append(missd)
                    else:
                        float_list.append(hlist5[i])                       
    return float_list

def totalListOfHeightOfSensor(elanem_list, elterm_list, tmax_list, tmin_list):
    # This function makes a list of all the sensor heights:
        # 302035: 302032: for temperature and humidity measurement j = 0
        # 302035: 302033: for visibility measurement j = 1
        # 302035: 302034: for precipitation measurement j = 2
        # 302035: j = 3
        # 302043: 302040: for precipitation measurement j = 4
        # 302043: 302041: for temperature measurement j = 5
            # depends on:
                # tmax_list = TMAX = maximum temperature
                # tmin_list = TMIN = minimum temperature 
            # F77 does not use values of elterm_list = ELTERM
            # but maybe it should be added here?
        # 302043: 302042: for wind measurement j = 6
            # depends on values of elanem_list = ELANEM
        # 302043: j = 7
    float_list = []
    miss = CODES_MISSING_DOUBLE
    for i in range(0, len(elanem_list)):
        tmax = tmax_list[i]
        tmin = tmin_list[i]
        for j in range(0, 8):
            if (j == 0):                            
                float_list.append(2.0)          
            elif (j == 5):                          
                if (tmax == miss or tmin == miss):
                    float_list.append(miss)
                else:
                    float_list.append(2.00)
            elif (j == 6):                          
                float_list.append(elanem_list[i])  
                    # F77 must have a mistake with this, since there:
                    # in sub 3 this is 15, not miss
                    # and in subs 16, 21 ja 26 this 12, not miss .                  
            else:
                float_list.append(miss)   
    return float_list

def totalListOfR24H(HH24_list, R24H_list):
    # This function makes a total list of precipitation past 24 hours.
    # It depends on:
        # HH24_list = HH24 = hour of the measurement
        # values in data
    float_list = []
    miss = CODES_MISSING_DOUBLE
    for i in range(1, len(R24H_list) + 1):
        if (HH24_list[i-1] == 5):
            float_list.append(R24H_list[i-1])
        else:
            float_list.append(miss)
    return float_list

def chooseGroundData(key_list, list1, list2):
    # This function chooses ground data. If key_list includes key GROUND06,
    # the values of GROUND06 (list2) is used. If not, values of GROUND (list1)
    # is used.
    if('GROUND06' in key_list):
        int_list = list2
    else:
        int_list = list1
    return int_list

def totalListOfSnowDepth(HH24_list, key_list, GR_list, SNOW06_list, SNOW18_list, SNOW_AWS_list):
    # This function makes a total list of snow depth. It depends on:
        # HH24_list = HH24 = hour of the measurement
        # key_list, if it includes values SNOW06 or SNOW18
        # GR_list = GR = ground data
        # values of data:
            # SNOW06_list = SNOW06
            # SNOW18_list = SNOW18
            # SNOW_AWS_list = SNOW_AWS
    float_list = []
    for i in range(0, len(HH24_list)):
        if('SNOW06' in key_list and HH24_list[i] == 5):
            if (SNOW06_list[i] == 0 and GR_list[i] >= 11 and GR_list[i] <= 12):
                float_list.append(-0.02)
            elif (SNOW06_list[i] == 0 and GR_list[i] == 13):
                float_list.append(-0.01)
            elif (SNOW06_list[i] == 0):
                float_list.append(-0.01)
            elif (SNOW06_list[i] == -0.01):
                float_list.append(0.0)
            else:
                float_list.append(SNOW06_list[i])
        elif('SNOW18' in key_list and HH24_list[i] == 17):
            if (SNOW18_list[i] == 0 and GR_list[i] >= 11 and GR_list[i] <= 12):
                float_list.append(-0.02)
            elif (SNOW18_list[i] == 0 and GR_list[i] == 13):
                float_list.append(-0.01)
            elif (SNOW18_list[i] == 0):
                float_list.append(-0.01)
            elif (SNOW18_list[i] == -0.01):
                float_list.append(0.0)
            else:
                float_list.append(SNOW18_list[i])
        else:
            if (SNOW_AWS_list[i] == 0 and GR_list[i] >= 11 and GR_list[i] <= 12):
                float_list.append(-0.02)
            elif (SNOW_AWS_list[i] == 0 and GR_list[i] == 13):
                float_list.append(-0.01)
            elif (SNOW_AWS_list[i] == 0):
                float_list.append(-0.01)
            elif (SNOW_AWS_list[i] == -0.01):
                float_list.append(0.0)
            else:
                float_list.append(SNOW_AWS_list[i])
    return float_list

def replication(ns, NREP1_list, NREP2_list):
    # This functions combines the 2 replications, which is used to make
    # the array for delaid replication. It depends on:
        # ns = NSUB = number of subsets
        # NREP1_list = NREP1 = number of replication in sequence 302005
        # NREP2_list = NREP2 = number of replication in sequence 302036
    int_list = []
    for i in range(0, ns):
        int_list.append(NREP1_list[i])      # 302005
        int_list.append(NREP2_list[i])      # 302036
    return int_list

def totalPrecipitation(STATION_TYPE_list, R12HM_list, R1HM_list, R12HA_list, R1HA_list):
    # This function makes a total list of precipitation:
    # totalPrecipitationOrTotalWaterEquivalent 13011. It depends on:
        # STATION_TYPE_list = STATION_TYPE = tells if the station is
            # automatic of not.
        # R12HM_list = R_12H_MAN = Precipitation past 12 hours in manual station
        # R1HM_list = R_1H_MAN = Precipitation past 1 hour in manual station
        # R12HA_list = R_12H_AWS = Precipitation past 12 hours in automatic  station
        # R1HA_list = R_1H_AWS = Precipitation past 1 hour in automatic station
    float_list = []
    for i in range (0, len(STATION_TYPE_list)):
        if (STATION_TYPE_list[i] == 0):
            float_list.append(R12HA_list[i])
            float_list.append(R1HA_list[i])
        else:
            float_list.append(R12HM_list[i])
            float_list.append(R1HM_list[i])
    return float_list

def temperature(HH24_list, t1_list, t2_list):
    # This function is used to choose right values for temperature.
    # It depends on:
        # HH24_list = HH24 = hour of measurement
        # t1_list = TMAX06 or TMIN06
        # t2_list = TMAX18 or TMIN18
    float_list = []
    miss = CODES_MISSING_DOUBLE
    for i in range (1, len(t1_list) + 1):
        if (HH24_list[i-1] == 6):
            float_list.append(t1_list[i-1])
        elif (HH24_list[i-1] == 18):
           float_list.append(t2_list[i-1])
        else:
            float_list.append(miss)
    return float_list

def numberOfRepetition2(ns):
    # This function gives delaid repetition for 302036.
    int_list = []
    for i in range(0, ns):
        int_list.append(0)
    return int_list

def timePeriodForPrecipitation(totalR_H_list):
    # This function gives time period values for precipitation. It depends on:
        # totalR_H_list = PRECIPITATION = total list of precipitation.
    int_list = []
    miss = CODES_MISSING_LONG
    missD = CODES_MISSING_DOUBLE
    for i in range (0, len(totalR_H_list)):
        if (totalR_H_list[i] == missD):
            int_list.append(miss)
        elif (i % 2):
            int_list.append(-1)
        else:
            int_list.append(-12)
    return int_list

def timePeriod(ns, hh_list, w1_list, tp_list, tmax_list, tmin_list):
    # This funkction gives all the time period values. It depends on:
        # ns = NSUB = number of subsets
        # 302038 [h] j = 0
            # hh_list = HH24 = hour of measurement
            # w1_list = W1_CALC = past weather 1
        # 302039 [h] j = 1 and 2
        # 302040 [h] j = 3 and 4
            # tp_list = PRECIPITATION_TIME_PERIOD = time period for precipitation
        # 302041 [h] j = 5, 6, 7 and 8
            # tmax_list = TMAX = maximum temperature
            # tmin_list = TMIN = minimum temperature
        # 302042 [min] j = 9, 10 and 11
        # 302044 [h] j = 12
        # 302045 [h] j = 13 and 14
        # 302046 [h] j = 15 and 16
    int_list = []
    miss = CODES_MISSING_LONG
    missD = CODES_MISSING_DOUBLE
    t = 0
    for i in range (0, ns):
        tmax = tmax_list[i]
        tmin = tmin_list[i]
        for j in range (0, 17):
            if (j == 0):
                if (w1_list[i] != 31):
                    h = [0, 5, 6, 11, 12, 17, 18, 23]
                    if (hh_list[i] in h):
                        int_list.append(-6)
                    else:
                        int_list.append(-3)
                else:
                    int_list.append(miss)           
            elif (j == 9 or j == 10):
                int_list.append(-10)
            elif (j == 11):
                int_list.append(-60)
            elif (j == 3):
                int_list.append(tp_list[t])
                t = t + 1
            elif (j == 5 or j == 7):
                if (j == 5 and tmax == missD):
                    int_list.append(miss)
                elif (j == 7 and tmin == missD):
                    int_list.append(miss)
                else:
                    int_list.append(-12)
            elif (j == 6 or j == 8):          
                if (j == 6 and tmax == missD):
                    int_list.append(miss)
                elif (j == 8 and tmin == missD):
                    int_list.append(miss)
                else:
                    int_list.append(0)
            elif (j == 4):
                int_list.append(tp_list[t])
                t = t + 1 
            else:
                int_list.append(miss)     
    return int_list

def typeOfInstrument(ns):
    # This function gives the total list of instrument types.
    # The size of list depends on ns = NSUB = number of subsets.
    float_list = []
    for n in range(1, ns + 1):
       float_list.append(8.0)
    return float_list

def timeSignificance(ns):
    # This function gives the total list of time significance.
    # The size of list depends on ns = NSUB = number of subsets.
    int_list = []
    miss = 31
    for i in range(1, ns + 1):
        int_list.append(2)
        int_list.append(miss)
    return int_list

def windGustDirection(ns):
    # This function gives the total list of direction of wind gust.
    # The size of list depends on ns = NSUB = number of subsets.
    float_list = []
    miss = CODES_MISSING_LONG
    for i in range(0, ns):
        float_list.append(miss)
        float_list.append(miss)
    return float_list

def windGustSpeed(list1, list2):
    # This function gives the total list of speed of wind gust.
    # It depends on values in:
        # list1 = WG_10MIN
        # list2 = WG_1H_MAX
    float_list = []
    for i in range(0, len(list1)):
        float_list.append(list1[i])       # WG_10MIN
        float_list.append(list2[i])       # WG_1H_MAX
    return float_list

def str2int(str_list, x):
    # This function makes a string list (str_list) to a integer list (int_list).
        # x represents the id of different values. Values are converted
        # from string to integer depending on x.
        # Before this function, missing values = '/' are changed to be '-1e+100'
        # which in eccodes is the missing value of float type value. It is
        # changed to be missing value of integer type value.
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(str_list)):
        if (str_list[i] == '-1e+100'):
            if (x == 22 or x == 23):
                int_list.append(31)
            elif (x == 29):
                int_list.append(miss)
            elif (x == 31):
                int_list.append(15)
            elif (x == 35):
                int_list.append(miss)
            elif (x == 53):
                int_list.append(miss)
            elif (x >= 54 and x <= 55):
                int_list.append(31)
            elif (x == 62):
                int_list.append(511)
            elif (x == 64):
                int_list.append(2)
            elif (x == 65):
                int_list.append(761)
            else:
                int_list.append(miss)
        else:
            if (x == 29):
                int_list.append(int(int(str_list[i])*12.5 + 0.5))
            elif (x == 53 and int(str_list[i]) > 81900):
                int_list.append(81900)
            elif (x == 64):
                wmo = str_list[i]
                b = wmo[:2]
                int_list.append(int(b))
            elif (x == 65):
                wmo = str_list[i]
                b = wmo[-3:]
                int_list.append(int(b))
            else:
                int_list.append(int(str_list[i]))
    return int_list

def str2float(str_list, x):
    # This function makes a string list (str_list) to a float list (float_list).
        # x represents the id of different values. Values are converted
        # from string to float depending on x.
        # Before this function, missing values = '/' are changed to be '-1e+100'
        # which in eccodes is the missing value of float type value.
    float_list = []
    for i in range (0, len(str_list)):
        if (str_list[i] == '-1e+100'):
            float_list.append(float(str_list[i]))
        elif (x >= 32 and x <= 34):
            float_list.append(float(str_list[i]) * 100)     # hPa -> Pa
        elif (x >= 36 and x <= 40):
            if (str_list[i] == '0'):
                float_list.append(-0.1)
            elif (str_list[i] == '-1'):
                float_list.append(0.0)
            else:
                float_list.append(float(str_list[i]))
        elif (x >= 41 and x <= 43):
            float_list.append(float(str_list[i]) * 0.010)   # cm -> m
        elif (x >= 45 and x <= 51):
            float_list.append(float(str_list[i]) + 273.15)  # C -> K 
        else:
            float_list.append(float(str_list[i]))
    return float_list