import threading as th
import yt_dlp
import os
from time import sleep

class Downloader:

	def __init__(self):
		
		self._worker = None

		self.progress = 0.0


	def get_progress(self, info: dict) -> None:

		if info['status'] == "downloading":

			total = info.get('total_bytes') or info.get('total_bytes_estimate')

			already_downloaded = info.get("downloaded_bytes", 0)

			if total:
				self.progress = (already_downloaded / total) * 100

		elif info['status'] == "finished":
			self.progress = 100.0

	def _loader(self, link:str, music_name: str) -> None:
		
		ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": music_name,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "progress_hooks": [self.get_progress],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True
        }

		try:

			with yt_dlp.YoutubeDL(ydl_opts) as ydl:
				ydl.download([link])
		except Exception as error:
			print(f"Erro: [{error}]", flush=True)

	def baixar(self, link: str, music_name: str) -> None:

		# Devemos verificar se já há uma baixando
		while self._worker:
			sleep(1) # Esperamos segundos enquanto o download anterior não for efetuado.


		# Iniciamos a thread de download
		self._worker = th.Thread(target=self._loader, args=(link, music_name), daemon=True)
		self._worker.start()


	def cancell(self):
		if self._worker:
			self._worker.join()
			self._worker = None

