import os
import random
import string


def get_env_var(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_email() -> str:
    return f"test_{random_string()}@echostash-test.com"
