"""Service for interacting with Google Gemini AI API."""

import json
from typing import Any

import google.generativeai as genai  # type: ignore[import-untyped]
from google.generativeai.types import GenerationConfig  # type: ignore[import-untyped]

from app.config import settings
from app.schemas.product import ProductInput, ProductOutput


class GeminiService:
    """Service class for transforming product data using Gemini AI."""

    def __init__(self) -> None:
        """Initialize the Gemini service with API configuration."""
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please configure it in your .env file.")

        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config=GenerationConfig(
                temperature=settings.gemini_temperature,
                max_output_tokens=settings.gemini_max_tokens,
            ),
        )

    async def transform_product_description(self, product: ProductInput) -> ProductOutput:
        """
        Transform complex/technical product data into consumer-friendly marketing copy.

        Args:
            product: ProductInput with technical title and description

        Returns:
            ProductOutput with consumer-friendly, engaging title and description

        Raises:
            ValueError: If the transformation fails or returns invalid data
            Exception: For other API errors
        """
        prompt = self._build_transformation_prompt(product)

        try:
            # Generate content using Gemini
            response = await self.model.generate_content_async(prompt)

            if not response.text:
                raise ValueError("Gemini API returned empty response")

            # Parse the JSON response
            transformed_data = self._parse_response(response.text)

            # Validate and return as ProductOutput
            return ProductOutput(**transformed_data)

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Gemini response as JSON: {e}") from e
        except Exception as e:
            raise Exception(f"Gemini API error: {e}") from e

    def _build_transformation_prompt(self, product: ProductInput) -> str:
        """
        Build the prompt for Gemini to transform product data.

        Args:
            product: Input product data

        Returns:
            Formatted prompt string
        """
        return f"""You are an expert ecommerce copywriter. Transform the following technical product information into engaging, consumer-friendly marketing copy.

INSTRUCTIONS:
1. Convert technical jargon into simple, benefit-focused language
2. Make the title catchy and appealing while maintaining accuracy
3. Write the description in a conversational, persuasive tone
4. Focus on benefits rather than technical specifications
5. Keep the same key product features but explain them in simple terms
6. Maintain the same approximate length as the original

INPUT PRODUCT:
Title: {product.title}
Description: {product.description}

OUTPUT FORMAT:
Return ONLY a valid JSON object with this exact structure (no markdown, no code blocks):
{{
    "title": "transformed title here",
    "description": "transformed description here"
}}

Respond with JSON only:"""

    def _parse_response(self, response_text: str) -> dict[str, Any]:
        """
        Parse and clean the Gemini API response.

        Args:
            response_text: Raw response text from Gemini

        Returns:
            Parsed dictionary with title and description

        Raises:
            json.JSONDecodeError: If response is not valid JSON
        """
        # Clean up the response (remove markdown code blocks if present)
        cleaned_text = response_text.strip()

        print("cleaned_text")
        print(cleaned_text)

        # Remove markdown code blocks if present
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]  # Remove ```json
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]  # Remove ```

        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]  # Remove trailing ```

        cleaned_text = cleaned_text.strip()

        # Parse JSON
        data = json.loads(cleaned_text)

        # Validate required fields
        if "title" not in data or "description" not in data:
            raise ValueError("Response missing required fields: title or description")

        return data


# Global service instance
gemini_service = GeminiService()
