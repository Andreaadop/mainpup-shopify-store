"""
Generate images with Google Nano Banana Pro (gemini-3-pro-image-preview).

Usage:
    python tools/generate_nanobanana_image.py \
        --prompt-file .tmp/prompt.txt \
        --refs brand_assets/models/kiwi/_MG_6381.jpg \
        --out .tmp/generated/kiwi_fisheye_y2k_01.png

Reads the API key from .env (GEMINI_API_KEY or GOOGLE_API_KEY) or, as a
fallback, from google-apikey.txt at the project root.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "gemini-3-pro-image-preview"


def load_api_key() -> str:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    fallback = PROJECT_ROOT / "google-apikey.txt"
    if fallback.exists():
        return fallback.read_text(encoding="utf-8").strip()
    raise RuntimeError(
        "No API key found. Set GEMINI_API_KEY in .env or create google-apikey.txt."
    )


def read_prompt(prompt: str | None, prompt_file: str | None) -> str:
    if prompt and prompt_file:
        raise ValueError("Pass either --prompt or --prompt-file, not both.")
    if prompt:
        return prompt
    if prompt_file:
        return Path(prompt_file).read_text(encoding="utf-8")
    raise ValueError("Must pass --prompt or --prompt-file.")


def load_image_parts(paths: list[str]) -> list[types.Part]:
    parts: list[types.Part] = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(f"Reference image not found: {p}")
        suffix = path.suffix.lower().lstrip(".")
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(
            suffix, "jpeg"
        )
        parts.append(
            types.Part.from_bytes(data=path.read_bytes(), mime_type=f"image/{mime}")
        )
    return parts


def generate(
    prompt: str,
    ref_paths: list[str],
    out_path: str,
    model: str = DEFAULT_MODEL,
) -> Path:
    client = genai.Client(api_key=load_api_key())
    parts: list[types.Part] = load_image_parts(ref_paths)
    parts.append(types.Part.from_text(text=prompt))

    response = client.models.generate_content(
        model=model,
        contents=[types.Content(role="user", parts=parts)],
    )

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    saved = None
    for candidate in response.candidates or []:
        for part in candidate.content.parts or []:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                out.write_bytes(part.inline_data.data)
                saved = out
                break
        if saved:
            break

    if not saved:
        text_bits = []
        for candidate in response.candidates or []:
            for part in candidate.content.parts or []:
                if getattr(part, "text", None):
                    text_bits.append(part.text)
        raise RuntimeError(
            "No image returned. Model response text:\n" + "\n".join(text_bits)
        )

    return saved


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", help="Prompt text (inline).")
    ap.add_argument("--prompt-file", help="Path to a file containing the prompt.")
    ap.add_argument(
        "--refs",
        nargs="*",
        default=[],
        help="Reference image paths (jpg/png/webp).",
    )
    ap.add_argument("--out", required=True, help="Output image path.")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    prompt = read_prompt(args.prompt, args.prompt_file)
    saved = generate(prompt, args.refs, args.out, model=args.model)
    print(f"Saved: {saved}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
