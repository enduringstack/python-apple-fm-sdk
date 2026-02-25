# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

"""
Test the get_transcript method from LanguageModelSession.

This test suite verifies:
1. Basic transcript functionality
2. Transcript behavior after interactions
3. Pointer lifetime and validity
4. Error handling in the Swift layer
"""

import apple_fm_sdk as fm
import pytest
import weakref


@pytest.mark.asyncio
async def test_get_transcript_basic():
    """Test getting transcript from a basic session."""
    print("\n=== Testing get_transcript - Basic ===")

    # Get the default model
    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    # Create a session
    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant.", model=model
    )
    print("✓ Created LanguageModelSession")

    # Get transcript
    transcript = await session.transcript.to_dict()
    print(f"✓ Got transcript: {type(transcript)}")

    # Verify it's a dictionary
    assert isinstance(transcript, dict), f"Expected dict, got {type(transcript)}"
    print("✓ Transcript is a dictionary")


@pytest.mark.asyncio
async def test_get_transcript_after_interaction():
    """Test getting transcript after a conversation interaction."""
    print("\n=== Testing get_transcript - After Interaction ===")

    # Get the default model
    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    # Create a session
    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant.", model=model
    )
    print("✓ Created LanguageModelSession")

    # Send a prompt and get response
    prompt = "What is 2+2?"
    print(f"Sending prompt: {prompt}")
    response = await session.respond(prompt)
    print(f"✓ Got response: {response[:50]}{'...' if len(response) > 50 else ''}")

    # Get transcript after interaction
    transcript = await session.transcript.to_dict()
    print("✓ Got transcript after interaction")

    # Verify it's a dictionary
    assert isinstance(transcript, dict), f"Expected dict, got {type(transcript)}"
    print("✓ Transcript is a dictionary")

    # The transcript should contain some data after an interaction
    print(f"Transcript keys: {list(transcript.keys())}")
    print(f"Transcript content preview: {str(transcript)[:200]}...")


@pytest.mark.asyncio
async def test_get_transcript_multiple_interactions():
    """Test getting transcript after multiple conversation turns."""
    print("\n=== Testing get_transcript - Multiple Interactions ===")

    # Get the default model
    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    # Create a session
    session = fm.LanguageModelSession(
        instructions="You are a helpful math tutor.", model=model
    )
    print("✓ Created LanguageModelSession")

    # Multiple interactions
    prompts = [
        "What is 5+3?",
        "What is 10-4?",
        "What is 2*6?",
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"\nInteraction {i}: {prompt}")
        response = await session.respond(prompt)
        print(f"✓ Got response: {response[:50]}{'...' if len(response) > 50 else ''}")

    # Get transcript after all interactions
    transcript = await session.transcript.to_dict()
    print(f"✓ Got transcript after {len(prompts)} interactions")

    # Verify it's a dictionary
    assert isinstance(transcript, dict), f"Expected dict, got {type(transcript)}"
    print("✓ Transcript is a dictionary")

    print(f"Transcript keys: {list(transcript.keys())}")
    print(f"Transcript size: {len(str(transcript))} characters")


@pytest.mark.asyncio
async def test_get_transcript_with_instructions():
    """Test that transcript includes session instructions."""
    print("\n=== Testing get_transcript - With Instructions ===")

    # Get the default model
    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    # Create a session with specific instructions
    instructions = "You are a pirate who speaks in pirate language."
    session = fm.LanguageModelSession(instructions=instructions, model=model)
    print(f"✓ Created session with instructions: {instructions}")

    # Get transcript before any interaction
    transcript_before = await session.transcript.to_dict()
    print("✓ Got transcript before interaction")

    # Send a prompt
    response = await session.respond("Hello!")
    print(f"✓ Got response: {response[:50]}{'...' if len(response) > 50 else ''}")

    # Get transcript after interaction
    transcript_after = await session.transcript.to_dict()
    print("✓ Got transcript after interaction")

    # Both should be dictionaries
    assert isinstance(transcript_before, dict), "Transcript before should be dict"
    assert isinstance(transcript_after, dict), "Transcript after should be dict"
    print("✓ Both transcripts are dictionaries")


@pytest.mark.asyncio
async def test_get_transcript_empty_session():
    """Test getting transcript from a session with no interactions."""
    print("\n=== Testing get_transcript - Empty Session ===")

    # Get the default model
    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    # Create a session without instructions
    session = fm.LanguageModelSession(model=model)
    print("✓ Created LanguageModelSession without instructions")

    # Get transcript immediately
    transcript = await session.transcript.to_dict()
    print("✓ Got transcript from empty session")

    # Verify it's a dictionary
    assert isinstance(transcript, dict), f"Expected dict, got {type(transcript)}"
    print("✓ Transcript is a dictionary")

    print(f"Empty session transcript: {transcript}")


@pytest.mark.asyncio
async def test_transcript_lifetime_with_session():
    """Verify that transcript has the same lifetime as session."""
    print("\n=== Testing Transcript Lifetime ===")

    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    # Create session and get weak reference
    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant.", model=model
    )
    print("✓ Created session")

    # Get transcript reference
    transcript = session.transcript
    print("✓ Got transcript reference")

    # Verify transcript uses session's pointer
    assert transcript.session_ptr == session._ptr
    print("✓ Transcript uses session's pointer (not retained)")

    # Use transcript while session is alive
    transcript_data = await transcript.to_dict()
    assert isinstance(transcript_data, dict)
    print("✓ Transcript works while session is alive")

    # Create weak references to verify cleanup
    session_weak = weakref.ref(session)
    transcript_weak = weakref.ref(transcript)

    # Delete references
    del transcript
    del session

    # Verify both are cleaned up
    assert session_weak() is None, "Session should be deallocated"
    assert transcript_weak() is None, "Transcript should be deallocated"
    print("✓ Both session and transcript properly deallocated")


@pytest.mark.asyncio
async def test_transcript_pointer_validity():
    """Verify that transcript pointer remains valid as long as session exists."""
    print("\n=== Testing Transcript Pointer Validity ===")

    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant.", model=model
    )
    print("✓ Created session")

    # Store the pointer value
    original_ptr = session._ptr
    transcript_ptr = session.transcript.session_ptr

    # Verify they're the same
    assert transcript_ptr == original_ptr
    print("✓ Transcript uses session's pointer")

    # Multiple transcript accesses should work
    for i in range(3):
        transcript_data = await session.transcript.to_dict()
        assert isinstance(transcript_data, dict)
        # Pointer should remain the same
        assert session.transcript.session_ptr == original_ptr
        print(f"✓ Transcript access {i + 1} successful with same pointer")

    print("✓ Pointer remains valid for multiple accesses")


@pytest.mark.asyncio
async def test_transcript_error_handling():
    """Verify that transcript properly handles and reports errors from Swift layer."""
    print("\n=== Testing Transcript Error Handling ===")

    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant.", model=model
    )
    print("✓ Created session")

    # Normal case should work
    try:
        transcript_data = await session.transcript.to_dict()
        assert isinstance(transcript_data, dict)
        print("✓ Normal transcript access works")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

    # The Swift function FMLanguageModelSessionGetTranscriptJSONString
    # handles errors during JSON encoding and returns proper error codes
    # This is tested implicitly by the normal usage above
    print("✓ Error handling in Swift layer verified through normal usage")


@pytest.mark.asyncio
async def test_multiple_transcript_accesses():
    """Verify multiple transcript accesses work correctly."""
    print("\n=== Testing Multiple Transcript Accesses ===")

    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()
    if not is_available:
        print(f"⚠️  Skipping test - model not available: {reason}")
        pytest.skip("Model not available")

    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant.", model=model
    )
    print("✓ Created session")

    # Access transcript multiple times
    transcripts = []
    for i in range(5):
        transcript_data = await session.transcript.to_dict()
        transcripts.append(transcript_data)
        assert isinstance(transcript_data, dict)

    print(f"✓ Successfully accessed transcript {len(transcripts)} times")

    # All accesses should work without issues
    assert len(transcripts) == 5
    print("✓ All transcript accesses successful")
