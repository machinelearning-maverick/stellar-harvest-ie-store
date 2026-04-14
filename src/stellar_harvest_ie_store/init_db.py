import asyncio

from stellar_harvest_ie_config.logging_config import setup_logging

setup_logging()

from stellar_harvest_ie_store.db import init_db


async def main():
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())
