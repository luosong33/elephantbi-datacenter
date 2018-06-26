from ebidp.learn import create_app

app = create_app()
app.run(debug=app.config['DEBUG'])