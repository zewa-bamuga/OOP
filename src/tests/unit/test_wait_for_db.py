from a8t_tools.db import wait_for_db


async def test_wait_for_db(container_singletone):
    await wait_for_db.main()
