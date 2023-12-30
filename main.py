import traceback
from threading import Thread
from io import BytesIO
from PIL import Image, ImageTk
import requests
import customtkinter as ctk
from pytube_service_class import *


# Downloader GUI Class
# Constructed with modifying blank main CTk app
class YouTubeDownloaderApp:
    # Constructs GUI and all widgets/elements on blank master CTk app
    def __init__(self, master: ctk.CTk) -> None:
        # Set appearance preferences
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Initialize root window
        self.root = master
        self.root.resizable(False, False)
        self.root.geometry("620x460")
        self.root.title("YouTube Video Downloader")

        # Initialize main frame
        self.main_frame = ctk.CTkFrame(master=self.root)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Set up title to appear in intro_label
        self.intro_label = ctk.CTkLabel(master=self.main_frame, text="PyTube Video Downloader",
                                        font=("Arial bold", 22), text_color="#00F904")
        self.intro_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Add void spacing label
        self.spacing_label = ctk.CTkLabel(master=self.main_frame, text="", height=20)
        self.spacing_label.grid(row=1, column=0)

        # Options in combo box
        options = ["Video as .mp4", "Video as .mp3", "Playlist as .mp4's", "Playlist as .mp3's"]
        # Initialize combo box and set visual parameters
        # The selection() method handles combo box input to update selected_option variable
        self.selected_option = ""
        self.option_box = ctk.CTkComboBox(master=self.main_frame, width=160, height=10,
                                          corner_radius=10, values=options,
                                          state="readonly", justify="center", font=("Arial bold", 14),
                                          text_color="black",
                                          fg_color="light green", button_color="light green",
                                          border_color="light green",
                                          dropdown_text_color="light green", command=self.selection)
        # Set initial instructing value
        self.option_box.set("Download Type")
        self.option_box.grid(row=2, column=0, sticky="w", padx=20)

        # Add 3 radio buttons for low, medium, and high quality video
        # Buttons placed vertically atop on another and aligned horizontally
        # Buttons update selected_quality class variable (set "low" by default)
        self.selected_quality = ctk.StringVar(value="low")
        self.low_quality_radio = ctk.CTkRadioButton(master=self.main_frame, text="Low Quality       ",
                                                    variable=self.selected_quality,
                                                    value="low",
                                                    font=("Arial bold", 12), text_color="light green")
        self.low_quality_radio.grid(row=2, column=1)
        self.medium_quality_radio = ctk.CTkRadioButton(master=self.main_frame, text="Medium Quality",
                                                       variable=self.selected_quality,
                                                       value="medium",
                                                       font=("Arial bold", 12), text_color="light green")
        self.medium_quality_radio.grid(row=3, column=1)
        self.high_quality_radio = ctk.CTkRadioButton(master=self.main_frame, text="High Quality      ",
                                                     variable=self.selected_quality,
                                                     value="high",
                                                     font=("Arial bold", 12), text_color="light green")
        self.high_quality_radio.grid(row=4, column=1)

        # URL entry space placed at the center of the screen below the selection options
        # Formatted and placeholder instruction value set
        self.url_entry = ctk.CTkEntry(master=self.main_frame, width=420, corner_radius=10, border_width=2,
                                      font=("Arial", 14), text_color="#00F904",
                                      placeholder_text="Enter YouTube Video or Playlist URL")
        self.url_entry.grid(row=5, column=0, pady=30, sticky="e")

        # Format download button and place to the right of entry field
        # Assign download_func command
        self.download_button = ctk.CTkButton(master=self.main_frame, text="Download", font=("Arial bold", 14),
                                             fg_color="light green", text_color="black",
                                             command=self.download_func)
        self.download_button.grid(row=5, column=1, sticky="w")

        # Declare indeterminate progressbar to serve as loading animation
        self.progressbar = ctk.CTkProgressBar(master=self.main_frame, mode="indeterminate", progress_color="#00F904",
                                              corner_radius=0)

        # Add error label below entry field, will display relevant error message as determined in download_func
        self.error_info_label = ctk.CTkLabel(master=self.main_frame, width=150, height=28, text="",
                                             font=("Arial bold", 16),
                                             text_color="red", bg_color="transparent")
        self.error_info_label.grid(row=6, column=0, columnspan=2)

        # Format and place video info label, stores both thumbnail image and text info
        self.video_label = ctk.CTkLabel(master=self.main_frame, image=None, text="", compound=ctk.LEFT,
                                        font=("Arial narrow", 17), text_color="#00F904", justify="left")
        self.video_label.grid(row=7, column=0, sticky="nw", padx=30, columnspan=2)

    # Selection function translates combo box choice to an easy to handle selected_option string
        # that corresponds to video/playlist as mp3/mp4
    def selection(self, choice: str) -> None:
        if choice == "Video as .mp4":
            self.selected_option = "v4"
        elif choice == "Video as .mp3":
            self.selected_option = "v3"
        elif choice == "Playlist as .mp4's":
            self.selected_option = "p4"
        elif choice == "Playlist as .mp3's":
            self.selected_option = "p3"

    # Considers selection options and calls relevant service class and info methods
    def download_content(self) -> None:
        try:
            # Gets video URL
            url = self.url_entry.get()
            # Depending on combo box and quality selection, calls relevant video/playlist - mp3/mp4 method
            # and passes relevant parameters
            # Displays thumbnail info
            # Depending on if video or playlist displays relevant info with respective info function
            if self.selected_option == "v4":
                download_as_mp4(url, self.selected_quality.get())
                self.display_video_info(url)
                self.display_thumbnail_from_url(get_thumbnail(url))
            elif self.selected_option == "v3":
                download_as_mp3(url)
                self.display_video_info(url)
                self.display_thumbnail_from_url(get_thumbnail(url))
            elif self.selected_option == "p4":
                download_playlist_as_mp4(url, self.selected_quality.get())
                self.display_playlist_info(url)
                self.display_thumbnail_from_url(get_thumbnail(url))
            elif self.selected_option == "p3":
                download_playlist_as_mp3(url)
                self.display_playlist_info(url)
                self.display_thumbnail_from_url(get_thumbnail(url))
            # If no combo box selection, display error without clearing entry field
            else:
                self.error_info_label.configure(text="Select a Download Type!")
        # In case of exception, request valid URL for the selected download type
        except Exception:
            self.error_info_label.configure(text="Enter a valid type URL!")
        # Upon completion, stop and hide progressbar
        # Re-enabled buttons
        # Clear link entry
        finally:
            self.progressbar.stop()
            self.progressbar.place_forget()
            self.download_button.configure(state="normal")
            self.url_entry.configure(state="normal")
            self.url_entry.delete(0, ctk.END)

    # Main download function, handles widgets during download state as well as download thread
    def download_func(self) -> None:
        # Start downloading process as a separate thread to avoid freezing
        download_thread = Thread(target=self.download_content, daemon=True)
        download_thread.start()
        # Disable download button and entry field
        self.download_button.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        # Place and start loading animation
        self.progressbar.place(x=200, y=270)
        self.progressbar.start()
        # Reset Error Message
        self.error_info_label.configure(text="")
        # Reset Info Message
        self.video_label.configure(image="", text="")
        # Update frame
        self.main_frame.update()

    # Displays thumbnail image from thumbnail URL in relevant label
    # Called upon in download_content to only display when download is complete
    def display_thumbnail_from_url(self, image_url: str) -> None:
        # Downloads and converts image data from JPEG URL
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        # Resizes image and converts to Tkinter appropriate image format
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        # Closes process
        img.close()

        # Configures label
        self.video_label.configure(image=img_tk)

    # Displays video info message in relevant label
    # Called upon in download_content to only display (if necessary) when download is complete
    def display_video_info(self, link: str) -> None:
        self.video_label.configure(text=f"   VIDEO DOWNLOADED TO DOWNLOADS FOLDER\n\n"
                                        f"   TITLE: {get_video_info(link)[0]} \n"
                                        f"   LENGTH: {get_video_info(link)[1]} seconds"
                                   )

    # Displays playlist info message in relevant label
    # Called upon in download_content to only display (if necessary) when download is complete
    def display_playlist_info(self, link: str) -> None:
        self.video_label.configure(text=f"   PLAYLIST DOWNLOADED TO "
                                        f"\n   '{get_playlist_info(link)[0].upper()}' FOLDER"
                                        f"\n   IN DOWNLOADS\n\n"
                                        f"   TITLE: {get_playlist_info(link)[0]} \n"
                                        f"   LENGTH: {get_playlist_info(link)[1]} videos"
                                   )

    # Execute and display GUI
    def mainloop(self) -> None:
        # PyTube updated when starting program
        update_pytube()
        # Display GUI
        self.root.mainloop()


# Main method constructs and runs YouTubeDownloaderApp with a CTk app as master
def main() -> None:
    app = ctk.CTk()
    YouTubeDownloaderApp(app).mainloop()


# Don't run main() if imported, only run if executed as script
if __name__ == "__main__":
    main()
