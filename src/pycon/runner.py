from gevent import wsgi, pool

def main():
	from pycon.riddles import app
	spawn_pool = pool.Pool(app.config['POOL_SIZE'])
	server = wsgi.WSGIServer((app.config['HOST'], app.config['PORT']), app, spawn=spawn_pool)
	server.serve_forever()

if __name__ == '__main__':
	main()
