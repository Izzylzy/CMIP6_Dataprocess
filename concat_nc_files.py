#Module: combine .nc files by time axis
#Author: Zhenngyang Li  <izzylzy@outlook.com>
#Last modified : 2020-07-01
#python3.7
import xarray as xr
import os
 
def file_name(file_dir):
    '''Obtain the path and name list of the NC file to be combined'''
    
    L=[] 
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.nc':
                L.append(os.path.join(root, file))
        L.sort()
    return L
def concat_nc(name_list,target):
    '''-------Description-------
    :param name_list: Path and name list of the NC file to be combined
    :param target: Path and name of the combined NC file '''
    
    data_f = xr.open_dataset(filess[0])

    for i in range(len(filess)-1):
        print(f'\r{(i+1)}/{(len(filess)-1)}',end ='        ')
        data_b = xr.open_dataset(filess[i+1])
        data_f = xr.concat([data_f,data_b],dim = 'time')
    data_f.to_netcdf(target)

if  __name__=="__main__" :
    filess = file_name('Y:/CRU/meta')
    concat_nc(filess,'Y:/CRU/pr_Amon_CRU_1981_2019.nc')
