from dotenv import load_dotenv
import os
import asyncio
import httpx

load_dotenv()
TASTEDIVE_API_KEY = os.getenv("TASTEDIVE_API_KEY")
OPEN_ALEX_API_KEY = os.getenv("OPEN_ALEX_API_KEY")


async def get_with_retry(
    client,
    url,
    params,
    headers,
    retries=3
):
    for attempt in range(retries):
        try:
            return await client.get(
                url,
                params=params,
                headers=headers
            )

        except (
            httpx.ConnectError,
            httpx.ReadTimeout,
            httpx.ConnectTimeout
        ):
            if attempt == retries - 1:
                raise

            await asyncio.sleep(2 ** attempt)