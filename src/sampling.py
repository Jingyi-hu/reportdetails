"""
Module contains methods for sampling the gnss data

"""
import gnssmapper as gm
import warnings
warnings.filterwarnings("ignore")
import copy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd
from shapely import geometry
from shapely.geometry import Point,Polygon,shape
from shapely.geometry import mapping
import math
from math import cos,sin
from pandas.core.frame import DataFrame

def random_frac(gdf,x):
    """
    sampling the GNSS data randomly by fraction(each 10%) of the sample to the population
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    x : int
        (x+1)/10 is the sampling fraction 
    Returns
    -------
    geodataframe:
        geodataframe after sampling and the length of the new geodataframe is [(x+1)/10]% of gdf
      
    """
    #Initialize the data frame
    df = pd.DataFrame()
    #do random sampling by fraction
    sample = gdf.sample(frac=(x+1)/10,axis=0)
    #Assign samples to the empty data frame
    df = df.append(sample)
    return df

def random_row(gdf,x,y):
    """
    sampling the GNSS data randomly by entering the specific number of samples
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    x : int
        x is the number of samples
    y: int
        y is the random seed, different random seeds have the same sample size after random sampling, but the results are different
    Returns
    -------
    geodataframe:
        geodataframe after sampling and the length of the new geodataframe is x
      
    """
    #Initialize the data frame
    df = pd.DataFrame()
    #do random sampling by number
    sample = gdf.sample(n = x,random_state = y,axis=0)
    #Assign samples to the empty data frame
    df = df.append(sample)
    return df

def sample_size(gdf,x,i):
    """
    
    Parameters
    ----------
    gdf:geodataframe
    x: int
        size of sample
    i : int
        number of samples

    Returns
    -------
    list:
        list of samples with input size
      
    """
    sample_list = [gdf.sample(x) for j in range(i)]
    
    return sample_list

def rmse(x):
    """
    calculate the Root Mean Squared Error
    
    Parameters
    ----------
    x: dataframe
    i:int
        number of samples

    Returns
    -------
    list:
        rmse
      
    """
    a = sum(((x[j] -405) **2) for j in range(len(x)))
    b = a/len(x)
    c = math.sqrt(b)
    
    return c

def combine_height(listx):
    """
    combine three heights
    
    Parameters
    ----------
    listx: list 

    Returns
    -------
    dataframe which contains three estimated heights:lower bound,mid point and upper bound
      
    """
    a = pd.DataFrame(pd.concat(listx[i].lower_bound for i in range(len(listx))))
    a=a.reset_index()
    a.drop('index',axis=1,inplace=True)
    a1 = pd.DataFrame(pd.concat(listx[i].mid_point for i in range(len(listx))))
    a1=a1.reset_index()
    a1.drop('index',axis=1,inplace=True)
    a2 = pd.DataFrame(pd.concat(listx[i].upper_bound for i in range(len(listx))))
    a2=a2.reset_index()
    a2.drop('index',axis=1,inplace=True)
    heights = pd.concat([a,a1,a2],axis=1)
    
    return heights




def direction_north(gdf,building):
    """
    sampling the GNSS data by direction-data is in the north of the building
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    building: geodataframe 
        geodataframe of building which contains the geometry of the building(2D)
       
    Returns
    -------
    geodataframe:
        geodataframe of north GNSS data 
      
    """
    #get the minimum longitude of gnss data
    longitude1 = gdf.geometry.x.min()
    #get the maximum longitude of gnss data
    longitude2 = gdf.geometry.x.max()
    #get the latitude and longitude of the vertices 
    #that constitute the building polygon
    building_list = list(mapping(building)['bbox'])
    building_list.sort()
    #maximum latituide of building
    latitude1 = building_list[1]
    #maximum latitude of gnss data
    latitude2 = gdf.geometry.y.max()
    #Intercept the data located on the north side of the building
    north = gdf.cx[longitude1:longitude2,latitude1:latitude2]
    return north

def direction_south(gdf,building):
    """
    sampling the GNSS data by direction-data is in the south of the building
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    building: geodataframe 
        geodataframe of building which contains the geometry of the building(2D)
       
    Returns
    -------
    geodataframe:
        geodataframe of south GNSS data 
      
    """
    #get the minimum longitude of gnss data
    longitude1 = gdf.geometry.x.min()
    #get the maximum longitude of gnss data
    longitude2 = gdf.geometry.x.max()
    #get the latitude and longitude of the vertices 
    #that constitute the building polygon
    building_list = list(mapping(building)['bbox'])
    building_list.sort()
    #minimum latitude of gnss data
    latitude1 = gdf.geometry.y.min()
    #minimum latituide of building
    latitude2 = building_list[0]
    #Intercept the data located on the south side of the building
    south = gdf.cx[longitude1:longitude2,latitude1:latitude2]
    return south

def direction_west(gdf,building):
    """
    sampling the GNSS data by direction-data is in the west of the building
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    building: geodataframe 
        geodataframe of building which contains the geometry of the building(2D)
       
    Returns
    -------
    geodataframe:
        geodataframe of west GNSS data 
      
    """
    #get the latitude and longitude of the vertices 
    #that constitute the building polygon
    building_list = list(mapping(building)['bbox'])
    building_list.sort()
    #get the minimum longitude of gnss data
    longitude1 = gdf.geometry.x.min()
    #get the minimum longitude of building
    longitude2 = building_list[2]  
    #get the minimum latitude of gnss data
    latitude1 = gdf.geometry.y.min()
    #get the maximum latitude of gnss data
    latitude2 = gdf.geometry.y.max()
    #Intercept the data located on the west side of the building
    west = gdf.cx[longitude1:longitude2,latitude1:latitude2]
    return west

def direction_east(gdf,building):
    """
    sampling the GNSS data by direction-data is in the east of the building
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    building: geodataframe 
        geodataframe of building which contains the geometry of the building(2D)
       
    Returns
    -------
    geodataframe:
        geodataframe of east GNSS data 
      
    """
    #get the latitude and longitude of the vertices 
    #that constitute the building polygon
    building_list = list(mapping(building)['bbox'])
    building_list.sort()
    #get the maximum longitude of building
    longitude1 = building_list[3]
    #get the maximum longitude of gnss data
    longitude2 = gdf.geometry.x.max() 
    #get the minimum latitude of gnss data
    latitude1 = gdf.geometry.y.min()
    #get the maximum latitude of gnss data
    latitude2 = gdf.geometry.y.max()
    #Intercept the data located on the east side of the building
    east = gdf.cx[longitude1:longitude2,latitude1:latitude2]
    return east

def distance(longitudeA,latitudeA,longitudeB,latitudeB):
    """
    calculate distance in meters of point A and point B
    
    Parameters
    ----------
    longitudeA: float
        longitude of point A
    latitudeA: float
        latitude of point A
    longitudeB: float
         longitude of point B    
    latitudeB:float
         latitude of point B 
       
    Returns
    -------
    int:
        distance between point A and point B   
      
    """
    #define radius of earth
    R = 6371.004
    MLonA = longitudeA
    MLonB = longitudeB
    #since points are at north latitude
    MLatA = 90 - latitudeA
    MLatB = 90 - latitudeB
    
    C = sin(MLatA)*sin(MLatB)*cos(MLonA-MLonB)+cos(MLatA)*cos(MLatB)
    distance = round(1000*R*np.arccos(C)*math.pi/180,0)
    
    return distance
    
def distance_list(gdf,building):
    """
    calculate distances between all gnss received points and centroid of building
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    building: geodataframe 
        geodataframe of building which contains the geometry of the building(2D)
 
       
    Returns
    -------
    geodataframe:
        geodataframe contains all distances   
      
    """
    #centroid longitude of building
    longitudeA = building.centroid.x
    #centroid latitude of building
    latitudeA = building.centroid.y
    #Initialize the list
    distance_list = [0]*len(gdf)
    
    #for loop to get all distances
    for i in range(len(gdf)):
        distance_list[i] = (distance(longitudeA,latitudeA,gdf.iloc[i].geometry.x,gdf.iloc[i].geometry.y))
    #List to DataFrame
    d = DataFrame(distance_list)
    d=d.reset_index()
    d.drop('index',axis=1,inplace=True)
    d.columns = ['distance']
    d = d.reset_index()
    #combine geodatrame and distances value
    gdf = gdf.reset_index()
    gdf = pd.concat([gdf,d],axis=1)
    gdf.drop(['index'], axis=1)
    
    return gdf

def distance_circles(gdf,x):
    """
    sampling the GNSS data by distance
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    x: int
        distance interval
       
    Returns
    -------
    geodataframe:
        geodataframe of GNSS data after sampling by distance interval
      
    """
    #obtain the minimum distance
    distance_min = int(gdf['distance'].unique().min())
    #obtain the maximum distance
    distance_max = int(gdf['distance'].unique().max())
    #initialize the list
    d = [0]*len(gdf['distance'].unique())
    #for loop to get all distance interval
    for i in range(distance_min,distance_max+1,x):
        d.append(i)
    
    #Remove redundant 0 values
    d = list(filter(lambda number : number > 0, d))
    #Keep gnss data at some specific distances
    gdf = gdf.loc[gdf['distance'].isin(d),['time','svid','Cn0DbHz','geometry','distance']]
    
    return gdf

def buffer(gdf,building,x):
    """
    sampling the GNSS data by distance
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    building: geodataframe 
        geodataframe of building which contains the geometry of the building(2D)
    x: int
        distance buffer
       
    Returns
    -------
    geodataframe:
        geodataframe of GNSS data after sampling by distance buffer
      
    """
 
    #initialize list
    bools_map = []
    #Determine whether the gnss data is in the buffer
    for i in range (len(gdf)):
        bools_map.append(building.geometry.buffer(x).contains(gdf.iloc[i].geometry))
    #list to dataframe     
    list_pd = pd.Series(bools_map,name = 'newbools')
    #True to 1,False to 0
    list_pd = list_pd.apply(lambda r:int(r))
    #combine new column
    gdf = pd.concat([gdf,list_pd],axis = 1)
    #return the contained gnss data
    gdf = gdf[gdf['newbools'] == 1]
    
    return gdf

def time_interval(gdf,x):
    """
    sampling the GNSS data by time
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    x: int
        time interval
       
    Returns
    -------
    geodataframe:
        geodataframe of GNSS data after sampling by time interval
      
    """
    #sort the geodataframe by time
    gdf = gdf.sort_values(by = 'time')
    #create a new column to calculate the time of day in minutes
    gdf['minute'] = gdf.apply(lambda x: (60*x['time'].hour+x['time'].minute), axis=1)
    #create a new column to calculate the difference between the time 
    #of day in minutes for each gnss data and the first collected gnss data
    gdf['minite_diff'] = gdf['minute']- gdf.iloc[0]['minute']
    
    #obtain the minimum difference
    time_min = int(gdf['minite_diff'].unique().min())
    #obtain the maximum difference
    time_max = int(gdf['minite_diff'].unique().max())
    #initialize the list
    t = [0]*len(gdf.minite_diff.unique())
    #for loop to get all distance interval
    for i in range(time_min,time_max+1,x):
        t.append(i)
    #Remove redundant 0 values
    t = list(filter(lambda number : number > 0, t))
    t.append(0)
    
    gdf = gdf.loc[gdf['minite_diff'].isin(t),['time','svid','Cn0DbHz','geometry','minute','minite_diff']]
    
    return gdf

def grid_increment(gdf,x):
    """
    obtaining increment of grid based on gnss data's geometry
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    x: int
        grid side length in meters
       
    Returns
    -------
    int:
        increment of grid in longitude and latitude
      
    """
    #define radius of earth
    R = 6371.004
    #get the maximum,minimum of gnss data's longitude and latitude
    lon_min = gdf.geometry.x.min()
    lon_max = gdf.geometry.x.max()
    lat_min = gdf.geometry.y.min()
    lat_max = gdf.geometry.y.max()
    #perimeter of earth
    perimeter = 2*math.pi*R*1000
    #Angle to radians
    radian = perimeter*cos(((lat_min+lat_max)/2)*(2*math.pi/360))
    #increments
    lon_incre = x*360/radian
    lat_incre = x*360/perimeter
    
    return lon_incre,lat_incre

def grid_create(gdf,lon_incre,lat_incre):
    """
    create grid based on gnss data's geometry
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
    lon_num: int
        number of grid in longitude
    lat_num: int
        nnumber of grid in latitude
       
    Returns
    -------
    geodataframes:
        one is geodataframe of whole grids,another is geodataframe of intersected grids
      
    """
    #get the minimum of gnss data's longitude and latitude
    lon_min = gdf.geometry.x.min()
    lat_min = gdf.geometry.y.min()
    #get grid id for all gnss data
    gdf['lon_id'] = gdf.apply(lambda r:int((r.geometry.x-lon_min)/lon_incre),axis=1)
    gdf['lat_id'] = gdf.apply(lambda r:int((r.geometry.y-lat_min)/lat_incre),axis=1)
    #get number of longituide id
    log_num = len(gdf['lon_id'].unique())
    lat_num = len(gdf['lat_id'].unique())
    #initialize geometry of grids
    geometry = []
    
    for i in range(len(gdf['lon_id'].unique())):
        for j in range(len(gdf['lat_id'].unique())):
            geometry.append(Polygon([
                (lon_min+i*lon_incre,lat_min+j*lat_incre),
                (lon_min+(i+1)*lon_incre,lat_min+j*lat_incre),
                (lon_min+(i+1)*lon_incre,lat_min+(j+1)*lat_incre),
                (lon_min+i*lon_incre,lat_min+(j+1)*lat_incre)]))
    #create grids which from smallest to largest longitude 
    #and smallest to largest latitude        
    created_grid = gpd.GeoDataFrame()
    created_grid['geometry'] = geometry
    #Intercept the part of the grid that has intersection with gnss data
    grip_map = created_grid[created_grid.intersects(gdf.unary_union)]
    
    return created_grid,grip_map,gdf

def grid(gdf):
    """
    sampling the GNSS data by grids
    
    Parameters
    ----------
    gdf: geodataframe
        geodataframe of all gnss data(population)
        
       
    Returns
    -------
    list:
        list of each grid which contains all related gnss data
      
    """
    #create new column to determine grid
    gdf['grid'] = gdf.apply(lambda x:(x['lon_id'],x['lat_id']),axis=1)
    #sort by longitude number first and then latituide number
    gdf = gdf.sort_values(by = ['lon_id','lat_id'])
    #initialze grid list
    grid = [0]*len(gdf['grid'].unique())
    #for loop to add all gnss data included in each grid 
    #as the elements in the list
    for grids in gdf['grid'].unique():
        grid_data = gdf[gdf['grid'].isin([grids])]
        grid.append(grid_data)
    #Remove values that do not meet the criteria    
    grid = list(filter(lambda x: not isinstance(x, int), grid))
    
    return grid


    


    
    