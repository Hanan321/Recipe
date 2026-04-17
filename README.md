# Arabic AI Chef

A minimal Streamlit app that generates one traditional recipe from a selected Arab country.

## What It Does

- Choose an Arab country from one dropdown
- Generate a recipe with one button
- Display the generated recipe on the same page
- Load `OPENAI_API_KEY` from an environment variable or Streamlit secrets

## Project Structure

```text
.
|-- app.py                  # Streamlit entry point
|-- recipe_chef.py          # Country list, prompt, OpenAI call, recipe parsing
|-- requirements.txt        # Python dependencies
`-- Arabic_AI_Chef.ipynb    # Original notebook kept for reference
```

## Run Locally

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

4. Start the app:

```bash
streamlit run app.py
```

## Streamlit Secrets

For Streamlit Community Cloud or local secrets, add:

```toml
OPENAI_API_KEY = "your_api_key_here"
```
