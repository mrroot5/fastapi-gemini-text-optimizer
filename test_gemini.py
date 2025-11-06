"""Simple test script to verify Gemini integration works."""

import asyncio
import json

from app.config import settings
from app.schemas.product import ProductInput
from app.services.gemini_service import gemini_service


async def test_transformation() -> None:
    """Test the Gemini product transformation."""
    print("=" * 80)
    print("Testing Gemini AI Product Transformation")
    print("=" * 80)

    # Load sample complex data
    with open("app/data/sample-complex-data.json", encoding="utf-8") as f:
        sample_data = json.load(f)

    product = ProductInput(**sample_data)

    print("\n📥 INPUT (Complex/Technical):")
    print(f"Title: {product.title}")
    print(f"Description: {product.description[:100]}...")

    print("\n🤖 Transforming with Gemini AI...")
    print(f"Model: {settings.gemini_model}")
    print(f"Temperature: {settings.gemini_temperature}")

    try:
        # TODO Avoid using the realmodel, mock it
        transformed = await gemini_service.transform_product_description(product)

        print("\n✅ TRANSFORMATION SUCCESSFUL!")
        print("\n📤 OUTPUT (Marketing-Optimized):")
        print(f"Title: {transformed.title}")
        print(f"Description: {transformed.description}")

        print("\n" + "=" * 80)
        print("✨ Test completed successfully!")
        print("=" * 80)

    except ValueError as e:
        print(f"\n❌ Configuration/Parsing Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_transformation())