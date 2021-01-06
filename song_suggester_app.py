
from flask import Flask, render_template, request
import pandas as pd
from sklearn.neighbors import NearestNeighbors

APP = Flask(__name__)


def check_song(df, title, artist):
    title_check = df['name'].isin([title])
    artist_check = df['artists'][title_check].isin([str([artist])])
    if len(title_check) > 0:
        if len(df['artists'][title_check][artist_check]) > 0:
            found = df['artists'][title_check][artist_check].index
            return found[0]
        else:
            return 'Not Found'

    else:
        return 'Not Found'

def add_song(df, title, artist, identity):
    df = df.append({'title': title, 'artist': artist, 'id': identity}, ignore_index=True)
    return df

@APP.route('/')
def root():
    """Base view."""
    user_likes = pd.read_csv('data/user_likes.csv')
    return render_template('main.html', df=user_likes['title'], ats=user_likes['artist'])


@APP.route('/add', methods=["POST"])
def add():
    title, artist = [request.values["title"], request.values["artist"]]
    user_likes = pd.read_csv('data/user_likes.csv')
    spotify_data = pd.read_csv('data/spotify_data.csv')
    check = check_song(spotify_data, title, artist)
    if not(check == 'Not Found'):
        user_likes = add_song(user_likes, title, artist, check)
        user_likes.to_csv('data/user_likes.csv', index=False)
        return render_template('main.html', df=user_likes['title'], ats=user_likes['artist'])
    else:
        return str(check)

@APP.route('/suggest', methods=["POST"])
def suggest():
    spotify_data = pd.read_csv('data/spotify_data.csv')
    spotify_data.index = spotify_data['id']
    spotify_data = spotify_data.drop(columns='id')
    features = spotify_data.drop(columns=['artists', 'name', 'release_date'])
    user_likes = pd.read_csv('data/user_likes.csv')

    model_input = []
    for i in user_likes['id']:
        model_input.append(i)

    model_input = features.iloc[model_input]

    nn = NearestNeighbors(n_neighbors=10, algorithm='brute')
    nn.fit(features)
    output = nn.kneighbors(model_input)

    display = pd.DataFrame()
    for i in range(0, len(user_likes['title'])):
        display = display.append(spotify_data.iloc[output[1][i][1]])

    return render_template('suggestions.html', df=display['name'], ats=display['artists'])

@APP.route("/clear", methods=["POST"])
def clear():
    user_likes = pd.DataFrame({'title': [], 'artist': [], 'id': []})
    user_likes.to_csv('data/user_likes.csv', index=False)
    return render_template('main.html', df=user_likes['title'], ats=user_likes['artist'])