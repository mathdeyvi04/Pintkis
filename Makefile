# Nome do Ambiente
VENV_NAME = venv

# Caminho para os pythons e sanhaços corretos
PYTHON = $(VENV_NAME)/bin/python3
PIP = $(VENV_NAME)/bin/pip

# Dependências
REQ = requirements.txt

# -------------------------------------------------------

all: 
	@$(PYTHON) src/UserInterface.py;

# Criar ambiente
venv:
	@python3 -m venv $(VENV_NAME);

# Para adicionarmos e atualizar posteriores bibliotecas
add:
ifndef LIB
	$(error Deve escrever LIB=<nome_da_lib>)
endif
	@$(PIP) install $(LIB);
	@$(PIP) freeze > $(REQ);


# Caso esteja executando do zero.
install:
	@$(PIP) install --upgrade pip;
	@$(PIP) install -r $(REQ);
	@$(PIP) freeze > $(REQ);
