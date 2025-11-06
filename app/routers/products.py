"""Product transformation endpoints using Gemini AI."""

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_token_header
from app.schemas.product import ProductInput, TransformRequest, TransformResponse
from app.services.gemini_service import gemini_service

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/transform",
    response_model=TransformResponse,
    status_code=status.HTTP_200_OK,
    summary="Transform product data using Gemini AI",
    description="Converts technical/complex product information into consumer-friendly marketing copy using Google Gemini AI.",
)
async def transform_product(request: TransformRequest) -> TransformResponse:
    """
    Transform technical product data into engaging marketing copy.

    This endpoint takes complex product information (technical specs, jargon)
    and uses Gemini AI to transform it into consumer-friendly, benefit-focused
    marketing content that's easier to understand and more persuasive.

    Args:
        request: TransformRequest containing the product data to transform

    Returns:
        TransformResponse with original and transformed product data

    Raises:
        HTTPException: If transformation fails
    """
    try:
        # Transform the product using Gemini service
        transformed = await gemini_service.transform_product_description(request.product)

        print("transformed")
        print(transformed)

        return TransformResponse(
            success=True,
            original=request.product,
            transformed=transformed,
            error=None,
        )

    except ValueError as e:
        # Configuration or parsing errors
        return TransformResponse(
            success=False,
            original=request.product,
            transformed=None,
            error=f"Transformation error: {str(e)}",
        )

    except Exception as e:
        # Other unexpected errors
        return TransformResponse(
            success=False,
            original=request.product,
            transformed=None,
            error=f"Unexpected error: {str(e)}",
        )


@router.get(
    "/sample/complex",
    response_model=ProductInput,
    status_code=status.HTTP_200_OK,
    summary="Get sample complex product data",
    description="Returns sample complex/technical product data from JSON file for testing.",
)
async def get_sample_complex() -> ProductInput:
    """
    Load and return sample complex product data.

    Returns sample technical product data that can be used to test
    the transformation endpoint.

    Returns:
        ProductInput with complex/technical product data

    Raises:
        HTTPException: If sample file cannot be loaded
    """
    try:
        data_path = Path(__file__).parent.parent / "data" / "sample-complex-data.json"

        with open(data_path, encoding="utf-8") as f:
            data = json.load(f)

        return ProductInput(**data)

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sample data file not found",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading sample data: {str(e)}",
        ) from e


@router.get(
    "/sample/optimized",
    response_model=ProductInput,
    status_code=status.HTTP_200_OK,
    summary="Get sample optimized product data",
    description="Returns sample optimized/marketing product data from JSON file (example output).",
)
async def get_sample_optimized() -> ProductInput:
    """
    Load and return sample optimized product data.

    Returns sample marketing-optimized product data as an example
    of what the transformation endpoint should produce.

    Returns:
        ProductInput with optimized/marketing product data

    Raises:
        HTTPException: If sample file cannot be loaded
    """
    try:
        data_path = Path(__file__).parent.parent / "data" / "sample-optimized-data.json"

        with open(data_path, encoding="utf-8") as f:
            data = json.load(f)

        return ProductInput(**data)

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sample data file not found",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading sample data: {str(e)}",
        ) from e
