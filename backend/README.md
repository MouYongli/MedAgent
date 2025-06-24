# MedAgent Backend

## Project structure
```
📦 MedAgent 
├── 📁 backend       # Backend project root directory
│   ├── 📁 src      # Source code directory
│   ├── pyproject.toml  # Project dependency configuration
│   ├── app.py      # Application entry point
│   └── README.md   # Project documentation
├── ...   
└── README.md       # Main project documentation

```

## Environment Setup


Create conda environment and install dependencies.

### Prerequisites
- Python 3.10 or higher
- Conda package manager

### Installation Steps
1. Create and activate the Conda environment
```bash
# Create environment
conda create --name medagent python=3.10

# Activate environment
conda activate medagent

# Install dependencies
pip install -e .
```

2. Start the service
```bash
# Start in development mode (with hot reload)
python -m uvicorn app.main:app --reload
```


## API Documentation

### Overview

- **Base URL**: `http://127.0.0.1:8000/api`

|        Category | Method | Endpoint                       | Description                                 |
|----------------:|--------|---------------------------------|---------------------------------------------|
|  Knowledge Base | `GET`  | `/knowledge/pdf/`           | List all available PDF files                |
|        Workflow | `POST` | `/workflow/init`               | Initialize a new workflow from config       |
|        Workflow | `GET`  | `/workflow/list`               | List all active workflow instances          |
|            Chat | `POST` | `/chat/init`                   | Create a new chat session                   |
|            Chat | `GET`  | `/chat/list`                   | List all active chat sessions               |
|            Chat | `POST` | `/chat/{chat_id}/ask`          | Ask a question in a specific chat session   |

### Details

#### List all PDFs: `GET /api/knowledge/pdf/`
##### Example Request
```http
GET /api/knowledge/pdf/
```

##### Example Response
```json
["file1.pdf", "file2.pdf"]
```

##### Curl Example
```bash
curl http://127.0.0.1:8000/api/knowledge/pdf/
```

##### Notes
- Only `.pdf` files are supported.
- Filenames should be in English and not contain special characters.
- The `data/` directory is automatically created at startup.

