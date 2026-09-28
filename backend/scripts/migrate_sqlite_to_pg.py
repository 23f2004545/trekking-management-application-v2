"""
Database Migration Utility: SQLite -> Neon PostgreSQL
Transfers schema, all rows in dependency order, and synchronizes PostgreSQL sequences.
"""

import os
import sys
from sqlalchemy import create_engine, MetaData, Table, select, func, text

# Add backend directory to sys.path so controller/models can be imported
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(backend_dir, ".env"))
except ImportError:
    pass

from controller.models import db, User, Role, UserRoles, Trek, StaffProfile, Booking, MedicalRecord, Review, TrekImage, Notification, AuditLog, DispatchTicket


TABLE_ORDER = [
    ('role', 'id'),
    ('user', 'id'),
    ('user_roles', 'id'),
    ('staff_profile', 'staff_id'),
    ('medical_record', 'id'),
    ('trek', 'trek_id'),
    ('trek_image', 'id'),
    ('booking', 'booking_id'),
    ('review', 'id'),
    ('notification', 'id'),
    ('audit_log', 'id'),
    ('dispatch_ticket', 'id')
]


def normalize_pg_uri(uri: str) -> str:
    if uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql+psycopg2://", 1)
    elif uri.startswith("postgresql://") and not uri.startswith("postgresql+"):
        return uri.replace("postgresql://", "postgresql+psycopg2://", 1)
    return uri


def run_migration(source_sqlite_uri=None, target_pg_uri=None):
    if not source_sqlite_uri:
        # Default local sqlite database location
        db_path = os.path.join(backend_dir, "database.sqlite3")
        source_sqlite_uri = f"sqlite:///{db_path}"

    if not target_pg_uri:
        target_pg_uri = os.environ.get("TARGET_DATABASE_URL") or os.environ.get("DATABASE_URL")

    if not target_pg_uri or "postgres" not in target_pg_uri:
        print("❌ Error: A valid PostgreSQL connection string must be provided via TARGET_DATABASE_URL or DATABASE_URL.")
        print("Example: postgresql://user:password@ep-xyz.neon.tech/neondb?sslmode=require")
        return False

    target_pg_uri = normalize_pg_uri(target_pg_uri)

    print(f"📦 Source (SQLite): {source_sqlite_uri}")
    print(f"🚀 Target (PostgreSQL): {target_pg_uri.split('@')[-1] if '@' in target_pg_uri else target_pg_uri}")

    sqlite_engine = create_engine(source_sqlite_uri)
    pg_engine = create_engine(target_pg_uri)

    # 1. Create tables on destination PostgreSQL if not present
    print("\n🔨 Ensuring schema exists on PostgreSQL target...")
    db.metadata.create_all(bind=pg_engine)

    src_meta = MetaData()
    src_meta.reflect(bind=sqlite_engine)

    tgt_meta = MetaData()
    tgt_meta.reflect(bind=pg_engine)

    print("\n🚚 Migrating data table by table...")
    with sqlite_engine.connect() as src_conn, pg_engine.begin() as tgt_conn:
        for table_name, pk_col in TABLE_ORDER:
            if table_name not in src_meta.tables:
                print(f"  ⏭️  Skipping {table_name} (not found in source SQLite)")
                continue

            src_table = src_meta.tables[table_name]
            tgt_table = tgt_meta.tables[table_name]

            # Fetch rows from source
            rows = src_conn.execute(select(src_table)).fetchall()
            row_count = len(rows)

            if row_count == 0:
                print(f"  ⚪ Table '{table_name}': 0 records to migrate.")
                continue

            # Convert rows to dicts
            insert_data = [dict(row._mapping) for row in rows]

            # Clear destination table first or insert
            tgt_conn.execute(tgt_table.delete())
            tgt_conn.execute(tgt_table.insert(), insert_data)
            print(f"  ✅ Table '{table_name}': Migrated {row_count} records.")

            # Update PostgreSQL sequence to prevent duplicate key errors on future inserts
            if pk_col:
                try:
                    seq_query = text(f"""
                        SELECT setval(
                            pg_get_serial_sequence('{table_name}', '{pk_col}'),
                            COALESCE((SELECT MAX({pk_col}) FROM "{table_name}"), 1),
                            (SELECT MAX({pk_col}) FROM "{table_name}") IS NOT NULL
                        );
                    """)
                    tgt_conn.execute(seq_query)
                except Exception as seq_err:
                    # Some tables might not use SERIAL if id is manually assigned
                    pass

    print("\n🎉 Migration completed successfully! Verifying destination counts...")
    with pg_engine.connect() as verify_conn:
        for table_name, _ in TABLE_ORDER:
            if table_name in tgt_meta.tables:
                count = verify_conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar()
                print(f"  • {table_name}: {count} rows")

    return True


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else None
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    success = run_migration(src, dst)
    sys.exit(0 if success else 1)
