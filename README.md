# AWS Pricing Calculator MCP Server

MCP server that provides tools for automating AWS Pricing Calculator estimate generation.

## Features

- **discover_services**: Fetch service schemas from AWS Pricing Calculator
- **build_estimate**: Build complete estimate JSON from specification
- **save_estimate**: Save estimate to AWS and get shareable URL
- **get_region_name**: Convert AWS region codes to display names

## Installation

### From PyPI (Recommended)

The easiest way to use the MCP server is via `uvx` (no installation needed):

```bash
uvx elchanio76-aws-pricing-calculator-mcp
```

Or install it with pip:

```bash
pip install elchanio76-aws-pricing-calculator-mcp
```

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (for uvx method)

### Install uv (if using uvx)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/elchanio-76/aws-pricing-calculator-mcp.git
cd aws-pricing-calculator-mcp

# Install in editable mode
pip install -e .
```

## Usage with Kiro

This MCP server is designed to work with the [AWS Pricing Calculator Power](https://github.com/elchanio-76/aws-pricing-calculator-power) for Kiro.

### Configuration

Add to your Kiro MCP configuration (`.kiro/settings/mcp.json`):

```json
{
  "mcpServers": {
    "aws-pricing-calculator": {
      "command": "uvx",
      "args": ["elchanio76-aws-pricing-calculator-mcp"],
      "disabled": false
    }
  }
}
```

Or install the [Kiro Power](https://github.com/elchanio-76/aws-pricing-calculator-power) which includes this configuration automatically.

### Usage Examples

Once configured, you can use the MCP server tools through Kiro:

**Example 1: Discover available AWS services**
```
Ask Kiro: "What AWS services are available in the pricing calculator?"
```

**Example 2: Build an estimate for a simple web application**
```
Ask Kiro: "Create an AWS pricing estimate for a web app with:
- 2 t3.medium EC2 instances in us-east-1
- 100 GB S3 storage
- CloudFront distribution"
```

**Example 3: Generate a shareable pricing calculator URL**
```
Ask Kiro: "Build and save an estimate for my architecture described in architecture.md"
```

## Tools

### discover_services

Fetch AWS Pricing Calculator service schemas.

**Parameters:**
- `service_codes` (optional): Array of service codes to discover

**Example:**
```json
{
  "service_codes": ["ec2Enhancement", "amazonS3"]
}
```

### build_estimate

Build complete estimate JSON from specification.

**Parameters:**
- `spec` (required): Estimate specification with groups and services

**Example:**
```json
{
  "spec": {
    "name": "My Estimate",
    "groups": [
      {
        "name": "Production",
        "services": [...]
      }
    ]
  }
}
```

### save_estimate

Save estimate to AWS and get shareable URL.

**Parameters:**
- `estimate` (required): Complete estimate JSON from build_estimate

### get_region_name

Convert AWS region code to display name.

**Parameters:**
- `region_code` (required): AWS region code (e.g., "us-east-1")

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/elchanio-76/aws-pricing-calculator-mcp.git
cd aws-pricing-calculator-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Testing

```bash
# Run tests
pytest tests/

# Test via stdio
python3 test_mcp_stdio.py
```

### Running Locally

```bash
python3 -m mcp_server.server
```

## Publishing to PyPI (Maintainers Only)

### Prerequisites

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Create a PyPI account at https://pypi.org

3. Set up PyPI API token (see Security section below)

### Release Process

1. **Update version numbers:**
   ```bash
   # Update version in pyproject.toml and mcp_server/__init__.py
   # Example: version = "0.2.0"
   ```

2. **Build the package:**
   ```bash
   # Clean previous builds
   rm -rf dist/ build/ *.egg-info
   
   # Build distributions
   python -m build
   ```

3. **Validate the package:**
   ```bash
   # Check package metadata and structure
   twine check dist/*
   ```

4. **Test with TestPyPI (recommended):**
   ```bash
   # Upload to TestPyPI
   twine upload --repository testpypi dist/*
   
   # Test installation
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ elchanio76-aws-pricing-calculator-mcp
   ```

5. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```

6. **Create GitHub release:**
   ```bash
   # Tag the release
   git tag v0.2.0
   git push origin v0.2.0
   
   # Create release on GitHub with release notes
   ```

### Creating and Securing PyPI API Tokens

**Creating a PyPI API Token:**

1. Log in to your PyPI account at https://pypi.org
2. Navigate to Account Settings → API tokens
3. Click "Add API token"
4. Choose token scope:
   - **Project-specific** (recommended): Limits token to this package only
   - **Entire account**: Access to all your projects
5. Set token name (e.g., "aws-pricing-calculator-mcp-publishing")
6. Copy the token immediately (it will only be shown once)

**Securing Your API Token:**

Option 1: Using `.pypirc` file (recommended for local development)

```bash
# Create ~/.pypirc
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
EOF

# Secure the file (Unix/macOS/Linux)
chmod 600 ~/.pypirc
```

Option 2: Using environment variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-TOKEN-HERE
```

Option 3: Command-line arguments (not recommended - visible in shell history)

```bash
twine upload --username __token__ --password pypi-YOUR-TOKEN-HERE dist/*
```

**Security Best Practices:**

- ✅ Use project-scoped tokens when possible
- ✅ Store tokens in `.pypirc` with restrictive permissions (chmod 600)
- ✅ Add `.pypirc` to `.gitignore` (already configured)
- ✅ Use GitHub Secrets for CI/CD workflows
- ✅ Rotate tokens periodically
- ✅ Enable 2FA on your PyPI account
- ❌ Never commit tokens to version control
- ❌ Never share tokens in chat, email, or documentation

### CI/CD Integration with GitHub Actions

**Automated Publishing Workflow:**

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
      - name: Check out code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      
      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Check package
        run: twine check dist/*
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

**Setup Instructions:**

1. Create a PyPI API token (project-scoped recommended)
2. Add the token to GitHub repository secrets:
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token (starts with `pypi-`)
3. Create a GitHub release to trigger the workflow:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   # Then create release on GitHub UI
   ```

**Testing Workflow (Optional):**

Create `.github/workflows/test.yml` for cross-platform testing:

```yaml
name: Test Package

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build twine pytest
      
      - name: Build package
        run: python -m build
      
      - name: Check package
        run: twine check dist/*
      
      - name: Install package
        run: pip install dist/*.whl
      
      - name: Test import
        run: python -c "import mcp_server; print(mcp_server.__version__)"
      
      - name: Run tests
        run: pytest tests/
```

## Troubleshooting

### Installation Issues

**Problem: `pip install` fails with "No matching distribution found"**

Solution:
- Ensure you're using Python 3.10 or higher: `python --version`
- Try upgrading pip: `pip install --upgrade pip`
- Check package name spelling: `elchanio76-aws-pricing-calculator-mcp`

**Problem: Entry point `aws-pricing-calculator-mcp` not found**

Solution:
- Ensure the package is installed: `pip list | grep aws-pricing-calculator`
- Check that Python's Scripts/bin directory is in PATH
- On Windows: Add `%APPDATA%\Python\Python3X\Scripts` to PATH
- On Unix/macOS: Add `~/.local/bin` to PATH
- Try reinstalling: `pip uninstall elchanio76-aws-pricing-calculator-mcp && pip install elchanio76-aws-pricing-calculator-mcp`

**Problem: `uvx` command not found**

Solution:
- Install uv: See installation instructions above
- Verify installation: `uv --version`
- Ensure uv's bin directory is in PATH

### Runtime Issues

**Problem: SSL certificate errors when calling AWS APIs**

Solution:
- The server uses `curl` subprocess to avoid Python SSL issues
- Ensure `curl` is installed and in PATH
- On Windows: Install curl via chocolatey or download from https://curl.se/windows/

**Problem: "Service not found" errors**

Solution:
- Verify service code spelling (e.g., "ec2Enhancement" not "ec2")
- Use `discover_services` tool to list available services
- Check AWS Pricing Calculator documentation for correct service codes

**Problem: Estimate save fails with 400 error**

Solution:
- Validate estimate JSON structure matches AWS requirements
- Ensure all required fields are present
- Check that service configurations are valid for the selected region
- Try building estimate with `build_estimate` first before saving

### Development Issues

**Problem: Tests fail after installation**

Solution:
- Ensure all dev dependencies are installed: `pip install -r requirements-dev.txt`
- Run tests from project root directory
- Check Python version compatibility

**Problem: Package build fails**

Solution:
- Clean previous builds: `rm -rf dist/ build/ *.egg-info`
- Verify `pyproject.toml` syntax
- Ensure all required files exist (README.md, LICENSE)
- Check that `mcp_server/__init__.py` has `__version__` defined

**Problem: Twine upload fails with authentication error**

Solution:
- Verify API token is correct and not expired
- Check `.pypirc` file permissions: `chmod 600 ~/.pypirc`
- Ensure username is `__token__` (not your PyPI username)
- Try using environment variables instead of `.pypirc`

### Getting Help

If you encounter issues not covered here:

1. Check existing [GitHub Issues](https://github.com/elchanio-76/aws-pricing-calculator-mcp/issues)
2. Create a new issue with:
   - Python version (`python --version`)
   - Operating system
   - Full error message
   - Steps to reproduce
3. For security issues, email lchanio@echyperion.com directly

## Architecture

The MCP server wraps existing Python scripts that handle:
- CloudFront API calls for service definitions
- Estimate JSON generation
- AWS Save API integration

All scripts use `curl` subprocess to avoid Python SSL issues with CloudFront.

## License

MIT

## Credits

Inspired by [aws-pricing-calculator](https://github.com/quincysting/aws-pricing-calculator) by Ian Qin.
Tools have been created by converting scripts from that repo.
Power.md and steering docs are based on the original repo with minor changes to make them compatible with Kiro Powers.
