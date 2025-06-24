```
📦 MedAgent
├── 📁 backend
│   ├── 📁 src
│   ├── pyproject.toml
│   ├── app.py
│   └── README.md
├── ...
└── README.md
```

## Conda env

Create conda environment and install dependencies. Run from src/

```
conda create --name medagent python=3.10
conda activate medagent
pip install -e .
python -m uvicorn app.main:app --reload
```
