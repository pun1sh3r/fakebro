from app import create_app, db
from app.models import User, Comments, Handle,FakeFollower, Task


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Comments': Comments, 'Handle': Handle,
            'FakeFollower': FakeFollower, 'Task': Task}