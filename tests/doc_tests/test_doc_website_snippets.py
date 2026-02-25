# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.

"""
Test all code snippets from the documentation website.

RULES:
Use this consistent testing format:
- Each test function should correspond to a specific code snippet or section in the documentation.
- Include comments indicating the source documentation file and section for clarity.
- No extra tests beyond those needed to validate the snippets.

Copy the snippet from the source **exactly** as it appears in the documentation.
Surround the original source with:
##############################################################################
# From: docs/source/<doc_file>.rst
# Section: <section_name>
<actual code here uncommented>
##############################################################################

The test passes if the snippet runs without errors. No additional assertions are necessary
beyond ensuring the snippet executes successfully.
"""

import pytest

# =============================================================================
# BASIC USAGE TESTS (from docs/source/basic_usage.rst)
# =============================================================================


@pytest.mark.asyncio
async def test_basic_usage_model_creation():
    """
    Test from: docs/source/basic_usage.rst
    Section: Creating a Model - basic model creation
    """
    print("\n=== Testing Basic Model Creation ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Creating a Model
    import apple_fm_sdk as fm

    model = fm.SystemLanguageModel()
    ##############################################################################

    print("✅ Model creation - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_availability_check(model):
    """
    Test from: docs/source/basic_usage.rst
    Section: Checking Model Availability
    """
    print("\n=== Testing Model Availability Check ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Checking Model Availability
    is_available, reason = model.is_available()

    if not is_available:
        print(f"Model not available: {reason}")
        # Handle unavailability (for example, show error to user)
    else:
        # Proceed with model usage
        pass
    ##############################################################################

    print("✅ Availability check - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_custom_model_config():
    """
    Test from: docs/source/basic_usage.rst
    Section: Custom Model Configuration
    """
    print("\n=== Testing Custom Model Configuration ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Custom Model Configuration
    import apple_fm_sdk as fm

    model = fm.SystemLanguageModel(
        use_case=fm.SystemLanguageModelUseCase.CONTENT_TAGGING,
        guardrails=fm.SystemLanguageModelGuardrails.PERMISSIVE_CONTENT_TRANSFORMATIONS,
    )
    ##############################################################################

    print("✅ Custom model configuration - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_basic_session(model):
    """
    Test from: docs/source/basic_usage.rst
    Section: Creating a Session - Basic Session
    """
    print("\n=== Testing Basic Session Creation ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Basic Session
    import apple_fm_sdk as fm

    # Create a session with default model
    session = fm.LanguageModelSession()
    ##############################################################################

    assert session is not None
    print("✅ Basic session - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_session_with_custom_model():
    """
    Test from: docs/source/basic_usage.rst
    Section: Session with Custom Model
    """
    print("\n=== Testing Session with Custom Model ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Session with Custom Model
    import apple_fm_sdk as fm

    custom_model = fm.SystemLanguageModel(
        use_case=fm.SystemLanguageModelUseCase.CONTENT_TAGGING,
    )

    session = fm.LanguageModelSession(
        instructions="You are a tagging assistant who can help tag journal entries.",
        model=custom_model,
    )
    ##############################################################################

    print("✅ Session with custom model - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_simple_text_generation(model):
    """
    Test from: docs/source/basic_usage.rst
    Section: Simple Text Generation
    """
    print("\n=== Testing Simple Text Generation ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Simple Text Generation
    import apple_fm_sdk as fm

    async def generate_response():
        model = fm.SystemLanguageModel()
        is_available, _ = model.is_available()

        if is_available:
            session = fm.LanguageModelSession()

            response = await session.respond("What is the Swift bird species?")
            print(response)

    # Run the async function
    await generate_response()
    ##############################################################################

    print("✅ Simple text generation - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_multi_turn_session(model):
    """
    Test from: docs/source/basic_usage.rst
    Section: Multi-turn Sessions
    """
    print("\n=== Testing Multi-turn Session ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Multi-turn Sessions
    import apple_fm_sdk as fm

    async def multi_turn_session():
        session = fm.LanguageModelSession()

        # First question
        response1 = await session.respond("What is the capital of France?")
        print(f"Assistant: {response1}")

        # Follow-up question (context is maintained)
        response2 = await session.respond("What are some famous landmarks there?")
        print(f"Assistant: {response2}")

    await multi_turn_session()
    ##############################################################################

    print("✅ Multi-turn session - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_session_state(session):
    """
    Test from: docs/source/basic_usage.rst
    Section: Checking Session State
    """
    print("\n=== Testing Session State ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Checking Session State
    if session.is_responding:
        print("Session is currently generating a response")
    else:
        print("Session is idle")
    ##############################################################################

    print("✅ Session state check - PASSED")


@pytest.mark.asyncio
async def test_basic_usage_error_handling(model):
    """
    Test from: docs/source/basic_usage.rst
    Section: Error Handling
    """
    print("\n=== Testing Error Handling ===")

    ##############################################################################
    # From: docs/source/basic_usage.rst
    # Section: Error Handling
    import apple_fm_sdk as fm

    async def safe_generation():
        session = fm.LanguageModelSession()

        try:
            response = await session.respond("Your prompt here")
            print(response)
        except fm.ExceededContextWindowSizeError:
            print("Prompt is too long")
        except fm.GuardrailViolationError as e:
            print(f"Caught GuardrailViolationError: {e}")
        except fm.GenerationError as e:
            print(f"Generation error: {e}")

    ##############################################################################

    await safe_generation()
    print("✅ Error handling - PASSED")


# =============================================================================
# GUIDED GENERATION TESTS (from docs/source/guided_generation.rst)
# =============================================================================


@pytest.mark.asyncio
async def test_guided_generation_basic_example(model):
    """
    Test from: docs/source/guided_generation.rst
    Section: The @generable Decorator - Basic Example
    """
    print("\n=== Testing Basic Guided Generation ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: Basic Example
    import apple_fm_sdk as fm
    from typing import List

    @fm.generable("Product review analysis")
    class ProductReview:
        sentiment: str = fm.guide(
            "Overall sentiment", anyOf=["positive", "negative", "neutral"]
        )
        rating: float = fm.guide("Product rating", range=(1.0, 5.0))
        keywords: List[str] = fm.guide("Key features mentioned", count=3)

    async def analyze_review():
        session = fm.LanguageModelSession(
            instructions="You are a product review analyzer."
        )

        result = await session.respond(
            "This laptop is amazing! Great performance and battery life.",
            generating=ProductReview,
        )

        print(f"Sentiment: {result.sentiment}")  # for example, "positive"
        print(f"Rating: {result.rating}")  # for example, 4.5
        print(
            f"Keywords: {result.keywords}"
        )  # for example, ["performance", "battery", "laptop"]

    ##############################################################################

    await analyze_review()
    print("✅ Basic guided generation - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_anyof_constraint():
    """
    Test from: docs/source/guided_generation.rst
    Section: anyOf - Enum Values
    """
    print("\n=== Testing anyOf Constraint ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: anyOf - Enum Values
    import apple_fm_sdk as fm

    @fm.generable("Classification")
    class Category:
        type: str = fm.guide("Category type", anyOf=["tech", "sports", "politics"])
        priority: str = fm.guide("Priority level", anyOf=["high", "medium", "low"])

    ##############################################################################

    print("✅ anyOf constraint - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_range_constraint():
    """
    Test from: docs/source/guided_generation.rst
    Section: range - Numeric Ranges
    """
    print("\n=== Testing range Constraint ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: range - Numeric Ranges
    import apple_fm_sdk as fm

    @fm.generable("Temperature reading")
    class Temperature:
        celsius: float = fm.guide("Temperature in Celsius", range=(-50.0, 50.0))
        confidence: float = fm.guide("Confidence score", range=(0.0, 1.0))

    ##############################################################################

    assert Temperature.generation_schema() is not None
    print("✓ range constraint schema created")
    print("✅ range constraint - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_count_constraint():
    """
    Test from: docs/source/guided_generation.rst
    Section: count - List Length
    """
    print("\n=== Testing count Constraint ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: count - List Length
    import apple_fm_sdk as fm
    from typing import List

    @fm.generable("Top items")
    class TopItems:
        items: List[str] = fm.guide("Top 5 items", count=5)
        tags: List[str] = fm.guide("Exactly 3 tags", count=3)

    ##############################################################################

    schema = TopItems.generation_schema()
    assert schema is not None
    print("✓ count constraint schema created")
    print("✅ count constraint - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_regex_constraint():
    """
    Test from: docs/source/guided_generation.rst
    Section: regex - Pattern Matching
    """
    print("\n=== Testing regex Constraint ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: regex - Pattern Matching
    import apple_fm_sdk as fm

    @fm.generable("Contact information")
    class Contact:
        name: str = fm.guide("Full name", regex=r"\w+\s\w+")
        age: str = fm.guide("Age", regex=r"\d+")

    ##############################################################################

    schema = Contact.generation_schema()
    assert schema is not None
    print("✓ regex constraint schema created")
    print("✅ regex constraint - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_nested_objects(model):
    """
    Test from: docs/source/guided_generation.rst
    Section: Complex Structures - Nested Objects
    """
    print("\n=== Testing Nested Objects ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: Nested Objects
    import apple_fm_sdk as fm

    @fm.generable("Address")
    class Address:
        street: str = fm.guide("Street address")
        city: str = fm.guide("City name")
        state: str = fm.guide("State code", regex=r"\w")
        zip_code: str = fm.guide("ZIP code", regex=r"\d+")

    @fm.generable("Cat profile")
    class Cat:
        name: str = fm.guide("Cat's name")
        age: int = fm.guide("Age in years", range=(0, 20))
        address: Address = fm.guide("Home address")
        breed: str = fm.guide("Cat breed")

    async def extract_cat():
        session = fm.LanguageModelSession(
            "Create a fictional cat from the user's prompt"
        )

        result = await session.respond(
            "Maomao, 2 years old, lives in Maine and is a fluffy tabby.", generating=Cat
        )

        print(f"Name: {result.name}")
        print(f"City: {result.address.city}")
        print(f"Breed: {result.breed}")

    ##############################################################################

    await extract_cat()
    print("✅ Nested objects - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_lists_of_objects(model):
    """
    Test from: docs/source/guided_generation.rst
    Section: Lists of Objects
    """
    print("\n=== Testing Lists of Objects ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: Lists of Objects
    import apple_fm_sdk as fm
    from typing import List

    @fm.generable("Task item")
    class Task:
        title: str = fm.guide("Task title")
        priority: str = fm.guide("Priority", anyOf=["high", "medium", "low"])
        completed: bool = fm.guide("Completion status")

    @fm.generable("Task list")
    class TaskList:
        tasks: List[Task] = fm.guide("List of tasks", count=3)
        total_count: int = fm.guide("Total number of tasks")

    async def extract_tasks():
        session = fm.LanguageModelSession("Extract tasks from text.")

        result = await session.respond(
            "I need to: 1) Buy groceries (high priority), "
            "2) Call dentist (medium), 3) Read book (low)",
            generating=TaskList,
        )

        for task in result.tasks:
            print(f"- {task.title} [{task.priority}]")

    ##############################################################################

    await extract_tasks()
    print("✅ Lists of objects - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_swift_python_mapping():
    """
    Test from: docs/source/guided_generation.rst
    Section: Swift to Python Schema Mapping - Python equivalent
    """
    print("\n=== Testing Swift to Python Schema Mapping ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: Swift to Python Schema Mapping - Equivalent Python Code
    import apple_fm_sdk as fm
    from typing import List

    @fm.generable("Product review")
    class ProductReview:
        sentiment: str = fm.guide("Sentiment")
        rating: float = fm.guide("Rating", range=(1.0, 5.0))
        keywords: List[str] = fm.guide("Keywords", count=3)

    ##############################################################################

    schema = ProductReview.generation_schema()
    assert schema is not None
    print("✓ Swift-compatible Python schema created")
    print("✅ Swift to Python schema mapping - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_schema_compatibility(model):
    """
    Test from: docs/source/guided_generation.rst
    Section: Validating Schema Compatibility - Load and use in Python
    """
    print("\n=== Testing Schema Compatibility Validation ===")

    with pytest.raises(FileNotFoundError):
        ##############################################################################
        # From: docs/source/guided_generation.rst
        # Section: Validating Schema Compatibility - Load and use in Python
        import json
        import apple_fm_sdk as fm

        # Load Swift schema
        with open("schema.json", "r") as f:
            swift_schema = json.load(f)

        # Use in a LanguageModelSession
        session = fm.LanguageModelSession(instructions="Generate a product review.")
        result = await session.respond(
            "This laptop is amazing! Great performance and battery life.",
            json_schema=swift_schema,
        )

        ##############################################################################

        print("✅ Schema compatibility validation - PASSED")


@pytest.mark.asyncio
async def test_guided_generation_error_handling(model):
    """
    Test from: docs/source/guided_generation.rst
    Section: Error Handling
    """
    print("\n=== Testing Guided Generation Error Handling ===")

    ##############################################################################
    # From: docs/source/guided_generation.rst
    # Section: Error Handling
    import apple_fm_sdk as fm
    from typing import Optional

    async def safe_guided_generation(prompt: str, MyGenerable: Optional[type] = None):
        try:
            if MyGenerable:
                return await fm.LanguageModelSession().respond(
                    prompt, generating=MyGenerable
                )
            else:
                return await fm.LanguageModelSession().respond(prompt)
        except fm.InvalidGenerationSchemaError as e:
            print(f"Schema error: {e}")
        except fm.UnsupportedGuideError as e:
            print(f"Unsupported constraint: {e}")
        except Exception as e:
            print(f"Generation error: {e}")

    ##############################################################################

    # Note: This snippet defines a function but doesn't call it since it references
    # undefined variables (session, prompt, MyClass) in the documentation
    await safe_guided_generation("Test prompt")
    print("✅ Guided generation error handling - PASSED")


# =============================================================================
# STREAMING TESTS (from docs/source/streaming.rst)
# =============================================================================


@pytest.mark.asyncio
async def test_streaming_basic_example(model):
    """
    Test from: docs/source/streaming.rst
    Section: Basic Streaming
    """
    print("\n=== Testing Basic Streaming ===")

    ##############################################################################
    # From: docs/source/streaming.rst
    # Section: Basic Streaming
    import apple_fm_sdk as fm

    model = fm.SystemLanguageModel()
    is_available, _ = model.is_available()

    if is_available:
        session = fm.LanguageModelSession()

        async for chunk in session.stream_response("Tell me a short story"):
            print(chunk, end="", flush=True)

    ##############################################################################

    print("✅ Basic streaming - PASSED")


@pytest.mark.asyncio
async def test_streaming_with_context(model):
    """
    Test from: docs/source/streaming.rst
    Section: Streaming with Context
    """
    print("\n=== Testing Streaming with Context ===")

    ##############################################################################
    # From: docs/source/streaming.rst
    # Section: Streaming with Context
    import apple_fm_sdk as fm

    session = fm.LanguageModelSession()

    # First streaming response
    async for chunk in session.stream_response(
        "What are some differences between Swift and Python?"
    ):
        print(chunk, end="", flush=True)
    print("\n")

    # Follow-up with context maintained
    async for chunk in session.stream_response("Show me an example"):
        print(chunk, end="", flush=True)

    ##############################################################################

    print("✅ Streaming with context - PASSED")


# =============================================================================
# TOOLS TESTS (from docs/source/tools.rst)
# =============================================================================


@pytest.mark.asyncio
async def test_tools_basic_tool_definition():
    """
    Test from: docs/source/tools.rst
    Section: Creating a Tool - Basic Tool
    """
    print("\n=== Testing Basic Tool Definition ===")

    ##############################################################################
    # From: docs/source/tools.rst
    # Section: Basic Tool
    import apple_fm_sdk as fm

    class WeatherTool(fm.Tool):
        name = "WeatherTool"
        description = "Provides weather information for a given location and units."

        @fm.generable("Weather query parameters")
        class Arguments:
            location: str = fm.guide("City name")
            units: str = fm.guide("Temperature units", anyOf=["celsius", "fahrenheit"])

        @property
        def arguments_schema(self) -> fm.GenerationSchema:
            return self.Arguments.generation_schema()

        async def call(self, args: fm.GeneratedContent) -> str:
            # Extract arguments
            location = args.value(str, for_property="location")
            units = args.value(str, for_property="units")

            # Simulate API call
            temp = 72 if units == "fahrenheit" else 22
            return f"The weather in {location} is {temp}°{units[0].upper()}"

    ##############################################################################

    print("✅ Basic tool definition - PASSED")


@pytest.mark.asyncio
async def test_tools_using_with_sessions():
    """
    Test from: docs/source/tools.rst
    Section: Using tools with sessions
    """
    print("\n=== Testing Using Tools with Sessions ===")

    # Define WeatherTool first
    import apple_fm_sdk as fm

    class WeatherTool(fm.Tool):
        name = "WeatherTool"
        description = "Provides weather information for a given location and units."

        @fm.generable("Weather query parameters")
        class Arguments:
            location: str = fm.guide("City name")
            units: str = fm.guide("Temperature units", anyOf=["celsius", "fahrenheit"])

        @property
        def arguments_schema(self) -> fm.GenerationSchema:
            return self.Arguments.generation_schema()

        async def call(self, args: fm.GeneratedContent) -> str:
            location = args.value(str, for_property="location")
            units = args.value(str, for_property="units")
            temp = 72 if units == "fahrenheit" else 22
            return f"The weather in {location} is {temp}°{units[0].upper()}"

    ##############################################################################
    # From: docs/source/tools.rst
    # Section: Using tools with sessions
    import apple_fm_sdk as fm

    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant with access to tools.",
        tools=[WeatherTool()],  # See above for WeatherTool definition
    )

    # The model can now call the tool
    response = await session.respond("What's the weather like in Taipei?")
    print(response)

    ##############################################################################

    print("✅ Using tools with sessions - PASSED")


@pytest.mark.asyncio
async def test_tools_error_handling():
    """
    Test from: docs/source/tools.rst
    Section: Error handling
    """
    print("\n=== Testing Tools Error Handling ===")

    # Define WeatherTool first
    import apple_fm_sdk as fm

    class WeatherTool(fm.Tool):
        name = "WeatherTool"
        description = "Provides weather information for a given location and units."

        @fm.generable("Weather query parameters")
        class Arguments:
            location: str = fm.guide("City name")
            units: str = fm.guide("Temperature units", anyOf=["celsius", "fahrenheit"])

        @property
        def arguments_schema(self) -> fm.GenerationSchema:
            return self.Arguments.generation_schema()

        async def call(self, args: fm.GeneratedContent) -> str:
            location = args.value(str, for_property="location")
            units = args.value(str, for_property="units")
            temp = 72 if units == "fahrenheit" else 22
            return f"The weather in {location} is {temp}°{units[0].upper()}"

    ##############################################################################
    # From: docs/source/tools.rst
    # Section: Error handling
    import apple_fm_sdk as fm

    session = fm.LanguageModelSession(
        instructions="You are a helpful assistant with access to tools.",
        tools=[WeatherTool()],  # See above for WeatherTool definition
    )

    try:
        response = await session.respond(
            "Use the weather tool to get the current temperature in Taipei."
        )
    except fm.ToolCallError as e:
        print(f"Tool error: {e.tool_name} - {e.underlying_error}")
    except Exception as e:
        print(f"Error: {e}")

    ##############################################################################

    print("✅ Tools error handling - PASSED")


# =============================================================================
# EVALUATION TESTS (from docs/source/evaluation.rst)
# =============================================================================


@pytest.mark.asyncio
async def test_evaluation_producing_transcripts():
    """
    Test from: docs/source/evaluation.rst
    Section: Processing transcripts in Python - Producing transcripts
    """
    print("\n=== Testing Producing Transcripts in Python ===")

    ##############################################################################
    # From: docs/source/evaluation.rst
    # Section: Processing transcripts in Python - Producing transcripts
    import apple_fm_sdk as fm

    session = fm.LanguageModelSession()
    await session.respond(prompt="Hello, how are you?")

    # Export transcript
    transcript = session.transcript
    transcript_dict = await transcript.to_dict()  # Convert to dictionary

    ##############################################################################

    print("✅ Producing transcripts - PASSED")


@pytest.mark.asyncio
async def test_evaluation_transcript_processing():
    """
    Test from: docs/source/evaluation.rst
    Section: Processing Transcripts in Python - Loading from file
    """
    print("\n=== Testing Transcript Processing ===")
    filepath = "tests/tester_schemas/test_transcript.json"

    ##############################################################################
    # From: docs/source/evaluation.rst
    # Section: Processing Transcripts in Python
    import json

    # Load transcript from Swift app
    with open(filepath, "r") as f:
        transcript_data = json.load(f)

    print("Transcript loaded successfully: ", transcript_data)

    # Analyze the session
    for entry in transcript_data["transcript"]["entries"]:
        role = entry["role"]
        content = entry["contents"]
        print(f"{role}: {content}")
    ##############################################################################

    print("✅ Transcript processing - PASSED")


@pytest.mark.asyncio
async def test_evaluation_batch_processing(model):
    """
    Test from: docs/source/evaluation.rst
    Section: Batch Evaluation Patterns
    """
    print("\n=== Testing Batch Evaluation Pattern ===")

    ##############################################################################
    # From: docs/source/evaluation.rst
    # Section: Batch Evaluation
    import apple_fm_sdk as fm
    import json

    # Load test cases
    test_cases = [
        {"prompt": "Test case 1", "expected": {...}},
        {"prompt": "Test case 2", "expected": {...}},
        # ... more test cases
    ]

    # Run batch evaluation
    results = []

    for i, test_case in enumerate(test_cases):
        session = fm.LanguageModelSession()

        try:
            if "schema" in test_case:
                result = await session.respond(
                    prompt=test_case["prompt"], json_schema=test_case["schema"]
                )  # structured generable response
            else:
                result = await session.respond(
                    prompt=test_case["prompt"]
                )  # string response

            # Compare with expected result
            success = test_case["expected"] in result
            results.append({"test_id": i, "success": success, "result": result})

        except Exception as e:
            results.append({"test_id": i, "success": False, "error": str(e)})

    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    ##############################################################################

    print("✅ Batch evaluation pattern - PASSED")


# =============================================================================
# GETTING STARTED TESTS (from docs/source/getting_started.rst)
# =============================================================================


@pytest.mark.asyncio
async def test_getting_started_verifying_installation():
    """
    Test from: docs/source/getting_started.rst
    Section: Verifying Installation
    """
    print("\n=== Testing Verifying Installation ===")

    ##############################################################################
    # From: docs/source/getting_started.rst
    # Section: Verifying Installation
    import apple_fm_sdk as fm

    # Check if the model is available
    model = fm.SystemLanguageModel()
    is_available, reason = model.is_available()

    if is_available:
        print("✓ Foundation Models SDK is ready!")
    else:
        print(f"✗ Foundation Models not available: {reason}")

    ##############################################################################

    print("✅ Verifying installation - PASSED")


# =============================================================================
# INDEX TESTS (from docs/source/index.rst)
# =============================================================================


@pytest.mark.asyncio
async def test_index_basic_usage():
    """
    Test from: docs/source/index.rst
    Section: Basic Usage
    """
    print("\n=== Testing Index Basic Usage ===")

    ##############################################################################
    # From: docs/source/index.rst
    # Section: Basic Usage
    import apple_fm_sdk as fm

    # Get the default system foundation model
    model = fm.SystemLanguageModel()

    # Check if the model is available
    is_available, reason = model.is_available()
    if is_available:
        # Create a session
        session = fm.LanguageModelSession(model=model)

        # Generate a response
        response = await session.respond(prompt="Hello, how are you?")
        print(f"Model response: {response}")
    else:
        print(f"Foundation Models not available: {reason}")

    ##############################################################################

    print("✅ Index basic usage - PASSED")
