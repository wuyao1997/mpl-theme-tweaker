import contextlib
import io
import sys
import warnings
from PIL import Image

from matplotlib.figure import Figure


@contextlib.contextmanager
def suppress_stderr():
    original_stderr = sys.stderr
    sys.stderr = open("nul", "w")  # Linux/macOS '/dev/nul', Windows 'nul'
    try:
        yield
    finally:
        sys.stderr.close()
        sys.stderr = original_stderr


def Figure2Image(fig: Figure) -> Image.Image:
    buf = io.BytesIO()
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", category=UserWarning, message=".*missing from font.*"
        )

        # Suppress the stderr output of font-related errors
        with suppress_stderr():
            fig.savefig(buf, format="png")

    buf.seek(0)
    img = Image.open(buf)
    return img
