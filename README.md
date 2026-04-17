# Arabic AI Chef

Arabic AI Chef is a Streamlit web app that generates beginner-friendly recipes for traditional dishes from Arab countries. The original project lived in a Google Colab notebook with command-line style input and printed output. It has now been refactored into a polished local web interface that is easier to run, present, and deploy.

## What The App Does

- Supports all 22 Arab countries
- Lets users choose a country, recipe style, serving count, and optional preferences
- Uses the OpenAI API to select one traditional dish from the selected country
- Displays the generated recipe in clear web sections
- Separates ingredients, plating description, and preparation steps
- Shows friendly validation and API errors

## Project Structure

```text
.
|-- app.py                  # Streamlit interface and layout
|-- recipe_chef.py          # Country validation, prompt building, API call, parsing
|-- requirements.txt        # Python dependencies
|-- .streamlit/config.toml  # Streamlit theme colors
|-- Arabic_AI_Chef.ipynb    # Original notebook kept for reference
`-- README.md
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

3. Start the app:

```bash
streamlit run app.py
```

4. Open the local Streamlit URL in your browser and enter your OpenAI API key in the sidebar.

You can also create a local `.env` file:

```bash
OPENAI_API_KEY="your_api_key_here"
```

Or set an environment variable before running the app:

```bash
export OPENAI_API_KEY="your_api_key_here"
streamlit run app.py
```

## Deploy On Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a new app on Streamlit Community Cloud.
3. Set the main file path to `app.py`.
4. Add your `OPENAI_API_KEY` as a Streamlit secret if you do not want users to type a key each time.

Example secret:

```toml
OPENAI_API_KEY = "your_api_key_here"
```

## Original Notebook Flow

The notebook asked for an API key with `getpass`, accepted country names through `input()`, validated the country against a fixed list, sent a prompt to the OpenAI Responses API, and printed the result with divider lines.

## New Streamlit Flow

The Streamlit version keeps the same core idea, but replaces notebook and terminal interaction with:

- Sidebar API key and recipe settings
- Generate button
- Loading spinner
- Formatted recipe card
- Ingredient and step sections
- Friendly warning and error messages

## Author

Developed by Hanan, an aspiring AI developer focused on building practical AI applications.
