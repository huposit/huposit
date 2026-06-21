import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://root:1234@localhost:5432/pgvdb",
)
