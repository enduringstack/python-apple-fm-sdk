# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

"""
Test all code snippets from Python library code source documentation

RULES:
Use this consistent testing format:
- Each test function should correspond to a specific code snippet or section in the documentation.
- Include comments indicating the source documentation file and section for clarity.
- No extra tests beyond those needed to validate the snippets.

Copy the snippet from the source **exactly** as it appears in the documentation.
Surround the original source with:
##############################################################################
# From: src/apple_fm_sdk/<source_file>.py
# class, function, or other entity name: <source_section_name>
<actual code here uncommented>
##############################################################################

The test passes if the snippet runs without errors. No additional assertions are necessary
beyond ensuring the snippet executes successfully.
"""

import pytest


# =============================================================================
# GENERABLE_UTILS TESTS (from src/apple_fm_sdk/generable_utils.py)
# =============================================================================


@pytest.mark.asyncio
async def test_generable_utils_basic_usage(model):
    """Test from: src/apple_fm_sdk/generable_utils.py - Module docstring - Basic usage"""
    print("\n=== Testing Generable Utils Basic Usage ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generable_utils.py
    # class, function, or other entity name: Module - Basic usage
    import apple_fm_sdk as fm

    @fm.generable("A cat's profile")
    class Cat:
        name: str = fm.guide("Cat's name")
        age: int = fm.guide("Age in years", range=(0, 20))
        breed: str = fm.guide("Cat breed")

    # The class now has generation_schema() method
    schema = Cat.generation_schema()

    # Can be used with Session.respond() for guided generation
    # cat = session.respond(Cat, prompt="Generate a cat named Maomao who is 2 years old")
    ##############################################################################

    assert schema is not None
    print("✅ Generable utils basic usage - PASSED")


@pytest.mark.asyncio
async def test_generable_decorator_basic_usage(model):
    """Test from: src/apple_fm_sdk/generable_utils.py - generable function docstring - Basic usage with a dataclass"""
    print("\n=== Testing Generable Decorator Basic Usage ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generable_utils.py
    # class, function, or other entity name: generable - Basic usage with a dataclass
    import apple_fm_sdk as fm

    @fm.generable("A cat's profile")
    class Cat:
        name: str = fm.guide("Cat's name")
        age: int = fm.guide("Age in years", range=(0, 20))
        profile: str = fm.guide("What makes this cat unique")

    ##############################################################################

    # Verify the class has the generable attributes
    assert hasattr(Cat, "generation_schema")
    assert Cat._generable is True
    print("✅ Generable decorator basic usage - PASSED")


@pytest.mark.asyncio
async def test_generable_decorator_with_session(model):
    """Test from: src/apple_fm_sdk/generable_utils.py - generable function docstring - Using with Session for guided generation"""
    print("\n=== Testing Generable Decorator with Session ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generable_utils.py
    # class, function, or other entity name: generable - Using with Session for guided generation
    import apple_fm_sdk as fm

    @fm.generable("A cat's profile")
    class Cat:
        name: str = fm.guide("Cat's name")
        age: int = fm.guide("Age in years", range=(0, 20))
        profile: str = fm.guide("What makes this cat unique")

    session = fm.LanguageModelSession()
    cat = await session.respond(
        "Generate a cat named Maomao who is 2 years old and has a fluffy tail",
        generating=Cat,
    )
    print(f"{cat.name} is {cat.age} years old: {cat.profile}")
    ##############################################################################

    assert cat is not None
    assert hasattr(cat, "name")
    print("✅ Generable decorator with session - PASSED")


@pytest.mark.asyncio
async def test_generable_decorator_nested_types(model):
    """Test from: src/apple_fm_sdk/generable_utils.py - generable function docstring - Nested generable types"""
    print("\n=== Testing Generable Decorator Nested Types ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generable_utils.py
    # class, function, or other entity name: generable - Nested generable types
    import apple_fm_sdk as fm

    @fm.generable("A cat's profile")
    class Cat:
        name: str = fm.guide("Cat's name")
        age: int = fm.guide("Age in years", range=(0, 20))
        profile: str = fm.guide("What makes this cat unique")

    @fm.generable("Pet club")
    class PetClub:
        name: str = fm.guide("Club name")
        cats: list[Cat] = fm.guide("List of cats in the club")

    ##############################################################################

    # Verify the nested structure
    assert hasattr(PetClub, "generation_schema")
    schema = PetClub.generation_schema()
    assert schema is not None
    print("✅ Generable decorator nested types - PASSED")
