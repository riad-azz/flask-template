from app import create_app

app = create_app(debug=True)

if __name__ == "__main__":
    app.run()
