#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from app.db.session import db_session

print("Creating database tables...")
try:
    db_session.create_tables()
    print("Database tables created successfully!")
except Exception as e:
    print(f"Error creating database tables: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
