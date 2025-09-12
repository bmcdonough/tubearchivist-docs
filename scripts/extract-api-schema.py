#!/usr/bin/env python3
"""
Extract API schema from a running TubeArchivist instance.

This script can be used to manually extract the OpenAPI schema 
for development and testing purposes.
"""

import argparse
import json
import requests
import sys
from pathlib import Path


def extract_schema(base_url, token=None, output_file=None):
    """Extract OpenAPI schema from TubeArchivist instance."""
    
    # Construct the schema URL
    schema_url = f"{base_url.rstrip('/')}/api/schema/"
    
    # Set up headers
    headers = {}
    if token:
        headers['Authorization'] = f'Token {token}'
    
    print(f"Extracting schema from: {schema_url}")
    
    try:
        # Make the request
        response = requests.get(schema_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse JSON
        schema = response.json()
        
        # Validate it's a proper OpenAPI schema
        if 'openapi' not in schema:
            print("Warning: Response doesn't appear to be a valid OpenAPI schema")
        
        # Determine output file
        if not output_file:
            output_file = Path('api-schema.json')
        else:
            output_file = Path(output_file)
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(schema, f, indent=2)
        
        print(f"Schema extracted successfully to: {output_file}")
        print(f"Schema version: {schema.get('info', {}).get('version', 'unknown')}")
        print(f"Endpoints found: {len(schema.get('paths', {}))}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Extract OpenAPI schema from TubeArchivist instance'
    )
    parser.add_argument(
        'url', 
        help='Base URL of TubeArchivist instance (e.g., http://localhost:8000)'
    )
    parser.add_argument(
        '-t', '--token',
        help='API token for authentication (optional if publicly accessible)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: api-schema.json)'
    )
    
    args = parser.parse_args()
    
    success = extract_schema(args.url, args.token, args.output)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()