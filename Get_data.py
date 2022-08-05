#Module: GetGCMsdata
#Author: Zhenngyang Li  <izzylzy@outlook.com>
#Last modified : 2022-08-04
#python3.7
import numpy as np
from pylab import *
import xarray as xr
from scipy import stats
import bisect
from math import sin,asin,cos,radians,fabs,sqrt
EARTH_RADIUS = 6371

def get_data(lon1:float,lat1:float,dst,var_name: str):
    ''' ----------Description----------
    This function tool is used to extract a single point of data from an NC file. This tool is especially useful if your research is site-based.
    Basic logic: Through the input latitude and longitude values, find the four grids close to the input site in the latitude and longitude table of NC file, 
                 calculate the spatial distance between the center points of the four grids and the input site, and use IDW algorithm to combine the data series of the four grids into one weighted.
    Notes: Please ensure that the latitude and longitude of the input site does not exist in the latitude and longitude table in the NC file, otherwise the denominator will be 0 when determining the weight.
    :param lon1: site's longitude
    :param lat1: site's latitude
    :param dst: .nc file
    :param var_name: variable name
    
    :return: The data sequence in the corresponding NC file at the site location
    '''
    va = var_name
 

    if 'lon' in dst:
        dlons = dst['lon'][:]
        dlats = dst['lat'][:]
    else:
        dlons = dst['longitude'][:]
        dlats = dst['latitude'][:]
    

    lon_station = lon1
    lat_station = lat1

    
    
    def fcindex(a,x):
        'Find the two values closest to the input value'
        i = bisect.bisect_left(a,x)#二分查找算法
        if i >= len(a):
            i = len(a) - 1
        elif i and a[i] - x > x - a[i - 1]:
            i = i - 1
        if a[i+1]-a[i] > a[i]-a[i-1]:
            return(i-1,a[i-1],i,a[i+1])
        else:
            return(i,a[i],i+1,a[i+1])
    
    'The following function is used to calculate the distance between points'
    def hav(theta):
        s = sin(theta/2)
        return s * s
    
    def get_distance_hav(lat0,lng0,lat1,lng1):
        #Convert latitude and longitude into radians
        lat0 = radians(lat0)
        lat1 = radians(lat1)
        lng0 = radians(lng0)
        lng1 = radians(lng1)
        dlng = fabs(lng0 - lng1)
        dlat = fabs(lat0 - lat1)
        h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
        distance = 2 * EARTH_RADIUS * asin(sqrt(h))             
        return distance
    
    #********IDW********#
    
    #Gets the latitude and longitude of the four points closest to the input site
    lon = fcindex(dlons,lon_station)
    lat = fcindex(dlats,lat_station)
    
    #Get the weight of each point (inverse distance)
    ele1=get_distance_hav(lat_station,lon_station,lat[1],lon[1])
    ele2=get_distance_hav(lat_station,lon_station,lat[1],lon[3])
    ele3=get_distance_hav(lat_station,lon_station,lat[3],lon[1])
    ele4=get_distance_hav(lat_station,lon_station,lat[3],lon[3])
    
    ele=1/ele1 + 1/ele2 + 1/ele3 + 1/ele4
    
    e1=(1/ele1)/ele
    e2=(1/ele2)/ele
    e3=(1/ele3)/ele
    e4=(1/ele4)/ele    
    
   
    var = dst[va][:]


    lista = np.empty((len(var)))
    
    for i in range(len(var.data)):
        var_point1 = np.squeeze(float(var[i,[lat[0]],[lon[0]]]))
        var_point2 = np.squeeze(float(var[i,[lat[0]],[lon[2]]]))
        var_point3 = np.squeeze(float(var[i,[lat[2]],[lon[0]]]))
        var_point4 = np.squeeze(float(var[i,[lat[2]],[lon[2]]]))
        lista[i] = (var_point1*e1+var_point2*e2+var_point3*e3+var_point4*e4)

    return lista


if  __name__=="__main__" :
    dst = xr.open_dataset('Y:/Daily_GCM/tasmin_day_ACCESS-CM2_historical_r1i1p1f1_gn_20000101-20141231.nc')
    site_data = get_data(114.0001,45.0001,data,'tasmin')