from eccodes import *

class Subset:

    def __init__(self, value_array):
        self.TTAAII = value_array[0]                                                
        self.NSUB = len(self.TTAAII)                                               
        self.ELANEM = str2float(value_array[1], 1)                              
        self.ELBARO = str2float(value_array[2], 2)                                
        self.ELSTAT = str2float(value_array[3], 3)                               
        self.ELTERM = str2float(value_array[4], 4)                                 
        self.HEIGHT_OF_SENSOR = totalListOfHeightOfSensor(self.ELANEM, self.ELTERM)
        self.LAT = str2float(value_array[5], 5)
        self.LON = str2float(value_array[6], 6)
        self.STATION_NAME = value_array[7]
        self.STATION_TYPE = str2int(value_array[8], 8)
        self.WMON = value_array[9]                                             
        self.BLOCK_NUMBER = str2int(self.WMON, 64)                              
        self.STATION_NUMBER = str2int(self.WMON, 65)                 
        self.N_CALC = str2int(value_array[29], 29)                                
        self.NH_CALC = str2intForCloudAmount(self.N_CALC, value_array[28], 28)    
        self.CH = typeOfcloud(self.N_CALC, value_array[10], 10)                    
        self.CL = typeOfcloud(self.N_CALC, value_array[11], 11)                   
        self.CM = typeOfcloud(self.N_CALC, value_array[20], 20)                     
        self.VS = verticalSignificance(self.N_CALC, self.NH_CALC, self.CL, self.CM)         
        self.HH_CALC = str2float(value_array[25], 25)                             
        self.CLA2 = str2intForCloudAmount(self.N_CALC, value_array[12], 12)        
        self.CLA3 = str2intForCloudAmount(self.N_CALC, value_array[13], 13)        
        self.CLA4 = str2intForCloudAmount(self.N_CALC, value_array[14], 14)
        self.CLA5 = str2intForCloudAmount(self.N_CALC, value_array[15], 15)
        self.CLHB2 = str2float(value_array[16], 16)                                 
        self.CLHB3 = str2float(value_array[17], 17)    
        self.CLHB4 = str2float(value_array[18], 18)
        self.CLHB5 = str2float(value_array[19], 19)
        self.NREP1 = numberOfRepetition(self.CLA2, self.CLA3, self.CLA4, self.CLA5)
        self.NREP2 = numberOfRepetition2(self.NSUB)                                
        self.EXDESC = extendedDelaye(self.NSUB, self.NREP1, self.NREP2)  
        self.TIME_PERIOD = timePeriod(self.NSUB)                                    
        self.VS_TOTAL = totalListOfVerticalSignificance(1, self.NREP1, self.NREP2, self.VS, self.N_CALC, self.CLA2, self.CLA3, self.CLA4, self.CLA5)
        self.CLA_TOTAL = totalListOfCloudAmount(self.NH_CALC, self.CLA2, self.CLA3, self.CLA4, self.CLA5)
        self.CLOUD_TYPE_TOTAL = totalListOfCloudType(self.NREP1, self.NREP2, self.CL, self.CM, self.CH)
        self.HB_TOTAL = totalListOfHeightOfBase(self.N_CALC, self.CLA2, self.CLA3, self.CLA4, self.CLA5, self.NREP1, self.HH_CALC, self.CLHB2, self.CLHB3, self.CLHB4, self.CLHB5)
        self.DD = str2int(value_array[21], 21)
        self.GROUND = value_array[22] 
        self.GROUND06 = str2int(value_array[23], 23)   
        self.HH24 = str2int(value_array[24], 24)
        self.MI = str2int(value_array[26], 26)
        self.MM = str2int(value_array[27], 27)       
        self.OBSTIME = value_array[30]
        self.P_A = str2int(value_array[31], 31)
        self.P_PPP = str2float(value_array[32], 32)
        self.P_SEA = str2float(value_array[33], 33)
        self.P_ST = str2float(value_array[34], 34)
        self.RH = str2int(value_array[35], 35)
        self.R_12H_AWS = str2float(value_array[36], 36)
        self.R_12H_MAN = str2float(value_array[37], 37)
        self.R_1H_AWS = str2float(value_array[38], 38)
        self.R_1H_MAN = str2float(value_array[39], 39)
        self.PRECIPITATION = totalPrecipitation(self.STATION_TYPE, self.R_12H_MAN, self.R_1H_MAN, self.R_12H_AWS, self.R_1H_AWS) 
        self.R_24H = str2float(value_array[40], 40)
        self.R_24H_TOTAL = totalListOfR24H(self.HH24, self.R_24H) 
        self.SNOW06 = str2float(value_array[41], 41)
        self.SNOW18 = str2float(value_array[42], 42)
        self.SNOW_AWS = str2float(value_array[43], 43)
        self.SNOW_TOTAL = totalListOfSnowDepth(self.HH24, self.SNOW06, self.SNOW18, self.SNOW_AWS)
        self.SYNOP = value_array[44]
        self.T = str2float(value_array[45], 45)
        self.TD = str2float(value_array[46], 46)
        self.TGMIN06 = str2float(value_array[47], 47)
        self.TMAX06 = str2float(value_array[48], 48)
        self.TMAX18 = str2float(value_array[49], 49)
        self.TMIN06 = str2float(value_array[50], 50)
        self.TMIN18 = str2float(value_array[51], 51)
        self.TMAX = temperature(self.HH24, self.TMAX06, self.TMAX18)
        self.TMIN = temperature(self.HH24, self.TMIN06, self.TMIN18)
        self.INSTRUMENT = typeOfInstrument(self.NSUB)
        self.TIME_SIGNIFICANCE = timeSignificance(self.NSUB)
        self.VALUE_COUNT = value_array[52]
        self.VIS = str2int(value_array[53], 53)
        self.W1_CALC = str2int(value_array[54], 54)   
        self.W2_CALC = str2int(value_array[55], 55)   
        self.WD_10MIN = str2float(value_array[56], 56)  
        self.WG_10MIN = str2float(value_array[57], 57)  
        self.WG_1H_MAX = str2float(value_array[58], 58)  
        self.WS_10MIN = str2float(value_array[59], 59)  
        self.WS_MAX_3H = value_array[60]
        self.WS_MAX_3H_T = value_array[61]                                         
        self.WW_CALC = str2int(value_array[62], 62)   
        self.YYYY = str2int(value_array[63], 63)
        self.WGD_MAX = windGustDirection(self.NSUB)
        self.WGS_MAX = windGustSpeed(self.WG_10MIN, self.WG_1H_MAX)


def verticalSignificance(n_list, nh_list, CL_list, CM_list):
    # This function calculates vertical significance 8002 for sequence 302004
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

def totalListOfVerticalSignificance(aws, NREP1_list, NREP2_list, VS_list, n_list , c2list, c3list, c4list, c5list): 
    # This fnction makes a total list of vertical significance in 307080
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(VS_list)):
        w = 5 + NREP1_list[i] + NREP2_list[i]              
        for j in range(0, w):
            if (j == 0):                                         # 302004
                int_list.append(VS_list[i])
            elif (j > 0 and j <= NREP1_list[i]):                # 302005               
                if (aws == 0):                                   # manual station
                    int_list.append(j)
                else:                                            # automatic station
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
            else:                                               # 302036, 302047 and 8002
                int_list.append(miss)                           
    return int_list

def totalListOfCloudAmount(list1, list2, list3, list4, list5):
    # This funtion makes a total list of cloud amont:
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(list1)):
        for j in range (0, 5):
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
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range(0, len(list2)):
        int_list.append(1)

    for i in range(0, len(list2)):
        if (list3[i] == miss or list3[i] == 0):
            int_list[i] == 1
            if (list4[i] == miss or list4[i] == 0):
                int_list[i] == 1
                if (list5[i] == miss or list5[i] == 0):
                    int_list[i] == 1
                else:
                    int_list[i] = 4
            else:
                int_list[i] = 3
        else:
            int_list[i] = 2
    return int_list

def str2intForCloudAmount(n_list, str_list, x):
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(str_list)):
        if (x >= 12 and x <= 15):    
            if (x == 12 and str_list[i] == '0'):
                int_list.append(0)
                    # pidetaan viela tassa nollana, myohemmin -> miss
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
                    # sama kun 15?
            else:
                int_list.append(int(str_list[i]))
        else:
            int_list.append(miss)
    return int_list

def totalListOfHeightOfBase(n_list, clist2, clist3, clist4, clist5, NREP1_list, HH_CALC_list, hlist2, hlist3, hlist4, hlist5):
    # This function makes total list of height of base from sequances 302004 and 302005
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
                        float_list.append(list4[i])
                else:                                           # 302005
                    if (clist5[i] == miss):
                        float_list.append(missd)
                    else:
                        float_list.append(hlist5[i])                       
    return float_list

def totalListOfHeightOfSensor(elanem_list, elterm_list):
    float_list = []
    miss = CODES_MISSING_DOUBLE
    for i in range(0, len(elanem_list)):
        for j in range(0, 8):
            if (j == 0):                            # 302035: 302032: for temperature and humidity measurement
                float_list.append(2.0)          
            elif (j == 5):                          # 302043: 302041: for temperature measurement
                #float_list.append(elterm_list[i]) ??
                float_list.append(2.00)
            elif (j == 6):                          # 302043: 302042: for wind measurement
                float_list.append(elanem_list[i])                     
            else:
                float_list.append(miss)
                    # j = 1: 302035: 302033: for visibility measurement
                        # f77 ei aseta mitaan data(25)
                    # j = 2: 302035: 302034: for precipitation measurement
                        # f77 ei aseta mitaan data(27)
                    # j = 3: 302035: set to missing to cancel the previous value
                        # f77 ei aseta mitaan data(29)
                    # j = 4: 302043: 302040: for precipitation measurement
                        # f77 ei aseta mitaan
                    # j = 7: 302043: set to missing to cancel the previous value
                        # f77 ei aseta mitaan data(72 + eps)    
    return float_list

def totalListOfR24H(HH24_list, R24H_list):
    float_list = []
    miss = CODES_MISSING_DOUBLE
    for i in range(1, len(R24H_list) + 1):
        if (HH24_list[i-1] == 5):
            float_list.append(R24H_list[i-1])
        else:
            float_list.append(miss)
    return float_list

def totalListOfSnowDepth(HH24_list, SNOW06_list, SNOW18_list, SNOW_AWS_list):
    float_list = []
    for i in range(0, len(HH24_list)):
        if(HH24_list[i] == 5):
            float_list.append(SNOW06_list[i])
        elif(HH24_list[i] == 17):
            float_list.append(SNOW18_list[i])
        else:
            float_list.append(SNOW_AWS_list[i])
    return float_list

def extendedDelaye(ns, NREP1_list, NREP2_list):
    int_list = []
    for i in range(0, ns):
        int_list.append(NREP1_list[i])      # 302005
        int_list.append(NREP2_list[i])      # 302036
    return int_list

def totalPrecipitation(STATION_TYPE_list, R12HM_list, R1HM_list, R12HA_list, R1HA_list):
    # This function makes a total list of precipitation: totalPrecipitationOrTotalWaterEquivalent 13011
    float_list = []
    for i in range (1, len(STATION_TYPE_list) + 1):
        if (STATION_TYPE_list[i-1] == 0):
            float_list.append(R12HA_list[i-1])
            float_list.append(R1HA_list[i-1])
        else:
            float_list.append(R12HM_list[i-1])
            float_list.append(R1HM_list[i-1])
    return float_list

def temperature(HH24_list, t1_list, t2_list):
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
    # Delaid  repetition for 302036
    int_list = []
    for i in range(0, ns):
        int_list.append(0)
    return int_list

def timePeriod(ns):
    # This gives still wrong values
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, ns):
        for j in range (0, 17):
            if (j == 9 or j == 10):
                int_list.append(-10)
                    # 302042 j = 9 ja 10 [min] -> -10
            elif (j == 11):
                int_list.append(-60)
                    # 302042 j = 11 [min] -> -60
            elif (j == 3 or j == 5 or j == 7):
                int_list.append(-12)
                    # 302040 j = 3 [h] -> -12
                    # 302041 j = 5 ja j = 7 [h] -> -12
            elif (j == 6 or j == 8):          
                int_list.append(0)
                    # 302041 j = 6 ja j = 6 [h] -> 0 (see Note)
            elif (j == 4):
                int_list.append(-1)  
                    # 302040 j = 4 [h] -> -1
            else:
                int_list.append(miss)
                    # 302038 j = 0 [h] -> miss
                    # 302039 j = 1 ja j = 2 [h] -> miss
                    # 302044 j = 12 [h] -> miss
                    # 302045 j = 13 ja j = 14 [h] -> miss
                    # 302046 j = 15 ja j = 16 [h] -> miss

    return int_list

def typeOfInstrument(ns):
    float_list = []
    for n in range(1, ns + 1):
       float_list.append(8.0)
    return float_list

def timeSignificance(ns):
    int_list = []
    miss = 31
    for i in range(1, ns + 1):
        int_list.append(2)
        int_list.append(miss)
    return int_list

def windGustDirection(ns):
    float_list = []
    miss = CODES_MISSING_LONG
    for i in range(1, ns + 1):
        float_list.append(miss)
        float_list.append(miss)
    return float_list

def windGustSpeed(list1, list2):
    float_list = []
    for i in range(1, len(list1) + 1):
        float_list.append(list1[i-1])       # WG_10MIN
        float_list.append(list2[i-1])       # WG_1H_MAX
    return float_list

def str2int(str_list, x):
    int_list = []
    miss = CODES_MISSING_LONG
    for i in range (0, len(str_list)):
        if (str_list[i] == '-1e+100'):
            if (x == 23):
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
                float_list.append(0)
            else:
                float_list.append(float(str_list[i]))
        elif (x >= 41 and x <= 43):
            if (float(str_list[i]) == 0):
                float_list.append(-0.01)
                    # ei oo ihan varma tasta
            else:
                float_list.append(float(str_list[i]) * 0.010)   # cm -> m
        elif (x >= 45 and x <= 51):
            float_list.append(float(str_list[i]) + 273.15)  # C -> K 
        else:
            float_list.append(float(str_list[i]))
    return float_list