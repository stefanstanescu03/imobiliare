from website import create_app, connect_to_database

app = create_app()
db = connect_to_database()

if __name__ == '__main__':
    app.run(debug=True)
