# AI API Response Formatter

AI-powered backend utility that transforms messy or inconsistent API responses into clean, standardized JSON using the Groq API.

## What it does

- Normalizes inconsistent key names into `snake_case`
- Cleans and standardizes response structure
- Converts obvious primitive types (numbers/booleans) when possible
- Returns strict, parseable JSON output

## Tech Stack

- Python
- Groq API
- `python-dotenv`

## Project Structure

```text
API Response Formatter/
├── assistant/
│   ├── __init__.py
│   ├── io_utils.py
│   ├── llm_client.py
│   └── workflows.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add environment variables:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

## Usage

### Option 1: Direct JSON text

```bash
python main.py --json "{\"Status\":\"ok\",\"Items\":[{\"UserName\":\"Aman\",\"score\":\"94\",\"isActive\":\"true\"}]}"
```

### Option 2: Input file

```bash
python main.py --file sample_input.txt
```

### Save output to file

```bash
python main.py --file sample_input.txt --save-output output.json
```

