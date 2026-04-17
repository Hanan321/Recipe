"""Business logic for Arabic AI Chef."""

from __future__ import annotations

import re
from dataclasses import dataclass

from openai import OpenAI


DEFAULT_MODEL = "gpt-5.4"

ARAB_COUNTRIES = [
    "Algeria",
    "Bahrain",
    "Comoros",
    "Djibouti",
    "Egypt",
    "Iraq",
    "Jordan",
    "Kuwait",
    "Lebanon",
    "Libya",
    "Mauritania",
    "Morocco",
    "Oman",
    "Palestine",
    "Qatar",
    "Saudi Arabia",
    "Somalia",
    "Sudan",
    "Syria",
    "Tunisia",
    "United Arab Emirates",
    "Yemen",
]

NORMALIZED_COUNTRIES = {country.lower(): country for country in ARAB_COUNTRIES}

RECIPE_STYLES = [
    "Classic traditional",
    "Beginner friendly",
    "Weeknight friendly",
    "Vegetarian leaning",
    "Family gathering",
]


@dataclass(frozen=True)
class Recipe:
    """A parsed recipe response that the UI can render cleanly."""

    country: str
    dish_name: str
    plating_description: str
    ingredients: list[str]
    steps: list[str]
    raw_text: str


def normalize_country(country: str) -> str | None:
    """Return a canonical Arab country name, or None if unsupported."""

    return NORMALIZED_COUNTRIES.get(country.strip().lower())


def build_recipe_prompt(
    country: str,
    recipe_style: str,
    servings: int,
    preferences: str = "",
) -> str:
    """Build the same core prompt from the notebook with app-friendly options."""

    preference_line = (
        f"User preferences or notes: {preferences.strip()}"
        if preferences.strip()
        else "User preferences or notes: none"
    )

    return f"""
You are a professional culinary AI assistant.

The selected country is: {country}
Recipe style: {recipe_style}
Servings: about {servings}
{preference_line}

Choose ONE well-known traditional dish from this country and generate the answer using this exact format:

Dish Name:
- write the name of one popular traditional dish

Plating Description:
- describe how the dish looks when served

Ingredients:
- list 6 to 8 items with practical amounts for the requested servings

Recipe Steps:
1. write 4 to 6 simple steps

Keep the answer culturally appropriate, realistic, warm, and beginner-friendly.
Do not add extra sections outside the requested format.
""".strip()


def generate_recipe(
    api_key: str,
    country: str,
    recipe_style: str,
    servings: int,
    preferences: str = "",
    model: str = DEFAULT_MODEL,
) -> Recipe:
    """Generate and parse a traditional Arabic recipe."""

    if not api_key.strip():
        raise ValueError("Please enter an OpenAI API key to generate a recipe.")

    canonical_country = normalize_country(country)
    if not canonical_country:
        raise ValueError("Please choose one of the supported Arab countries.")

    prompt = build_recipe_prompt(
        country=canonical_country,
        recipe_style=recipe_style,
        servings=servings,
        preferences=preferences,
    )

    client = OpenAI(api_key=api_key.strip())
    response = client.responses.create(model=model, input=prompt)
    recipe_text = response.output_text.strip()

    return parse_recipe(recipe_text, canonical_country)


def parse_recipe(recipe_text: str, country: str) -> Recipe:
    """Parse the model's structured text into display sections."""

    sections = {
        "dish name": "",
        "plating description": "",
        "ingredients": "",
        "recipe steps": "",
    }
    current_section: str | None = None

    for raw_line in recipe_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        heading = line.rstrip(":").lower()
        if heading in sections:
            current_section = heading
            continue

        if current_section:
            sections[current_section] = (
                f"{sections[current_section]}\n{line}".strip()
                if sections[current_section]
                else line
            )

    dish_name = _first_clean_line(sections["dish name"]) or "Traditional dish"
    plating_description = (
        _first_clean_line(sections["plating description"])
        or "A warm, inviting plate inspired by the country's culinary traditions."
    )
    ingredients = _clean_list_items(sections["ingredients"])
    steps = _clean_list_items(sections["recipe steps"])

    return Recipe(
        country=country,
        dish_name=dish_name,
        plating_description=plating_description,
        ingredients=ingredients,
        steps=steps,
        raw_text=recipe_text,
    )


def _first_clean_line(text: str) -> str:
    for line in text.splitlines():
        cleaned = _clean_item(line)
        if cleaned:
            return cleaned
    return ""


def _clean_list_items(text: str) -> list[str]:
    items = [_clean_item(line) for line in text.splitlines()]
    return [item for item in items if item]


def _clean_item(line: str) -> str:
    return re.sub(r"^(\d+[\).\s-]*|[-*]\s*)", "", line.strip()).strip()
