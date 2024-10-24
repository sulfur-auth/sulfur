# Sulfur

Sulfur is a robust, secure authentication library for Python.

## Installation

```bash
pip install sulfur-auth
```

## Examples

```python
from sulfur_auth import auth

sulfur = auth()

# Register a new user
auth_token = sulfur.register("username", "passwordHash")

# Login
auth_token = sulfur.auth("username", "passwordHash")

# Subscribe to events
sulfur.subscribe("userRegister", lambda ctx: print(ctx))
```

To create an API, you can use `flask` to create a web server serving endpoints for login and registration.
