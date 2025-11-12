import traceback

from mpl_theme_tweaker.application import Application
from mpl_theme_tweaker.logger import log


def main():
    try:
        app = Application()
        app.run()
    except Exception as e:
        log.error(f"Application crashed: {e}")
        log.error(f"{'=' * 48}Traceback: \n{traceback.format_exc()}\n{'=' * 48}")


if __name__ == "__main__":
    main()
