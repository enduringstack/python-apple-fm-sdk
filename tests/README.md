# Foundation Models SDK for Python - Tests

Tests for the Foundation Models SDK for Python package using pytest.

## Running Tests

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_session.py
```

Show all debug printouts:

```bash
pytest -s
```

Run documentation website snippet tests:

```bash
pytest tests/test_doc_website_snippets.py -v
```

## Test Files

- `test_session.py` - Session management and basic operations
- `test_system_model.py` - System model functionality
- `test_streaming.py` - Streaming response handling
- `test_prompts.py` - Prompt processing and scenarios
- `test_transcript.py` - Transcript operations
- `test_tool.py` - Tool calling functionality
- `test_guided_generation.py` - Guided generation features
- `test_guides.py` - Generation guides
- `test_json_guided_generation.py` - JSON-guided generation
- `test_memory.py` - Memory management
- `test_memory_stress.py` - Memory stress testing
- `test_readme_snippets.py` - README code examples validation
- `test_doc_website_snippets.py` - Documentation website code examples validation
- `test_error_handling.py` - Error handling
- `conftest.py` - Shared pytest fixtures and configuration

## Documentation Website Tests

The `test_doc_website_snippets.py` file contains comprehensive tests for all code examples in the documentation website. This ensures that:

1. All code examples are syntactically correct
2. Examples are runnable without errors
3. Examples follow best practices
4. Examples check model availability before use

### Test Coverage

The documentation tests cover:

- **basic_usage.rst**: Model creation, availability checks, sessions, text generation, multi-turn sessions, batch evaluation, error handling
- **guided_generation.rst**: @generable decorator, constraints (anyOf, range, count, regex), nested objects, lists of objects, real-world examples
- **streaming.rst**: Basic streaming, streaming with context, collecting content, error handling, cancellation
- **tools.rst**: Tool definition, calculator tool, file system tool
- **evaluation.rst**: Transcript processing, batch evaluation, transcript format validation

### Known Pylance Warnings

The `test_doc_website_snippets.py` file may show some Pylance warnings that are expected:

1. **Tool `arguments_schema` override**: The documentation examples show `def arguments_schema(self)` but the actual API uses `@property`. The tests use the method form to match documentation examples. This is intentional for testing documentation accuracy.

2. **Transcript import**: `fm.Transcript` may show as unknown because Transcript is not exported in `__init__.py`. The tests use a workaround by testing transcript data structures directly rather than importing Transcript.

3. **`is_responding()` callable**: The session method `is_responding()` may show type warnings. This is a known issue with the type stubs and does not affect functionality.

These warnings do not prevent the tests from running successfully and are tracked for documentation/API alignment.

## Test Organization

Tests are organized by feature area and documentation page. Each test function:

- Has a descriptive name indicating what it tests
- Includes print statements for debugging
- Uses the `model` fixture from `conftest.py` for model availability
- Handles errors gracefully with appropriate assertions

## Adding New Tests

When adding new code examples to the documentation:

1. Add corresponding tests to `test_doc_website_snippets.py`
2. Follow the existing test structure and naming conventions
3. Include print statements for test progress tracking
4. Ensure tests check model availability before use
5. Update the test coverage summary at the end of the file

---
For licensing see accompanying LICENSE file.
Copyright (C) 2026 Apple Inc. All Rights Reserved.

