import customtkinter as ctk
from pytube.exceptions import RegexMatchError, VideoUnavailable, AgeRestrictedError

from threading import Thread
import traceback

from PyTubeServiceModule import *
from config import *


"""
App GUI Class file
- Downloader GUI Class YouTubeDownloaderApp inherits from ctk.CTk as root window
- Constants used found in config.py
- Download methods used found in PyTubeServiceModule.py
- PyTube updated on run
"""

class YouTubeDownloaderApp(ctk.CTk):
    # Constructed with calling the constructor of the parent class (YouTubeDownloaderApp) such that it is the root
    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        # Set appearance preferences
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Set parent class root window params
        self.resizable(True, False)
        self.geometry(SCREEN_SIZE)
        self.minsize(WIDTH, HEIGHT)
        self.title(TITLE)

        # Initialize main frame with class root as parent to serve as staging ground for all widgets
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Set up title to appear in intro_label
        self.intro_label = ctk.CTkLabel(master=self.main_frame, text="PyTube Video Downloader",
                                        font=("Arial bold", 22), text_color=VERDANT_GREEN)
        self.intro_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Add void spacing label
        self.spacing_label = ctk.CTkLabel(master=self.main_frame, text="", height=20)
        self.spacing_label.grid(row=1, column=0)

        # Initialize combo box and set visual parameters
        # Combo box updates selected_option class variable
        self.selected_option = ctk.StringVar(value="")
        self.option_box = ctk.CTkComboBox(master=self.main_frame, width=160, height=10,
                                          corner_radius=10, values=DOWNLOAD_OPTIONS,
                                          state="readonly", justify="center", font=("Arial bold", 14),
                                          text_color="black", variable=self.selected_option,
                                          fg_color="light green", button_color="light green",
                                          border_color="light green",
                                          dropdown_text_color="light green")
        # Set initial instructing value and grid place combo box
        self.option_box.set("Download Type")
        self.option_box.grid(row=2, column=0, sticky="w", padx=20)

        # Add 3 radio buttons for low, medium, and high quality video
        # Buttons placed vertically atop on another and aligned horizontally
        # Buttons update selected_quality class variable (set "low" by default)
        self.selected_quality = ctk.StringVar(value="low")
        self.low_quality_radio = ctk.CTkRadioButton(master=self.main_frame, text="Low Quality          ",
                                                    variable=self.selected_quality,
                                                    value="low",
                                                    font=("Arial bold", 12), text_color="light green")
        self.low_quality_radio.grid(row=2, column=1, sticky="e")
        self.medium_quality_radio = ctk.CTkRadioButton(master=self.main_frame, text="Medium Quality",
                                                       variable=self.selected_quality,
                                                       value="medium",
                                                       font=("Arial bold", 12), text_color="light green")
        self.medium_quality_radio.grid(row=3, column=1, sticky="e", padx=10)
        self.high_quality_radio = ctk.CTkRadioButton(master=self.main_frame, text="High Quality         ",
                                                     variable=self.selected_quality,
                                                     value="high",
                                                     font=("Arial bold", 12), text_color="light green")
        self.high_quality_radio.grid(row=4, column=1, sticky="e")

        # URL entry space placed at the center of the screen below the selection options
        # Formatted and placeholder instruction value set
        self.url_entry = ctk.CTkEntry(master=self.main_frame, width=420, corner_radius=10, border_width=2,
                                      font=("Arial", 14), text_color=VERDANT_GREEN,
                                      placeholder_text="Enter YouTube Video or Playlist URL")
        self.url_entry.grid(row=5, column=0, pady=30, sticky="e")

        # Format download button and place to the right of entry field
        # Assign download_func command
        self.download_button = ctk.CTkButton(master=self.main_frame, text="Download", font=("Arial bold", 14),
                                             fg_color="light green", text_color="black",
                                             command=self.download_func)
        self.download_button.grid(row=5, column=1, sticky="w")

        # Declare indeterminate progressbar to serve as loading animation
        self.progressbar = ctk.CTkProgressBar(master=self.main_frame, mode="indeterminate",
                                              progress_color=VERDANT_GREEN, corner_radius=0)

        # Add error label below entry field, to be configured to display relevant error message
        self.error_info_label = ctk.CTkLabel(master=self.main_frame, width=150, height=28, text="",
                                             font=("Arial bold", 16),
                                             text_color="red", bg_color="transparent")
        self.error_info_label.grid(row=6, column=0, columnspan=2)

        # Format and place video info label, will store both thumbnail image and text info
        self.video_label = ctk.CTkLabel(master=self.main_frame, image=None, text="", compound=ctk.LEFT,
                                        font=("Arial narrow", 17), text_color=VERDANT_GREEN, justify="left")
        self.video_label.grid(row=7, column=0, padx=30, columnspan=2)

    # Main download function, handles widgets during download state as well as download thread
    def download_func(self) -> None:
        # Start download process as a separate thread to avoid freezing
        download_thread = Thread(target=self.download_content, daemon=True)
        download_thread.start()

        # Handle GUI elements during download
        self.on_download_start()

    # Handle GUI elements during download
    def on_download_start(self) -> None:
        # Disable download button and entry field
        self.download_button.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        # Place and start loading animation
        self.progressbar.grid(row=7, column=0, columnspan=2)
        self.progressbar.start()
        # Reset Error Message
        self.error_info_label.configure(text="")
        # Reset Info Message
        self.video_label.configure(image="", text="")

        # Update frame
        self.main_frame.update()

    # Clean up GUI after download
    def on_download_end(self) -> None:
        # Stop and hide progressbar
        self.progressbar.stop()
        self.progressbar.grid_remove()
        # Re-enabled fields
        self.download_button.configure(state="normal")
        self.url_entry.configure(state="normal")
        # Clear link entry
        self.url_entry.delete(0, ctk.END)

        # Update frame
        self.main_frame.update()

    # Considers selection options and calls relevant download and error methods
    def download_content(self) -> None:
        try:
            # Store current URL, quality, and download type
            url = self.url_entry.get()
            quality = self.selected_quality.get()
            selected_option = self.selected_option.get()

            # Class method contains logic to download videos and display video info
            if selected_option in [DOWNLOAD_OPTION_1_VIDEO_MP4, DOWNLOAD_OPTION_2_VIDEO_MP3]:
                self.download_video(url, quality, selected_option)
            # Class method contains logic to download playlists and display playlist info
            elif selected_option in [DOWNLOAD_OPTION_3_PLAYLIST_MP4, DOWNLOAD_OPTION_4_PLAYLIST_MP3]:
                self.download_playlist(url, quality, selected_option)
            # Display error if no download type selected
            else:
                self.display_error("Select a Download Type!")
        except AgeRestrictedError:
            self.display_error("Content is Age Restricted")
        # Display invalid URL error (video URL error, playlist URL error) and Content Unavailable error message
        except (RegexMatchError, KeyError, VideoUnavailable):
            self.display_error("Enter a Valid Type URL and Ensure Content is Available")
        # Display error message if selected quality not available for content
        except AttributeError:
            self.display_error("Quality not Available")
        # Clean up GUI after download
        finally:
            self.on_download_end()

    # Handles video mp4/mp3 download in specified quality
    def download_video(self, link: str, quality: str, selected_option: str) -> None:
        # bool if mp4 download
        is_mp4 = selected_option == DOWNLOAD_OPTION_1_VIDEO_MP4
        # Call video as mp4 or mp3 depending on selection
        download_as_mp4(link, quality) if is_mp4 else download_as_mp3(link)
        # Display thumbnail and video info
        self.display_video_info(link)
        self.display_thumbnail(link)

    # Handles playlist mp4/mp3 download in specified quality
    # download_video() logic modified to fit playlist methods
    def download_playlist(self, link: str, quality: str, selected_option: str) -> None:
        is_mp4 = selected_option == DOWNLOAD_OPTION_3_PLAYLIST_MP4
        download_playlist_as_mp4(link, quality) if is_mp4 else download_playlist_as_mp3(link)
        playlist_info = get_playlist_info(link)
        # Specify folder name content type suffix to display in info label
        folder_name = f"{playlist_info[0]} ({'mp4' if is_mp4 else 'mp3'})"
        self.display_playlist_info(link, folder_name)
        self.display_thumbnail(link)

    # Configures error label with passed message
    def display_error(self, message: str) -> None:
        self.error_info_label.configure(text=message)

    # Displays thumbnail image for content in relevant label
    def display_thumbnail(self, link: str) -> None:
        # Call service module method to return thumbnail image
        self.video_label.configure(image=get_thumbnail(link))

    # Displays video info message in relevant label
    def display_video_info(self, link: str) -> None:
        self.video_label.configure(text=f"   VIDEO DOWNLOADED TO DOWNLOADS FOLDER\n\n"
                                        f"   TITLE: {get_video_info(link)[0]} \n"
                                        f"   LENGTH: {get_video_info(link)[1]}"
                                   )

    # Displays playlist info message in relevant label
    def display_playlist_info(self, link: str, folder_name: str) -> None:
        self.video_label.configure(text=f"   PLAYLIST DOWNLOADED TO "
                                        f"\n   '{folder_name}' FOLDER"
                                        f"\n   IN DOWNLOADS\n\n"
                                        f"   TITLE: {get_playlist_info(link)[0]} \n"
                                        f"   LENGTH: {get_playlist_info(link)[1]} videos"
                                   )

    # Update PyTube and run GUI
    def run(self) -> None:
        # PyTube updated when starting program
        update_pytube()
        # Display GUI
        self.mainloop()
