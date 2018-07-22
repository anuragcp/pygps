import serial
import math
gps = serial.Serial("/dev/ttyS0", 9600)
concatenate = lambda data, con_data : (data+con_data)
make_change = lambda data : float(data)/100
def GPS_Receive_Data_RMC():
    finish = 0
    position_count = 0
    comma_count = 0
    lat = ""
    lg = ""
    lat_dir = None
    lg_dir = None
    while finish is 0:
        gps_data = gps.read()
        flag = 1
        if (gps_data is '$' and position_count is 0):
            position_count = 1
        if (gps_data is "G" and position_count is 1):
            position_count=2
        if (gps_data is "P" and position_count is 2):
            position_count = 3
        if (gps_data is "R" and position_count is 3):
            position_count=4
        if (gps_data is "M" and position_count is 4):
            position_count = 5
        if (gps_data is "C" and position_count is 5):
            position_count = 6
        if (gps_data is "," and position_count is 6):
            comma_count += 1
        if (comma_count is 2 and flag is 1):
           if (gps_data is "V"):
              #print("status:Not connected")
              finish =1
           if (gps_data is "A"):
              #print("status:valid GPS fix")
              pass
        if (comma_count is 3 and flag is 1 and gps_data is not ","):
            lat = concatenate(lat, gps_data)
            flag = 0
        if (comma_count is 4 and flag is 1):
            lat_dir = gps_data
            flag = 0
        if (comma_count is 5 and flag is 1 and gps_data is not ","):
            lg = concatenate(lg, gps_data)
            flag = 0
        if (comma_count is 6 and flag is 1):
            lg_dir = gps_data
            flag = 0
        if (gps_data is "*" and comma_count>=5):
            flag = 0
            finish = 1
    return [round(make_change(lat),6), lat_dir, round(make_change(lg),6), lg_dir]
def dist_calc_present(dest_lat, dest_lg):
    current_lat, current_lg = GPS_Receive_Data_RMC()[0], GPS_Receive_Data_RMC()[2]
    theta1 = math.radians(current_lat)  #theta is lattitde
    theta2 = math.radians(dest_lat)
    delta_theta = math.radians(dest_lat - current_lat)
    delta_lambda = math.radians(dest_lg - current_lg)   #lambda is longitude
    a = (math.sin(delta_theta/2)*math.sin(delta_theta/2)) + (math.cos(theta1)*math.cos(theta2)*(math.sin(delta_lambda/2)*math.sin(delta_lambda/2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = (6371 * c)
    return distance
def dir_to_dest(dest_lat, dest_lg):    #data list is the output of GPS_Receive_Data_RMC
    """if(data_list[1] == "N"):
        dest_lat = (data_list[1])
    if(data_list[3] == "E"):
        dest_lg = (data_list[3])""" #it is not needed in india region the values as in N E direction which is +ve
    current_lat, current_lg = GPS_Receive_Data_RMC()[0], GPS_Receive_Data_RMC()[2]
    theta1 = math.radians(current_lat)
    theta2 = math.radians(dest_lat)
    delta_theta = math.radians(dest_lat - current_lat)
    delta_lambda = math.radians(dest_lg - current_lg)
    X = math.cos(theta2) * math.sin(delta_lambda)
    Y = math.cos(theta1) * math.sin(theta2) - (math.sin(theta1) * math.cos(theta2) * math.cos(delta_lambda))
    bearing_angle = math.atan2(X, Y)
    bearing_angle = math.degrees(bearing_angle)
    return bearing_angle
#while True:
# print(GPS_Receive_Data_RMC())
