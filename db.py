import asyncpg

pool: asyncpg.Pool | None = None


async def init_pool(dsn: str) -> None:
    global pool
    pool = await asyncpg.create_pool(dsn, min_size=1, max_size=10)


async def close_pool() -> None:
    if pool:
        await pool.close()


def get_pool() -> asyncpg.Pool:
    if pool is None:
        raise RuntimeError("DB pool is not initialized")
    return pool