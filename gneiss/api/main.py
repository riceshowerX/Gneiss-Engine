"""
FastAPI application for Gneiss Engine with modern features.
"""

from contextlib import asynccontextmanager
from typing import Dict, List, Optional

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from prometheus_client import make_asgi_app

from gneiss.core import Image
from gneiss.ai import AIImageProcessor
from gneiss.utils.monitoring import setup_metrics, setup_tracing


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("Starting Gneiss Engine API")
    
    # Initialize AI processor with GPU support
    device = "cuda" if torch.cuda.is_available() else "cpu"
    app.state.ai_processor = AIImageProcessor(device=device)
    logger.info(f"AI Processor initialized on {device}")
    
    # Warm up models
    await app.state.ai_processor.warmup()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Gneiss Engine API")
    if hasattr(app.state, "ai_processor"):
        await app.state.ai_processor.cleanup()


app = FastAPI(
    title="Gneiss Engine API",
    description="Modern image processing engine with AI capabilities",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Setup monitoring
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
setup_metrics(app)
setup_tracing(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}


@app.get("/health")
async def health_check():
    """Comprehensive health check."""
    return {
        "status": "healthy",
        "gpu_available": torch.cuda.is_available(),
        "models_loaded": hasattr(app.state, "ai_processor"),
    }


@app.post("/process/batch")
async def process_batch_images(
    files: List[UploadFile],
    operation: str,
    parameters: Optional[Dict] = None,
):
    """Process multiple images with specified operation."""
    try:
        results = []
        
        for file in files:
            # Process each file asynchronously
            image = await Image.load_async(await file.read())
            
            if operation == "enhance_ai":
                enhanced = await app.state.ai_processor.enhance(image)
                results.append(enhanced.to_dict())
            elif operation == "style_transfer":
                styled = await app.state.ai_processor.style_transfer(
                    image, style=parameters.get("style")
                )
                results.append(styled.to_dict())
            else:
                # Fallback to traditional operations
                processed = await process_traditional(image, operation, parameters)
                results.append(processed.to_dict())
        
        return JSONResponse(content={"results": results})
    
    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process/ai/generate")
async def generate_image(
    prompt: str,
    style: Optional[str] = None,
    size: str = "512x512",
):
    """Generate image using AI models."""
    try:
        generator = app.state.ai_processor
        image = await generator.generate_from_prompt(prompt, style=style, size=size)
        
        return {
            "image_url": await image.upload_to_cloud(),
            "metadata": image.get_metadata(),
        }
    
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_traditional(image: Image, operation: str, parameters: Dict) -> Image:
    """Process image using traditional methods."""
    # Implementation for traditional operations
    if operation == "resize":
        return image.resize(**parameters)
    elif operation == "crop":
        return image.crop(**parameters)
    # Add more operations as needed
    
    return image


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)