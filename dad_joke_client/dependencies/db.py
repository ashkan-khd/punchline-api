import asyncio
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from nameko.extensions import DependencyProvider

from documents import SearchCache, DadJoke

logger = logging.getLogger(__name__)


class BeanieDatabaseProvider(DependencyProvider):
    def __init__(self, db_uri: str, db_name: str):
        self.db_uri = db_uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.loop = None

    async def _initialize_beanie(self):
        # Initialize Beanie with the desired document models
        logger.info("Initializing Beanie")
        self.db = self.client[self.db_name]
        await init_beanie(database=self.db, document_models=[SearchCache, DadJoke])
        logger.info("Beanie initialized")

    def setup(self):
        # Set up the Motor client
        logger.info(f"Connecting to database: {self.db_uri}")
        self.client = AsyncIOMotorClient(self.db_uri)

        # Create a new event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Initialize Beanie asynchronously
        self.loop.run_until_complete(self._initialize_beanie())
        logger.info("Connected to database")

    def get_dependency(self, worker_ctx):
        # Provide the database instance and event loop to the service
        return self.loop

    def stop(self):
        # Close the Motor client connection
        if self.client:
            self.client.close()
        if self.loop:
            self.loop.close()
