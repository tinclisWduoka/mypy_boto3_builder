"""
Multiple string utils collection.
"""
import builtins
import keyword
import re
import textwrap
import typing
from unittest.mock import MagicMock

from botocore.utils import get_service_module_name

RESERVED_NAMES = {
    *dir(typing),
    *dir(builtins),
    *keyword.kwlist,
}
MAX_DOCSTRING_LENGTH: int = 300


def get_class_prefix(func_name: str) -> str:
    """
    Get a valid Python class prefix from `func_name`.

    Arguments:
        func_name -- Any string.

    Returns:
        String with a class prefix.
    """
    parts = [f"{i[:1].upper()}{i[1:]}" for i in func_name.split("_") if i]
    return "".join(parts)


def get_anchor_link(text: str) -> str:
    """
    Convert header to markdown anchor link.
    """
    return text.strip().replace(" ", "-").replace(".", "").lower()


def is_reserved(word: str) -> bool:
    """
    Check whether varialbe name conflicts with Python reserved names.
    """
    return word in RESERVED_NAMES


def get_short_docstring(doc: str) -> str:
    """
    Create a short docstring from boto3 documentation.

    Trims docstring to 300 chars.
    Removes double and triple backticks.
    Stops on `**Request syntax**` and `::`.
    Ensures that backticks are closed.
    Replaces `Text <link>` with [Text](link).
    Wraps docstring to 80 chars.
    """
    doc = str(doc)
    if len(doc) > MAX_DOCSTRING_LENGTH:
        doc = f"{doc[:MAX_DOCSTRING_LENGTH - 3]}..."
    result: list[str] = []
    if not doc:
        return ""
    for line in doc.splitlines():
        line = line.strip().removesuffix("::")
        if line.startswith(":"):
            break
        if line.lower().startswith("**request syntax**"):
            break
        if not line:
            continue
        if ". " in line:
            result.append(line.split(". ")[0])
            break
        result.append(line)
        if line.endswith("."):
            break

    result_str = " ".join(result).replace("```", "`").replace("``", "`").strip()
    if result_str.count("`") % 2:
        result_str = f"{result_str}`"
    if result_str and not result_str.endswith("."):
        result_str = f"{result_str}."

    if "<https:" in result_str:
        result_str = re.sub(
            r"`([^`]+\S)\s*<https://(\S+)>`(\_)?", r"[\g<1>](https://\g<2>)", result_str
        )

    return "\n".join(textwrap.wrap(result_str, width=80, break_long_words=False))


def get_botocore_class_name(metadata: dict[str, str]) -> str:
    """
    Get Botocore class name from Service metadata.
    """
    service_model = MagicMock()
    service_model.service_name = metadata.get("serviceId", "")
    service_model.metadata = metadata
    return get_service_module_name(service_model)


def get_typed_dict_name(*parts: str) -> str:
    """
    Get a valid Python TypedDict class name from `parts`.

    Examples:
        ```python
        get_typed_dict_name("MyClass", "my_method")  # MyClassMyMethodTypeDef
        ```
    """
    if not parts:
        raise ValueError("At least one part is required")

    parts_camelcased = [get_class_prefix(i) for i in parts]
    name = "".join(parts_camelcased)
    return f"{name}TypeDef"
