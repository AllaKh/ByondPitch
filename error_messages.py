ERROR_MESSAGES: dict[str, dict[str, str]] = {
    "he": {
        "invalid_credentials": "שם משתמש או סיסמה שגויים",
        "required_field": "זהו שדה חובה",
        "attempts_exceeded": "Password attempts exceeded"
    },
    "en": {
        "invalid_credentials": "Invalid username or password",
        "required_field": "This field is required",
        "attempts_exceeded": "Password attempts exceeded"
    }
}


def get_error(language: str, key: str) -> str:
    return ERROR_MESSAGES[language][key]