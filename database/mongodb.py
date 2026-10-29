import os
import logging
from typing import Optional

logger = logging.getLogger("adhikar_setu.database")

# Environment configuration with safe defaults
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "adhikar_setu")

# Cache connection availability to avoid repeated connection timeouts
_is_mongodb_available: Optional[bool] = None


def get_mongodb_uri() -> str:
    """Returns configured MongoDB connection URI."""
    return os.getenv("MONGODB_URI", MONGODB_URI)


def get_database_name() -> str:
    """Returns configured MongoDB database name."""
    return os.getenv("MONGODB_DB_NAME", MONGODB_DB_NAME)


def check_mongodb_connection(uri: Optional[str] = None, timeout_ms: int = 200, force_recheck: bool = False) -> bool:
    """
    Check if MongoDB server is reachable.
    Returns True if connected and responsive, False otherwise.
    Never throws unhandled exceptions. Caches result unless force_recheck=True.
    """
    global _is_mongodb_available
    if _is_mongodb_available is not None and not force_recheck and uri is None:
        return _is_mongodb_available

    client = None
    try:
        from pymongo import MongoClient

        target_uri = uri or get_mongodb_uri()
        client = MongoClient(target_uri, serverSelectionTimeoutMS=timeout_ms)
        client.admin.command("ping")
        _is_mongodb_available = True
        return True
    except Exception as e:
        logger.debug("MongoDB connection check failed: %s", e)
        _is_mongodb_available = False
        return False
    finally:
        if client is not None:
            try:
                client.close()
            except Exception:
                pass


def get_sync_db(uri: Optional[str] = None, db_name: Optional[str] = None):
    """
    Returns a synchronous PyMongo Database instance if MongoDB is reachable,
    otherwise None. Safely handles connection teardown.
    """
    if not check_mongodb_connection(uri=uri):
        return None

    try:
        from pymongo import MongoClient

        target_uri = uri or get_mongodb_uri()
        target_db = db_name or get_database_name()
        client = MongoClient(target_uri, serverSelectionTimeoutMS=500)
        client.admin.command("ping")
        return client[target_db]
    except Exception as e:
        logger.warning("Could not obtain MongoDB database instance: %s", e)
        return None


def init_profiles_indexes(db) -> bool:
    """
    Applies indexes defined in PROFILES_INDEXES to the 'profiles' collection.
    """
    if db is None:
        return False
    try:
        from Nimisha.schemas.profile import PROFILES_COLLECTION, PROFILES_INDEXES

        collection = db[PROFILES_COLLECTION]
        for idx in PROFILES_INDEXES:
            collection.create_index(
                idx["keys"],
                unique=idx.get("unique", False),
                name=idx.get("name")
            )
        return True
    except Exception as e:
        logger.warning("Failed to initialize profile indexes: %s", e)
        return False
