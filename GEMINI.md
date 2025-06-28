# SMS Gateway Python Client Development Rules

## Project Overview

This is a Python client library for the @SMS Gateway for Android API. The project provides both synchronous and asynchronous interfaces for sending SMS messages through Android devices.

## Project Structure

### Core Library
- **Main Package**: @android_sms_gateway/
  - @__init__.py - Public API exports
  - @client.py - Main client classes (APIClient, AsyncAPIClient)
  - @domain.py - Data models and domain objects
  - @http.py - Synchronous HTTP client implementations
  - @ahttp.py - Asynchronous HTTP client implementations
  - @encryption.py - End-to-end encryption support
  - @enums.py - Enumeration definitions
  - @constants.py - Version and constants

### Web Interface
- **Web App**: @sms-gateway-web/
  - @app.py - Flask web application
  - @run.py - Application entry point
  - @templates/ - HTML templates

### Testing
- **Tests**: @tests/ - Test suite for the library

### Configuration
- @pyproject.toml - Project configuration and dependencies
- @Pipfile - Pipenv dependencies
- @requirements.txt - Standard requirements
- @.flake8 - Flake8 configuration
- @.isort.cfg - Import sorting configuration

## Development Principles

### Code Style and Standards
- **Python Version**: 3.9+ (as specified in @pyproject.toml)
- **Type Hints**: Use type hints extensively for better IDE support
- **Code Formatting**: Use Black for code formatting
- **Import Sorting**: Use isort for import organization
- **Linting**: Use flake8 for code quality checks

### Architecture Patterns
- **Dual Client Interface**: Support both synchronous (`APIClient`) and asynchronous (`AsyncAPIClient`) patterns
- **HTTP Abstraction**: Abstract HTTP clients to support multiple backends (requests, aiohttp, httpx)
- **Domain Models**: Use dataclasses for immutable data structures
- **Encryption Support**: Optional end-to-end encryption using AES-CBC-256

## Key Components

### Client Classes
```python
# Synchronous client
from android_sms_gateway import APIClient

with APIClient(login, password) as client:
    state = client.send(message)
    status = client.get_state(state.id)

# Asynchronous client
from android_sms_gateway import AsyncAPIClient

async with AsyncAPIClient(login, password) as client:
    state = await client.send(message)
    status = await client.get_state(state.id)
```

### Domain Models
- **Message**: SMS message with recipients and options
- **MessageState**: Status tracking for sent messages
- **RecipientState**: Individual recipient status
- **Webhook**: Webhook configuration for event notifications

### HTTP Client Support
The library supports multiple HTTP clients with automatic detection:
1. **aiohttp** (async priority)
2. **requests** (sync priority)
3. **httpx** (universal fallback)

## Development Guidelines

### Adding New Features
1. **Type Safety**: Always add type hints to new functions and methods
2. **Documentation**: Add docstrings for public APIs
3. **Testing**: Write tests for new functionality
4. **Backward Compatibility**: Maintain compatibility with existing APIs

### Error Handling
- Use specific exception types for different error conditions
- Provide clear error messages for debugging
- Handle HTTP errors gracefully with retry logic

### Security Considerations
- Never log sensitive information (credentials, message content)
- Use environment variables for configuration
- Support end-to-end encryption for sensitive messages

### Testing Strategy
- Unit tests for individual components
- Integration tests for API interactions
- Mock external dependencies in tests
- Test both sync and async interfaces

## Dependencies Management

### Core Dependencies
- **HTTP Clients**: requests, aiohttp, httpx (optional)
- **Encryption**: pycryptodome (optional)
- **Development**: pytest, black, flake8, isort

### Installation Patterns
```bash
# Basic installation
pip install android-sms-gateway

# With specific HTTP client
pip install android-sms-gateway[requests]
pip install android-sms-gateway[aiohttp]
pip install android-sms-gateway[httpx]

# With encryption support
pip install android-sms-gateway[encryption]

# Development setup
pip install -e ".[dev,requests,encryption]"
```

## API Design Patterns

### Context Manager Usage
Both client classes support context manager pattern for resource management:
```python
with APIClient(login, password) as client:
    # Client automatically handles connection lifecycle
    result = client.send(message)
```

### Immutable Data Models
Use frozen dataclasses for domain models to ensure immutability:
```python
@dataclasses.dataclass(frozen=True)
class Message:
    message: str
    phone_numbers: List[str]
    with_delivery_report: bool = True
```

### Factory Methods
Use class methods for creating instances from API responses:
```python
@classmethod
def from_dict(cls, payload: Dict[str, Any]) -> "MessageState":
    return cls(
        id=payload["id"],
        state=ProcessState(payload["state"]),
        # ...
    )
```

## Web Interface Development

### Flask Application Structure
- **App Factory**: Use application factory pattern for better testing
- **Blueprints**: Organize routes by functionality
- **Configuration**: Use environment-based configuration
- **Templates**: Use Jinja2 templates for HTML rendering

### Security for Web Interface
- **Authentication**: Implement user authentication
- **Input Validation**: Validate all user inputs
- **CSRF Protection**: Protect against cross-site request forgery
- **Secure Headers**: Use security headers for web responses

## Deployment and Distribution

### Package Distribution
- **PyPI**: Package is distributed via PyPI as `android-sms-gateway`
- **Version Management**: Use dynamic versioning from `__version__` attribute
- **Wheel Distribution**: Build and distribute wheels for better performance

### CI/CD Pipeline
- **Testing**: Run tests on multiple Python versions
- **Code Quality**: Enforce code style and quality checks
- **Documentation**: Build and deploy documentation
- **Release**: Automated PyPI releases on version tags

## Common Development Tasks

### Adding New HTTP Client Support
1. Implement the `HttpClient` or `AsyncHttpClient` protocol
2. Add detection logic in client initialization
3. Update tests to cover the new client
4. Update documentation and examples

### Extending Domain Models
1. Add new fields to existing dataclasses
2. Update serialization/deserialization methods
3. Add validation logic if needed
4. Update tests and documentation

### Adding New API Endpoints
1. Add new methods to client classes
2. Implement HTTP client support
3. Add domain models for request/response
4. Write comprehensive tests
5. Update documentation

## Project References
- **Main Documentation**: @README.md
- **Project Configuration**: @pyproject.toml
- **License**: @LICENSE
- **Web Interface**: @sms-gateway-web/
- **Test Suite**: @tests/
