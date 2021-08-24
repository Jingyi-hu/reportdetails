"""
Module contains methods for process gnss data

"""
import gnssmapper as gm
import warnings
warnings.filterwarnings("ignore")
import copy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd



def create_geodata(x):
    """
    create one geodataframe for input list where each elemnt is geopandas dataframe of gnss receiverpoints

    Parameters
    ----------
    x : list
        list of the multify gnss geopandas dataframe data.
        
    Returns
    -------
    geodataframe:
        combine all elements in the list of gnss receiverpoints including:
        time
        Cn0DbHz
        svid
        receiver position (as point geometry)
    """
    list_len = len(x)
    pilot_log = pd.concat(x[i][['time','Cn0DbHz','svid','geometry']] for i in range(list_len))
    
    return pilot_log

def time_form(gdf):
    """
    change the time form in geodataframe from microseconds to seconds

    Parameters
    ----------
    gdf : geodataframe
        geodataframe of gnss data which has column of time
        
    Returns
    -------
    geodataframe:
        new time form in %Year-%month-%dayT%Hour:%Minite:%Second
    """
    gdf['time'] = gdf['time'].dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    return gdf

def valid_svid(gdf):
    """
    removed invalid satellites from geodataframe

    Parameters
    ----------
    gdf : geodataframe
        geodataframe of gnss data which has column of svid
        
    Returns
    -------
    geodataframe:
        geodataframe of gnss data and the satellites are gps,glonass,beidou and galileo
    """
    #define all valid satellites
    svid = ('G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20', 'G21', 'G22', 'G23', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29', 'G30', 'G31', 'G32',
'R01', 'R02', 'R03', 'R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23', 'R24',
'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37',
'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E19', 'E20', 'E21', 'E22', 'E23', 'E24', 'E25', 'E26', 'E27', 'E28', 'E29', 'E30', 'E31', 'E32', 'E33', 'E34', 'E35', 'E36')
    
    gdf = gdf.loc[gdf['svid'].isin(svid),['svid','time','Cn0DbHz','geometry']]
    
    return gdf

def data_format(gdf):
    """
    Adjust data format

    Parameters
    ----------
    gdf : geodataframe
        geodataframe of gnss data
        
    Returns
    -------
    geodataframe:
        geodataframe of gnss data with new format and sea level
    """
    #Adjust data format
    gdf.time = gdf.time.astype('datetime64')
    gdf.svid = gdf.svid.astype('string')
    #re-define ground sea level of altitude
    gdf.geometry=gpd.points_from_xy(gdf.geometry.x,gdf.geometry.y,float(381))
    
    return gdf

def data_sort(gdf,str):
    """
    sort the geodataframe by special string

    Parameters
    ----------
    gdf : geodataframe
        geodataframe of gnss data
    str: sort based on this string
    Returns
    -------
    geodataframe:
        geodataframe of gnss data after sorting
    """
    gdf = gdf.sort_values(by = [str])
    
    return gdf

def day_night(gdf):
    """
    divide the geodataframe by day and night

    Parameters
    ----------
    gdf : geodataframe
        geodataframe of gnss data

    Returns
    -------
    geodataframe:
        two geodataframes of gnss data, one is 
        data collected during data, another is
        during night
    """
    #add day column to define different data collected day
    gdf['day'] = gdf['time'].apply(lambda r:r.day)
    gdf_day = gdf[gdf['day']==1]
    gdf_night = gdf[gdf['day']==3]
    
    return gdf_day,gdf_night

