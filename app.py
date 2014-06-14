from flask import Flask, jsonify
from werkzeug.contrib.cache import SimpleCache
import requests
import config

app = Flask(__name__)
cache = SimpleCache()

def fetch_playtime():
    steam_response = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&format=json' % (config.STEAM_API_KEY,config.USER_ID,))
    games = steam_response.json()['response']['games']
    for game in games:
        if game['appid'] == config.GAME_ID:
            return game['playtime_forever']
    return -1

def get_playtime():
    playtime = cache.get('playtime')
    if playtime is None:
        try:
            playtime = fetch_playtime()
        except:
            playtime = -1
        cache.set('playtime', playtime, timeout=config.CACHE_TIME)
    return playtime

@app.route('/')
def index():
    return jsonify({'playtime': get_playtime()})

if __name__ == '__main__':
    app.run(debug=True)