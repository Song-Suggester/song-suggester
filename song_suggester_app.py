
from flask import Flask, render_template, request
import pandas as pd

user_likes = pd.DataFrame()
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
    return render_template('main.html', title="Home", df=user_likes['title'], ats=user_likes['artist'])


@APP.route('/add', methods=["POST"])
def add():
    title, artist = [request.values["title"], request.values["artist"]]
    user_likes = pd.read_csv('data/user_likes.csv')
    spotify_data = pd.read_csv('data/spotify_data.csv')
    check = check_song(spotify_data, title, artist)
    if not(check == 'Not Found'):
        user_likes = add_song(user_likes, title, artist, check)
        user_likes.to_csv('data/user_likes.csv', index=False)
        return render_template('main.html', title="Home", df=user_likes['title'], ats=user_likes['artist'])
    else:
        return str(check)

@APP.route('/suggest', methods=["POST"])
def suggest():
    return 'Here you go'

@APP.route("/clear", methods=["POST"])
def clear():
    user_likes = pd.DataFrame({'title': [], 'artist': [], 'id': []})
    user_likes.to_csv('data/user_likes.csv', index=False)
    return render_template('main.html', title="Home", df=user_likes['title'], ats=user_likes['artist'])