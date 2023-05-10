import os
import sys
import tkinter
import tkinter.messagebox
from tkinter import filedialog

import customtkinter
from pytube import YouTube


# Системные настройки
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        def on_progress(stream, chunk, bytes_remaining):
            """
            Заполняет и обновляет полосу прогресса
            """
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            per = str(int(percentage_of_completion))
            self.progress_percentage.configure(text=per + "%")
            self.progress_percentage.update()

            # обновление полосы загрузки
            self.progress_bar.set(float(percentage_of_completion) / 100)

        def start_download():
            """
            Загружает видео по ссылке YouTube
            """
            try:
                # Вызывает окно выбора директории
                yt_link = self.link.get()
                path_to_file = filedialog.askdirectory()
                yt_object = YouTube(yt_link, on_progress_callback=on_progress)
                self.video = yt_object.streams.get_highest_resolution()
                self.title.configure(text=f"Видео: {yt_object.title[:25]}...", text_color="white")
                self.finish_label.configure(text="")

                self.video.download(output_path=path_to_file)
                self.finish_label.configure(text="Download complete", text_color="green")

            except:
                self.finish_label.configure(text="Download Error", text_color="red")

        # окно нашего приложения
        self.title("YouTube Downloader")
        self.geometry(f"{480}x{240}")

        # Добавление и размещение UI элементов
        self.title = customtkinter.CTkLabel(self, text="Вставьте сcылку YouTube")
        self.title.pack(padx=10, pady=10)

        # Вставка поля для ссылки
        self.url_var = tkinter.StringVar()
        self.link = customtkinter.CTkEntry(self, width=350, height=40, textvariable=self.url_var)
        self.link.pack()

        # Кнопка "Download"
        self.download = customtkinter.CTkButton(self, text="Download", command=start_download)
        self.download.pack(padx=10, pady=10)

        # # Кнопка "Stop"
        # self.stop = customtkinter.CTkButton(self, text="Stop", command=stop_download)
        # self.stop.pack(padx=10, pady=10)

        # Полоса прогресса загрузки
        self.progress_percentage = customtkinter.CTkLabel(self, text="0%")
        self.progress_percentage.pack()
        self.progress_bar = customtkinter.CTkProgressBar(self, width=200,)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=10, pady=10)

        # Окончание загрузки
        self.finish_label = customtkinter.CTkLabel(self, text="")
        self.finish_label.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
