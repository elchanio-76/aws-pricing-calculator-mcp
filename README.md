# AWS Pricing Calculator MCP Server

MCP server that provides tools for automating AWS Pricing Calculator estimate generation.

## Features

- **discover_services**: Fetch service schemas from AWS Pricing Calculator
- **build_estimate**: Build complete estimate JSON from specification
- **save_estimate**: Save estimate to AWS and get shareable URL
- **get_region_name**: Convert AWS region codes to display names

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Run the MCP Server

The server is designed to be run via `uvx` directly from GitHub (no installation needed):

```bash
uvx --from git+https://github.com/elchanio-76/aws-pricing-calculator-mcp aws-pricing-calculator-mcp
```

Or install it globally:

```bash
uv tool install git+https://github.com/elchanio-76/aws-pricing-calculator-mcp
```

Once published to PyPI, you can use the simpler form:

```bash
uvx aws-pricing-calculator-mcp
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
      "args": ["--from", "git+https://github.com/elchanio-76/aws-pricing-calculator-mcp", "aws-pricing-calculator-mcp"],
      "disabled": false
    }
  }
}
```

Or if published to PyPI:

```json
{
  "mcpServers": {
    "aws-pricing-calculator": {
      "command": "uvx",
      "args": ["aws-pricing-calculator-mcp"],
      "disabled": false
    }
  }
}
```

Or install the [Kiro Power](https://github.com/elchanio-76/aws-pricing-calculator-power) which includes this configuration automatically.

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

# Install dependencies
uv pip install -e .
```

### Testing

```bash
# Run tests
python3 test_mcp_server.py

# Test via stdio
python3 test_mcp_stdio.py
```

### Running Locally

```bash
python3 -m mcp_server.server
```

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
