import pandas  as pd 
from pandas import _typing
import matplotlib.pyplot as plt
import geopandas as gpd 
import os 
import regex as re 




class Map:
    '''
    Nepal Map\n
    This is a new nepal map. It has 77 districts.
    
    '''
    __folder_path = './districts_geojson'
    map_gdfs = []
    __original_gdfs = []
    def __init__(self):
        self.__original_gdfs = self.__concatGeoDataFrame()
        self.map_gdfs = self.__original_gdfs.copy()
        self.__fixDifference() 
    
    def __loadgeoJson(self):
        gdfs = []
        for file in os.listdir(self.__folder_path):
            gdf = gpd.read_file(os.path.join(self.__folder_path,file))
            gdfs.append(gdf)
        return gdfs

    def __concatGeoDataFrame(self):
        gdfs =  self.__loadgeoJson()
        return gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)

    def mergeDF(self,dataFrame):
        '''DataFrame must have the District Column'''
        if not isinstance(dataFrame, pd.DataFrame):
            raise "Pandas DataFrame is required"
        # Merge DataFrame
        dataFrame['DISTRICT'] = dataFrame['District'].str.upper().sort_values()
        #check for the difference
        self.map_gdfs = pd.merge(self.map_gdfs, dataFrame,on='DISTRICT',how='outer')
        self.map_gdfs=self.map_gdfs.drop('District',axis=1)
        return self.map_gdfs
    def merge(self,dataFrame,on,how:_typing.MergeHow='inner'):
        '''Merge the dataframe map_gdfs'''
        if not isinstance(dataFrame, pd.DataFrame):
            raise "Pandas DataFrame is required"
        #check for the difference
        self.map_gdfs = pd.merge(self.map_gdfs, dataFrame,on=on,how=how)
        self.map_gdfs.reset_index(inplace=True)
        return self.map_gdfs

    def __fixDifference(self):
        '''
            Fix the spelling mistake
        '''
        # Define the district names with differences
        difference = ['CHITWAN', 'EASTERN RUKUM', 'KAVREPALANCHOWK', 'NAWALPUR',
                    'PARASI', 'SINDHUPALCHOK', 'TANAHU', 'TEHRATHUM', 'WESTERN RUKUM']
        district = ['CHITAWAN', 'RUKUM', 'KAVREPALANCHOK', 'NAWALPARASI',
                    'NAWALPARASI', 'SINDHUPALCHOWK', 'TANAHUN', 'TERHATHUM', 'RUKUM']

        # Create a list of tuples for the replacements
        replacements = list(zip(difference, district))

        # Sort replacements to handle "NAWALPUR" and "PARASI" correctly by length (longer first)
        replacements.sort(key=lambda x: len(x[0]), reverse=True)

        # Replace the district names
        for diff, dist in replacements:
            pattern = r'\b{}\b'.format(re.escape(diff))  # Create a word boundary pattern
            self.map_gdfs['DISTRICT'] = self.map_gdfs['DISTRICT'].str.replace(pattern, dist, regex=True)

        return None
    

    def __repairInvalidArgs(self):
        # Clean geometries by buffering with a distance of 0
        self.map_gdfs['geometry'] = self.map_gdfs['geometry'].buffer(0)

        # Further clean invalid geometries
        def repair_geometry(geom):
            if not geom.is_valid:
                return geom.buffer(0)
            return geom

        self.map_gdfs['geometry'] = self.map_gdfs['geometry'].apply(repair_geometry)
        
        # Remove any remaining invalid geometries
        self.map_gdfs = self.map_gdfs[self.map_gdfs.is_valid]


    def dissolve_by_district(self):
        '''Dissolve polygons by district name'''
        #repair the invalid args 
        self.__repairInvalidArgs()
        # Dissolve polygons by district name
        self.map_gdfs = self.map_gdfs.dissolve(by='DISTRICT')
        return self.map_gdfs
    
    def dissolve_by_zone(self):
        '''Dissolve polygons by Zone name'''
        # Clean geometries by buffering with a distance of 0
          #repair the invalid args 
        self.__repairInvalidArgs()
        # Dissolve polygons by Zone name
        self.map_gdfs = self.map_gdfs.dissolve(by='Zone')
        return self.map_gdfs
    def dissolve_by_province(self):
        '''Dissolve polygons by PROVINCE name'''
        # Clean geometries by buffering with a distance of 0
          #repair the invalid args 
        self.__repairInvalidArgs()
        # Dissolve polygons by Zone name
        self.map_gdfs = self.map_gdfs.dissolve(by='PROVINCE')
        return self.map_gdfs

    def reset(self):
        '''
        This function is used to reset\n
        It resets all the dissolve and merge operations 
        '''
        self.map_gdfs = self.__original_gdfs.copy()
        self.__fixDifference() 
        return self.map_gdfs
