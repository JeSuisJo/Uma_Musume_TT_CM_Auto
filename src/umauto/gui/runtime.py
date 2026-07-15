"""Run a CLI feature from the GUI without touching feature code.

Features ``print`` progress and occasionally call ``input()``. For the duration
of a run we redirect that console (see :func:`_patched_console`): stdout becomes
a polled log, ``input()`` becomes a modal prompt, ``os.system("cls")`` clears the
log, and a stop flag checked before each screenshot lets Stop abort the run.

Only one run happens at a time, so a single module-level :class:`Session` holds
the state shared with the API layer.
"""

import builtins
import collections
import contextlib
import io
import os
import sys
import threading


class _LogWriter(io.TextIOBase):
    """A file-like object that funnels ``print`` into the session log."""

    def __init__(self, session):
        self._session = session
        self._pending = ""

    def write(self, text):
        # Buffer partial lines so a bare ``print(end="")`` progress update does
        # not spam the log until a newline arrives.
        self._pending += text
        while "\n" in self._pending:
            line, self._pending = self._pending.split("\n", 1)
            self._session.log(line)
        return len(text)

    def flush(self):
        if self._pending:
            self._session.log(self._pending)
            self._pending = ""


class Session:
    """Shared state between the worker thread and the pywebview API."""

    def __init__(self):
        self._lock = threading.Lock()
        self._log = collections.deque()
        self.running = False
        self.stop_requested = False
        self.last_error = None
        # Pending input() prompt handshake.
        self._prompt_message = None
        self._prompt_answer = None
        self._prompt_event = threading.Event()
        self._thread = None

    def log(self, line):
        with self._lock:
            self._log.append(str(line))

    def drain_log(self):
        with self._lock:
            lines = list(self._log)
            self._log.clear()
        return lines

    def clear_log(self):
        with self._lock:
            self._log.clear()
            self._log.append("\x00clear")  # sentinel: tell the UI to wipe

    def pending_prompt(self):
        return self._prompt_message

    def _ask(self, message):
        """Block the worker until the UI answers (or Stop is pressed)."""
        if self.stop_requested:
            raise StopScriptProxy()
        self._prompt_answer = None
        self._prompt_event.clear()
        self._prompt_message = str(message)
        self._prompt_event.wait()
        self._prompt_message = None
        if self.stop_requested:
            raise StopScriptProxy()
        return self._prompt_answer if self._prompt_answer is not None else ""

    def answer_prompt(self, value):
        self._prompt_answer = value
        self._prompt_event.set()

    def request_stop(self):
        self.stop_requested = True
        # Release a worker that is blocked waiting on a prompt.
        self._prompt_event.set()

    def start(self, key):
        if self.running:
            return False
        self.running = True
        self.stop_requested = False
        self.last_error = None
        self._thread = threading.Thread(
            target=self._run, args=(key,), daemon=True
        )
        self._thread.start()
        return True

    def _run(self, key):
        # Imported lazily: these modules read config.json at import time, so
        # they must not load until a config exists and a run is requested.
        from ..driver import StopScript, driver
        from ..features.registry import FEATURES

        feature = FEATURES.get(key)
        if feature is None:
            self.log(f"Unknown mode: {key}")
            self.running = False
            return

        writer = _LogWriter(self)
        with _patched_console(self, writer, driver, StopScript):
            try:
                driver.ensure_ready()
                args = feature.prepare() if feature.prepare else ()
                driver.focus()
                feature.run(*args)
                self.log("")
                self.log("Done.")
            except (StopScript, StopScriptProxy) as exc:
                self.log("")
                self.log(f"Stopped: {exc}" if str(exc) else "Stopped.")
            except Exception as exc:  # surface crashes in the log, not a console
                self.last_error = str(exc)
                self.log("")
                self.log(f"Error: {exc}")
            finally:
                writer.flush()
                self.running = False


class StopScriptProxy(Exception):
    """Local stop signal used before the real driver StopScript is importable.

    Raised by prompt cancellation and the screenshot guard; caught alongside
    the driver's ``StopScript`` so both read as a clean user-initiated stop.
    """

    def __init__(self, message="Stopped by user"):
        super().__init__(message)


@contextlib.contextmanager
def _patched_console(session, writer, driver, StopScript):
    """Temporarily reroute stdout, input, cls and screenshots to the session."""
    real_stdout = sys.stdout
    real_input = builtins.input
    real_system = os.system
    real_screenshot = driver._screenshot

    def gui_input(prompt=""):
        if prompt:
            writer.flush()
            session.log(str(prompt))
        return session._ask(prompt or "…")

    def gui_system(command):
        # Swallow the console-clear the runners issue between iterations.
        if str(command).strip().lower() in ("cls", "clear"):
            session.clear_log()
            return 0
        return real_system(command)

    def guarded_screenshot(dest="temp.png"):
        if session.stop_requested:
            raise StopScript("Stopped by user")
        return real_screenshot(dest)

    sys.stdout = writer
    builtins.input = gui_input
    os.system = gui_system
    driver._screenshot = guarded_screenshot
    try:
        yield
    finally:
        sys.stdout = real_stdout
        builtins.input = real_input
        os.system = real_system
        driver._screenshot = real_screenshot


# Single shared session for the whole GUI process.
session = Session()
