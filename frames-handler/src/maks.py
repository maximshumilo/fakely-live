from redis import Redis

from config import CONFIG


class FaceMask:

    _KEY_BYTES: str = 'mask_bytes'
    _KEY_MD5: str = 'mask_md5'

    def __init__(self):
        self.client = Redis(host=CONFIG.REDIS_HOST, port=6379, db=0)

    def get_bytes(self) -> bytes:
        return self.client.get(self._KEY_BYTES)

    def get_md5(self) -> str:
        return self.client.get(self._KEY_MD5).decode()

face_mask = FaceMask()