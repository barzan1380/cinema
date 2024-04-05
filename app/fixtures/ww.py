import json
data = [{"title": "Children of heaven", "release_year": "1997", "play_time": "2018/4/20 22:00"},
        {"title": "A separation", "release_year": "2011", "play_time": "2018/4/22 18:00"}]

with open('movies.json', 'w') as jf:
    json.dump(data, jf)
