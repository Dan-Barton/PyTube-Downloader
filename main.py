from PyTubeAppClass import *

# Driver file to serve as entry point, creates and executes instance of YouTubeDownloaderApp

# Main method creates instance of YouTubeDownloaderApp "app" and runs it
def main() -> None:
    app = YouTubeDownloaderApp()
    app.run()

# Call main() method to construct and display GUI from PyTubeAppClass.py if run as script
if __name__ == "__main__":
    main()
