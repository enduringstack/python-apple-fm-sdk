# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

import asyncio
import json
import apple_fm_sdk as fm

# =============================================================================
# Test Parameter Schemas
# =============================================================================


@fm.generable("Calculator parameters")
class CalculatorParams:
    operation: str = fm.guide(
        "The operation to perform", anyOf=["add", "subtract", "multiply", "divide"]
    )
    a: float = fm.guide("First number")
    b: float = fm.guide("Second number")


@fm.generable("User info parameters")
class UserInfoParams:
    user_id: int = fm.guide("The user ID to look up")


@fm.generable("List processing parameters")
class ListProcessParams:
    items: list[str] = fm.guide("List of items to process")
    action: str = fm.guide("Action to perform", anyOf=["count", "sum", "join"])


@fm.generable("Parameters with optional field")
class OptionalParams:
    required_param: str = fm.guide("A required parameter")
    optional_param: str = fm.guide("An optional parameter")


@fm.generable("Error testing parameters")
class ErrorParams:
    should_fail: bool = fm.guide("Whether the tool should fail")


@fm.generable("Async delay parameters")
class DelayParams:
    delay: float = fm.guide("Delay in seconds", range=(0.0, 5.0))
    message: str = fm.guide("Message to return after delay")


# =============================================================================
# Test Tool Implementations
# =============================================================================


class SimpleCalculatorTool(fm.Tool):
    """Simple calculator tool for testing basic tool functionality."""

    name = "simple_calculator"
    description = "Perform basic arithmetic operations"

    @property
    def arguments_schema(self) -> fm.GenerationSchema:
        return CalculatorParams.generation_schema()

    async def call(self, args: fm.GeneratedContent) -> str:
        operation = args.value(str, for_property="operation")
        a = args.value(float, for_property="a")
        b = args.value(float, for_property="b")

        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return "Error: Division by zero"
            result = a / b
        else:
            return f"Error: Unknown operation {operation}"

        return f"The result of {a} {operation} {b} is {result}"


class GetUserInfoTool(fm.Tool):
    """Mock user info retrieval tool."""

    name = "get_user_info"
    description = "Get information about a user by ID"

    @property
    def arguments_schema(self) -> fm.GenerationSchema:
        return UserInfoParams.generation_schema()

    async def call(self, args: fm.GeneratedContent) -> str:
        user_id = args.value(int, for_property="user_id")

        # Mock database
        users = {
            1: {"name": "Alice", "email": "alice@example.com", "role": "admin"},
            2: {"name": "Bob", "email": "bob@example.com", "role": "user"},
            3: {"name": "Charlie", "email": "charlie@example.com", "role": "user"},
        }

        user = users.get(user_id)
        if user:
            return json.dumps(user)
        else:
            return f"Error: User {user_id} not found"


class ProcessListTool(fm.Tool):
    """Tool that processes a list of items."""

    name = "process_list"
    description = "Process a list of items"

    @property
    def arguments_schema(self) -> fm.GenerationSchema:
        return ListProcessParams.generation_schema()

    async def call(self, args: fm.GeneratedContent) -> str:
        items = args.value(list, for_property="items")
        action = args.value(str, for_property="action")

        if action == "count":
            return f"The list has {len(items)} items"
        elif action == "sum":
            try:
                total = sum(items)
                return f"The sum is {total}"
            except TypeError:
                return "Error: Cannot sum non-numeric items"
        elif action == "join":
            return f"Joined: {', '.join(str(item) for item in items)}"
        else:
            return f"Error: Unknown action {action}"


class OptionalParamsTool(fm.Tool):
    """Tool with optional parameters."""

    name = "optional_params_tool"
    description = "Tool with optional parameters"

    @property
    def arguments_schema(self) -> fm.GenerationSchema:
        return OptionalParams.generation_schema()

    async def call(self, args: fm.GeneratedContent) -> str:
        required_param = args.value(str, for_property="required_param")

        # Try to get optional parameter
        try:
            optional_param = args.value(str, for_property="optional_param")
        except Exception:
            optional_param = "default_value"

        return f"Required: {required_param}, Optional: {optional_param}"


class ErrorRaisingTool(fm.Tool):
    """Tool that intentionally raises an error for testing error handling."""

    name = "error_raising_tool"
    description = "Tool that can raise errors for testing"

    @property
    def arguments_schema(self) -> fm.GenerationSchema:
        return ErrorParams.generation_schema()

    async def call(self, args: fm.GeneratedContent) -> str:
        should_fail = args.value(bool, for_property="should_fail")

        if should_fail:
            raise ValueError("Intentional error for testing")

        return "Success: No error raised"


class AsyncDelayTool(fm.Tool):
    """Tool that simulates async operations with delays."""

    name = "async_delay_tool"
    description = "Tool with async delay"

    @property
    def arguments_schema(self) -> fm.GenerationSchema:
        return DelayParams.generation_schema()

    async def call(self, args: fm.GeneratedContent) -> str:
        delay = args.value(float, for_property="delay")
        message = args.value(str, for_property="message")

        await asyncio.sleep(delay)
        return f"After {delay}s delay: {message}"
