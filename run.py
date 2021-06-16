from weather_api.processors import app

app.include_routers()
server = app.server

if __name__ == '__main__':
    app.run()
