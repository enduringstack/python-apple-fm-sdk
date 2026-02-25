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
from tester_tools.tester_tools import SimpleCalculatorTool


# =============================================================================
# TOOL TESTS (from src/apple_fm_sdk/tool.py)
# =============================================================================


@pytest.mark.asyncio
async def test_tool_simple_calculator(model):
    """Test from: src/apple_fm_sdk/tool.py - Tool class docstring - Simple calculator tool"""
    print("\n=== Testing Simple Calculator Tool ===")

    ##############################################################################
    # From: src/apple_fm_sdk/tool.py
    # class, function, or other entity name: Tool - Simple calculator tool
    import apple_fm_sdk as fm

    @fm.generable("Calculator parameters")
    class CalculatorParams:
        operation: str = fm.guide("The operation to perform")
        a: float = fm.guide("First number")
        b: float = fm.guide("Second number")

    class CalculatorTool(fm.Tool):
        name = "calculator"
        description = "Performs basic arithmetic operations"

        @property
        def arguments_schema(self) -> fm.GenerationSchema:
            return CalculatorParams.generation_schema()

        async def call(self, args: fm.GeneratedContent) -> str:
            op = args.value(str, for_property="operation")
            a = args.value(float, for_property="a")
            b = args.value(float, for_property="b")

            if op == "add":
                result = a + b
            elif op == "multiply":
                result = a * b
            else:
                raise ValueError(f"Unknown operation: {op}")

            return str(result)

    ##############################################################################

    # Verify the tool was created successfully
    tool = CalculatorTool()
    assert tool.name == "calculator"
    print("✅ Simple calculator tool - PASSED")


@pytest.mark.asyncio
async def test_tool_with_async_api_call(model):
    """Test from: src/apple_fm_sdk/tool.py - Tool class docstring - Tool with async API call"""
    print("\n=== Testing Tool with Async API Call ===")

    ##############################################################################
    # From: src/apple_fm_sdk/tool.py
    # class, function, or other entity name: Tool - Tool with async API call
    import apple_fm_sdk as fm

    @fm.generable("Weather parameters")
    class WeatherParams:
        city: str = fm.guide("The city to get weather for")
        units: str = fm.guide("Temperature units (metric or imperial)")

    class WeatherTool(fm.Tool):
        name = "get_weather"
        description = "Gets current weather for a city"

        @property
        def arguments_schema(self) -> fm.GenerationSchema:
            return WeatherParams.generation_schema()

        async def call(self, args: fm.GeneratedContent) -> str:
            city = args.value(str, for_property="city")
            try:
                units = args.value(str, for_property="units")
            except Exception:
                units = "metric"

            # Implement async API call to fetch weather here
            return "Sunny, 25°C"  # Placeholder response

    ##############################################################################

    # Verify the tool was created successfully
    tool = WeatherTool()
    assert tool.name == "get_weather"
    print("✅ Tool with async API call - PASSED")


@pytest.mark.asyncio
async def test_tool_with_error_handling(model):
    """Test from: src/apple_fm_sdk/tool.py - Tool class docstring - Tool with error handling"""
    print("\n=== Testing Tool with Error Handling ===")

    ##############################################################################
    # From: src/apple_fm_sdk/tool.py
    # class, function, or other entity name: Tool - Tool with error handling
    import apple_fm_sdk as fm

    @fm.generable("Database query parameters")
    class DatabaseParams:
        user_id: int = fm.guide("The user ID to query")

    class DatabaseTool(fm.Tool):
        name = "query_database"
        description = "Queries the user database"

        @property
        def arguments_schema(self) -> fm.GenerationSchema:
            return DatabaseParams.generation_schema()

        async def call(self, args: fm.GeneratedContent) -> str:
            user_id = args.value(int, for_property="user_id")
            # Implement database query with error handling here
            return f"User data for ID {user_id}"  # Placeholder response

    ##############################################################################

    # Note: This test just verifies the tool can be created
    # The actual database functions are not implemented
    print("✅ Tool with error handling - PASSED (structure verified)")


@pytest.mark.asyncio
async def test_tool_using_tools_in_session(model):
    """Test from: src/apple_fm_sdk/tool.py - Tool class docstring - Using tools in a session"""
    print("\n=== Testing Using Tools in Session ===")

    ##############################################################################
    # From: src/apple_fm_sdk/tool.py
    # class, function, or other entity name: Tool - Using tools in a session
    from apple_fm_sdk import LanguageModelSession

    session = LanguageModelSession(
        instructions="You are a helpful assistant with access to tools.",
        tools=[SimpleCalculatorTool()],
    )

    # Model will automatically use tools when appropriate
    response = await session.respond("What's 15% of 240?")
    # Model invokes CalculatorTool internally
    ##############################################################################

    assert response is not None
    print("✅ Using tools in session - PASSED")


@pytest.mark.asyncio
async def test_tool_arguments_schema_property(model):
    """Test from: src/apple_fm_sdk/tool.py - arguments_schema property docstring"""
    print("\n=== Testing Arguments Schema Property ===")

    ##############################################################################
    # From: src/apple_fm_sdk/tool.py
    # class, function, or other entity name: arguments_schema - Property example
    import apple_fm_sdk as fm

    @fm.generable("Search parameters")
    class SearchParams:
        query: str = fm.guide("The search query")
        limit: int = fm.guide("Maximum number of results")

    @property
    def arguments_schema(self) -> fm.GenerationSchema:
        return SearchParams.generation_schema()

    ##############################################################################

    # Note: This is just a method definition, not a complete test
    print("✅ Arguments schema property - PASSED (structure verified)")


@pytest.mark.asyncio
async def test_tool_call_method(model):
    """Test from: src/apple_fm_sdk/tool.py - call method docstring"""
    print("\n=== Testing Call Method ===")

    ##############################################################################
    # From: src/apple_fm_sdk/tool.py
    # class, function, or other entity name: call - Method example
    import apple_fm_sdk as fm

    async def call(self, args: fm.GeneratedContent) -> str:
        query = args.value(str, for_property="query")
        try:
            limit = args.value(int, for_property="limit")
        except Exception:
            limit = 10

        # Perform async operation, e.g., database search or another session call here

        return f"Results for '{query}' with limit {limit}"  # Placeholder response

    ##############################################################################

    # Note: This is just a method definition, not a complete test
    print("✅ Call method - PASSED (structure verified)")
