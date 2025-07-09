from fastapi import APIRouter, UploadFile, File, HTTPException, Response, status
from fastapi.responses import JSONResponse
from ..Services.ocr_service import enhance_book_cover
from ..Services.gemini_service import extract_book_details
import numpy as np
import cv2
from typing import Dict, Any
import logging
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("book_router")

router = APIRouter()

@router.post("/scan")
async def scan_book(file: UploadFile = File(...), response: Response = None):
    """
    Endpoint to scan a book cover image and extract title and author information.
    Direct image processing approach without OCR for faster processing.
    
    Args:
        file: Uploaded image file of a book cover
        
    Returns:
        JSON response containing extracted book details or appropriate error
    """
    start_time = time.time()
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        logger.warning(f"Invalid file type: {file.content_type}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": "Uploaded file is not an image",
                "details": f"Got content type: {file.content_type}"
            }
        )
    
    try:
        # Read the uploaded image file as bytes
        file_bytes = await file.read()
        
        if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={
                    "success": False,
                    "error": "Image file too large",
                    "details": "Maximum allowed size is 10MB"
                }
            )

        # Convert bytes to NumPy array and decode image
        np_arr = np.frombuffer(file_bytes, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if image_np is None or image_np.size == 0:
            logger.warning("Failed to decode image")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "error": "Failed to decode image",
                    "details": "The image data could not be processed"
                }
            )

        # Enhance the image (no OCR)
        enhanced_image, is_valid_book_cover = enhance_book_cover(image_np)
        
        if not is_valid_book_cover:
            logger.info("Image not recognized as a valid book cover")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "success": False,
                    "error": "Not a valid book cover",
                    "details": "The image does not appear to be a book cover or is too blurry"
                }
            )

        # Extract book title & author using Gemini directly from enhanced image
        result = await extract_book_details(enhanced_image)
        
        # Check for errors in the result
        if "error" in result and result["title"] == "Unknown" and result["author"] == "Unknown":
            logger.warning(f"Gemini processing error: {result.get('error')}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "success": False,
                    "error": "Failed to extract book details",
                    "details": result.get("error", "Unknown error in AI processing")
                }
            )

        # Add total processing time information
        total_time = time.time() - start_time
        result["total_processing_time_ms"] = round(total_time * 1000)
        
        # Return success response
        return {
            "success": True, 
            "data": result
        }

    except Exception as e:
        logger.error(f"Error processing book cover: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "Server error while processing the image",
                "details": str(e)
            }
        )