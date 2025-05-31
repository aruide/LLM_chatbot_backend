pip install -r requirements.txt

python -m venv venv
venv\Scripts\activate
.\.venv\Scripts\Activate.ps1
source .venv/Scripts/activate
pip install -r requirements.txt
python -m http.server 8000

```bach
project/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── utils/
│       ├── __init__.py
│       ├── qa.py
│       ├── vectordb.py
│       └── websearch.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── assets/
│       └── model/
│           ├── model.json
│           ├── *.moc3
│           ├── *.png
│           └── ...
├── README.md
└── .gitignore
```

pyenv install 3.10.11
pyenv global 3.10.11

python -m venv .venv
.venv\Scripts\activate