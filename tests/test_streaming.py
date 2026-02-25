# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

"""
Tests for streaming response functionality.
"""

import apple_fm_sdk as fm
import pytest


@pytest.mark.asyncio
async def test_streaming(model):
    """Test streaming response functionality."""
    print("\n=== Testing Streaming Response ===")

    # Get the default model
    session = fm.LanguageModelSession("You are a helpful assistant.", model=model)

    print("Starting streaming response...")
    chunks = []
    chunk_count = 0

    # Stream response chunks
    async for chunk in session.stream_response(
        "Tell me a very short story about a cat"
    ):
        chunks.append(chunk)
        chunk_count += 1
        if chunk_count <= 3:  # Show first 3 chunks
            print(f"✓ Received chunk {chunk_count}: {chunk[:50]}...")

    full_response = chunks[-1] if chunks else ""
    print(f"✓ Streaming completed with {chunk_count} chunks")
    print(f"✓ Final response length: {len(full_response)} characters")

    # Validate we got a reasonable response
    assert len(full_response) > 10, "Response too short"
    assert isinstance(full_response, str), (
        f"Expected string response, got {type(full_response)}"
    )
    print("Full response:", full_response)
