"""Product data models for transformation requests and responses."""

from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    """Input model for complex/technical product data."""

    title: str = Field(
        ...,
        description="Technical or complex product title",
        min_length=1,
        max_length=500,
    )
    description: str = Field(
        ...,
        description="Technical or complex product description with specifications",
        min_length=1,
        max_length=5000,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Advanced Whey Protein Isolate Formula",
                    "description": "Our proprietary WPI blend features 25g of rapidly absorbed complete amino acid profile with enhanced bioavailability through CFM and ultra-filtration processes...",
                }
            ]
        }
    }


class ProductOutput(BaseModel):
    """Output model for consumer-friendly, marketing-optimized product data."""

    title: str = Field(
        ...,
        description="Consumer-friendly, engaging product title",
        min_length=1,
        max_length=500,
    )
    description: str = Field(
        ...,
        description="Marketing-optimized, benefit-focused product description",
        min_length=1,
        max_length=5000,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Premium Protein Shake for Faster Recovery",
                    "description": "Fuel your fitness goals with our smooth, delicious protein shake that delivers 25g of high-quality protein per serving...",
                }
            ]
        }
    }


class TransformRequest(BaseModel):
    """Request model for product transformation endpoint."""

    product: ProductInput = Field(..., description="Product data to transform")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product": {
                        "title": "Advanced Whey Protein Isolate Formula",
                        "description": "Our proprietary WPI blend features 25g of rapidly absorbed complete amino acid profile...",
                    }
                }
            ]
        }
    }


class TransformResponse(BaseModel):
    """Response model for product transformation endpoint."""

    success: bool = Field(..., description="Whether transformation was successful")
    original: ProductInput = Field(..., description="Original product data")
    transformed: ProductOutput | None = Field(
        None, description="Transformed product data (None if failed)"
    )
    error: str | None = Field(None, description="Error message if transformation failed")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "original": {
                        "title": "Advanced Whey Protein Isolate Formula",
                        "description": "Technical description...",
                    },
                    "transformed": {
                        "title": "Premium Protein Shake for Faster Recovery",
                        "description": "Marketing description...",
                    },
                    "error": None,
                }
            ]
        }
    }
