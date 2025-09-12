# API Documentation Scripts

This directory contains scripts for managing API documentation generation.

## extract-api-schema.py

Extracts the OpenAPI schema from a running TubeArchivist instance.

### Usage

```bash
# Basic usage
python extract-api-schema.py http://localhost:8000

# With API token
python extract-api-schema.py http://localhost:8000 -t YOUR_API_TOKEN

# Custom output file
python extract-api-schema.py http://localhost:8000 -o custom-schema.json
```

### Requirements

Install the required dependencies:

```bash
pip install -r requirements-schema.txt
```

## Automated Updates

The API documentation is automatically updated via GitHub Actions whenever:

1. TubeArchivist releases a new version (requires webhook setup)
2. Manual trigger via GitHub Actions UI  
3. Daily scheduled check for new releases

The workflow will:

1. Spin up a TubeArchivist instance with the specified version
2. Extract the OpenAPI schema
3. Generate markdown documentation
4. Update the MkDocs navigation
5. Commit changes to the repository

## Manual Testing

To test the documentation generation locally:

1. Start a TubeArchivist instance
2. Extract the schema: `python scripts/extract-api-schema.py http://localhost:8000`
3. Process with the GitHub Actions workflow or manually generate docs