import cv2
import numpy as np
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

from config import CONFIG
from maks import face_mask
from utils import get_logger


class FaceSwapper:
    current_mask: np.ndarray | None = None
    current_mask_hash: str | None = None

    def __init__(self):
        self._logger = get_logger(self.__class__.__name__)
        self.face_extractor = FaceAnalysis(
            name="buffalo_l",
            providers=["CUDAExecutionProvider"],
            root=CONFIG.MODELS_PATH.parent,
            allowed_modules=['detection', 'recognition']
        )
        det_size = (CONFIG.DET_SIZE_W, CONFIG.DET_SIZE_H)
        self.face_extractor.prepare(ctx_id=0, det_thresh=CONFIG.DET_THRESH, det_size=det_size)
        self.swapper = get_model(
            name=CONFIG.MODELS_PATH.joinpath('inswapper_128.onnx').as_posix(),
            providers=["CUDAExecutionProvider"]
        )

    def set_face_mask(self, image_bytes: bytes | None, md5hash: str | None = None) -> None:
        if not image_bytes:
            self.current_mask = None
        else:
            image_array = np.frombuffer(image_bytes, dtype=np.uint8)
            target_img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            faces = self.face_extractor.get(target_img, max_num=1)
            if not faces:
                self._logger.error(f'The face has not been detected on mask {md5hash}!')
                self.current_mask = None
            else:
                self.current_mask = faces[0]

        self.current_mask_hash = md5hash

    def swap_face(self, source_img: np.ndarray) -> np.ndarray:
        final_img = source_img

        actual_md5_hash = face_mask.get_md5()
        if actual_md5_hash != self.current_mask_hash:
            image_bytes = face_mask.get_bytes()
            self.set_face_mask(image_bytes=image_bytes, md5hash=actual_md5_hash)

        if self.current_mask is not None:
            faces = self._extract_face(source_img)
            if faces:
                final_img = self._swap(source_img, faces[0])

        return final_img

    def _extract_face(self, source_img: np.ndarray) -> np.ndarray:
        return self.face_extractor.get(source_img, max_num=1)

    def _swap(self, source_img: np.ndarray, face) -> np.ndarray:
        try:
            return self.swapper.get(source_img, face, self.current_mask)
        except Exception as e:
            self._logger.error(f"Swap error: {e}")