# Contributing to Career Path Architect

Thank you for your interest in contributing! This project welcomes contributions from the community.

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs
- Provide detailed reproduction steps
- Include environment information (OS, Node version, Python version, AWS region)
- Check existing issues to avoid duplicates

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the use case and expected behavior
- Explain how it fits with the project vision
- Consider implementation complexity

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with clear commit messages
4. Add tests for new functionality (maintain 99% coverage)
5. Ensure all tests pass: `cd apps/backend && uv run pytest`
6. Run linting: `cd apps/backend && uv run ruff check .`
7. Update documentation if needed
8. Submit a pull request with detailed description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/career-path-architect.git
cd career-path-architect

# Install git hooks
./scripts/install-git-hooks.sh

# Run dev environment
./dev.sh
```

## Code Standards

### Python (Backend)
- **Type hints**: Required for all functions
- **Formatting**: Ruff (line length 100)
- **Testing**: pytest with 99% coverage target
- **Docstrings**: Required for public functions
- **Error handling**: Proper exception handling with logging

### TypeScript (Frontend)
- **Strict mode**: Enabled
- **Components**: Functional components with hooks
- **Styling**: Cloudscape Design System
- **State**: Zustand for global state
- **Types**: Explicit types, avoid `any`

### LangGraph Agents
- **Single responsibility**: Each agent has one clear purpose
- **State management**: Use CareerPathState type
- **Error handling**: Return error state, don't raise
- **Testing**: Mock LLM responses
- **Logging**: Use logger, not print

### Testing Requirements
- **Coverage**: Maintain 99% coverage
- **Unit tests**: Test individual functions
- **Integration tests**: Test agent workflows
- **Mocking**: Mock AWS Bedrock calls
- **Assertions**: Clear, descriptive assertions

## Project Structure

```
career-path-architect/
├── apps/
│   ├── backend/          # FastAPI + LangGraph
│   │   ├── src/
│   │   │   └── career_path/
│   │   │       ├── graph/    # LangGraph agents
│   │   │       ├── main.py   # FastAPI app
│   │   │       └── ...
│   │   └── tests/
│   └── web/              # Next.js frontend
│       ├── app/
│       ├── components/
│       └── ...
├── docs/                 # Documentation
├── scripts/              # Utility scripts
└── ...
```

## Commit Message Guidelines

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Move cursor to..." not "Moves cursor to..."
- Limit first line to 72 characters
- Reference issues: "Fix #123: Description"

Examples:
```
Add critical review agent
Fix rate limiting bug in main.py
Update README with new screenshots
Test: Add coverage for gap analysis
```

## Testing

### Run All Tests
```bash
cd apps/backend
uv run pytest tests/ -v --cov=src/career_path
```

### Run Specific Test File
```bash
uv run pytest tests/test_nodes.py -v
```

### Check Coverage
```bash
uv run pytest --cov=src/career_path --cov-report=html
open htmlcov/index.html
```

## Security

- **Never commit secrets**: Use .env files (gitignored)
- **Input validation**: Validate all user inputs
- **Rate limiting**: Consider rate limit impact
- **Dependencies**: Keep dependencies updated
- **Secrets scanning**: Pre-commit hooks check for secrets

## Questions?

- Open a GitHub Discussion for general questions
- Open an Issue for bug reports or feature requests
- Reach out via LinkedIn for private inquiries

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
