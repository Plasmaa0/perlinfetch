GREEN=$(tput setaf 2)
RESET=$(tput sgr0)
echo ${GREEN}Creating python virtual environment${RESET}
python -m venv venv
echo ${GREEN}Downloading dependencies${RESET}
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
echo ${GREEN}Paste the following line to your shell config. It will execute perlinfetch at startup.${RESET}
echo $(pwd)/venv/bin/python $(pwd)/perlinfetch.py