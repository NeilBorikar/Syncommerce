from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.utils.logger import logger


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(settings.MONGO_URI)
            self.db = self.client[settings.DATABASE_NAME]

            # Test connection
            self.client.admin.command("ping")

            logger.info("MongoDB connected successfully")

        except Exception as e:
            logger.error("MongoDB connection failed", exc_info=True)
            raise e

    def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


class AsyncMongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.DATABASE_NAME]

            logger.info("Async MongoDB connected")

        except Exception as e:
            logger.error("Async MongoDB failed", exc_info=True)
            raise e

    async def close(self):
        if self.client:
            self.client.close()


# Global instances
mongo = MongoDB()
async_mongo = AsyncMongoDB()