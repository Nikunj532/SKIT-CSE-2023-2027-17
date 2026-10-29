import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

logger = logging.getLogger("adhikar_setu.database")


class DatabaseManager:
    """Async MongoDB Database Manager using Motor."""

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect(self) -> None:
        """Initialize MongoDB client connection pool."""
        try:
            logger.info("Connecting to MongoDB at %s...", settings.MONGODB_URI)
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
                maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                serverSelectionTimeoutMS=5000,
            )
            self.db = self.client[settings.MONGODB_DB_NAME]
            # Verify connection with a ping
            await self.client.admin.command("ping")
            logger.info(
                "Successfully connected to MongoDB database '%s'.",
                settings.MONGODB_DB_NAME,
            )
        except Exception as e:
            logger.error("Failed to connect to MongoDB: %s", str(e))
            raise e

    async def close(self) -> None:
        """Close MongoDB client connection pool."""
        if self.client:
            logger.info("Closing MongoDB connection pool...")
            self.client.close()
            logger.info("MongoDB connection closed.")

    async def ping(self) -> bool:
        """Check if MongoDB server is responsive."""
        if not self.client:
            return False
        try:
            await self.client.admin.command("ping")
            return True
        except Exception:
            return False


db_manager = DatabaseManager()


def get_database() -> AsyncIOMotorDatabase:
    """FastAPI Dependency to inject database instance."""
    if db_manager.db is None:
        raise RuntimeError("Database connection has not been initialized.")
    return db_manager.db
