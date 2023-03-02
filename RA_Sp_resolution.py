''' Author: Zhengyang Li  
    Last Modified: Mar-2023  
    Contact:izzylzy@outlook.com
'''
import xarray as xr
import numpy as np
import os
def get_new2dlist(data):
    
    lonary = np.array(data.lon.values)
    latary = np.array(data.lat.values)
    
    return latary,lonary

if __name__ == '__main__':
    # reshape dst2 to the same resolution of dst1
    dst1 = xr.open_dataset('dir+filename')
    dst2 = xr.open_dataset('dir+filename')
    
    lats,lons = get_new2dlist(dst1)
    
    RA_dst2 = dst2.interp(lat = lats, lon = lons,method= "zero",
                          kwargs={"fill_value": "extrapolate"})
    # method: 'linear', 'nearest', 'zero', 'slinear'
    
    RA_dst2.to_netcdf('dir+filename')
