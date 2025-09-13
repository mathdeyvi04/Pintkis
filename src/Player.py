import pygame as pyg
import threading as th
from time import sleep
from pprint import pprint


class Player:
	"""
	Responsável por gerir as músicas e todas as funcionalidades relacionadas.
	"""

	TIME_DELAY = 0.1

	def __init__(self):

		self._thread = None
		self._is_running = th.Event()
		self._paused = th.Event()
		self._music_is_set = th.Event()
		self.mode_infinity = True
		self.forced_stop = False

		self.is_equal_to_the_last_music = False
		self.music_to_be_played = None
		self.register = {
			# Ditaremos um ranking de tocadas a partir desse dicionário
		}

		# Apenas para não ficarmos digitando muito
		self.manager = pyg.mixer.music

		pyg.mixer.init()


	def _playing(self):

		# Enquanto estiver ativa
		while self._is_running.is_set():

			# Espera até o usuário selecione uma música
			self._music_is_set.wait()

			# Como fomos liberamos, podemos limpar a flag
			self._music_is_set.clear()

			# Devemos carregá-la, mas para evitar utilizar mais memória desnecessariamente, 
			# vamos utilizar outra flag mais simples.
			# Caso não seja igual a música anterior, a carregamos
			if not self.is_equal_to_the_last_music:

				print(f"Vou carregar a música: {self.music_to_be_played}")
				try:

					self.manager.load(self.music_to_be_played)
				except:

					print("Música não é tocável.")
					continue

			# Colocamos a música para tocar
			self.manager.play()

			print("Coloquei para tocar...")
			# Enquanto a música estiver tocando e a thread estiver ligada
			while self.manager.get_busy() and self._is_running.is_set():

				# Devemos fornecer a possibilidade de pause
				if self._paused.is_set():

					self.manager.pause()

					while self._paused.is_set() and self._is_running.is_set():
						sleep(Player.TIME_DELAY)

					self.manager.unpause()

				# Salvamos os registros
				self.register[
					self.music_to_be_played
				] = round(
					self.register.get(self.music_to_be_played, 0) + Player.TIME_DELAY,
					3
				)
				sleep(Player.TIME_DELAY)

			# Se estamos no modo infinito e não foi uma parada forçada
			# Então a música parou naturalmente e devemos iniciá-la de novo
			if self.mode_infinity and not self.forced_stop:

				self.is_equal_to_the_last_music = True
				self._music_is_set.set()

			# Independente se foi forçado, acabou
			self.forced_stop = False



	def set_music(self, music_desired: str):

		# Caso ela estiver tocando
		if self.manager.get_busy():

			# Devemos interromper
			self.manager.stop()
			self.forced_stop = True

		if self._paused.is_set():

			# Então devemos retirar do loop de pause
			self._paused.clear()
			# E parar a música que estava tocando
			self.manager.stop() 
			self.forced_stop = True

		# Apenas verificando se são iguais
		if self.music_to_be_played == music_desired:
			self.is_equal_to_the_last_music = True
		else:
			self.is_equal_to_the_last_music = False
			self.music_to_be_played = music_desired

		self._music_is_set.set()  # Deve ser a última linha dessa função

	def start(self):

		# Impedimos que há mais de uma thread tocadora ativa.
		if self._thread and self._thread.is_alive():
			return 

		self._is_running.set()
		self._paused.clear()
		self._music_is_set.clear()
		self._thread = th.Thread(
								target=self._playing,
								daemon=True
								)
		self._thread.start()

	def stop(self):

		print("Tentando encerrar...")
		self._is_running.clear()
		self._music_is_set.set()
		self._thread.join()
		pyg.mixer.quit()
		pprint(self.register)

	def pause(self):
		self._paused.set()

	def resume(self):
		self._paused.clear()

	def is_paused(self):
		return self._paused.is_set()


























