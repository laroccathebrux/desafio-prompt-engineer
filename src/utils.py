"""
Utility functions for the LangSmith Prompt Optimization Challenge.

This module provides helper functions for environment loading, YAML file
operations, and common utilities used across the project scripts.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


def load_env(env_path: Optional[str] = None) -> bool:
    """
    Load environment variables from a .env file.

    Args:
        env_path: Optional path to .env file. If not provided, searches in
                  the current directory and parent directories.

    Returns:
        True if .env file was found and loaded, False otherwise.

    Raises:
        FileNotFoundError: If env_path is specified but file doesn't exist.

    Example:
        >>> load_env()
        True
        >>> os.getenv("LANGCHAIN_API_KEY")
        'lsv2_...'
    """
    if env_path:
        if not os.path.exists(env_path):
            raise FileNotFoundError(f".env file not found at: {env_path}")
        return load_dotenv(env_path)

    # Search for .env in current and parent directories
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        env_file = parent / ".env"
        if env_file.exists():
            return load_dotenv(env_file)

    return False


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML file.

    Args:
        file_path: Path to the YAML file to load.

    Returns:
        Dictionary containing the parsed YAML content.

    Raises:
        FileNotFoundError: If the YAML file doesn't exist.
        yaml.YAMLError: If the file contains invalid YAML syntax.

    Example:
        >>> data = load_yaml("prompts/bug_to_user_story_v2.yml")
        >>> data["metadata"]["name"]
        'bug_to_user_story_v2'
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in {file_path}: {e}")


def save_yaml(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to a YAML file.

    Args:
        data: Dictionary to save as YAML.
        file_path: Path where the YAML file will be saved.

    Raises:
        OSError: If the file cannot be written.

    Example:
        >>> data = {"name": "test", "value": 42}
        >>> save_yaml(data, "output.yml")
    """
    # Ensure directory exists
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120
        )


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path object pointing to the project root (directory containing .env or src/).

    Example:
        >>> root = get_project_root()
        >>> (root / "src").exists()
        True
    """
    current = Path.cwd()

    # Look for markers of project root
    markers = [".env", "src", "requirements.txt", ".git"]

    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent

    return current


def print_error(message: str) -> None:
    """
    Print an error message to stderr.

    Args:
        message: Error message to display.

    Example:
        >>> print_error("Authentication failed")
        Error: Authentication failed
    """
    print(f"Error: {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """
    Print a success message to stdout.

    Args:
        message: Success message to display.

    Example:
        >>> print_success("Operation completed")
        ✓ Operation completed
    """
    print(f"✓ {message}")


def validate_env_vars(required_vars: list) -> bool:
    """
    Validate that required environment variables are set.

    Args:
        required_vars: List of environment variable names to check.

    Returns:
        True if all required variables are set, False otherwise.

    Example:
        >>> validate_env_vars(["LANGCHAIN_API_KEY"])
        True
    """
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print_error(f"Missing required environment variables: {', '.join(missing)}")
        print("Please check your .env file.")
        return False

    return True
