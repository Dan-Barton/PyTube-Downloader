from tkinter.messagebox import showerror

import threading

from PyTubeAppClass import *

# Driver file to serve as entry point, creates and executes instance of YouTubeDownloaderApp

# Substitute method as threading.excepthook
# Designed to handle unexpected exceptions in download thread by displaying exception value in message box
def unexpectedError(args):
    showerror('Error', args.exc_value)

# Main method creates instance of YouTubeDownloaderApp "app" and runs it
def main() -> None:
    app = YouTubeDownloaderApp()
    app.run()

# Call main() method to construct and display GUI from PyTubeAppClass.py if run as script
# threading.excepthook specified
if __name__ == "__main__":
    threading.excepthook = unexpectedError
    main()
