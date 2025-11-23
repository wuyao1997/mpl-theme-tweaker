import io
import warnings
from PIL import Image

from matplotlib.figure import Figure


def Figure2Image(fig: Figure) -> Image.Image:
    buf = io.BytesIO()
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", category=UserWarning, message=".*missing from font.*"
        )
        fig.savefig(buf, format="png")
    buf.seek(0)
    img = Image.open(buf)
    return img
