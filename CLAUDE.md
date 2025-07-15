# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

slang is a SystemVerilog compiler and language services library developed in C++. It provides lexing, parsing, type checking, and elaboration of SystemVerilog code with a focus on performance, correctness, and robustness.

## Build System and Development Commands

### Primary Build Commands (CMake)
```bash
# Configure build
cmake -B build

# Build the project (use -j for parallel build)
cmake --build build -j8

# Run tests
ctest --test-dir build --output-on-failure

# Build with specific preset (see CMakePresets.json)
cmake --preset clang-debug
cmake --build build/clang-debug -j8
```

### Bazel Build Commands
```bash
# Build the main slang library
bazel build //...

# Build with debug configuration
bazel build --config=debug //...

# Build with release configuration (default)
bazel build --config=release //...

# Build specific targets
bazel build //:slang
bazel build //:slang_slang

# Run tests with Bazel
bazel test //...
```

### Python Bindings
```bash
# Install Python bindings locally
pip install . --no-build-isolation --config-settings build-dir=build/python_build

# Run Python tests
pytest
```

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

## Code Architecture

### Core Library Structure
The slang library follows a layered architecture:

**Text Processing → Lexing/Parsing → Syntax Trees → AST Creation → Semantic Analysis**

### Key Components

#### 1. Text Processing (`include/slang/text/`, `source/text/`)
- **SourceManager**: Manages source files and location tracking
- **SourceLocation**: Represents locations within source files
- **CharInfo**: Character classification utilities

#### 2. Lexing and Parsing (`include/slang/parsing/`, `source/parsing/`)
- **Lexer**: Tokenizes SystemVerilog source code
- **Parser**: Recursive descent parser that builds syntax trees
- **Preprocessor**: Handles macro expansion, includes, and directives
- **Token**: Represents individual tokens with location info

#### 3. Syntax Trees (`include/slang/syntax/`, `source/syntax/`)
- **SyntaxTree**: Main entry point for parsing source files
- **SyntaxNode**: Base class for all syntax tree nodes
- **SyntaxVisitor**: Visitor pattern for traversing syntax trees

#### 4. Abstract Syntax Tree (`include/slang/ast/`, `source/ast/`)
The AST is the heart of the compiler:
- **Compilation**: Central compilation manager and entry point
- **Symbol**: Base class for all semantic symbols
- **Expression**: Base class for all expressions
- **Statement**: Base class for all statements
- **Type**: Type system implementation
- **Scope**: Scope management and symbol lookup

Submodules:
- `symbols/`: All symbol types (modules, variables, functions, etc.)
- `expressions/`: Expression types (literals, operators, calls, etc.)
- `statements/`: Statement types (assignments, conditionals, loops, etc.)
- `types/`: Type system (built-in types, user-defined types, etc.)
- `builtins/`: Built-in functions and system tasks

#### 5. Semantic Analysis (`include/slang/analysis/`, `source/analysis/`)
- **AnalysisManager**: Coordinates various analysis passes
- **DataFlowAnalysis**: Data flow analysis framework
- **DriverTracker**: Tracks signal drivers and conflicts
- **ClockInference**: Infers clock domains and timing

#### 6. Diagnostics (`include/slang/diagnostics/`, `source/diagnostics/`)
- **DiagnosticEngine**: Core diagnostic reporting system
- **TextDiagnosticClient**: Console output for diagnostics
- **JsonDiagnosticClient**: JSON output for diagnostics

#### 7. Numeric System (`include/slang/numeric/`, `source/numeric/`)
- **SVInt**: SystemVerilog integer representation
- **ConstantValue**: Compile-time constant values
- **Time**: Time scale and timing utilities

#### 8. Driver Interface (`include/slang/driver/`, `source/driver/`)
- **Driver**: High-level API for compilation workflows
- **SourceLoader**: Loads and manages source files

### Main Entry Points

1. **`ast::Compilation`** - The central compilation manager
2. **`syntax::SyntaxTree`** - Entry point for parsing
3. **`driver::Driver`** - High-level compilation workflow

### Tools

#### Command-line Tools (`tools/`)
- **driver/**: Main `slang` executable for compilation and linting
- **hier/**: Hierarchy analysis tool
- **reflect/**: Type reflection and C++ code generation
- **rewriter/**: Source code rewriting tool
- **tidy/**: Linting and style checking tool

#### Tool Usage
```bash
# Main compiler/linter
./build/bin/slang file.sv

# Hierarchy analysis
./build/bin/slang-hier file.sv

# Type reflection
./build/bin/slang-reflect file.sv

# Code rewriting
./build/bin/slang-rewriter file.sv

# Linting
./build/bin/slang-tidy file.sv
```

## Testing

### Test Structure
- **Unit Tests**: `tests/unittests/` - Comprehensive unit tests for all components
- **Integration Tests**: `tests/regression/` - End-to-end compilation tests
- **Python Tests**: `pyslang/tests/` - Tests for Python bindings

### Running Tests
```bash
# Run all C++ tests
ctest --test-dir build --output-on-failure

# Run specific test categories
ctest --test-dir build -R "parsing"
ctest --test-dir build -R "ast"

# Run Python tests
pytest pyslang/tests/
```

## Code Style and Guidelines

### Language Requirements
- **All code must be written in English** (variable names, comments, documentation)
- Modern C++20 features are preferred
- Column width: 100 characters
- Use lowerCase for functions, parameters, and local variables
- Use `#pragma once` instead of header guards

### Development Standards
- Follow existing code patterns and style
- Write unit tests for new functionality
- Use pre-commit hooks for formatting
- Document public APIs with Doxygen comments
- Maintain high code quality and performance focus

### Key Development Patterns
- **Visitor Pattern**: Used extensively for AST and syntax tree traversal
- **RAII**: Memory management through smart pointers and allocators
- **Immutable AST**: AST nodes are generally immutable once created
- **Diagnostic Collection**: Errors are collected rather than thrown as exceptions

## Common Development Workflows

### Adding New Language Features
1. Update lexer for new tokens (if needed)
2. Update parser for new syntax
3. Add AST node types
4. Update semantic analysis
5. Add tests and documentation

### Extending Analysis Passes
1. Implement analysis logic in `source/analysis/`
2. Register with `AnalysisManager`
3. Add corresponding tests
4. Update documentation

### Working with Python Bindings
1. C++ changes may require updates to `bindings/python/`
2. Test both C++ and Python interfaces
3. Update Python documentation in `pyslang/docs/`

## Memory Management

The codebase uses custom memory management:
- **BumpAllocator**: Fast allocation for AST nodes
- **PoolAllocator**: Efficient allocation for specific types
- Most objects are allocated from compilation-scoped allocators
- Use provided smart pointer types and containers

## Important Files

### Build System
- `CMakeLists.txt`: Main CMake build configuration
- `CMakePresets.json`: CMake build presets for different configurations
- `BUILD.bazel`: Main Bazel build file
- `MODULE.bazel`: Bazel module configuration with dependencies
- `.bazelrc`: Bazel build configuration and compiler flags
- `gen_sources.py`: Python script for generating source files in Bazel builds

### Other Configuration
- `pyproject.toml`: Python package configuration
- `scripts/`: Code generation scripts for diagnostics and syntax
- `external/`: Third-party dependencies