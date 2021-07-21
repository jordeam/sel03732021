import io
import time
import picamera
from . import base_camera

class Camera(base_camera.BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # Tempo para a câmera iniciar 
            time.sleep(2)
            camera.rotation = 180

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # Retornar quadro atual
                stream.seek(0)
                yield stream.read()

                # Redefine o fluxo para o próximo quadro
                stream.seek(0)
                stream.truncate()
