from sklearn.neighbors import kneighbors_graph
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/spotify_data.csv')

#def plot_graph(song_name):
#takes in song name and returns graph of nearest neighbors
features = df.drop(columns=['id', 'artists', 'name', 'release_date'])
features.reset_index(drop=True, inplace=True)

data = kneighbors_graph(features, 10, mode='distance')
song_num = df.loc[df['name'] == song_name].index(0)
print(data.head())
#TODO create graph of plotted points from data
#data_points = 
#graph = 
   # return graph