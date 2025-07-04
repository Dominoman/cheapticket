from sqlalchemy import func

import config
from database import Database, Search

if __name__ == "__main__":
    db=Database(config.DB_FILENAME, config.DB_DEBUG)
    max_timestamp = db.session.query(func.max(Search.timestamp)).scalar()
    max_prefix = max_timestamp[:13]
    # Update all matching rows
    db.session.query(Search).filter(
        func.substr(Search.timestamp, 1, 13) == max_prefix
    ).update({Search.actual: 1}, synchronize_session=False)
    db.session.commit()
