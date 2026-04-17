from __future__ import annotations

import os

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
                background: #fbfaf7;
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
    st.divider()
    st.subheader(recipe.dish_name)
    st.caption(recipe.country)
    st.write(recipe.plating_description)

    st.markdown("**Ingredients**")
    if recipe.ingredients:
        for ingredient in recipe.ingredients:
            st.markdown(f"- {ingredient}")
    else:
        st.write("Ingredients were not clearly separated in the generated recipe.")

    st.markdown("**Recipe Steps**")
    if recipe.steps:
        for index, step in enumerate(recipe.steps, start=1):
            st.markdown(f"{index}. {step}")
    else:
        st.write("Steps were not clearly separated in the generated recipe.")


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
