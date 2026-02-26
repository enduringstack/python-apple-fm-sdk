# Python Apple Foundation Models SDK - Architecture

## High-Level Overview

```
+------------------------------------------------------------------+
|                        User Application                          |
|  (async/await Python code using apple_fm_sdk)                    |
+------------------------------------------------------------------+
        |                    |                     |
        v                    v                     v
+----------------+  +------------------+  +-----------------+
| LanguageModel  |  |  @generable      |  |    Tool         |
| Session        |  |  Decorator       |  |  (ABC)          |
| - respond()    |  |  + Generation    |  |  - call()       |
| - stream()     |  |    Schema/Guide  |  |  - args_schema  |
| - transcript   |  |  + Property      |  |                 |
+----------------+  +------------------+  +-----------------+
        |                    |                     |
        v                    v                     v
+------------------------------------------------------------------+
|                   Python/C Bridge Layer                           |
|  c_helpers.py: _ManagedObject, callbacks, handle registry        |
|  type_conversion.py: Python <-> Swift type mapping               |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
|              _ctypes_bindings.py  (auto-generated)               |
|  ctypes FFI bindings to libFoundationModels C API                |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
|              foundation-models-c  (Swift Package)                |
|  FoundationModelsCBindings.swift + FoundationModels.h            |
|  C-compatible wrappers around Swift FoundationModels framework   |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
|           Apple FoundationModels Framework (macOS 26+)           |
|               On-Device Foundation Model                         |
+------------------------------------------------------------------+
```

## Module Dependency Graph

```mermaid
graph TD
    subgraph "Public API (apple_fm_sdk)"
        init["__init__.py<br/><i>Package exports</i>"]
        session["session.py<br/><b>LanguageModelSession</b>"]
        core["core.py<br/><b>SystemLanguageModel</b>"]
        tool["tool.py<br/><b>Tool (ABC)</b>"]
        generable["generable.py<br/><b>Generable Protocol</b><br/>GeneratedContent"]
        generable_utils["generable_utils.py<br/><b>@generable decorator</b>"]
        gen_schema["generation_schema.py<br/><b>GenerationSchema</b>"]
        gen_guide["generation_guide.py<br/><b>GenerationGuide</b><br/>GuideType"]
        gen_prop["generation_property.py<br/><b>Property</b>"]
        transcript["transcript.py<br/><b>Transcript</b>"]
        errors["errors.py<br/><b>Exception hierarchy</b>"]
    end

    subgraph "Internal Bridge"
        c_helpers["c_helpers.py<br/>_ManagedObject<br/>Callbacks"]
        type_conv["type_conversion.py<br/>Type mapping"]
        ctypes_bind["_ctypes_bindings.py<br/><i>Auto-generated FFI</i>"]
    end

    subgraph "Native Layer"
        swift["foundation-models-c/<br/>Swift C Bindings"]
        apple["Apple FoundationModels<br/>Framework"]
    end

    init --> session & core & tool & generable & generable_utils & gen_schema & gen_guide & errors

    session --> core
    session --> tool
    session --> transcript
    session --> generable
    session --> gen_schema
    session --> errors
    session --> c_helpers

    core --> c_helpers
    core --> ctypes_bind

    tool --> generable
    tool --> gen_schema
    tool --> c_helpers

    generable_utils --> generable
    generable_utils --> gen_schema
    generable_utils --> gen_prop
    generable_utils --> gen_guide
    generable_utils --> type_conv

    gen_schema --> c_helpers
    gen_prop --> gen_guide
    gen_prop --> type_conv
    gen_prop --> ctypes_bind

    transcript --> c_helpers

    c_helpers --> ctypes_bind
    c_helpers --> errors
    ctypes_bind --> swift
    swift --> apple
```

## Class Relationships

```mermaid
classDiagram
    class LanguageModelSession {
        -_model: SystemLanguageModel
        -_tools: list~Tool~
        -_transcript: Transcript
        -_session_ptr: c_void_p
        +respond(prompt, generating?) AsyncResult
        +stream_response(prompt) AsyncGenerator
        +is_responding: bool
        +transcript: Transcript
    }

    class SystemLanguageModel {
        -_ptr: c_void_p
        +use_case: SystemLanguageModelUseCase
        +guardrails: SystemLanguageModelGuardrails
    }

    class Tool {
        <<abstract>>
        +name: str
        +description: str
        +arguments_schema: GenerationSchema*
        +call(args: GeneratedContent) str*
    }

    class Transcript {
        -_session_ptr: c_void_p
        +to_dict() dict
    }

    class Generable {
        <<protocol>>
        +generation_schema()$ GenerationSchema
        +_from_generated_content()$ instance
        +generated_content: GeneratedContent
    }

    class GeneratedContent {
        -_ptr: c_void_p
        +value(key) Any
        +is_complete: bool
    }

    class GenerationSchema {
        -_ptr: c_void_p
        -_properties: list~Property~
        -_schemas: list~GenerationSchema~
        +to_dict() dict
    }

    class Property {
        +name: str
        +type: str
        +description: str
        +guides: list~GenerationGuide~
        +convert_to_c(schema_ptr)
    }

    class GenerationGuide {
        +type: GuideType
        +value: Any
    }

    class _ManagedObject {
        <<internal>>
        -_ptr: c_void_p
        +_retain()
        +_release()
    }

    LanguageModelSession --> SystemLanguageModel : owns
    LanguageModelSession --> Tool : uses 0..*
    LanguageModelSession --> Transcript : owns
    LanguageModelSession --> GeneratedContent : produces

    Tool --> GenerationSchema : defines args via
    Tool --> GeneratedContent : receives args as

    Generable --> GenerationSchema : creates
    Generable --> GeneratedContent : converts to/from

    GenerationSchema --> Property : contains 1..*
    GenerationSchema --> GenerationSchema : nests

    Property --> GenerationGuide : constrained by 0..*

    SystemLanguageModel --|> _ManagedObject
    GeneratedContent --|> _ManagedObject
    GenerationSchema --|> _ManagedObject
    Transcript --|> _ManagedObject
```

## Data Flow

### 1. Basic Text Generation

```mermaid
sequenceDiagram
    participant User as User Code
    participant Session as LanguageModelSession
    participant CH as c_helpers
    participant C as C Bindings (ctypes)
    participant Swift as Swift / Apple FM

    User->>+Session: await session.respond("prompt")
    Session->>CH: _register_handle(future)
    Session->>C: FMLanguageModelSessionRespond(ptr, prompt, handle, callback)
    C->>Swift: Forward to FoundationModels framework
    Swift-->>C: Generation complete (native thread)
    C-->>CH: _session_callback(handle, response, status)
    CH->>CH: asyncio.run_coroutine_threadsafe(set_result)
    CH-->>Session: Future resolved with response string
    Session-->>-User: return "response text"
```

### 2. Guided (Structured) Generation

```mermaid
sequenceDiagram
    participant User as User Code
    participant Session as LanguageModelSession
    participant Schema as GenerationSchema
    participant C as C Bindings
    participant Swift as Swift / Apple FM

    User->>+Session: await session.respond("prompt", generating=Cat)
    Session->>Schema: Cat.generation_schema()
    Schema-->>Session: GenerationSchema (with properties & guides)
    Session->>C: FMLanguageModelSessionRespondWithSchema(ptr, prompt, schema_ptr, ...)
    C->>Swift: Constrained generation
    Swift-->>C: Structured JSON result
    C-->>Session: GeneratedContent (via structured callback)
    Session->>Session: Cat._from_generated_content(content)
    Session-->>-User: return Cat(name="Whiskers", age=3)
```

### 3. Streaming

```mermaid
sequenceDiagram
    participant User as User Code
    participant Session as LanguageModelSession
    participant Thread as Daemon Thread
    participant Queue as StreamingCallback Queue
    participant C as C Bindings

    User->>+Session: async for chunk in session.stream_response("prompt")
    Session->>Thread: Start daemon thread
    Thread->>C: FMLanguageModelSessionStreamResponse(...)
    loop Each token update
        C-->>Queue: callback puts snapshot into queue
        Queue-->>Session: queue.get() yields text
        Session-->>User: yield "partial text..."
    end
    C-->>Queue: callback puts None (sentinel)
    Queue-->>Session: queue.get() returns None
    Session->>Thread: thread.join()
    Session-->>-User: Iteration complete
```

### 4. Tool Calling

```mermaid
sequenceDiagram
    participant User as User Code
    participant Session as LanguageModelSession
    participant Model as On-Device Model
    participant Tool as Tool subclass
    participant C as C Bindings

    User->>Session: await session.respond("What is 2+2?")
    Session->>C: FMLanguageModelSessionRespond(...)
    C->>Model: Process prompt (with tool definitions)
    Model->>C: Decide to call "calculator" tool
    C->>Tool: _c_callback(content_ref, call_id)
    Tool->>Tool: parse args from GeneratedContent
    Tool->>Tool: await self.call(args)
    Tool->>C: FMBridgedToolFinishCall(result_string)
    C->>Model: Resume with tool result
    Model->>C: Final text response
    C-->>Session: callback with response
    Session-->>User: return "2 + 2 = 4"
```

## Error Handling Architecture

```
FoundationModelsError (base)
├── GenerationError (base for generation failures)
│   ├── ExceededContextWindowSizeError
│   ├── AssetsUnavailableError
│   ├── GuardrailViolationError
│   ├── UnsupportedGuideError
│   ├── UnsupportedLanguageOrLocaleError
│   ├── DecodingFailureError
│   ├── RateLimitedError
│   ├── ConcurrentRequestsError
│   └── RefusalError
├── ToolCallError
└── InvalidGenerationSchemaError
```

Errors originate as C status codes, are mapped via `GenerationErrorCode` enum, and raised as typed Python exceptions through `_status_code_to_exception()`.

## Memory Management

```
Python (_ManagedObject)          C / Swift
─────────────────────────        ─────────────
__init__(ptr)  ←─────────────── passRetained() [+1 refcount]
                                 ownership transferred to Python
    ...object in use...

__del__()  ──────────────────── FMRelease(ptr)  [-1 refcount]
                                 if refcount == 0: dealloc

Callback Safety:
  _register_handle(obj) ───────► _active_handles[id(obj)] = obj
      prevents GC while C holds reference
  _unregister_handle(obj) ─────► del _active_handles[id(obj)]
      allows GC after callback completes
```

## Build Pipeline

```
pyproject.toml
    │
    ▼
build_backend.py (PEP 517)
    │
    ├──► Check macOS 26+ & Xcode 26+
    │
    ├──► swift build -c release
    │    └──► libFoundationModels.dylib
    │
    ├──► Copy .dylib → src/apple_fm_sdk/lib/
    │
    ├──► ctypesgen FoundationModels.h → _ctypes_bindings.py
    │    └──► Post-process: inject runtime library path
    │
    └──► setuptools.build_meta → .whl package
```

## Directory Structure

```
python-apple-fm-sdk/
├── src/apple_fm_sdk/               # Python SDK package
│   ├── __init__.py                 #   Public API exports
│   ├── core.py                     #   SystemLanguageModel & config enums
│   ├── session.py                  #   LanguageModelSession (main entry point)
│   ├── generable.py                #   Generable protocol & GeneratedContent
│   ├── generable_utils.py          #   @generable decorator implementation
│   ├── generation_schema.py        #   GenerationSchema (C-backed)
│   ├── generation_property.py      #   Property for schema fields
│   ├── generation_guide.py         #   GenerationGuide constraints
│   ├── tool.py                     #   Tool abstract base class
│   ├── transcript.py               #   Session history
│   ├── errors.py                   #   Exception hierarchy
│   ├── c_helpers.py                #   Python/C bridge utilities
│   ├── type_conversion.py          #   Python <-> Swift type mapping
│   └── _ctypes_bindings.py         #   Auto-generated ctypes FFI
│
├── foundation-models-c/            # Swift C bindings package
│   ├── Package.swift               #   Swift package manifest
│   └── Sources/
│       ├── FoundationModelsCBindings/
│       │   ├── include/
│       │   │   └── FoundationModels.h    # C API header
│       │   └── FoundationModelsCBindings.swift
│       └── FoundationModelsCDeclarations/
│
├── examples/                       # Usage examples
│   ├── simple_inference.py
│   ├── streaming_example.py
│   └── transcript_processing.py
│
├── tests/                          # Test suite (pytest)
├── docs/                           # Sphinx documentation
├── build_backend.py                # Custom PEP 517 build backend
└── pyproject.toml                  # Project configuration
```
