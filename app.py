from __future__ import annotations

import os
from html import escape

import streamlit as st
from openai import OpenAIError

from recipe_chef import ARAB_COUNTRIES, Recipe, generate_recipe


st.set_page_config(
    page_title="Arabic AI Chef",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    linear-gradient(
                        180deg,
                        rgba(251, 250, 247, 0.94) 0%,
                        rgba(251, 250, 247, 0.9) 44%,
                        rgba(251, 250, 247, 0.96) 100%
                    ),
                    url("https://images.unsplash.com/photo-1661994215679-cde7c2c5c060?auto=format&fit=crop&fm=jpg&q=70&w=2200");
                background-attachment: fixed;
                background-position: center top;
                background-size: cover;
                color: #1f1f1d;
            }

            .block-container {
                max-width: 760px;
                padding-top: 3rem;
                padding-bottom: 3rem;
            }

            h1 {
                font-size: 2rem;
                margin-bottom: 0.25rem;
            }

            .stButton > button {
                border-radius: 8px;
                font-weight: 700;
            }

            div[data-testid="stAlert"] {
                border-radius: 8px;
            }

            .recipe-card {
                margin-top: 1.6rem;
                padding: 1.65rem 1.8rem;
                background: rgba(255, 253, 248, 0.94);
                border: 1px solid rgba(137, 99, 56, 0.18);
                border-radius: 8px;
                box-shadow: 0 18px 45px rgba(52, 37, 21, 0.12);
            }

            .recipe-card h2 {
                margin: 0;
                color: #2d241b;
                font-size: 1.65rem;
                line-height: 1.2;
            }

            .recipe-country {
                margin-top: 0.35rem;
                color: #8a6038;
                font-size: 0.9rem;
                font-weight: 700;
                letter-spacing: 0;
                text-transform: uppercase;
            }

            .recipe-description {
                margin: 1rem 0 1.25rem;
                color: #3b352e;
                line-height: 1.65;
            }

            .recipe-section {
                margin-top: 1.25rem;
            }

            .recipe-section h3 {
                margin: 0 0 0.55rem;
                color: #2d241b;
                font-size: 1rem;
            }

            .recipe-section ul,
            .recipe-section ol {
                margin: 0;
                padding-left: 1.25rem;
                color: #2f2b27;
                line-height: 1.65;
            }

            .recipe-section li + li {
                margin-top: 0.4rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def configured_api_key() -> str:
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY", "")
    except FileNotFoundError:
        secret_key = ""

    return (secret_key or os.environ.get("OPENAI_API_KEY", "")).strip()


def render_recipe(recipe: Recipe) -> None:
    if recipe.ingredients:
        ingredients_html = "\n".join(
            f"<li>{escape(ingredient)}</li>" for ingredient in recipe.ingredients
        )
    else:
        ingredients_html = (
            "<li>Ingredients were not clearly separated in the generated recipe.</li>"
        )

    if recipe.steps:
        steps_html = "\n".join(f"<li>{escape(step)}</li>" for step in recipe.steps)
    else:
        steps_html = "<li>Steps were not clearly separated in the generated recipe.</li>"

    st.markdown(
        f"""
<div class="recipe-card">
<h2>{escape(recipe.dish_name)}</h2>
<div class="recipe-country">{escape(recipe.country)}</div>
<p class="recipe-description">{escape(recipe.plating_description)}</p>
<div class="recipe-section">
<h3>Ingredients</h3>
<ul>
{ingredients_html}
</ul>
</div>
<div class="recipe-section">
<h3>Recipe Steps</h3>
<ol>
{steps_html}
</ol>
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def main() -> None:
    apply_theme()

    st.title("Arabic AI Chef")

    api_key = configured_api_key()
    country = st.selectbox("Choose an Arabic country", ARAB_COUNTRIES, index=4)
    generate = st.button("Generate recipe", type="primary", use_container_width=True)

    if generate:
        if not api_key:
            st.error("Set OPENAI_API_KEY in your environment or Streamlit secrets.")
            return

        try:
            with st.spinner("Generating recipe..."):
                st.session_state["latest_recipe"] = generate_recipe(
                    api_key=api_key,
                    country=country,
                )
        except ValueError as error:
            st.error(str(error))
        except OpenAIError as error:
            st.error(f"OpenAI could not generate the recipe: {error}")
        except Exception as error:
            st.error(f"Something unexpected happened: {error}")

    if "latest_recipe" in st.session_state:
        render_recipe(st.session_state["latest_recipe"])


if __name__ == "__main__":
    main()
