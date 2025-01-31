if __name__ == '__main__':
    try:
        from app import app
        app.run(debug=True)
    except ImportError:
        raise ImportError("Could not import app")



