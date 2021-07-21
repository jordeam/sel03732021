import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    # Uma classe semelhante a um evento que sinaliza a todos os clientes ativos quando um novo quadro é acessível.
    def __init__(self):
        self.events = {}

    def wait(self):
        # Invocado da thread dos clientes para esperar o novo quadro. 
        ident = get_ident()
        if ident not in self.events:
            # Este é um cliente novo
            # Adiciona uma entrada no self.events dict
            # Cada entrada possui dois elementos, threading.Event() e timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        # Invocado pela thread da câmera quando um novo quadro esta disponível.
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # Se o client's event não está setado, seta ele
                # Atualiza o timestamp
                event[0].set()
                event[1] = now
            else:
                # Se o client's event já está setado, significa que
                # ele não processou um frame anterior, e se
                # o evento fica setado por mais que 5 segundos, o programa
                # assume que o client não está presente e é removido
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        # Invoca a thread de cada cliente depois que o quadro for processado.
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # background thread -> lê os frames da câmera. 
    frame = None  # current frame -> está armazenado aqui pela background thread.
    last_access = 0  # horário em que houve o último acesso do cliente à câmera.
    event = CameraEvent()

    def __init__(self):
        # Inicia a thread da câmera de fundo, se ainda não estiver em execução.
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # Inicia o quadro da background thread.
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # Espera até que os quadros estejam disponível. 
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        # Retorna o quadro atual da câmera.
        BaseCamera.last_access = time.time()

        # Espera pelo sinal da thread da câmera.
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        # Gerador que retorna os quadros da câmera. 
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        # Background thread câmera.
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # Envie o sinal para os clientes.
            time.sleep(0)

            # Se não houver clientes requisitando quadros nos últimos 10 segundos então para a thread
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None
