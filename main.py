from tkinter.messagebox import showerror

import threading
import contextlib

from PyTubeAppClass import *

# Driver file to serve as entry point, creates and executes instance of YouTubeDownloaderApp

# Substitute method as threading.excepthook
# Designed to handle unexpected exceptions in download thread by displaying exception value in message box
def unexpectedError(args: threading.ExceptHookArgs) -> None:
    showerror('Error', args.exc_value)

# Main method creates instance of YouTubeDownloaderApp "app" and runs it
def main() -> None:
    app = YouTubeDownloaderApp()
    app.run()


# Call main() method to construct and display GUI from PyTubeAppClass.py if run as script
if __name__ == "__main__":
    # threading.excepthook specified
    threading.excepthook = unexpectedError
    # Run main and write (Moviepy) output to null file (necessary to package windowed executable)
    with contextlib.redirect_stdout(open(os.devnull, 'w')):
        main()
