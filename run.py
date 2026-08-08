from app import create_app
# run.py - Entry point for the Flask application

app = create_app()

if __name__ == '__main__':
    app.run(debug = True)
    
    
# Do three things here:
#   1. Import create_app from app (you'll define this in app/__init__.py)
#   2. Call create_app() and assign the result to a variable called app
#   3. Add the standard Python entry point block:
#        if __name__ == '__main__':
#            app.run(debug=True)
#
# To start the server, run: python run.py
# Then visit http://localhost:5000 in your browser.
