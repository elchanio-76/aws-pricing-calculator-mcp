"""MCP tools that wrap the AWS Pricing Calculator scripts."""

import json
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path so we can import the modules
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from calc_discover import discover_service, list_services
from calc_build import build_estimate, build_from_spec
from calc_save import save_estimate
from calc_utils import region_name


async def discover_services_tool(service_codes: list[str] | None = None) -> dict[str, Any]:
    """
    Discover AWS Pricing Calculator service schemas.
    
    Fetches live service definitions from CloudFront and extracts all configurable
    calculationComponent fields with their IDs, types, options, and defaults.
    
    Args:
        service_codes: List of service codes to discover (e.g., ["ec2Enhancement", "amazonS3"]).
                      If None or empty, returns list of all available services.
    
    Returns:
        Dictionary with discovered schemas or list of available services.
    """
    try:
        # If no service codes provided, list all services
        if not service_codes:
            services = list_services()
            return {
                "success": True,
                "service_count": len(services),
                "services": services
            }
        
        # Discover schemas for specified services
        schemas = {}
        for code in service_codes:
            try:
                schema = discover_service(code)
                schemas[code] = schema
            except Exception as e:
                schemas[code] = {
                    "error": str(e),
                    "success": False
                }
        
        return {
            "success": True,
            "schemas": schemas
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def build_estimate_tool(spec: dict[str, Any]) -> dict[str, Any]:
    """
    Build AWS Pricing Calculator estimate JSON from a specification.
    
    Takes a spec defining groups and services, and builds the complete estimate
    JSON structure ready to be saved to the AWS Pricing Calculator.
    
    Args:
        spec: Estimate specification with format:
              {
                "name": "My Estimate",
                "groups": [
                  {
                    "name": "Production",
                    "services": [
                      {
                        "serviceCode": "ec2Enhancement",
                        "serviceName": "Amazon EC2",
                        "estimateFor": "template",
                        "version": "0.0.68",
                        "region": "us-east-1",
                        "monthlyCost": 175.20,
                        "configSummary": "1x m5.xlarge Linux On-Demand",
                        "calculationComponents": { ... }
                      }
                    ]
                  }
                ]
              }
    
    Returns:
        Dictionary with the built estimate or error information.
    """
    try:
        # Extract groups from spec
        groups_list = []
        for group in spec.get("groups", []):
            groups_list.append((group["name"], group["services"]))
        
        # Build the estimate
        estimate = build_estimate(spec.get("name", "Estimate"), groups_list)
        
        # Calculate summary info
        total_monthly = estimate["totalCost"]["monthly"]
        total_services = sum(len(g["services"]) for g in estimate["groups"].values())
        
        return {
            "success": True,
            "estimate": estimate,
            "summary": {
                "name": estimate["name"],
                "groups": len(estimate["groups"]),
                "services": total_services,
                "monthly_cost": total_monthly,
                "annual_cost": total_monthly * 12
            }
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def save_estimate_tool(estimate: dict[str, Any]) -> dict[str, Any]:
    """
    Save an estimate to AWS Pricing Calculator and get a shareable URL.
    
    POSTs the estimate JSON to the AWS Pricing Calculator Save API and returns
    a shareable calculator URL that can be opened in a browser.
    
    Args:
        estimate: Complete estimate JSON (output from build_estimate_tool)
    
    Returns:
        Dictionary with the saved key and calculator URL, or error information.
    """
    try:
        import traceback
        result = save_estimate(estimate)
        
        # Calculate summary
        total_monthly = estimate.get("totalCost", {}).get("monthly", 0)
        total_services = sum(
            len(g.get("services", {}))
            for g in estimate.get("groups", {}).values()
        )
        
        return {
            "success": True,
            "saved_key": result["savedKey"],
            "calculator_url": result["url"],
            "summary": {
                "name": estimate.get("name", "Unknown"),
                "services": total_services,
                "monthly_cost": total_monthly,
                "annual_cost": total_monthly * 12
            }
        }
    
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


async def get_region_name_tool(region_code: str) -> dict[str, Any]:
    """
    Get the display name for an AWS region code.
    
    Args:
        region_code: AWS region code (e.g., "us-east-1")
    
    Returns:
        Dictionary with the region display name.
    """
    try:
        name = region_name(region_code)
        return {
            "success": True,
            "region_code": region_code,
            "region_name": name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
