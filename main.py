from PyTubeAppClass import *

# DRIVER FILE

# Main method creates instance of YouTubeDownloaderApp "app" and runs it
def main() -> None:
    app = YouTubeDownloaderApp()
    app.run()

# Call main() method to construct and display GUI from PyTubeAppClass.py if run as script
if __name__ == "__main__":
    main()
