# Gemini AI Integration Usage Guide

This guide shows you how to use the Gemini AI product transformation feature.

## Setup

1. **Get a Gemini API Key** (Free tier available)
   - Visit https://aistudio.google.com/app/api-keys
   - Create or sign in with your Google account
   - Click "Create API Key"
   - Copy your API key

2. **Configure the API Key**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your API key
   GEMINI_API_KEY=your_actual_api_key_here

   GEMINI_MODEL="your_model"
   ```

3. **Configure other env variables: model, temperature, etc.**

4. **Install Dependencies**
   ```bash
   poetry install
   ```

## Running the Application

Start the FastAPI development server:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

All product endpoints require authentication set it in your `.env` file.

### 1. Transform Product Data

**Endpoint:** `POST /products/transform?token=your_query_token`

**Headers:**
```
X-Token: your_header_token
Content-Type: application/json
```

**Request Body:**
```json
{
  "product": {
    "title": "Advanced Whey Protein Isolate Formula",
    "description": "Our proprietary WPI blend features 25g of rapidly absorbed complete amino acid profile..."
  }
}
```

**Response:**
```json
{
  "success": true,
  "original": {
    "title": "Advanced Whey Protein Isolate Formula",
    "description": "Our proprietary WPI blend..."
  },
  "transformed": {
    "title": "Premium Protein Shake for Faster Recovery",
    "description": "Fuel your fitness goals with our smooth, delicious protein shake..."
  },
  "error": null
}
```

### 2. Get Sample Complex Data

**Endpoint:** `GET /products/sample/complex?token=your_query_token`

Returns the sample technical product data for testing.

### 3. Get Sample Optimized Data

**Endpoint:** `GET /products/sample/optimized?token=your_query_token`

Returns an example of optimized marketing copy.

## Testing with cURL

```bash
# Get sample complex data
curl -X GET "http://localhost:8000/products/sample/complex?token=your_query_token" \
  -H "X-Token: your_header_token"

# Transform product data
curl -X POST "http://localhost:8000/products/transform?token=your_query_token" \
  -H "X-Token: your_header_token" \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "title": "Advanced Whey Protein Isolate Formula",
      "description": "Our proprietary WPI blend features 25g of rapidly absorbed complete amino acid profile with enhanced bioavailability through CFM and ultra-filtration processes."
    }
  }'
```

## Testing

Run the included test script:

```bash
poetry run python test_gemini.py
```

This will load the sample complex data, transform it using Gemini AI, and display the results.

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test all endpoints directly from these interfaces!

## Architecture

The implementation follows FastAPI best practices:

- **[app/config.py](app/config.py)** - Configuration management using Pydantic Settings
- **[app/schemas/product.py](app/schemas/product.py)** - Pydantic models for request/response validation
- **[app/services/gemini_service.py](app/services/gemini_service.py)** - Service layer for Gemini API interaction
- **[app/routers/products.py](app/routers/products.py)** - API endpoints for product transformation
- **[app/main.py](app/main.py)** - Main application with router registration

## Troubleshooting

### API Key Not Set Error

```
ValueError: GEMINI_API_KEY is not set. Please configure it in your .env file.
```

**Solution:** Make sure you've created a `.env` file with your Gemini API key.

### Rate Limits

Gemini free tier has rate limits. If you hit them, wait a moment and try again.
