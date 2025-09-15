## @file UserInterface.py
## @brief Agrupa as responsabilidades de comunicação usuário-sistema
from blessed import Terminal
from Player import Player
from Downloader import Downloader
from shutil import rmtree
from time import sleep
from tqdm import tqdm
import os

class UserInterface:

	## @brief Classe representadora da interface
	def __init__(
		self
	):
		self._term = Terminal()
		self._is_playing = False
		self.root_music = "Músicas"
		self.mode_expanded = False

		# Obtém as músicas presentes em cada pasta
		self.playlist: dict  = self._get_playables()
		# Salvará a ordenação de apresentação das músicas.
		self.idx_order: dict = self._calculate_specials()	
		# Iniciamos sempre na coluna de pastas, os seguintes se relacionam apenas com o texto
		self.is_folder = True
		self.idx_total_folder = 0
		self.idx_total_file = 0
		self.idx_folder_select = 0
		self.idx_file_select  = 0

		self.folder_select = None
		self.file_select = None

		# Nosso reprodutor
		self.player = Player()
		self.player.start()

		# Nosso downloader
		self.downloader = Downloader()

		print(self._term.clear, end="")

	## @brief Responsável por obter lista de músicas existentes
	## @details
	## Obtemos todas as músicas presentes em cada playlist. A ordenação deve acontecer em etapas posteriores.
	def _get_playables(self) -> dict:

		# Verificamos se pasta de músicas existe.
		if not os.path.isdir(self.root_music):
			os.mkdir(self.root_music)
			return {}

		return {
			subplaylist: [
				music.replace(".mp3", "") for music in os.listdir(os.path.join(self.root_music, subplaylist)) if music.endswith(".mp3")
			] for subplaylist in os.listdir(self.root_music)
		}

	## @brief Calculará os índices das músicas a serem exibidas primeiro.
	## @details
	## Fornecerá uma lógica para ordenação das músicas dentro de suas respectivas pastas.
	def _calculate_specials(self) -> dict:

		# Apenas a primeira
		return {
			subplaylist: 0 for subplaylist in self.playlist if self.playlist[subplaylist]
		}

	## @brief Responsável por apresentar cabeçalho de entrada e de saída.
	## @param switch_phase Flag de operação para sabermos se estamos na entrada ou saída
	def draw_headers(
		self,
		switch_phase: bool
	) -> None:
		if switch_phase:
			# Devemos apresentar o cabeçalho
			print(self._term.gray60("-" * self._term.width))
			print(self._term.bold_blue("Pintkis"))
		else:
			print(self._term.gray60("-" * self._term.width))

	## @brief Responsável por apresentar a playlist de forma satisfatória.
	def draw_playlist(self) -> None:

		# Por conseguinte, ainda conseguimos definir a cor da tabela
		pp = lambda string="", end="\n": print(self._term.seashell2(string), end=end)
		pp_special = lambda string="": print(self._term.italic(self._term.purple(string)), end="")  # Para o especial

				
		# Espaços que preencheremos ao redor da palavra
		space_container = [10, 20 if self.mode_expanded else 39]

		pp()

		#####################################################
		# Vamos precisar montar 'from scratch' a fim de possuir
		# mais poder de customização. Prezaremos pela escalabilidade.
		#####################################################

		titulos = ["Playlist", "Músicas"]

		# Corrigimos os nomes para ter tamanho suficiente para todas
		titulos = [
			title.center(length_space_container, " ") for title, length_space_container in zip(titulos, space_container)
		]

		# Vamos montar o header da tabela
		length = sum(
			len(title) for title in titulos
		) + 1
		pp(
			f"+{'-' * length}+"
		)
		for title in titulos:
			pp(
				f"|{title}",
				end=""
			)
		pp(
			f"|\n+{'-' * length}+"
		)

		# Apenas para os testes: 

		self.idx_total_file = 0
		self.idx_total_folder = 0
		for folder in self.playlist:

			# Se estamos iterando sobre as pastas
			# E estamos na pasta selecionada
			if self.is_folder and self.idx_total_folder == self.idx_folder_select:

				pp(f"|", end="")
				pp_special(folder.center(space_container[0], " "))
				pp(f"|", end="")

				self.folder_select = folder
				self.file_select = None
			else:

				pp(f"|{folder.center(space_container[0], ' ')}|", end="")

			if self.mode_expanded:

				pp(f"{('v' if len(self.playlist[folder]) else '<').center(space_container[1])}|")
				pp(
					f"+{'-' * length}+"
				)

				for file in self.playlist[folder]:

					pp(f"|{' '.center(space_container[0])}|", end="")

					if not self.is_folder and self.idx_total_folder == self.idx_folder_select:

						if self.idx_total_file == self.idx_file_select:
							# Vamos apresentar o especial

							self.file_select = file
							pp_special(file.center(space_container[1], " "))
							pp("|")

						else:
							pp(f"{file.center(space_container[1], " ")}|")

						self.idx_total_file += 1
					else:

						pp(f"{file.center(space_container[1], " ")}|")
					
					pp(
						f"+{'-' * length}+"
					)
			else:

				# Devemos imprimir apenas a selecionada e colocar as adjacentes sombreadas.
				if not len(self.playlist[folder]):
					pp(f"{'<'.center(space_container[1], ' ')}|")
				else:
					# Garantimos que há algo a ser colocado
					
					files_list = [
						self.playlist[folder][self.idx_order[folder] - 1] if self.idx_order[folder] != 0 else "",
						self.playlist[folder][self.idx_order[folder]],
						self.playlist[folder][self.idx_order[folder] + 1] if self.idx_order[folder]+1 != len(self.playlist[folder]) else ""
					]

					for index, file in enumerate(files_list):
						if not self.is_folder and self.idx_total_folder == self.idx_folder_select and index == 1:
							pp_special(f"{file.center(space_container[1] // 3, ' ')}")
							self.file_select = file
						else:
							pp(f"{file.center(space_container[1] // 3, ' ')}", end="")

					pp("|")

				pp(
					f"+{'-' * length}+"
				)

			self.idx_total_folder += 1

	## @brief Responsável por apresentar configurações específicas
	def draw_modes(self) -> None:

		pp = lambda string="", end="\n": print(self._term.seashell2(string), end=end)
		pp_special = lambda string="": print(self._term.italic(self._term.purple(string)), end="")  # Para o especial

		pp(self._term.seashell2(f"Repetições: {'infinity' if self.player.mode_infinity else 'one'} (TAB to change)"))

	def draw_bar_progress(self) -> None:

		with tqdm(total=100) as pbar:

			print("Baixando...  ", flush=True, end="")
 
			while self.downloader.progress < 100:
				sleep(0.5)

			self.downloader.progress = 0
			self.downloader.cancell()
			self.playlist: dict  = self._get_playables()
			# Salvará a ordenação de apresentação das músicas.
			self.idx_order: dict = self._calculate_specials()	


	def criar_remover_subplaylist(self, decisao: bool) -> None:

		if decisao:
			print("Nome da PLaylist: ", flush=True, end="")

			folder_name = ""
			while True:

				key = self._term.inkey()

				if key.name == "KEY_ENTER" and folder_name:
					break 

				elif key.name == "KEY_ESCAPE":
					return None

				elif key.name == "KEY_BACKSPACE":

					if folder_name:
						folder_name = folder_name[:-1]
						print(self._term.move_left + " " + self._term.move_left, end="", flush=True)
				else:
					folder_name += key
					print(key.name, end="", flush=True)

			if folder_name:
				os.makedirs(os.path.join(self.root_music, folder_name))
				self.playlist: dict  = self._get_playables()
				# Salvará a ordenação de apresentação das músicas.
				self.idx_order: dict = self._calculate_specials()
		else:

			print(f"Deseja remover mesmo: {self.folder_select}?(ESC Nega)", flush=True, end="")

			if not self._term.inkey().name == "KEY_ESCAPE":
				# Então removemos
				rmtree(os.path.join(self.root_music, self.folder_select))
				self.playlist: dict  = self._get_playables()
				# Salvará a ordenação de apresentação das músicas.
				self.idx_order: dict = self._calculate_specials()

	def baixar_musica(self) -> None:

		print("Insira o link: ", end="", flush=True)
		link = ""
		while True:

			key = self._term.inkey()

			if key.name == "KEY_ENTER" and link:
				break

			elif key.name == "KEY_ESCAPE":
				return None

			elif key.name == "KEY_BACKSPACE":
				if link:
					link = link[:-1]
					print(self._term.move_left + " " + self._term.move_left, end="", flush=True)

			else:
				link += key 
				print(key, end="", flush=True)

		print(flush=True)
		print("Insira o nome: ", end="", flush=True)
		nome = ""
		while True:
			key = self._term.inkey()

			if key.name == "KEY_ENTER" and nome:
				break

			elif key.name == "KEY_ESCAPE":
				return None

			elif key.name == "KEY_BACKSPACE":
				if nome:
					nome = nome[:-1]
					print(self._term.move_left + " " + self._term.move_left, end="", flush=True)

			else:
				nome += key 
				print(key, end="", flush=True)

		print(flush=True)

		self.downloader.baixar(
								link,
								os.path.join(self.root_music, self.folder_select, nome)
							  )

		self.draw_bar_progress()

	## @brief Responsável por apresentar o menu e obter as interações
	def mainloop(self) -> None:	

		with self._term.cbreak(), self._term.hidden_cursor():

			key = None

			while key != 'q':
				self.draw_headers(True)

				self.draw_playlist()
				self.draw_modes()
				key = self._term.inkey()

				# Faremos o controle da interface
				if key.name == "KEY_DOWN" or key == "s":

					if self.is_folder:
						self.idx_folder_select = (self.idx_folder_select + 1) % self.idx_total_folder
					else:
						if self.idx_total_file != 0:
							self.idx_file_select = (self.idx_file_select + 1) % self.idx_total_file

				elif key.name == "KEY_UP" or key == "w":
					
					if self.is_folder:
						self.idx_folder_select = (self.idx_folder_select - 1) % self.idx_total_folder
						print(self._term.clear, end="")
					else:
						if self.idx_total_file != 0:
							self.idx_file_select = (self.idx_file_select - 1) % self.idx_total_file

				elif (key.name == "KEY_RIGHT" or key == "d") and not self.is_folder:

					if not self.mode_expanded and not self.is_folder:
						self.idx_order[self.folder_select] = (self.idx_order[self.folder_select] + 1) % len(self.playlist[self.folder_select])

				elif (key.name == "KEY_LEFT" or key == "a") and not self.is_folder:

					if not self.mode_expanded:
						self.idx_order[self.folder_select] = (self.idx_order[self.folder_select] - 1) % len(self.playlist[self.folder_select])

				elif key == " ":
					# Caso a pasta não possua músicas
					self.is_folder = not self.is_folder

					# Devemos considerar que a mudança foi feita e vamos apresentar a nova
					# interface agora. Entretanto, caso não haja músicas...
					if not self.is_folder and len(self.playlist[self.folder_select]) == 0:
						self.is_folder = True

				elif key.name == "KEY_ENTER":

					if self.file_select is None:
						print(self._term.clear, end="")
						continue

					self.player.set_music(
										 os.path.join(self.root_music, self.folder_select, self.file_select + ".mp3")
										 )

				elif key == "p":

					if self.player.is_paused():
						self.player.resume()
					else:
						self.player.pause()

				elif key.name == "KEY_TAB":

					self.player.mode_infinity = not self.player.mode_infinity

				elif key == "+":

					if self.is_folder:
						
						self.criar_remover_subplaylist(True)

					else:
						self.baixar_musica()

				elif key == "-":

					if self.is_folder:

						self.criar_remover_subplaylist(False)

					else:

						# Precisamos remover a música
												

				print(self._term.clear, end="")

if __name__ == "__main__":
	example = UserInterface()

	example.mainloop()

	example.player.stop()

