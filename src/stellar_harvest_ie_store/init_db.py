import logging
import asyncio

from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

from stellar_harvest_ie_store.db import init_db

logger = logging.getLogger("stellar_harvest_ie_store.init_db")

async def main():
    await init_db()


if __name__ == "__main__":
    logger.info("STORE module __main__")
    asyncio.run(main())
