import panda as pd
import os
import time
import gps_data_read as gps

ret, gps_loc_data = gps.GPS_Read_Data_RMC()
gps_dist_present =None
path = os.getcwd()+"/gps_data_csv"
if (not os.path.exists(path)):
    os.makedirs(path)
try:
    os.chdir(path)
except NameError as e:
    print("Can not access path")
    exit()
i=0

while ret == True:
    try:
        ret, gps_loc_data.append(gps.GPS_Read_Data_RMC())
        gps_dist_present.append(gps.dist_calc_present(gps_loc_data[i][0],gps_loc_data[i][2]))
    except KeyboardInterrupt as e:
        data_set = list(zip(gps_loc_data,gps_dist_present))
        df = pd.DataFrame(data=data_set, columns=None)
        df.to_csv("gps_data_set.csv", index = False, header = False)