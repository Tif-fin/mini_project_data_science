import pandas  as pd 
import matplotlib.pyplot as plt
import geopandas as gpd 
import os 

class Map:
    __folder_path = './districts_geojson'
    map_gdfs = []
    def __init__(self):
        self.map_gdfs = self.__concatGeoDataFrame()
        self.__fixDiffernce() 
    
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
        self.map_gdfs = pd.merge(self.map_gdfs, dataFrame,on='DISTRICT',how='inner')
        self.map_gdfs=self.map_gdfs.drop('District',axis=1)
        return self.map_gdfs

    def __fixDiffernce(self):
        '''
            Fix the spelling mistake  
        '''
        difference= ['CHITWAN', 'EASTERN RUKUM', 'KAVREPALANCHOWK', 'NAWALPUR',
       'PARASI', 'SINDHUPALCHOK', 'TANAHU', 'TEHRATHUM', 'WESTERN RUKUM']
        district= ['CHITAWAN', 'RUKUM', 'KAVREPALANCHOK', 'NAWALPARASI',
       'NAWALPARASI', 'SINDHUPALCHOWK', 'TANAHUN', 'TEHRATHUM', 'RUKUM']
        district = district
        #replace the district name 
        for index in range(len(difference)):
            # print(f"Replacing district name :{difference[index]}  to {district[index]} ")
            self.map_gdfs['DISTRICT']=self.map_gdfs['DISTRICT'].str.replace(difference[index],district[index])
        return None