from plugins import *

bot = cipherx_bot

# Inline menu entries for addon-provided patterns (merged at runtime with Megatron).
InlinePlugin.update(
    {
        "GitHub": "gh ToxygenX",
        "PyPI Search": "pypi requests",
        "IMDb Search": "imdb inception",
        "Winget Search": "winget telegram",
    }
)
