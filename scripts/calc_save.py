#!/usr/bin/env python3
"""
Save an AWS Pricing Calculator estimate via the Save API.

Takes an estimate JSON file and POSTs it to get a shareable calculator URL.

Usage:
  python calc_save.py estimate.json
  python calc_save.py estimate.json --local-only
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from calc_utils import curl_post, SAVE_API, CALCULATOR_URL
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from calc_utils import curl_post, SAVE_API, CALCULATOR_URL


def save_estimate(estimate_dict):
    """POST estimate to Save API. Returns dict with savedKey and url."""
    import sys
    from pathlib import Path
    
    # Debug logging to file
    debug_file = Path("/tmp/aws_calc_debug.log")
    with open(debug_file, "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"[DEBUG save_estimate] Called at {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"[DEBUG save_estimate] Estimate type: {type(estimate_dict)}\n")
        f.write(f"[DEBUG save_estimate] Estimate keys: {list(estimate_dict.keys()) if isinstance(estimate_dict, dict) else 'N/A'}\n")
        
        # Validate estimate structure
        if not isinstance(estimate_dict, dict):
            f.write(f"[ERROR] estimate_dict is not a dict!\n")
            raise TypeError(f"estimate_dict must be a dict, got {type(estimate_dict).__name__}")
        
        # Check for required top-level keys
        required_keys = ["name", "groups", "totalCost", "metaData"]
        missing_keys = [k for k in required_keys if k not in estimate_dict]
        if missing_keys:
            f.write(f"[DEBUG save_estimate] Missing required keys: {missing_keys}\n")
        
        # Log estimate size and first 500 chars
        estimate_json = json.dumps(estimate_dict)
        f.write(f"[DEBUG save_estimate] JSON size: {len(estimate_json)} bytes\n")
        f.write(f"[DEBUG save_estimate] JSON preview: {estimate_json[:500]}...\n")
    
    resp = curl_post(SAVE_API, estimate_dict)
    
    # Check for error status codes
    status_code = resp.get("statusCode", 200)
    if status_code >= 400:
        # Error response
        body_str = resp.get("body", "")
        if isinstance(body_str, str):
            try:
                error_body = json.loads(body_str)
                error_msg = error_body.get("message", body_str)
            except:
                error_msg = body_str
        else:
            error_msg = str(body_str)
        raise RuntimeError(f"Save API error ({status_code}): {error_msg}")
    
    # Parse the nested body JSON string
    if isinstance(resp.get("body"), str):
        body = json.loads(resp["body"])
    else:
        body = resp
    
    # Extract savedKey from the response
    saved_key = body.get("savedKey", "")
    if not saved_key:
        # Fallback: sometimes it's in message field
        message = body.get("message", "")
        if "file name is" in message:
            # Extract from message like "The file name is abc123"
            saved_key = message.split()[-1]
        else:
            saved_key = ""
    
    if not saved_key:
        raise RuntimeError(f"No savedKey in response: {json.dumps(body)}")
    
    url = CALCULATOR_URL.format(key=saved_key)
    return {"savedKey": saved_key, "url": url}


def save_to_file(estimate_dict, path):
    """Save estimate JSON to a local file."""
    with open(path, "w") as f:
        json.dump(estimate_dict, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Save estimate to AWS Pricing Calculator",
    )
    parser.add_argument("estimate_json", help="Path to estimate JSON file")
    parser.add_argument("--local-only", action="store_true",
                        help="Only validate, don't upload")
    args = parser.parse_args()

    with open(args.estimate_json, "r") as f:
        estimate = json.load(f)

    total = estimate.get("totalCost", {}).get("monthly", 0)
    total_services = sum(
        len(g.get("services", {}))
        for g in estimate.get("groups", {}).values()
    )
    print(f"Estimate: {estimate.get('name', 'Unknown')}")
    print(f"Services: {total_services}")
    print(f"Monthly: ${total:,.2f}")

    if args.local_only:
        print("\n(local-only mode, skipping upload)")
        return

    print("\nSaving to AWS Pricing Calculator...")
    result = save_estimate(estimate)
    print(f"Saved Key: {result['savedKey']}")
    print(f"\nCalculator URL:")
    print(f"  {result['url']}")

    url_path = args.estimate_json.replace(".json", "_url.txt")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(url_path, "w") as f:
        f.write(f"{estimate.get('name', 'Estimate')}\n")
        f.write(f"Generated: {ts}\n")
        f.write(f"Key: {result['savedKey']}\n")
        f.write(f"URL: {result['url']}\n")
        f.write(f"\nMonthly: ${total:,.2f}\n")
        f.write(f"Annual:  ${total * 12:,.2f}\n")
    print(f"Saved URL: {url_path}")


if __name__ == "__main__":
    main()
