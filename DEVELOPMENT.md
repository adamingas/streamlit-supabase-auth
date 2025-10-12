# Development Guide

## Setup

### 1. Clone and Install

```bash
cd streamlit-supabase-auth

# Install dependencies with uv
uv sync

# Or install in editable mode to current environment
uv pip install -e .
```

### 2. Configure Environment

Create a `.env` file:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
REDIRECT_URI=http://localhost:8501
```

### 3. Run Demo

```bash
# Load environment variables and run with uv
uv run streamlit run examples/demo.py

# Or if you prefer to load .env manually
source .env  # or use direnv
uv run streamlit run examples/demo.py
```

## Project Structure

```
streamlit-supabase-auth/
├── src/
│   |── public/
│   |   └── index.html  # Component for clearing URL fragments
│   └── streamlit_supabase_auth/
│       ├── __init__.py           # Package exports
│       ├── auth.py               # Main SupabaseAuth class
├── examples/
│   └── demo.py                   # Demo application
├── pyproject.toml                # Package configuration
├── README.md                     # User documentation
├── DEVELOPMENT.md               # This file
├── LICENSE                       # MIT License
└── MANIFEST.in                  # Package data files
```

## Architecture

### Components

1. **SupabaseAuth Class** (`auth.py`)
   - Main authentication handler
   - Manages OAuth flow and session state
   - Provides simple API for Streamlit apps

2. **Clear Fragment Component** (`frontend/clear_fragment.html`)
   - Custom Streamlit component
   - Clears URL fragments after OAuth callback
   - Ensures tokens don't persist in browser URL

### OAuth Flow

```
┌─────────┐                  ┌──────────┐                 ┌──────────┐
│  User   │                  │ Supabase │                 │  Google  │
│ (App)   │                  │   Auth   │                 │  OAuth   │
└────┬────┘                  └─────┬────┘                 └─────┬────┘
     │                             │                            │
     │ 1. Click Login              │                            │
     ├────────────────────────────>│                            │
     │                             │                            │
     │ 2. Get OAuth URL            │                            │
     │<────────────────────────────┤                            │
     │                             │                            │
     │ 3. Redirect to Provider     │                            │
     ├───────────────────────────────────-─────────────────────>│
     │                             │                            │
     │ 4. User Authenticates       │                            │
     │<──────────────────────────────────-──────────────────────┤
     │                             │                            │
     │ 5. Redirect with tokens (#access_token=...)             │
     │<────────────────────────────┤                            │
     │                             │                            │
     │ 6. Extract tokens           │                            │
     │ 7. Set Supabase session     │                            │
     │ 8. Clear URL fragment       │                            │
     │ 9. Store in session state   │                            │
     │                             │                            │
```

### Session State Keys

The library uses the following session state keys:

- `supabase_auth_client`: Supabase client instance
- `supabase_auth_authenticated`: Boolean authentication status
- `supabase_auth_access_token`: Access token
- `supabase_auth_refresh_token`: Refresh token
- `supabase_auth_tokens_processed`: Flag to prevent reprocessing tokens

## Testing

### Manual Testing

1. Run the demo app
2. Click "Login with Google"
3. Authenticate
4. Verify user info displays correctly
5. Click logout
6. Verify you're logged out

### Test Different Providers

Update the demo to test other OAuth providers:

```python
# In examples/demo.py
auth.login_button(provider="github")
auth.login_button(provider="gitlab")
```

## Building and Publishing

### Build Package

```bash
# Build with uv
uv build

# Or use traditional build
python -m build
```

This creates:
- `dist/streamlit_supabase_auth-0.1.0.tar.gz` (source distribution)
- `dist/streamlit_supabase_auth-0.1.0-py3-none-any.whl` (wheel)

### Test Installation

```bash
# Test installation with uv
uv pip install dist/streamlit_supabase_auth-0.1.0-py3-none-any.whl

# Or with pip
pip install dist/streamlit_supabase_auth-0.1.0-py3-none-any.whl
```

### Publish to PyPI

```bash
# Install twine if needed
uv pip install twine

# Test PyPI first
uv run twine upload --repository testpypi dist/*

# Production PyPI
uv run twine upload dist/*
```

## Common Issues

### Component Not Loading

If the clear_fragment component doesn't load:

1. Check that `frontend/clear_fragment.html` exists
2. Verify `MANIFEST.in` includes frontend files
3. Reinstall package: `uv pip install -e .`

### Tokens Not Clearing

If tokens remain in URL:

1. Check browser console for errors
2. Verify JavaScript is executing
3. Test in different browsers

### Session Not Persisting

If session doesn't persist across reruns:

1. Check session state keys are correct
2. Verify `_restore_session()` is called
3. Check token expiration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Code Style

Follow PEP 8 and use:
- Black for formatting
- Ruff for linting
- Type hints for all public methods

## License

MIT - See LICENSE file for details

