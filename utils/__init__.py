"""Shared utilities for Echostash UI automation."""

from utils.helpers import (
    api_create_project,
    api_create_prompt,
    api_delete_project,
    api_login_guest,
    get_monaco_value,
    random_email,
    random_prompt_content,
    random_string,
    set_auth_cookie,
    set_monaco_value,
    unique_name,
    wait_for_no_spinners,
)

__all__ = [
    "api_create_project",
    "api_create_prompt",
    "api_delete_project",
    "api_login_guest",
    "get_monaco_value",
    "random_email",
    "random_prompt_content",
    "random_string",
    "set_auth_cookie",
    "set_monaco_value",
    "unique_name",
    "wait_for_no_spinners",
]
