"""
This module makes subset objects by different functions and Subset class.
"""
import sys
from eccodes import CODES_MISSING_LONG as miss
from eccodes import CODES_MISSING_DOUBLE as missD

class Subset:
    """
    This class makes keyname objects with key names that are mostly used in synop
    data. All the values with same keyname are placed into the same object as an array.
    The values are modified in different functions according to Codes manual.
        1. At first Subset class makes all the values, which are not dependent
        on any other objects to be missing. Only the number of subsets (NSUB) is given.
        2. The values are read form v_a, and value is placed in keyname object acording
        keyname's index position. Values that don't depend on any other are given first.
        As an exception, block number and sation number are given acording to WMO:
            A 5-digit number yyxxx: the first 2 digits (yy) are called a block number
            (for example, 02 is for Finland and Sweden), the last 3 digits (xxx) are
            called a station number, which tells the id of the station.
        3. After that, values that depend on N_CALC are set to missing.
        4. Values that depend only on N_CALC (cloud cover total) are given.
        5. The rest of all the needed values are given.
        6. Functions which gives the right values to bufr message, are placed below.
    """
    # 1.
    def __init__(self, key_array, value_array):
        k_a = key_array
        v_a = value_array
        self.NSUB = len(v_a[0])
        miss_list = []
        miss_char_list = []
        for i in range(0, self.NSUB):
            miss_list.append('-1e+100')
            miss_char_list.append('')
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
        self.WSI_IDS = str2int(miss_list, 0)
        self.WSI_IDI = str2int(miss_list, 0)
        self.WSI_INR = str2int(miss_list, 0)
        self.WSI_LID = miss_char_list
        self.BLOCK_NUMBER = str2int(self.WMON, 64)
        self.STATION_NUMBER = str2int(self.WMON, 65)
        self.N_CALC = str2int(miss_list, 29)
        self.HH_CALC = str2float(miss_list, 25)
        self.CLHB2 = str2float(miss_list, 16)
        self.CLHB3 = str2float(miss_list, 17)
        self.CLHB4 = str2float(miss_list, 18)
        self.CLHB5 = str2float(miss_list, 19)
        self.CLHB = [self.HH_CALC, self.CLHB2, self.CLHB3, self.CLHB4, self.CLHB5]
        self.DD = str2int(miss_list, 21)
        self.GLOB = str2float(miss_list, 43)
        self.GROUND = miss_list
        self.GROUND06 = str2int(miss_list, 23)
        self.HH24 = str2int(miss_list, 24)
        self.MI = str2int(miss_list, 26)
        self.MM = str2int(miss_list, 27)
        self.OBSTIME = miss_list
        self.P_A = str2int(miss_list, 31)
        self.P_PPP = str2float(miss_list, 34)
        self.P_SEA = str2float(miss_list, 34)
        self.P_ST = str2float(miss_list, 34)
        self.RH = str2int(miss_list, 35)
        self.R_12H_AWS = str2float(miss_list, 40)
        self.R_12H_MAN = str2float(miss_list, 40)
        self.R_1H_AWS = str2float(miss_list, 40)
        self.R_1H_MAN = str2float(miss_list, 40)
        self.R_H = [self.R_1H_AWS, self.R_1H_MAN, self.R_12H_AWS, self.R_12H_MAN]
        self.R_24H = str2float(miss_list, 40)
        self.SNOW06 = str2float(miss_list, 41)
        self.SNOW18 = str2float(miss_list, 41)
        self.SNOW_AWS = str2float(miss_list, 41)
        self.SNOW = [self.SNOW06, self.SNOW18, self.SNOW_AWS]
        self.SUND = str2int(miss_list, 42)
        self.SYNOP = miss_list
        self.T = str2float(miss_list, 50)
        self.TD = str2float(miss_list, 50)
        self.TGMIN06 = str2float(miss_list, 50)
        self.TMAX06 = str2float(miss_list, 50)
        self.TMAX18 = str2float(miss_list, 50)
        self.TMIN06 = str2float(miss_list, 50)
        self.TMIN18 = str2float(miss_list, 50)
        self.VALUE_COUNT = miss_list
        self.VIS = str2int(miss_list, 53)
        self.W1_CALC = str2int(miss_list, 54)
        self.W1_AWS = str2int(miss_list, 54)
        self.W2_CALC = str2int(miss_list, 55)
        self.W2_AWS = str2int(miss_list, 55)
        self.WD_10MIN = str2float(miss_list, 56)
        self.WG_10MIN = str2float(miss_list, 57)
        self.WG_1H_MAX = str2float(miss_list, 58)
        self.WS_10MIN = str2float(miss_list, 59)
        self.WS_MAX_3H = miss_list
        self.WS_MAX_3H_T = miss_list
        self.WW_CALC = str2int(miss_list, 62)
        self.WW_AWS = str2int(miss_list, 62)
        self.YYYY = str2int(miss_list, 63)

    # 2.
        for key in k_a:
            if key == 'TTAAII':
                self.TTAAII = v_a[k_a.index(key)]
            elif key == 'ELANEM':
                self.ELANEM = str2float(v_a[k_a.index(key)], 1)
            elif key == 'ELBARO':
                self.ELBARO = str2float(v_a[k_a.index(key)], 2)
            elif key == 'ELSTAT':
                self.ELSTAT = str2float(v_a[k_a.index(key)], 3)
            elif key == 'ELTERM':
                self.ELTERM = str2float(v_a[k_a.index(key)], 4)
            elif key == 'LAT':
                self.LAT = str2float(v_a[k_a.index(key)], 5)
            elif key == 'LON':
                self.LON = str2float(v_a[k_a.index(key)], 6)
            elif key == 'STATION_NAME':
                self.STATION_NAME = v_a[k_a.index(key)]
            elif key == 'STATION_TYPE':
                self.STATION_TYPE = str2int(v_a[k_a.index(key)], 8)
            elif key == 'WMON':
                self.WMON = v_a[k_a.index(key)]
                self.BLOCK_NUMBER = str2int(self.WMON, 64)
                self.STATION_NUMBER = str2int(self.WMON, 65)
            elif key == 'WSI':
                self.WSI_IDS = get_wigos(v_a[k_a.index(key)], 0)
                self.WSI_IDI = get_wigos(v_a[k_a.index(key)], 1)
                self.WSI_INR = get_wigos(v_a[k_a.index(key)], 2)
                self.WSI_LID = get_wigos(v_a[k_a.index(key)], 3)
            elif key =='N_CALC':
                self.N_CALC = str2int(v_a[k_a.index(key)], 29)
            elif key == 'HH_CALC':
                self.HH_CALC = str2float(v_a[k_a.index(key)], 25)
                self.CLHB[0] = self.HH_CALC
            elif key == 'CLHB2':
                self.CLHB2 = str2float(v_a[k_a.index(key)], 16)
                self.CLHB[1] = self.CLHB2
            elif key == 'CLHB3':
                self.CLHB3 = str2float(v_a[k_a.index(key)], 17)
                self.CLHB[2] = self.CLHB3
            elif key == 'CLHB4':
                self.CLHB4 = str2float(v_a[k_a.index(key)], 18)
                self.CLHB[3] = self.CLHB4
            elif key == 'CLHB5':
                self.CLHB5 = str2float(v_a[k_a.index(key)], 19)
                self.CLHB[4] = self.CLHB5
            elif key == 'DD':
                self.DD = str2int(v_a[k_a.index(key)], 21)
            elif key == 'GLOB':
                self.GLOB = str2float(v_a[k_a.index(key)], 43)
            elif key == 'GROUND':
                self.GROUND = str2int(v_a[k_a.index(key)], 22)
            elif key == 'GROUND06':
                self.GROUND06 = str2int(v_a[k_a.index(key)], 23)
            elif key == 'HH24':
                self.HH24 = str2int(v_a[k_a.index(key)], 24)
            elif key == 'MI':
                self.MI = str2int(v_a[k_a.index(key)], 26)
            elif key == 'MM':
                self.MM = str2int(v_a[k_a.index(key)], 27)
            elif key == 'OBSTIME':
                self.OBSTIME = v_a[k_a.index(key)]
            elif key == 'P_A':
                self.P_A = str2int(v_a[k_a.index(key)], 31)
            elif key == 'P_PPP':
                self.P_PPP = str2float(v_a[k_a.index(key)], 34)
            elif key == 'P_SEA':
                self.P_SEA = str2float(v_a[k_a.index(key)], 34)
            elif key == 'P_ST':
                self.P_ST = str2float(v_a[k_a.index(key)], 34)
            elif key == 'RH':
                self.RH = str2int(v_a[k_a.index(key)], 35)
            elif key == 'R_12H_AWS':
                self.R_12H_AWS = str2float(v_a[k_a.index(key)], 40)
                self.R_H[2] = self.R_12H_AWS
            elif key == 'R_12H_MAN':
                self.R_12H_MAN = str2float(v_a[k_a.index(key)], 40)
                self.R_H[3] = self.R_12H_MAN
            elif key == 'R_1H_AWS':
                self.R_1H_AWS = str2float(v_a[k_a.index(key)], 40)
                self.R_H[0] = self.R_1H_AWS
            elif key == 'R_1H_MAN':
                self.R_1H_MAN = str2float(v_a[k_a.index(key)], 40)
                self.R_H[1] = self.R_1H_MAN
            elif key == 'R_24H':
                self.R_24H = str2float(v_a[k_a.index(key)], 40)
            elif key == 'SNOW06':
                self.SNOW06 = str2float(v_a[k_a.index(key)], 41)
                self.SNOW[0] = self.SNOW06
            elif key == 'SNOW18':
                self.SNOW18 = str2float(v_a[k_a.index(key)], 41)
                self.SNOW[1] = self.SNOW18
            elif key == 'SNOW_AWS':
                self.SNOW_AWS = str2float(v_a[k_a.index(key)], 41)
                self.SNOW[2] = self.SNOW_AWS
            elif key == 'SUND':
                self.SUND = str2int(str2float(v_a[k_a.index(key)], 42), 42)
            elif key == 'SYNOP':
                self.SYNOP = v_a[k_a.index(key)]
            elif key == 'T':
                self.T = str2float(v_a[k_a.index(key)], 50)
            elif key == 'TD':
                self.TD = str2float(v_a[k_a.index(key)], 50)
            elif key == 'TGMIN06':
                self.TGMIN06 = str2float(v_a[k_a.index(key)], 50)
            elif key == 'TMAX06':
                self.TMAX06 = str2float(v_a[k_a.index(key)], 50)
            elif key == 'TMAX18':
                self.TMAX18 = str2float(v_a[k_a.index(key)], 50)
            elif key == 'TMIN06':
                self.TMIN06 = str2float(v_a[k_a.index(key)], 50)
            elif key == 'TMIN18':
                self.TMIN18 = str2float(v_a[k_a.index(key)], 50)
            elif key == 'VALUE_COUNT':
                self.VALUE_COUNT = v_a[k_a.index(key)]
            elif key == 'VIS':
                self.VIS = str2int(v_a[k_a.index(key)], 53)
            elif key == 'W1_CALC':
                self.W1_CALC = str2int(v_a[k_a.index(key)], 54)
            elif key == 'W1_AWS':
                self.W1_AWS = str2int(v_a[k_a.index(key)], 54)
            elif key == 'W2_CALC':
                self.W2_CALC = str2int(v_a[k_a.index(key)], 55)
            elif key == 'W2_AWS':
                self.W2_AWS = str2int(v_a[k_a.index(key)], 55)
            elif key == 'WD_10MIN':
                self.WD_10MIN = str2float(v_a[k_a.index(key)], 56)
            elif key == 'WG_10MIN':
                self.WG_10MIN = str2float(v_a[k_a.index(key)], 57)
            elif key == 'WG_1H_MAX':
                self.WG_1H_MAX = str2float(v_a[k_a.index(key)], 58)
            elif key == 'WS_10MIN':
                self.WS_10MIN = str2float(v_a[k_a.index(key)], 59)
            elif key == 'WS_MAX_3H':
                self.WS_MAX_3H = v_a[k_a.index(key)]
            elif key == 'WS_MAX_3H_T':
                self.WS_MAX_3H_T = v_a[k_a.index(key)]
            elif key == 'WW_CALC':
                self.WW_CALC = str2int(v_a[k_a.index(key)], 62)
            elif key == 'WW_AWS':
                self.WW_AWS = str2int(v_a[k_a.index(key)], 62)
            elif key == 'YYYY':
                self.YYYY = str2int(v_a[k_a.index(key)], 63)

    # 3.
        self.NH_CALC = str2int_cloud_amount(self.N_CALC, miss_list, 28)
        self.CH = cloud_type(self.N_CALC, miss_list, 10)
        self.CL = cloud_type(self.N_CALC, miss_list, 30)
        self.CM = cloud_type(self.N_CALC, miss_list, 20)
        self.CLA = [miss_list, miss_list, miss_list, miss_list]

    # 4.
        for key in k_a:
            if key == 'NH_CALC':
                self.NH_CALC = str2int_cloud_amount(self.N_CALC, v_a[k_a.index(key)], 28)
            elif key == 'CH':
                self.CH = cloud_type(self.N_CALC, v_a[k_a.index(key)], 10)
            elif key == 'CL':
                self.CL = cloud_type(self.N_CALC, v_a[k_a.index(key)], 30)
            elif key == 'CM':
                self.CM = cloud_type(self.N_CALC, v_a[k_a.index(key)], 20)
            elif key == 'CLA2':
                self.CLA2 = str2int_cloud_amount(self.N_CALC, v_a[k_a.index(key)], 12)
                self.CLA[0] = self.CLA2
            elif key == 'CLA3':
                self.CLA3 = str2int_cloud_amount(self.N_CALC, v_a[k_a.index(key)], 13)
                self.CLA[1] = self.CLA3
            elif key == 'CLA4':
                self.CLA4 = str2int_cloud_amount(self.N_CALC, v_a[k_a.index(key)], 14)
                self.CLA[2] = self.CLA4
            elif key == 'CLA5':
                self.CLA5 = str2int_cloud_amount(self.N_CALC, v_a[k_a.index(key)], 15)
                self.CLA[3] = self.CLA5

    # 5.
        self.VS = vertical_significance(self.N_CALC, self.NH_CALC, self.CL, self.CM)
        self.NR1 = number_of_repetition1(self.CLA)
        self.NR2 = number_of_repetition2(self.NSUB)
        self.GLOB = global_radiation(self.GLOB, self.NSUB)
        self.SUND = sunshine(self.SUND, self.NSUB)
        self.DEL = replication(self.NSUB, self.NR1, self.NR2)
        self.CLOUD_TYPE = cloud_type_total(self.DEL, self.CL, self.CM, self.CH)
        self.CLA_TOTAL = cloud_amount(self.NR2, self.NH_CALC, self.CLA)
        self.HB = height_of_base(self.N_CALC, self.NR1, self.CLA, self.CLHB)
        self.VS_TOTAL = vertical_significance_total(1, self.DEL, self.VS, self.CLA)
        self.PRECIPITATION = precipitation_total(self.STATION_TYPE, self.R_H)
        self.TPP = precipitation_time_period(self.PRECIPITATION)
        self.R_24H_TOTAL = r24h_total(self.HH24, self.R_24H)
        self.GR = ground_data(k_a, self.HH24, self.GROUND, self.GROUND06)
        self.SNOW_TOTAL = snow_depth_total(self.HH24, k_a, self.GR, self.SNOW)
        self.TMAX = temperature(self.HH24, self.TMAX06, self.TMAX18)
        self.TMIN = temperature(self.HH24, self.TMIN06, self.TMIN18)
        self.SENSOR = height_of_sensor(self.ELANEM, self.ELTERM, self.TMAX, self.TMIN)
        self.INSTRUMENT = instrument_type(self.NSUB)
        self.TIME_SIGNIFICANCE = time_significance(self.NSUB)
        self.TP = time_period(self.HH24, self.W1_CALC, self.SUND,
                                self.TPP, self.TMAX, self.TMIN, self.GLOB)
        self.WW = weather(self.STATION_TYPE, 'WW_AWS', k_a, self.WW_CALC, self.WW_AWS)
        self.W1 = weather(self.STATION_TYPE, 'W1_AWS', k_a, self.W1_CALC, self.W1_AWS)
        self.W2 = weather(self.STATION_TYPE, 'W2_AWS', k_a, self.W2_CALC, self.W2_AWS)
        self.WGD_MAX = wind_gust_direction(self.NSUB)
        self.WGS_MAX = wind_gust_speed(self.WG_10MIN, self.WG_1H_MAX)

# 6.

def get_wigos(wigos_id, key_id):
    """
    This function splits WIGOS identifier (wigos_id)from "-" to get a wigos_array with:
        wigos_array[0] = WIGOS identifier series = WSI_IDS  (value between 0-14)
        wigos_array[1] = WIGOS issuer of identifier = WSI_IDI
            Value between 1 and 9 999 when no WMO number.
            Value between 10 000 and 99 999 otherwise.
        wigos_array[2] = WIGOS issue number = WSI_INR
        wigos_array[3] = WIGOS local identifier (character) = WSI_LID
            NSI number is used if WMO number is missing provided.
    https://wiki.fmi.fi/pages/viewpage.action?pageId=107195152
    """
    wigos_term = []
    for i in range(0, len(wigos_id)):
        if wigos_id[i] != '-1e+100':
            wigos_array = wigos_id[i].split('-')

            if len(wigos_array)!= 4:
                print('WIGOS identifier is wrongly written!\n')
                sys.exit(1)
            try:
                wigos_array[0] = int(wigos_array[0])
                wigos_array[1] = int(wigos_array[1])
                wigos_array[2] = int(wigos_array[2])
                if wigos_array[0] not in range(0, 15):
                    print('WIGOS identifier series number should be in range (0, 14).\n')
                    sys.exit(1)
                elif wigos_array[1] not in range(1, 100000):
                    print('WIGOS issuer of identifier number should be in range (1, 99 999).\n')
                    sys.exit(1)
                elif wigos_array[2] not in range(0, 100000):
                    print('WIGOS issue number should be in range (0, 99 999.\n')
                    sys.exit(1)
                elif len(wigos_array[3])> 16:
                    print('WIGOS local identifier should be 16 characters max.\n')
                    sys.exit(1)
                wigos_term.append(wigos_array[key_id])
            except ValueError:
                print('WIGOS identifier series, WIGOS issuer of identifier')
                print('and WIGOS issuer number should be positive integers.\n')
                sys.exit(1)
        else:
            wigos_array = [miss, miss, miss, '']
            wigos_term.append(wigos_array[key_id])

    return wigos_term

def vertical_significance(n_list, nh_list, cl_list, cm_list):
    """
    This function calculates vertical significance for sequence 302004. It depends on:
        n_list = N_CALC = cloud cover total
        nh_list = NH_CALC = cloud amount
        cl_list = CL = cloud type (low clouds)
        cm_list = CM = cloud type (middle clouds)
    """
    int_list = []
    for i in range (0, len(n_list)):
        if n_list[i] == miss:
            int_list.append(miss)
        elif n_list[i] == 0:
            int_list.append(62)
        elif n_list[i] == 113:
            int_list.append(5)
        elif cl_list[i] > 0:
            int_list.append(7)
        elif cl_list[i] == 0 and cm_list[i] > 0:
            int_list.append(8)
        elif nh_list[i] == 0 and n_list != 0:
            int_list.append(0)
        else:
            int_list.append(miss)
    return int_list

def vertical_significance_total(aws, del_list, vs_list , cla_list):
    """
    This function makes a total list of vertical significance in 307080:
        302004: j = 0, values are made in function vertical_significance = vs_list.
        302005: j > 0 and j <= nr1, depends on:
            del_list = DEL = delayed replicatoin, which includes
            nr1 = NR1 = number of repetitions of sequance 302005.
            aws = automatic station (=1) or manual station (=0)
            cla_list = [CLA2, CLA3, CLA4, CLA5] = cloud amount list in different layers.
        302036: nr1 < j <= nr2 depends on:
            del_list = DEL = delayed replicatoin, which includes
            nr2 = NR2 = number of repetitions of sequance 302036.
        302047: j > nr2, required from land stations mainly in the tropics.
        8002: j > nr2 + 1, Set to missing to cancel the previous value.
    """
    int_list = []
    list2 = cla_list[0]
    list3 = cla_list[1]
    list4 = cla_list[2]
    list5 = cla_list[3]
    k = 0
    for i in range (0, len(vs_list)):
        nr1 = del_list[k]
        nr2 = del_list[k+1]
        for j in range(0, 5 + nr1 + nr2):
            if j == 0:
                int_list.append(vs_list[i])
            elif 0 < j <= nr1:
                if aws == 0:
                    int_list.append(j)
                else:
                    if nr1 == 1 and list2[i] == miss:
                        int_list.append(miss)
                    elif nr1 == 2 and list3[i] == miss:
                        int_list.append(miss)
                    elif nr1 == 3 and list4[i] == miss:
                        int_list.append(miss)
                    elif nr1 == 4 and list5[i] == miss:
                        int_list.append(miss)
                    else:
                        int_list.append(20 + j)
            else:
                int_list.append(miss)
        k = k + 2
    return int_list

def cloud_amount(nr2_list, list1, cla_list):
    """
    This funtion makes a total list of cloud amount:
        302004: j = 0. Depends on list1 = NH_CALC = cloud amount.
        302005: j = 1, 2, 3, 4. Depends on:
            cla_list = [CLA2, CLA3, CLA4, CLA5] = cloud amount list in different layers.
        302036: j > 5. Number of cloud amount depends on the
            nr2_list = NR2 = number of repetitions of sequance 302036.
    """
    int_list = []
    list2 = cla_list[0]
    list3 = cla_list[1]
    list4 = cla_list[2]
    list5 = cla_list[3]
    for i in range (0, len(list1)):
        for j in range (0, 5 + nr2_list[i]):
            if j == 0:
                int_list.append(list1[i])
            elif j == 1:
                value = list2[i]
                if list2[i] == 0:
                    value = miss
                int_list.append(value)
            elif j == 2 and list3[i] != miss:
                value = list3[i]
                if list3[i] == 0:
                    value = miss
                int_list.append(value)
            elif j == 3 and list4[i] != miss:
                value = list4[i]
                if list4[i] == 0:
                    value = miss
                int_list.append(value)
            elif j == 4 and list5[i] != miss:
                value = list5[i]
                if list5[i] == 0:
                    value = miss
                int_list.append(value)
            elif j > 5:
                int_list.append(miss)
    return int_list

def value_for_cloud_type(c_id, cloud_value ):
    """
    This function gets right value for cloud type. c_id is the cloud type id:
        for CL c_id = 30
        for CM c_id = 20
        for CH c_id = 10
    cloud_value is either the data value of cloud type (string) or value of cloud cover (integer).
    """
    value = int(cloud_value ) + c_id
    if cloud_value  == 113:
        if c_id == 30:
            value = 62
        elif c_id == 20:
            value = 61
        elif c_id == 10:
            value = 60
    elif int(cloud_value ) == 10:
        value = 63
    return value

def cloud_type(n_list, str_list, x):
    """
    This function calculates cloud type 20012 for sequence 302004. It depends on:
        n_list = N_CALC = cloud cover total
        str_list = values of cloud type
        x = id of cloud type
    """
    int_list = []
    for i in range (0, len(str_list)):
        if n_list[i] == 113:
            int_list.append(value_for_cloud_type(x, n_list[i]))
        elif str_list[i] == '-1e+100' or n_list[i] == miss:
            int_list.append(miss)
        else:
            int_list.append(value_for_cloud_type(x, str_list[i]))
    return int_list

def cloud_type_total(del_list, cl_list, cm_list, ch_list):
    """
    This function makes the whole list of cloud types:
    302004: j = 0, 1, 2. Depends on:
        cl_list = CL = cloud type (low cloud)
        cm_list = CM = cloud type (middle cloud)
        ch_list = CH = cloud type (high cloud)
    302005: j > 2. Depends on:
        del_list = DEL = delayed replicatoin, which includes
        nr1 = NR1 = number of repetitions of sequance 302005.
    302036: j > 2. Number of cloud types depends on the
        del_list = DEL = delayed replicatoin, which includes
        nr2 = NR2 = number of repetitions of sequance 302036.
    302048: given if value of cloud type is given for cloud elevation
    """
    int_list = []
    m = 0
    for i in range(0, len(cl_list)):
        nr1 = del_list[m]
        nr2 = del_list[m+1]
        k = 4 + nr1 + nr2
        for j in range(0, k):
            if j == 0:
                int_list.append(cl_list[i])
            elif j == 1:
                int_list.append(cm_list[i])
            elif j == 2:
                int_list.append(ch_list[i])
            else:
                int_list.append(63)
        m = m + 2
    return int_list

def number_of_repetition1(cla_list):
    """
    Number of repetition in sequance 302005. Depends on:
        cla_list = [CLA2, CLA3, CLA4, CLA5] = cloud amount list in different layers.
    """
    list2 = cla_list[0]
    list3 = cla_list[1]
    list4 = cla_list[2]
    list5 = cla_list[3]
    int_list = []
    for i in range(0, len(list2)):
        int_list.append(1)

    for i in range (0, len(list2)):
        if list5[i] == miss or list5[i] == 0:
            if list4[i] == miss or list4[i] == 0:
                if list3[i] == miss or list3[i] == 0:
                    int_list[i] = 1
                else:
                    int_list[i] = 2
            else:
                int_list[i] = 3
        else:
            int_list[i] = 4
    return int_list

def str2int_cloud_amount(n_list, str_list, x):
    """
    Function converts cloud amount data from string to integer.
        302004: x = 28, the integer value depends on:
            n_list = N_CALC = cloud cover total
            str_list = values in data
        302005: 12 <= x <= 15, the integer value depends on:
            str_list = values in data
        302036: depends on values in data (there is none)
    """
    int_list = []
    for i in range (0, len(str_list)):
        if x == 12 and str_list[i] == '0':
            value = 0
        elif x == 12 and str_list[i] == '-1e+100':
            value = miss
        elif 13 <= x <= 15 and str_list[i] in ('0', '-1e+100'):
            value = miss
        elif x == 28 and n_list[i] == 0:
            value = 0
        elif x == 28 and n_list[i] == 113:
            value = 9
        elif x == 28 and str_list[i] == '-1e+100':
            value = miss
        elif x == 28 and n_list[i] == miss:
            value = miss
        else:
            value = int(str_list[i])
        int_list.append(value)
    return int_list

def value_for_height_of_base(h_value, c_value):
    """
    Funciton chooses value for height of base. Depends on:
        h_value = value of height of base
        c_value = value of cloud amount.
    """
    if c_value == miss:
        value = missD
    else:
        value = h_value
    return value

def height_of_base(n_list, nr1_list, cla_list, hb_list):
    """
    Function makes total list of height of base from.
        302004: j = 0. Depends on:
            n_list = N_CALC = cloud cover total
            hb_list[0] = HB[0] = NH_CALC ) height of base data.
        302005: j >= 1. Depends on:
            nr1_list = NR1 = number of repetition of sequence 302005.
            cla_list = [CLA2, CLA3, CLA4, CLA5] = cloud amount list in
                different layers.
            rest of hb_list = [CLHB2, CLHB3, CLHB4, CLHB5] = height of base
                of cloud layers.
    """
    float_list = []
    for i in range (0, len(nr1_list)):
        d = nr1_list[i] + 1
        for j in range (0, d):
            h_list = hb_list[j]
            if j == 0:
                if n_list[i] in (miss, 0):
                    float_list.append(missD)
                else:
                    float_list.append(h_list[i])
            else:
                c_list = cla_list[j-1]
                if j == 1:
                    float_list.append(value_for_height_of_base(h_list[i], c_list[i]))
                elif j == 2:
                    float_list.append(value_for_height_of_base(h_list[i], c_list[i]))
                elif j == 3:
                    float_list.append(value_for_height_of_base(h_list[i], c_list[i]))
                else:
                    float_list.append(value_for_height_of_base(h_list[i], c_list[i]))
    return float_list

def height_of_sensor(elanem_list, elterm_list, tmax_list, tmin_list):
    """
    This function makes a list of all the sensor heights:
        302035: 302032: for temperature and humidity measurement j = 0, depends on:
            elterm_list = ELTERM = height of sensor (temperature and humidity)
        302035: 302033: for visibility measurement j = 1
        302035: 302034: for precipitation measurement j = 2
        302035: j = 3
        302043: 302040: for precipitation measurement j = 4
        302043: 302041: for temperature measurement j = 5, depends on:
            tmax_list = TMAX = maximum temperature
            tmin_list = TMIN = minimum temperature
            elterm_list = ELTERM = height of sensor (temperature and humidity)
        302043: 302042: for wind measurement j = 6, depends on:
            elanem_list = ELANEM
        302043: j = 7
    """
    float_list = []
    for i in range(0, len(elanem_list)):
        tmax = tmax_list[i]
        tmin = tmin_list[i]
        for j in range(0, 8):
            if j == 0:
                float_list.append(elterm_list[i])
            elif j == 5:
                if missD in (tmax, tmin):
                    float_list.append(missD)
                else:
                    float_list.append(elterm_list[i])
            elif j == 6:
                float_list.append(elanem_list[i])
            else:
                float_list.append(missD)
    return float_list

def r24h_total(hh_list, r24h_list):
    """
    This function makes a total list of precipitation past 24 hours. It depends on:
        hh_list = HH24 = hour of the measurement
        r24h_list = R_24H = total precipitation values in data.
    """
    float_list = []
    for i in range(0, len(r24h_list)):
        if hh_list[i] == 5:
            float_list.append(r24h_list[i])
        else:
            float_list.append(missD)
    return float_list

def ground_data(key_list, hh_list, list1, list2):
    """
    This function chooses ground data from GROUND06 and GROUND, and modifies it.
        If key_list includes key "GROUND06" and hh_list = HH24 is 6, the values of
        GROUND06 (list2) are used. If not, then values of GROUND (list1) are used.
    """
    g = [1, 2, 4, 11, 11, 12, 13, 16, 17]
    int_list = []
    for i in range (0, len(hh_list)):
        if hh_list[i] == 6 and 'GROUND06' in key_list:
            ind = list2[i]
            if 1 <= ind <= 9:
                int_list.append(g[ind-1])
            else:
                int_list.append(ind)
        else:
            ind = list1[i]
            if 1 <= ind <= 9:
                int_list.append(g[ind-1])
            else:
                int_list.append(ind)
    return int_list

def snow_depth(snow_value, gr_value):
    """
    This function chooses a right value of snow depth. It depends on:
        snow_value = snow depth in data
        gr_value = ground value in data
    """
    value = snow_value
    if snow_value == 0:
        value = -0.01
        if gr_value in (11, 12):
            value = -0.02
    elif snow_value == -0.01:
        value = 0.0
    return value

def snow_depth_total(hh_list, key_list, gr_list, snow_list):
    """
    This function makes a total list of snow depth. It depends on:
        hh_list = HH24 = hour of the measurement
        key_list, if it includes values SNOW06 or SNOW18
        gr_list = GR = ground data
        snow_list = SNOW = [SNOW06, SNOW18, SNOW_AWS] = values of snow depth.
    """
    float_list = []
    snow06_list = snow_list[0]
    snow18_list = snow_list[1]
    snow_aws_list = snow_list[2]
    for i in range(0, len(hh_list)):
        if 'SNOW06' in key_list and hh_list[i] == 5:
            float_list.append(snow_depth(snow06_list[i], gr_list[i]))
        elif 'SNOW18' in key_list and hh_list[i] == 17:
            float_list.append(snow_depth(snow18_list[i], gr_list[i]))
        else:
            float_list.append(snow_depth(snow_aws_list[i], gr_list[i]))
    return float_list

def replication(ns, nr1_list, nr2_list):
    """
    Functions combines the 2 replications, which are used to make
    the array for delaid replication. It depends on:
        ns = NSUB = number of subsets
        nr1_list = NR1 = number of replication in sequence 302005
        nr2_list = NR2 = number of replication in sequence 302036
    """
    int_list = []
    for i in range(0, ns):
        int_list.append(nr1_list[i])
        int_list.append(nr2_list[i])
    return int_list

def precipitation_total(st_list, r_h_list):
    """
    Function makes a total list of precipitation 13011: It depends on:
        st_list = STATION_TYPE = tells if the station is automatic of not.
        r_h_list = [R_1H_AWS, R_1H_MAN, R_12H_AWS, R_12H_MAN]
            r12hm_list = R_12H_MAN = Precipitation past 12 hours in manual station
            r1hm_list = R_1H_MAN = Precipitation past 1 hour in manual station
            r12ha_list = R_12H_AWS = Precipitation past 12 hours in automatic station
            r1ha_list = R_1H_AWS = Precipitation past 1 hour in automatic station
    """
    float_list = []
    r1ha_list = r_h_list[0]
    r1hm_list = r_h_list[1]
    r12ha_list = r_h_list[2]
    r12hm_list = r_h_list[3]
    for i in range (0, len(st_list)):
        if st_list[i] == 0:
            float_list.append(r12ha_list[i])
            float_list.append(r1ha_list[i])
        else:
            float_list.append(r12hm_list[i])
            float_list.append(r1hm_list[i])
    return float_list

def temperature(hh_list, t1_list, t2_list):
    """
    This function is used to choose right values for temperature. It depends on:
        hh_list = HH24 = hour of measurement
        t1_list = TMAX06 or TMIN06
        t2_list = TMAX18 or TMIN18
    """
    float_list = []
    for i in range (0, len(t1_list)):
        if hh_list[i] == 6:
            float_list.append(t1_list[i])
        elif hh_list[i] == 18:
            float_list.append(t2_list[i])
        else:
            float_list.append(missD)
    return float_list

def number_of_repetition2(ns):
    """
    This function gives delaid repetition for 302036.
    """
    int_list = []
    i = 0
    while i < ns:
        int_list.append(0)
        i = i + 1
    return int_list

def sunshine(ss_list, ns):
    """
    This function chances sunshine data from hour units to minutes.
    The first replication is from last 1 hour period,
    and the second replication is from the last 24 hour period.
    """
    sund_list = []
    i = 0
    while i < ns:
        if ss_list[i] == miss:
            sund_list.append(miss)
        elif ss_list[i] >= 0 and ss_list[i] < 2048:
            sund_list.append(ss_list[i])
        else:
            sund_list.append(miss)
            print("Wrong SUND value: " + str(ss_list[i]) + " (min=0, max=2047)")
        sund_list.append(miss)
        i = i + 1
    return sund_list

def global_radiation(float_list, ns):
    """
    This function chances global radiation units from kJ/m² -> J/m².
    The first replication is from last 1 hour period,
    and the second replication is from the last 24 hour period.

    """
    glob_list = []
    i = 0
    while i < ns:
        if float_list[i] == missD:
            glob_list.append(missD)
        else:
            if float_list[i] >= 0.0 and float_list[i] < 1.04858e+05:
                glob_list.append(float_list[i] * 1000.0)
            else:
                glob_list.append(missD)
                print("Wrong GLOB value: " + str(float_list[i]) + " (min=0, max=1.04858e+08)")
        glob_list.append(missD)
        i = i + 1
    return glob_list

def precipitation_time_period(precipitation_list):
    """
    This function gives time period values for precipitation. It depends on:
        precipitation_list = PRECIPITATION = total list of precipitation.
    """
    int_list = []
    for i in range (0, len(precipitation_list)):
        if precipitation_list[i] == missD:
            int_list.append(miss)
        elif i % 2:
            int_list.append(-1)
        else:
            int_list.append(-12)
    return int_list

def past_weather_time_period(w1, hh):
    """
    This function retuns time period in sequance 302038. It depends on:
        w1 = W1 = past weather 1
        hh = HH24 = hour of measusrement
    """
    value = miss
    h = [0, 5, 6, 11, 12, 17, 18, 23]
    if w1 != 31:
        if hh in h:
            value = -6
        else:
            value = -3
    return value

def temperature_time_period(t_id, tmax, tmin):
    """
    This function gives time period values for sequance 302041. It depends on:
        t_id = id of time preriod
        tmax = value of maximum temperature
        tmin = value of minimum temperature
    """
    if t_id == 5 and tmax == missD:
        value = miss
    elif t_id == 7 and tmin == missD:
        value = miss
    elif t_id in (5, 7):
        value = -12
    elif t_id == 6 and tmax == missD:
        value = miss
    elif t_id == 8 and tmin == missD:
        value = miss
    elif t_id in (6, 8):
        value = 0
    else:
        value = miss
    return value

def time_period(hh_list, w1_list, sund_list, tp_list, tmax_list, tmin_list, glob_list):
    """
    This function gives all the time period values. It depends on:
        302038 [h] j = 0
            hh_list = HH24 = hour of measurement
            w1_list = W1_CALC = past weather 1
        302039 [h] j = 1 and 2
            sund_list = SUND = sunshine time [min]
            The first replication is from 1 hour period,
            and the second replication is form 24 hour period.
        302040 [h] j = 3 and 4
            tp_list = PRECIPITATION_TIME_PERIOD = time period for precipitation
        302041 [h] j = 5, 6, 7 and 8
            tmax_list = TMAX = maximum temperature
            tmin_list = TMIN = minimum temperature
        302042 [min] j = 9, 10 and 11
        302044 [h] j = 12
        302045 [h] j = 13 and 14
            glob_list = GLOB = global radiation [J/m²]
            The first replication is from 1 hour period,
            and the second replication is form 24 hour period.
        302046 [h] j = 15 and 16
    """
    int_list = []
    t = 0
    s = 0
    g = 0
    for i in range (0, len(hh_list)):
        for j in range (0, 17):
            value = miss
            if j == 0:
                value = past_weather_time_period(w1_list[i], hh_list[i])
            elif j == 1:
                if sund_list[s] != miss:
                    value = -1
                s = s + 1
            elif j == 2:
                if sund_list[s] != miss:
                    value = -24
                s = s + 1
            elif j in (3, 4):
                value = tp_list[t]
                t = t + 1
            elif 5 <= j <= 8:
                value = temperature_time_period(j, tmax_list[i], tmin_list[i])
            elif j in (9, 10):
                value = -10
            elif j == 11:
                value = -60
            elif j == 13:
                if glob_list[g] != missD:
                    value = -1
                g = g + 1
            elif j == 14:
                if glob_list[g] != missD:
                    value = -24
                g = g + 1
            int_list.append(value)
    return int_list

def instrument_type(ns):
    """
    This function gives the total list of instrument types.
    The size of list depends on ns = NSUB = number of subsets.
    """
    float_list = []
    i = 0
    while i < ns:
        float_list.append(8.0)
        i = i + 1
    return float_list

def time_significance(ns):
    """
    This function gives the total list of time significance.
    The size of list depends on ns = NSUB = number of subsets.
    """
    int_list = []
    i = 0
    while i < ns:
        int_list.append(2)
        int_list.append(31)
        i = i + 1
    return int_list

def weather(st_list, name, key_list, man_list, aws_list):
    """
    Function chooses values for present and past weather. Values are chosen between
    manual (man_list) and automatic (aws_list) observations. It depends on:
        st_list = STATION_TYPE
        key_list, if key name (name) is in the data.
    """
    int_list = []
    for i in range (0, len(man_list)):
        if st_list[i] == 0:
            if name in key_list:
                int_list.append(aws_list[i])
            else:
                int_list.append(man_list[i])
        else:
            int_list.append(man_list[i])
    return int_list

def wind_gust_direction(ns):
    """
    This function gives the total list of direction of wind gust.
    The size of list depends on ns = NSUB = number of subsets.
    """
    float_list = []
    i = 0
    while i < ns:
        float_list.append(missD)
        float_list.append(missD)
        i = i + 1
    return float_list

def wind_gust_speed(list1, list2):
    """
    Function gives the total list of speed of wind gust. It depends on values in:
        list1 = WG_10MIN
        list2 = WG_1H_MAX
    """
    float_list = []
    for i in range(0, len(list1)):
        float_list.append(list1[i])
        float_list.append(list2[i])
    return float_list

def precipitation(str_value):
    """
    Function retuns value for precipitation. It depends on str_value = given data value.
    """
    value = str_value
    if str_value == '0':
        value = '-0.1'
    elif str_value == '-1':
        value = '0.0'
    return float(value)

def make_missing(k_id):
    """
    This function gives right missing values according to value's id (k_id)
    """
    value = miss
    if 22 <= k_id <= 23:
        value = 31
    elif k_id == 31:
        value = 15
    elif 54 <= k_id <= 55:
        value = 31
    elif k_id == 62:
        value = 511
    elif k_id == 64:
        value = 2
    elif k_id == 65:
        value = 761
    return value

def not_missing(str_value, k_id):
    """
    Function gives right values according to given value (str_value) and its id (k_id).
    """
    value = int(str_value)
    if k_id == 29:
        value = int(value*12.5 + 0.5)
    elif k_id == 53 and value > 81900:
        value = 81900
    elif k_id == 64:
        value = int(str_value[:2])
    elif k_id == 65:
        value = int(str_value[-3:])
    return value

def str2int(str_list, k_id):
    """
    This function makes a string list (str_list) to a integer list (int_list).
        k_id represents the id of different values. Values are converted from string to
        integer depending on k_id. Before this function, missing values = '/' are changed
        to be '-1e+100', which in eccodes is the missing value of float type value.
        It is changed to be missing value of integer type value.
    """
    int_list = []
    for i in range (0, len(str_list)):
        if str_list[i] == '-1e+100':
            int_list.append(make_missing(k_id))
        else:
            int_list.append(not_missing(str_list[i], k_id))
    return int_list

def str2float(str_list, k_id):
    """
    This function makes a string list (str_list) to a float list (float_list).
        k_id represents the id of different values. Values are converted from string to
        float depending on k_id. Before this function, missing values = '/' are changed
        to be '-1e+100' which in eccodes is the missing value of float type value.
    """
    float_list = []
    for i in range (0, len(str_list)):
        if str_list[i] == '-1e+100' and k_id != 42:
            float_list.append(float(str_list[i]))
        elif k_id == 4 and 1.5 <= float(str_list[i]) < 3.0:
            float_list.append(2.00)
        elif k_id == 34:
            float_list.append(float(str_list[i]) * 100)
        elif k_id == 40:
            float_list.append(precipitation(str_list[i]))
        elif k_id == 41:
            float_list.append(float(str_list[i]) * 0.010)
        elif k_id == 42:
            if str_list[i] == miss or str_list[i] == '-1e+100':
                float_list.append(miss)
            else:
                float_list.append(float(str_list[i]) * 60.0)
        elif k_id == 50:
            float_list.append(float(str_list[i]) + 273.15)
        else:
            float_list.append(float(str_list[i]))
    return float_list
