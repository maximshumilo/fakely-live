import hashlib
from pathlib import Path

from aioredis import (
    Redis,
    create_redis,
)

from config import CONFIG


class FaceMask:
    """Class for managing face mask images in Redis.

    This class provides methods to initialize a Redis connection and update
    the face mask image stored in Redis.
    """

    _KEY_BYTES: str = "mask_bytes"
    _KEY_MD5: str = "mask_md5"

    client: Redis = None

    async def init(self):
        """Initialize the Redis client connection.

        This method must be called before using any other methods of this class.
        """
        self.client = await create_redis(f"redis://{CONFIG.REDIS_HOST}")

    async def update(self, image_path: Path | None) -> None:
        """Update the face mask image in Redis.

        Args:
            image_path: Path to the image file to use as a face mask.
                        If None, clears the current mask.
        """
        image_bytes = b""
        image_hash = b""
        if image_path is not None:
            image_bytes = image_path.read_bytes()
            image_hash = hashlib.md5(image_bytes).hexdigest()
        await self.client.set(self._KEY_BYTES, image_bytes)
        await self.client.set(self._KEY_MD5, image_hash)


face_mask = FaceMask()
