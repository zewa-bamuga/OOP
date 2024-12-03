import logging
import os.path

import nest_asyncio

__root_dir__ = os.path.dirname(os.path.abspath(__file__))

logging.getLogger("faker").setLevel(logging.WARN)
logging.getLogger("factory").setLevel(logging.WARN)
logging.getLogger("asyncio").setLevel(logging.WARN)
logging.getLogger("multipart").setLevel(logging.WARN)

nest_asyncio.apply()
