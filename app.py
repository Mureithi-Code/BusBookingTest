from app import create_app

app = create_app()

if __name__ == '__main__':
    app.app( port=5000, debug=True)
