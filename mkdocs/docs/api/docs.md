# Interactive API Documentation

!!! note
    Complete **interactive** API documentation is available on your **Tube Archivist** instance at `/api/docs/`.

## Quick Links

- **[API Reference](../generated/reference.md)** - Complete endpoint documentation (auto-generated)
- **[OpenAPI Schema](../generated/schema.json)** - Download the raw OpenAPI 3.0 schema
- **[Introduction](../introduction.md)** - Getting started with the API

## Accessing Interactive Documentation

To access the full Swagger UI documentation:

1. Navigate to your TubeArchivist instance
2. Go to `/api/docs/` (e.g., `https://your-instance.com/api/docs/`)
3. Use your API token for authentication if needed

The interactive documentation allows you to:

- Explore all available endpoints
- View detailed request/response schemas  
- Test API calls directly from the browser
- Download the OpenAPI specification

## Schema Download

You can also download the OpenAPI schema directly from your instance:

```bash
curl -o api-schema.json https://your-instance.com/api/schema/
```

Or use the pre-generated version: [schema.json](../generated/schema.json)
