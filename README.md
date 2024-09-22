# Text Translation

## Setup

`Note if you are using window use default terminal as Command prompt (cmd) else using Debian/RedHat/Fedora use any terminal.`

1. Clone the repository: 

```bash
git clone https://github.com/SauRavRwT/voice-translation.git
```
2. Navigate to the project directory: 

```bash
cd voice-translation
```
3. create python virtual env: 

```bash
mkdir venv # Making dir

python -m venv venv # Making virtual env
```
4. To activate virtual env: 

```bash
source venv/bin/activate  # For Linux/Mac

venv\scripts\activate  # For Windows
```
5. Install python dependencies: 

```bash
pip install -r requirements.txt

pip install --upgrade torch transformers
```

6. Now you are done!!, Run your python file: 

```bash
python server.py
```
