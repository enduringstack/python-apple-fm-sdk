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
# GENERATION_GUIDE TESTS (from src/apple_fm_sdk/generation_guide.py)
# =============================================================================


@pytest.mark.asyncio
async def test_generation_guide_module_example(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - Module docstring example"""
    print("\n=== Testing Generation Guide Module Example ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: Module - Example
    import apple_fm_sdk as fm
    from apple_fm_sdk.generation_guide import guide

    @fm.generable("A cat's profile")
    class Cat:
        name: str = guide("Cat's name")
        age: int = guide("Age in years", range=(0, 20))
        favoriteFood: str = guide("Favorite food", anyOf=["fish", "chicken", "tuna"])

    ##############################################################################

    # Verify the class was created successfully
    assert hasattr(Cat, "generation_schema")
    print("✅ Generation guide module example - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_anyof(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.anyOf"""
    print("\n=== Testing GenerationGuide.anyOf ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.anyOf
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.anyOf(["red", "green", "blue"])
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.anyOf - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_constant(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.constant"""
    print("\n=== Testing GenerationGuide.constant ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.constant
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.constant("active")
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.constant - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_count(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.count"""
    print("\n=== Testing GenerationGuide.count ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.count
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.count(5)
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.count - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_element(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.element"""
    print("\n=== Testing GenerationGuide.element ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.element
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.element(GenerationGuide.range((0, 100)))
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.element - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_max_items(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.max_items"""
    print("\n=== Testing GenerationGuide.max_items ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.max_items
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.max_items(10)
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.max_items - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_maximum(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.maximum"""
    print("\n=== Testing GenerationGuide.maximum ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.maximum
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.maximum(100.0)
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.maximum - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_min_items(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.min_items"""
    print("\n=== Testing GenerationGuide.min_items ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.min_items
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.min_items(1)
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.min_items - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_minimum(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.minimum"""
    print("\n=== Testing GenerationGuide.minimum ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.minimum
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.minimum(0.0)
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.minimum - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_range(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.range"""
    print("\n=== Testing GenerationGuide.range ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.range
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.range((0, 120))
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.range - PASSED")


@pytest.mark.asyncio
async def test_generation_guide_regex(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - GenerationGuide.regex"""
    print("\n=== Testing GenerationGuide.regex ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: GenerationGuide.regex
    from apple_fm_sdk.generation_guide import GenerationGuide

    guide = GenerationGuide.regex(r"#/[a-zA-Z]+/#")
    ##############################################################################

    assert guide is not None
    print("✅ GenerationGuide.regex - PASSED")


@pytest.mark.asyncio
async def test_guide_function_basic_field(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Basic field with description only"""
    print("\n=== Testing guide Function Basic Field ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Basic field with description only
    from apple_fm_sdk.generation_guide import guide

    name: str = guide("The person's full name")
    ##############################################################################

    assert name is not None
    print("✅ guide function basic field - PASSED")


@pytest.mark.asyncio
async def test_guide_function_numeric_range(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Numeric field with range constraint"""
    print("\n=== Testing guide Function Numeric Range ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Numeric field with range constraint
    from apple_fm_sdk.generation_guide import guide

    age: int = guide("Age in years", range=(0, 120))
    ##############################################################################

    assert age is not None
    print("✅ guide function numeric range - PASSED")


@pytest.mark.asyncio
async def test_guide_function_collection_count(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Collection with exact count"""
    print("\n=== Testing guide Function Collection Count ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Collection with exact count
    from apple_fm_sdk.generation_guide import guide
    from typing import List

    hobbies: List[str] = guide("List of hobbies", count=3)
    ##############################################################################

    assert hobbies is not None
    print("✅ guide function collection count - PASSED")


@pytest.mark.asyncio
async def test_guide_function_string_choices(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - String field with choices"""
    print("\n=== Testing guide Function String Choices ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - String field with choices
    from apple_fm_sdk.generation_guide import guide

    color: str = guide("Favorite color", anyOf=["red", "blue", "green"])
    ##############################################################################

    assert color is not None
    print("✅ guide function string choices - PASSED")


@pytest.mark.asyncio
async def test_guide_function_numeric_min_max(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Numeric field with separate min/max"""
    print("\n=== Testing guide Function Numeric Min/Max ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Numeric field with separate min/max
    from apple_fm_sdk.generation_guide import guide

    score: float = guide("Test score", minimum=0.0, maximum=100.0)
    ##############################################################################

    assert score is not None
    print("✅ guide function numeric min/max - PASSED")


@pytest.mark.asyncio
async def test_guide_function_collection_size(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Collection with size constraints"""
    print("\n=== Testing guide Function Collection Size ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Collection with size constraints
    from apple_fm_sdk.generation_guide import guide
    from typing import List

    tags: List[str] = guide("Tags list", min_items=1, max_items=5)
    ##############################################################################

    assert tags is not None
    print("✅ guide function collection size - PASSED")


@pytest.mark.asyncio
async def test_guide_function_constant_value(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Constant value constraint"""
    print("\n=== Testing guide Function Constant Value ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Constant value constraint
    from apple_fm_sdk.generation_guide import guide

    status: str = guide("Status", constant="active")
    ##############################################################################

    assert status is not None
    print("✅ guide function constant value - PASSED")


@pytest.mark.asyncio
async def test_guide_function_regex_pattern(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Regex pattern constraint"""
    print("\n=== Testing guide Function Regex Pattern ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Regex pattern constraint
    from apple_fm_sdk.generation_guide import guide

    email: str = guide("Name", regex=r"#/[a-zA-Z]+/#")
    ##############################################################################

    assert email is not None
    print("✅ guide function regex pattern - PASSED")


@pytest.mark.asyncio
async def test_guide_function_element_constraint(model):
    """Test from: src/apple_fm_sdk/generation_guide.py - guide function - Element constraint for arrays"""
    print("\n=== Testing guide Function Element Constraint ===")

    ##############################################################################
    # From: src/apple_fm_sdk/generation_guide.py
    # class, function, or other entity name: guide - Element constraint for arrays
    from apple_fm_sdk.generation_guide import guide, GenerationGuide
    from typing import List

    scores: List[int] = guide("Test scores", element=GenerationGuide.range((0, 100)))
    ##############################################################################

    assert scores is not None
    print("✅ guide function element constraint - PASSED")
