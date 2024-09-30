#This is the entry point to the app
from app import create_app, db
from flask_migrate import Migrate
from app.models import User, BlogPost

app = create_app('development')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'BlogPost': BlogPost}

if __name__ == '__main__':
    app.run(debug=True)
