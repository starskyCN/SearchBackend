from bottle import Bottle, request
from bottle_cache.plugin import (cache_for, CachePlugin)

from gevent.monkey import patch_all
patch_all()
from btsearch import Bitsearch


app = Bottle()
bt = Bitsearch()
cache = CachePlugin('url_cache', 'redis', host='localhost', port=6379, db=1)
app.install(cache)

@app.route('/search')
@cache_for(3600, cache_key_func='full_path')
def search():
    query = request.query.get('query', '')
    category = request.query.get('category', '')
    limit = request.query.get('limit', 20)
    page = request.query.get('page', 1)
    sort = request.query.get('sort', '')
    print('Cache miss:%s' % query)
    result = bt.search(query, page, limit, category, sort)
    print(result)
    return result


@app.route('/trend')
def trend():
    trend_search = {'回到太空':'14', '博物馆奇妙夜3':'16', '国漫':'14', '极品': '16', '杨超越':'14', 'garfield 2004':'14'}
    data = {'data': trend_search}
    return data

if __name__ == '__main__':
    app.run(server='gevent', host='0.0.0.0', port=8888)
