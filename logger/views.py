from django.http import HttpResponse
import os
import logging
import time

def do_log(request):
    # monkeypatch emit to our version, which behaves identically except for a delay before the write
    logging.StreamHandler.emit = stream_handler_emit

    pid = os.getpid()
    logger = logging.getLogger("logger.custom")

    logger.info(f"[{pid:08}] Message 1")
    logger.info(f"[{pid:08}] Message 2")

    return HttpResponse("Success! Response from /do_log.")

def stream_handler_emit(self, record):
    try:
        msg = self.format(record)
        stream = self.stream
        # issue 35046: merged two stream.writes into one.
        time.sleep(10)
        stream.write(msg + self.terminator)
        self.flush()
    except RecursionError:  # See issue 36272
        raise
    except Exception:
        self.handleError(record)
