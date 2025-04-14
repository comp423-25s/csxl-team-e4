import sys

sys.path.append(".")  # Add root to module search path

from backend.test.services.academics import practice_test_data
from backend.database import db_session


def main():
    session = next(db_session())
    practice_test_data.insert_fake_data(session)
    print("✅ Seeded practice test data!")


if __name__ == "__main__":
    main()
