"""
Clean Utility Module for BYRD

This module provides well-documented, clean utility functions
that demonstrate best practices for the BYRD codebase.

Philosophy:
- Single Responsibility: Each function does one thing well
- Clear Documentation: Docstrings follow Google style
- Type Safety: Type hints for all parameters and returns
- Error Handling: Explicit exceptions with helpful messages

Example:
    >>> from clean_utils import safe_parse_json
    >>> data = safe_parse_json('{"key": "value"}')
    >>> print(data)
    {'key': 'value'}
"""

import json
import re
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from functools import wraps
import time


def safe_parse_json(json_string: str, default: Any = None) -> Any:
    """Safely parse a JSON string with graceful error handling.

    Args:
        json_string: The JSON string to parse.
        default: The value to return if parsing fails. Defaults to None.

    Returns:
        The parsed JSON object or the default value if parsing fails.

    Raises:
        ValueError: If json_string is not a string.

    Example:
        >>> safe_parse_json('{"a": 1}')
        {'a': 1}
        >>> safe_parse_json('invalid', {})
        {}
    """
    if not isinstance(json_string, str):
        raise ValueError(f"Expected string, got {type(json_string).__name__}")
    
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        return default


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length with an optional suffix.

    Args:
        text: The text to truncate.
        max_length: Maximum length of the output. Defaults to 100.
        suffix: String to append if truncation occurs. Defaults to "...".

    Returns:
        The truncated text.

    Example:
        >>> truncate_text("Hello world", 8)
        'Hello...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def generate_hash(content: str, algorithm: str = "sha256") -> str:
    """Generate a cryptographic hash of the given content.

    Args:
        content: The string content to hash.
        algorithm: The hash algorithm to use. Defaults to "sha256".

    Returns:
        The hexadecimal hash string.

    Raises:
        ValueError: If the specified algorithm is not available.

    Example:
        >>> generate_hash("hello")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    try:
        hash_func = hashlib.new(algorithm)
    except ValueError:
        available = hashlib.algorithms_available
        raise ValueError(f"Algorithm '{algorithm}' not available. Available: {available}")
    
    hash_func.update(content.encode('utf-8'))
    return hash_func.hexdigest()


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from a given text using regex.

    Args:
        text: The text to search for URLs.

    Returns:
        A list of URLs found in the text.

    Example:
        >>> extract_urls("Visit https://example.com and http://test.org")
        ['https://example.com', 'http://test.org']
    """
    url_pattern = r'https?://[\w\-]+(\.[\w\-]+)+[\w\-\./?=%&]*'
    return re.findall(url_pattern, text)


def measure_time(func):
    """Decorator to measure and log function execution time.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function that prints execution time.

    Example:
        >>> @measure_time
        ... def slow_function():
        ...     time.sleep(0.1)
        ...     return "done"
        >>> slow_function()
        slow_function executed in 0.10s
        'done'
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"{func.__name__} executed in {elapsed:.2f}s")
        return result
    return wrapper


def format_timestamp(dt: Optional[datetime] = None, 
                     format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as a string.

    Args:
        dt: The datetime to format. If None, uses current time.
        format_string: The strftime format string. Defaults to ISO-like format.

    Returns:
        The formatted timestamp string.

    Example:
        >>> format_timestamp(datetime(2024, 1, 1, 12, 0))
        '2024-01-01 12:00:00'
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(format_string)


def merge_dicts(*dicts: Dict[str, Any], 
                priority: str = "last") -> Dict[str, Any]:
    """Merge multiple dictionaries with configurable conflict resolution.

    Args:
        *dicts: Dictionaries to merge.
        priority: Determines key priority. "first" means first dict wins,
                  "last" means last dict wins. Defaults to "last".

    Returns:
        A new merged dictionary.

    Raises:
        ValueError: If priority is not "first" or "last".

    Example:
        >>> d1 = {"a": 1, "b": 2}
        >>> d2 = {"b": 3, "c": 4}
        >>> merge_dicts(d1, d2, priority="last")
        {'a': 1, 'b': 3, 'c': 4}
    """
    if priority not in ("first", "last"):
        raise ValueError("priority must be 'first' or 'last'")
    
    result: Dict[str, Any] = {}
    for d in dicts:
        if priority == "last":
            result.update(d)
        else:  # priority == "first"
            for key, value in d.items():
                result.setdefault(key, value)
    return result


def validate_email(email: str) -> bool:
    """Validate an email address using regex.

    Args:
        email: The email address to validate.

    Returns:
        True if the email is valid, False otherwise.

    Note:
        This is a basic validation. For production use, consider
        sending a verification email instead.

    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid")
        False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


class RateLimiter:
    """A simple token bucket rate limiter.
    
    Useful for throttling API calls or other rate-limited operations.

    Attributes:
        max_tokens: Maximum number of tokens in the bucket.
        refill_rate: Tokens added per second.
        tokens: Current number of tokens.
        last_refill: Timestamp of last token refill.

    Example:
        >>> limiter = RateLimiter(max_tokens=10, refill_rate=1)
        >>> for _ in range(5):
        ...     limiter.acquire()
        True
        >>> limiter.acquire()  # Still has tokens
        True
        >>> time.sleep(2)
        >>> limiter.acquire()  # Tokens refilled
        True
    """

    def __init__(self, max_tokens: int = 10, refill_rate: float = 1.0):
        """Initialize the rate limiter.

        Args:
            max_tokens: Maximum capacity of the token bucket.
            refill_rate: Number of tokens to add per second.
        """
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.tokens = float(max_tokens)
        self.last_refill = time.time()

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.max_tokens, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def acquire(self, tokens: int = 1) -> bool:
        """Attempt to acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire. Defaults to 1.

        Returns:
            True if tokens were acquired, False otherwise.
        """
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def wait_time(self, tokens: int = 1) -> float:
        """Calculate wait time needed to acquire tokens.

        Args:
            tokens: Number of tokens desired.

        Returns:
            Seconds to wait, or 0 if tokens are available now.
        """
        self._refill()
        if self.tokens >= tokens:
            return 0.0
        return (tokens - self.tokens) / self.refill_rate


if __name__ == "__main__":
    # Run simple demonstrations
    print("=== Clean Utils Demo ===")
    
    # JSON parsing
    print("\n1. Safe JSON Parsing:")
    print(f"   Valid: {safe_parse_json('{"test": true}')}")
    print(f"   Invalid: {safe_parse_json('bad json', {})}")
    
    # Text utilities
    print("\n2. Text Truncation:")
    print(f"   {truncate_text('This is a very long text that should be truncated', 30)}")
    
    # Hash generation
    print("\n3. Hash Generation:")
    print(f"   SHA256: {generate_hash('BYRD')[:16]}...")
    
    # URL extraction
    print("\n4. URL Extraction:")
    text = "Check https://byrd.ai and http://example.com"
    print(f"   Found: {extract_urls(text)}")
    
    # Dictionary merging
    print("\n5. Dictionary Merging:")
    merged = merge_dicts({"a": 1}, {"b": 2}, {"a": 3})
    print(f"   Result: {merged}")
    
    # Rate limiter
    print("\n6. Rate Limiter:")
    limiter = RateLimiter(max_tokens=5, refill_rate=10)
    for i in range(7):
        acquired = limiter.acquire()
        print(f"   Request {i+1}: {'OK' if acquired else 'Rate Limited'}")
    
    print("\n=== Demo Complete ===")
