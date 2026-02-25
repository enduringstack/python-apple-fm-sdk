# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

"""
Test Foundation Models Generable protocol behavior
"""

import apple_fm_sdk as fm
import pytest


def test_direct_subclass_raises_error():
    """Test that directly subclassing Generable raises a TypeError."""
    print("\n=== Testing Direct Subclass of Generable ===")

    with pytest.raises(TypeError) as exc_info:

        class InvalidGenerable(fm.Generable):
            """This should raise an error."""

            name: str
            age: int

    # Verify the error message
    error_message = str(exc_info.value)
    assert "Subclassing Protocol Generable is not allowed" in error_message
    assert "Use the @fm.generable() decorator instead" in error_message
    print(f"✓ Correctly raised TypeError: {error_message}")


def test_decorator_approach_works():
    """Test that using the @fm.generable() decorator works correctly."""
    print("\n=== Testing Decorator Approach ===")

    # This should work without raising an error
    @fm.generable()
    class ValidGenerable:
        """This should work correctly."""

        name: str
        age: int

    # Verify it's recognized as a Generable
    assert isinstance(ValidGenerable, fm.Generable)
    print("✓ Decorator approach works correctly")

    # Verify it has the required methods
    assert hasattr(ValidGenerable, "generation_schema")
    assert hasattr(ValidGenerable, "_from_generated_content")
    print("✓ Has required Generable methods")


def test_error_message_content():
    """Test that the error message contains helpful information."""
    print("\n=== Testing Error Message Content ===")

    with pytest.raises(TypeError) as exc_info:

        class TestClass(fm.Generable):
            pass

    error_message = str(exc_info.value)

    # Check for key phrases in the error message
    assert "Subclassing Protocol Generable is not allowed" in error_message
    assert "@fm.generable()" in error_message or "decorator" in error_message

    print(f"✓ Error message is helpful: '{error_message}'")
