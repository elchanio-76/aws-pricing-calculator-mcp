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
