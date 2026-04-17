from __future__ import annotations

import os

import streamlit as st
from openai import OpenAIError
from dotenv import load_dotenv

from recipe_chef import ARAB_COUNTRIES, RECIPE_STYLES, Recipe, generate_recipe


load_dotenv()

st.set_page_config(
    page_title="Arabic AI Chef",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            :root {
                --saffron: #d99a2b;
                --olive: #536b45;
                --pomegranate: #9f2f45;
                --ink: #221c18;
                --soft: #fff8ef;
                --card: rgba(255, 252, 246, 0.94);
            }

            .stApp {
                background:
                    linear-gradient(180deg, rgba(255,248,239,0.96), rgba(248,239,225,0.98)),
                    url("https://images.unsplash.com/photo-1551218808-94e220e084d2?auto=format&fit=crop&w=1800&q=80");
                background-size: cover;
                background-attachment: fixed;
                color: var(--ink);
            }

            .block-container {
                padding-top: 2.4rem;
                padding-bottom: 3rem;
                max-width: 1180px;
            }

            [data-testid="stSidebar"] {
                background: rgba(255, 248, 239, 0.94);
                border-right: 1px solid rgba(83, 107, 69, 0.18);
            }

            .hero {
                padding: 2.2rem 2.4rem;
                border: 1px solid rgba(83, 107, 69, 0.16);
                background:
                    linear-gradient(135deg, rgba(255, 252, 246, 0.96), rgba(255, 238, 210, 0.88));
                border-radius: 8px;
                box-shadow: 0 24px 70px rgba(66, 45, 26, 0.14);
                margin-bottom: 1.4rem;
            }

            .eyebrow {
                color: var(--pomegranate);
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0;
                text-transform: uppercase;
                margin-bottom: 0.6rem;
            }

            .hero h1 {
                color: var(--ink);
                font-size: 3.1rem;
                line-height: 1.05;
                margin: 0 0 0.8rem;
            }

            .hero p {
                color: #5c4c40;
                font-size: 1.08rem;
                line-height: 1.65;
                max-width: 760px;
                margin: 0;
            }

            [data-testid="stVerticalBlockBorderWrapper"] {
                background: var(--card);
                border: 1px solid rgba(83, 107, 69, 0.16);
                border-radius: 8px;
                box-shadow: 0 18px 55px rgba(66, 45, 26, 0.12);
                padding: 1.5rem;
                margin-top: 1rem;
            }

            .dish-title {
                color: var(--ink);
                font-size: 2.1rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
            }

            .country-chip {
                display: inline-block;
                background: rgba(83, 107, 69, 0.12);
                border: 1px solid rgba(83, 107, 69, 0.22);
                border-radius: 8px;
                color: var(--olive);
                font-weight: 700;
                padding: 0.28rem 0.65rem;
                margin-bottom: 1rem;
            }

            .section-title {
                color: var(--pomegranate);
                font-size: 1.15rem;
                font-weight: 800;
                margin-top: 0.4rem;
                margin-bottom: 0.8rem;
            }

            .stButton > button {
                background: linear-gradient(135deg, var(--pomegranate), #bf5b46);
                color: white;
                border: 0;
                border-radius: 8px;
                padding: 0.8rem 1rem;
                font-weight: 800;
                box-shadow: 0 12px 28px rgba(159, 47, 69, 0.24);
            }

            .stButton > button:hover {
                color: white;
                border: 0;
                transform: translateY(-1px);
            }

            div[data-testid="stAlert"] {
                border-radius: 8px;
            }

            @media (max-width: 760px) {
                .hero {
                    padding: 1.5rem;
                }

                .hero h1 {
                    font-size: 2.2rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Arabic AI Chef</div>
            <h1>Cook a traditional Arab dish with AI guidance.</h1>
            <p>
                Choose a country, add a few preferences, and receive a warm,
                beginner-friendly recipe with clear ingredients and simple steps.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_recipe(recipe: Recipe) -> None:
    with st.container(border=True):
        st.markdown(f'<div class="country-chip">{recipe.country}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dish-title">{recipe.dish_name}</div>', unsafe_allow_html=True)
        st.write(recipe.plating_description)

        ingredients_col, steps_col = st.columns([0.9, 1.1], gap="large")

        with ingredients_col:
            st.markdown('<div class="section-title">Ingredients</div>', unsafe_allow_html=True)
            if recipe.ingredients:
                for ingredient in recipe.ingredients:
                    st.markdown(f"- {ingredient}")
            else:
                st.info("The recipe was generated, but the ingredients were not clearly separated.")

        with steps_col:
            st.markdown('<div class="section-title">Preparation Steps</div>', unsafe_allow_html=True)
            if recipe.steps:
                for index, step in enumerate(recipe.steps, start=1):
                    st.markdown(f"**{index}.** {step}")
            else:
                st.info("The recipe was generated, but the steps were not clearly separated.")

        with st.expander("View original AI response"):
            st.markdown(recipe.raw_text)


def configured_api_key() -> str:
    try:
        return st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
    except FileNotFoundError:
        return os.environ.get("OPENAI_API_KEY", "")


def sidebar_controls() -> tuple[str, str, int, str, str]:
    st.sidebar.header("Recipe Settings")

    stored_api_key = configured_api_key().strip()
    if stored_api_key:
        st.sidebar.caption("OpenAI API key loaded from app configuration.")

    typed_api_key = st.sidebar.text_input(
        "OpenAI API key",
        value="",
        key="openai_api_key_input_v2",
        type="password",
        placeholder="Optional: paste a key for this session",
        help="Stored keys are never displayed here. Leave this blank to use the configured key.",
    )
    api_key = typed_api_key.strip() or stored_api_key

    country = st.sidebar.selectbox("Country", ARAB_COUNTRIES, index=4)
    recipe_style = st.sidebar.selectbox("Recipe style", RECIPE_STYLES)
    servings = st.sidebar.slider("Servings", min_value=2, max_value=8, value=4, step=1)
    preferences = st.sidebar.text_area(
        "Optional preferences",
        placeholder="Example: less spicy, no nuts, pantry-friendly",
        height=110,
    )

    return api_key, country, recipe_style, servings, preferences


def main() -> None:
    apply_theme()
    render_header()

    api_key, country, recipe_style, servings, preferences = sidebar_controls()

    intro_col, action_col = st.columns([1.4, 0.8], gap="large")
    with intro_col:
        st.subheader("Start with a country")
        st.write(
            "The app selects one well-known traditional dish and turns it into "
            "a clear recipe you can follow without notebook or terminal output."
        )

    with action_col:
        st.write("")
        st.write("")
        generate = st.button("Generate Recipe", use_container_width=True)

    if not api_key:
        st.warning("Add your OpenAI API key in the sidebar before generating a recipe.")

    if generate:
        if not api_key:
            st.error("Please enter an OpenAI API key first.")
            return

        try:
            with st.spinner("Choosing a traditional dish and writing the recipe..."):
                recipe = generate_recipe(
                    api_key=api_key,
                    country=country,
                    recipe_style=recipe_style,
                    servings=servings,
                    preferences=preferences,
                )
        except ValueError as error:
            st.error(str(error))
        except OpenAIError as error:
            st.error(f"OpenAI could not generate the recipe: {error}")
        except Exception as error:
            st.error(f"Something unexpected happened: {error}")
        else:
            st.session_state["latest_recipe"] = recipe

    if "latest_recipe" in st.session_state:
        render_recipe(st.session_state["latest_recipe"])
    else:
        st.info("Your generated recipe will appear here with ingredients and preparation steps.")


if __name__ == "__main__":
    main()
