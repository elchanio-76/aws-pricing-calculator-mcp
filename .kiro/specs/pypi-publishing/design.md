# Design Document: PyPI Publishing for AWS Pricing Calculator MCP Server

## Overview

This design document outlines the approach for publishing the AWS Pricing Calculator MCP Server to PyPI as a cross-platform Python package. The design leverages modern Python packaging standards (PEP 517/518) with setuptools as the build backend, ensuring compatibility across Windows, macOS, and Linux platforms.

## Architecture

### Package Structure

The package follows the standard Python package layout:

```
aws-pricing-calculator-mcp/
├── .gitignore
├── LICENSE
├── MANIFEST.in
├── README.md
├── pyproject.toml          # Primary configuration (PEP 518)
├── setup.py                # Minimal shim for setuptools
├── mcp_server/
│   ├── __init__.py         # Package initialization with __version__
│   ├── server.py           # MCP server implementation
│   └── tools.py            # Tool implementations
└── scripts/
    ├── __init__.py
    ├── calc_build.py
    ├── calc_discover.py
    ├── calc_save.py
    └── calc_utils.py
```

### Build System Architecture

The build system uses:
- **pyproject.toml**: Primary configuration file (PEP 518 compliant)
- **setuptools**: Build backend for creating distributions
- **build**: Frontend tool for building packages
- **twine**: Tool for uploading to PyPI

### Publishing Workflow

```
Source Code → Build (wheel + sdist) → Validate → Upload to PyPI
```

## Components and Interfaces

### 1. Package Configuration (pyproject.toml)

The `pyproject.toml` file serves as the single source of truth for package metadata and build configuration.

**Key Sections:**
- `[build-system]`: Specifies build requirements and backend
- `[project]`: Package metadata (name, version, dependencies, etc.)
- `[project.scripts]`: Entry point definitions
- `[project.urls]`: Project links
- `[tool.setuptools]`: Setuptools-specific configuration

**Interface:**
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "elchanio76-aws-pricing-calculator-mcp"
version = "0.1.0"
# ... other metadata

[project.scripts]
aws-pricing-calculator-mcp = "mcp_server.server:run"
```

### 2. Build Process

**Tool:** `python -m build`

**Inputs:**
- Source code in `mcp_server/` and `scripts/`
- Configuration from `pyproject.toml`
- Additional files specified in `MANIFEST.in`

**Outputs:**
- Wheel distribution: `dist/elchanio76_aws_pricing_calculator_mcp-{version}-py3-none-any.whl`
- Source distribution: `dist/elchanio76-aws-pricing-calculator-mcp-{version}.tar.gz`

**Process:**
1. Read configuration from `pyproject.toml`
2. Discover packages using `setuptools.find_packages()`
3. Include additional files via `MANIFEST.in`
4. Build wheel (binary distribution)
5. Build sdist (source distribution)
6. Output to `dist/` directory

### 3. Distribution Upload

**Tool:** `twine`

**Authentication:**
- Uses PyPI API tokens (stored in `~/.pypirc` or environment variables)
- Token format: `pypi-AgEIcHlwaS5vcmc...`

**Interface:**
```bash
twine upload dist/*
```

**Process:**
1. Validate package metadata and structure
2. Authenticate with PyPI using API token
3. Upload wheel and sdist to PyPI
4. Verify upload success

### 4. Entry Point System

**Mechanism:** Console scripts defined in `pyproject.toml`

**Configuration:**
```toml
[project.scripts]
aws-pricing-calculator-mcp = "mcp_server.server:run"
```

**Behavior:**
- Creates executable script in Python's `Scripts/` (Windows) or `bin/` (Unix) directory
- Script imports `mcp_server.server` module and calls `run()` function
- Available in PATH after installation

### 5. Cross-Platform Compatibility

**Path Handling:**
- Use `pathlib.Path` for all file operations
- Avoid hardcoded path separators (`/` or `\`)

**Subprocess Calls:**
- Use `subprocess.run()` with `shell=False` for security
- Use `shutil.which()` to locate executables

**Platform Detection:**
```python
import platform
import sys

system = platform.system()  # 'Windows', 'Darwin', 'Linux'
```

**Testing Strategy:**
- Test on all three platforms before release
- Use platform-specific CI runners (GitHub Actions)

## Data Models

### Package Metadata

```python
{
    "name": "elchanio76-aws-pricing-calculator-mcp",
    "version": "0.1.0",
    "description": "MCP server for automating AWS Pricing Calculator estimate generation",
    "author": "Eleftherios Chaniotakis",
    "author_email": "lchanio@echyperion.com",
    "license": "MIT",
    "python_requires": ">=3.10",
    "dependencies": ["mcp>=0.9.0"],
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent"
    ]
}
```

### PyPI Configuration (~/.pypirc)

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

### Build Artifacts

```python
{
    "wheel": {
        "filename": "elchanio76_aws_pricing_calculator_mcp-0.1.0-py3-none-any.whl",
        "format": "wheel",
        "python_tag": "py3",
        "abi_tag": "none",
        "platform_tag": "any"
    },
    "sdist": {
        "filename": "elchanio76-aws-pricing-calculator-mcp-0.1.0.tar.gz",
        "format": "gztar"
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Package Metadata Completeness

*For any* built package distribution, all required metadata fields (name, version, description, author, license) SHALL be present and non-empty.

**Validates: Requirements 1.1**

### Property 2: Dependency Declaration

*For any* package configuration, all runtime dependencies SHALL be declared in the dependencies list with appropriate version constraints.

**Validates: Requirements 1.3**

### Property 3: Project URLs Presence

*For any* package metadata, the project URLs (homepage, repository, issues) SHALL be present and valid.

**Validates: Requirements 1.5**

### Property 4: Platform-Agnostic Path Handling

*For any* file operation in the codebase, path handling SHALL use `pathlib.Path` or equivalent platform-agnostic methods rather than string concatenation with hardcoded separators.

**Validates: Requirements 2.4**

### Property 5: Dual Distribution Generation

*For any* package build, both wheel (.whl) and source distribution (.tar.gz) files SHALL be generated in the dist/ directory.

**Validates: Requirements 3.2**

### Property 6: Source Files Inclusion

*For any* built distribution, all Python source files from `mcp_server/` and `scripts/` packages SHALL be included in the distribution archive.

**Validates: Requirements 3.3**

### Property 7: Critical Files Inclusion

*For any* built distribution, the README.md and LICENSE files SHALL be included in the distribution archive.

**Validates: Requirements 3.4**

### Property 8: Package Validation

*For any* built package, running `twine check` SHALL pass without errors or warnings.

**Validates: Requirements 3.5, 8.1**

### Property 9: Entry Point Availability

*For any* successful package installation in a clean environment, the entry point command `aws-pricing-calculator-mcp` SHALL be available in the system PATH and executable.

**Validates: Requirements 5.3, 8.4**

### Property 10: Dependency Installation

*For any* package installation in a clean environment, all declared dependencies SHALL be installed automatically and importable.

**Validates: Requirements 5.4**

### Property 11: Package Importability

*For any* installed package, importing `mcp_server` SHALL succeed and expose the `__version__` attribute matching the package version.

**Validates: Requirements 5.5, 7.4**

### Property 12: Documentation Completeness

*For any* README.md file, it SHALL contain sections for installation instructions, usage examples, publishing process, and troubleshooting guidance.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

### Property 13: README in Package Metadata

*For any* built distribution, the package metadata SHALL include the long description populated from README.md.

**Validates: Requirements 6.5**

### Property 14: Version Consistency

*For any* package build, the version string in `pyproject.toml`, `mcp_server/__init__.py`, and the built distribution filename SHALL be identical.

**Validates: Requirements 7.1, 7.5**

### Property 15: Semantic Versioning Format

*For any* version string in the package, it SHALL follow semantic versioning format (MAJOR.MINOR.PATCH with optional pre-release/build metadata).

**Validates: Requirements 7.3**

### Property 16: Required Files in Distribution

*For any* built distribution, all files specified in MANIFEST.in SHALL be included in the distribution archive.

**Validates: Requirements 8.2**

### Property 17: Security Configuration

*For any* repository, the .gitignore file SHALL include patterns to prevent committing sensitive files like .pypirc and API tokens.

**Validates: Requirements 9.2**

### Property 18: Token Documentation

*For any* README.md file, it SHALL include guidance on creating and securing PyPI API tokens.

**Validates: Requirements 9.4**

### Property 19: CI/CD Documentation

*For any* README.md or documentation, it SHALL include examples for CI/CD platform integration (e.g., GitHub Actions).

**Validates: Requirements 10.4**

## Error Handling

### Build Errors

**Missing Dependencies:**
```python
# Error: ModuleNotFoundError during build
# Solution: Ensure build dependencies in [build-system] are correct
```

**Invalid Metadata:**
```python
# Error: Invalid version string
# Solution: Validate version follows PEP 440 (e.g., "0.1.0", not "v0.1.0")
```

**Missing Files:**
```python
# Error: FileNotFoundError for README.md
# Solution: Ensure MANIFEST.in includes all required files
```

### Upload Errors

**Authentication Failure:**
```bash
# Error: 403 Forbidden - Invalid or expired token
# Solution: Generate new API token from PyPI account settings
```

**Package Name Conflict:**
```bash
# Error: 400 Bad Request - Package name already exists
# Solution: Choose a different package name or claim existing package
```

**Invalid Distribution:**
```bash
# Error: 400 Bad Request - Invalid distribution format
# Solution: Rebuild package with correct setuptools configuration
```

### Installation Errors

**Python Version Mismatch:**
```bash
# Error: Requires Python >=3.10 but found 3.9
# Solution: Upgrade Python or use compatible version
```

**Dependency Conflicts:**
```bash
# Error: Cannot install due to conflicting dependencies
# Solution: Review dependency version constraints
```

**Entry Point Not Found:**
```bash
# Error: Command 'aws-pricing-calculator-mcp' not found
# Solution: Ensure Scripts/bin directory is in PATH
```

## Testing Strategy

### Unit Tests

**Package Metadata Validation:**
- Test that `pyproject.toml` contains all required fields
- Test that version string follows semantic versioning
- Test that classifiers include all supported Python versions

**Version Consistency:**
- Test that `__version__` in `__init__.py` matches `pyproject.toml`
- Test that version can be extracted programmatically

**File Inclusion:**
- Test that `MANIFEST.in` patterns match expected files
- Test that critical files (README, LICENSE) are discoverable

### Property-Based Tests

**Build Validation:**
- Property 1: Verify metadata completeness across multiple builds
- Property 5: Verify all source files are included in distributions
- Property 6: Verify version consistency across all locations
- Property 10: Verify build reproducibility

**Installation Testing:**
- Property 2: Test installation on Windows, macOS, Linux (via CI)
- Property 3: Test entry point availability after installation
- Property 4: Test dependency installation
- Property 8: Test package import and version access

### Integration Tests

**End-to-End Build and Install:**
1. Clean environment setup
2. Build package from source
3. Install package in isolated environment
4. Verify entry point execution
5. Verify package import
6. Cleanup

**TestPyPI Validation:**
1. Build package
2. Upload to TestPyPI
3. Install from TestPyPI in clean environment
4. Run smoke tests
5. Verify functionality

### Manual Testing Checklist

**Pre-Release:**
- [ ] Build package locally
- [ ] Install in virtual environment
- [ ] Test entry point execution
- [ ] Test on Windows (if available)
- [ ] Test on macOS (if available)
- [ ] Test on Linux
- [ ] Upload to TestPyPI
- [ ] Install from TestPyPI
- [ ] Verify README renders correctly on TestPyPI

**Release:**
- [ ] Update version in `pyproject.toml` and `__init__.py`
- [ ] Update CHANGELOG (if exists)
- [ ] Build package
- [ ] Upload to PyPI
- [ ] Install from PyPI
- [ ] Verify README renders correctly on PyPI
- [ ] Create GitHub release tag
- [ ] Update documentation

### CI/CD Testing

**GitHub Actions Workflow:**
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
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install build twine
      - run: python -m build
      - run: twine check dist/*
      - run: pip install dist/*.whl
      - run: aws-pricing-calculator-mcp --help
```

## Publishing Process

### Step-by-Step Workflow

**1. Prepare Release**
```bash
# Update version in pyproject.toml and mcp_server/__init__.py
# Commit changes
git add pyproject.toml mcp_server/__init__.py
git commit -m "Bump version to 0.1.0"

# Tag the release
git tag v0.1.0
git push origin main
git push origin v0.1.0
```

**2. Build Package**
```bash
# Install build tools
pip install build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distributions
python -m build
```

**3. Validate Package**
```bash
# Check package with twine
twine check dist/*

# Test installation locally
pip install dist/*.whl

# Verify entry point
aws-pricing-calculator-mcp --help
```

**4. Upload to TestPyPI (Optional)**
```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ elchanio76-aws-pricing-calculator-mcp
```

**5. Upload to PyPI**
```bash
# Upload to PyPI
twine upload dist/*

# Verify on PyPI
# Visit: https://pypi.org/project/elchanio76-aws-pricing-calculator-mcp/
```

**6. Create GitHub Release**
```bash
# The tag was already created in step 1
# Now create a release on GitHub that references this tag
# Visit: https://github.com/elchanio-76/aws-pricing-calculator-mcp/releases/new
# Select tag: v0.1.0
# Add release notes and changelog
```

### API Token Setup

**Creating PyPI API Token:**
1. Log in to PyPI account
2. Navigate to Account Settings → API tokens
3. Click "Add API token"
4. Set scope (entire account or specific project)
5. Copy token (shown only once)

**Configuring Token:**

Option 1: `.pypirc` file
```bash
# Create ~/.pypirc
cat > ~/.pypirc << EOF
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

# Secure the file
chmod 600 ~/.pypirc
```

Option 2: Environment variables
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-TOKEN-HERE
```

Option 3: Command-line arguments
```bash
twine upload --username __token__ --password pypi-YOUR-TOKEN-HERE dist/*
```

### Automation with GitHub Actions

**Automated Publishing Workflow:**
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

**Setup:**
1. Create PyPI API token
2. Add token to GitHub repository secrets as `PYPI_API_TOKEN`
3. Create GitHub release to trigger workflow

## Documentation Updates

### README.md Updates

**Installation Section:**
```markdown
## Installation

### From PyPI (Recommended)

```bash
pip install elchanio76-aws-pricing-calculator-mcp
```

Or using uvx:

```bash
uvx elchanio76-aws-pricing-calculator-mcp
```

### From Source

```bash
git clone https://github.com/elchanio-76/aws-pricing-calculator-mcp.git
cd aws-pricing-calculator-mcp
pip install -e .
```
```

**Publishing Section (for maintainers):**
```markdown
## Publishing (Maintainers Only)

### Prerequisites

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Set up PyPI API token in `~/.pypirc`

### Release Process

1. Update version in `pyproject.toml` and `mcp_server/__init__.py`
2. Build package: `python -m build`
3. Validate: `twine check dist/*`
4. Upload to TestPyPI: `twine upload --repository testpypi dist/*`
5. Test installation: `pip install --index-url https://test.pypi.org/simple/ elchanio76-aws-pricing-calculator-mcp`
6. Upload to PyPI: `twine upload dist/*`
7. Create GitHub release tag
```

### Kiro Configuration Update

**After PyPI Publication:**
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

## Security Considerations

### API Token Security

**Best Practices:**
- Never commit API tokens to version control
- Use `.pypirc` with restrictive permissions (chmod 600)
- Use project-scoped tokens when possible
- Rotate tokens periodically
- Use GitHub secrets for CI/CD

**Token Storage:**
```bash
# Add .pypirc to .gitignore
echo ".pypirc" >> .gitignore

# Secure permissions
chmod 600 ~/.pypirc
```

### Package Security

**Supply Chain Security:**
- Pin build dependencies in `pyproject.toml`
- Use `pip-audit` to check for vulnerabilities
- Sign releases with GPG (optional)
- Enable 2FA on PyPI account

**Code Security:**
- Review all dependencies
- Avoid executing arbitrary code during installation
- Use `subprocess.run()` with `shell=False`
- Validate all user inputs

## Maintenance

### Version Updates

**Semantic Versioning:**
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Update Process:**
1. Update `pyproject.toml`: `version = "0.2.0"`
2. Update `mcp_server/__init__.py`: `__version__ = "0.2.0"`
3. Commit and tag: `git tag v0.2.0`
4. Build and publish

### Dependency Updates

**Regular Maintenance:**
```bash
# Check for outdated dependencies
pip list --outdated

# Update dependencies in pyproject.toml
# Test thoroughly before publishing
```

### Troubleshooting

**Common Issues:**

**1. **"Package already exists" error:**
   - Cannot reupload same version
   - Increment version number
   - Note: Package name is `elchanio76-aws-pricing-calculator-mcp` to avoid confusion with official AWS packages

2. **"Invalid distribution" error:**
   - Check `pyproject.toml` syntax
   - Ensure all required files exist
   - Rebuild package

3. **Entry point not working:**
   - Verify `[project.scripts]` configuration
   - Check that target function exists
   - Reinstall package

4. **Import errors after installation:**
   - Verify package structure
   - Check `[tool.setuptools.packages.find]`
   - Ensure `__init__.py` files exist
