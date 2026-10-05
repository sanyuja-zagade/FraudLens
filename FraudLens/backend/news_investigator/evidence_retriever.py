import requests
import json
import http.client
import re
import traceback
import os
from markdownify import markdownify
from dotenv import load_dotenv

load_dotenv()


def truncate_content(content: str, max_length: int) -> str:
    if len(content) <= max_length:
        return content

    return (
        content[: max_length // 2]
        + "\n...content truncated...\n"
        + content[-max_length // 2:]
    )


def web_browser(url, max_output_length=10000):
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        content = markdownify(response.text).strip()
        content = re.sub(r"\n{3,}", "\n\n", content)

        return truncate_content(content, max_output_length)

    except requests.exceptions.Timeout:
        return "The request timed out."

    except requests.exceptions.RequestException as e:
        return f"Error fetching webpage: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"


def search_web(query):
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "q": query,
        "gl": "in",
        "hl": "en",
        "num": 10
    })

    try:
        conn = http.client.HTTPSConnection("google.serper.dev")

        conn.request(
            "POST",
            "/search",
            payload,
            headers
        )

        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))

        return data.get("organic", [])

    except Exception as e:
        print(f"Search API error: {e}")
        return []