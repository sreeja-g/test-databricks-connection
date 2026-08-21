def count_medications(value: str | None) -> int:
    if value is None:
        return 0

    cleaned = str(value).strip()

    if cleaned.lower() in {"", "none", "nan"}:
        return 0

    return len(
        [
            item
            for item in cleaned.split("|")
            if item.strip()
        ]
    )


def fever_flag(temperature_f: float) -> int:
    return int(temperature_f >= 100.4)