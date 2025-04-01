import os
from website import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    # Close any existing database connections
    inspector = inspect(db.engine)
    if inspector.get_table_names():
        db.session.close_all()
        db.engine.dispose()

    # Check if database file exists and delete it
    db_path = 'instance/store.db'  # Update path if different
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")

    # Create all tables from scratch
    db.create_all()
    print("Created new database with updated schema")

print("Database reset successfully!")