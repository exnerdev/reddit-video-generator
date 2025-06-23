from typing import Final
from re import compile, escape, IGNORECASE

filters: Final[dict[str, str]] = {
    "aita": "am I the a-hole",
    "aitah": "am I the a-hole",
    "ass": "butt",
    "asshole": "a-hole",
    "fuck": "frick",
    "fucking": "fricking",
    "bullshit": "bs",
    "bitch": "female dog",
    "shit": "poop",
    "cock": "rooster",
    "pussy": "wimp",
    "semen": "see em",
    "hell": "heck",
    "damn": "darn",
    "cunt": "can't",
    "slut": "player",
    "whore": "player",
    "porn": "corn"
}

regex = compile(
    r"\b(" + "|".join(escape(w) for w in filters) + r")\b",
    IGNORECASE
)

def apply_casing(original: str, replacement: str) -> str:
    if original.isupper():
        return replacement.upper()
    elif original.islower():
        return replacement.lower()
    elif original[0].isupper() and original[1:].islower():
        return replacement.capitalize()
    else:
        # Mixed casing → character-by-character match (fallback)
        return ''.join(
            rep.upper() if orig.isupper() else rep.lower()
            for orig, rep in zip(original, replacement.ljust(len(original)))
        )

def FilterText(text: str) -> str:
    def replacer(match):
        word = match.group()
        base = word.lower()
        replacement = filters[base]
        return apply_casing(word, replacement)

    return regex.sub(replacer, text)