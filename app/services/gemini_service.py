"""Service for interacting with Google Gemini AI API."""

import json
import logging

from google import genai
from google.genai import errors
from pydantic import BaseModel

from app.config import get_settings
from app.schemas.product import ProductInput, ProductOutput


class GeminiResponse(BaseModel):
    title: str
    description: str


class GeminiService:
    """Service class for transforming product data using Gemini AI."""

    def __init__(self) -> None:
        """Initialize the Gemini service with API configuration."""
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)

        self.logger.debug(
            "Initialized GeminiService with model=%s", self.settings.gemini_model)

        if not self.settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please configure it in your .env file.")

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
            async with genai.Client(api_key=self.settings.gemini_api_key).aio as aclient:
                response = await aclient.models.generate_content(
                    model=self.settings.gemini_model,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=self.settings.gemini_temperature,
                        max_output_tokens=self.settings.gemini_max_tokens,
                        response_mime_type="application/json",
                        response_schema=GeminiResponse
                    ),
                )

                if response:
                    self.logger.info("Gemini raw response: %s",
                                     response.text)

                    if not response.text:
                        candidate: genai.types.Candidate = getattr(
                            response, "candidates", [])[0]

                        self.logger.error(
                            "Gemini no text: %s", candidate.finish_reason)

                        raise ValueError("Empty response")

                    transformed_data = json.loads(response.text)

                    return ProductOutput(**transformed_data)
                else:
                    raise ValueError("No response")

        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse response as JSON")

            raise ValueError(
                f"Failed to parse Gemini response as JSON: {e}") from e
        except errors.APIError as e:
            self.logger.error(
                "Gemini API error during content generation: %s", e)

            self._manage_gemini_api_errors(e)

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

    def _manage_gemini_api_errors(self, error: errors.APIError) -> None:
        if error.code == 429:
            raise ValueError("Rate limit exceeded")
        elif error.code == 503:
            raise ValueError(error.message)

        raise Exception(f"Gemini API error: {error}") from error
