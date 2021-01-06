
from flask import Flask, render_template, request
import pandas as pd

user_likes = pd.DataFrame()
APP = Flask(__name__)


def add_song(df, title, artist):
    df = df.append({'title' : title, 'artist' : artist}, ignore_index=True)
    return df

@APP.route('/')
def root():
    """Base view."""
    return render_template('main.html', title="Home")


@APP.route('/add', methods=["POST"])
def add():
    title, artist = [request.values["title"], request.values["artist"]]
    user_likes = pd.read_csv('data/user_likes.csv')
    user_likes = add_song(user_likes, title, artist)
    user_likes.to_csv('data/user_likes.csv', index=False)
    #message = new_df['title'][0] + ' ' + new_df['artist'][0] + ' added!'
    return str(user_likes)

@APP.route('/suggest', methods=["POST"])
def suggest():
    return 'Here you go'

@APP.route("/clear", methods=["POST"])
def clear():
    user_likes = pd.DataFrame({'title': [], 'artist': []})
    user_likes.to_csv('data/user_likes.csv', index=False)
    return 'List Cleared'