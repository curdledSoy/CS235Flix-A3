from cs235flix import create_app
from flask_caching import Cache

app = create_app()

if __name__ == "__main__":
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)
    app.run(host='localhost', port=5000)
