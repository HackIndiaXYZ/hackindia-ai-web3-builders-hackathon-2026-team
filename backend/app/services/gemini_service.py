import os
import time

from dotenv import load_dotenv
from google import genai

from app.prompts.parser_prompt import PARSER_PROMPT
from app.prompts.rule_engine_prompt import RULE_ENGINE_PROMPT


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing in .env file"
    )

client = genai.Client(
    api_key=API_KEY
)


# IMPORTANT:
# Use a model supported by your Gemini API account.
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.0-flash"
)


def ask_gemini(prompt: str) -> str:

    max_retries = 3

    for attempt in range(max_retries):

        try:

            print(
                f"\nGemini request "
                f"(attempt {attempt + 1}/{max_retries})"
            )

            print(
                f"Model: {GEMINI_MODEL}"
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            return response.text

        except Exception as e:

            error_text = str(e)

            print(
                f"Gemini attempt "
                f"{attempt + 1} failed: {error_text}"
            )

            # Retry temporary service errors
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            ):

                if attempt < max_retries - 1:

                    wait_time = 3 * (attempt + 1)

                    print(
                        f"Temporary Gemini error. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            # Model configuration error
            if (
                "model" in error_text.lower()
                and (
                    "not found" in error_text.lower()
                    or "not available" in error_text.lower()
                    or "unsupported" in error_text.lower()
                )
            ):

                raise RuntimeError(
                    "The configured Gemini model is not available. "
                    f"Current model: {GEMINI_MODEL}. "
                    "Set GEMINI_MODEL=gemini-2.0-flash in .env"
                )

            raise


def parse_document_with_gemini(
    document_text: str
) -> str:

    prompt = f"""
{PARSER_PROMPT}

DOCUMENT TEXT:
{document_text}

IMPORTANT:
Return ONLY valid JSON.
Do not use markdown.
Do not add explanations.
"""

    return ask_gemini(prompt)


def evaluate_bid_with_gemini(
    bid_requirements: str,
    bidder_submission: str
) -> str:

    prompt = f"""
{RULE_ENGINE_PROMPT}

====================
BID REQUIREMENTS
====================

{bid_requirements}

====================
BIDDER SUBMISSION
====================

{bidder_submission}

====================
END INPUT
====================

Compare the two JSON objects according to
the procurement rules.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations.
"""

    return ask_gemini(prompt)