import cv2
import numpy as np
from typing import Tuple
import logging
import time

# Initialize logger
logger = logging.getLogger(__name__)

def enhance_book_cover(image_np: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    Enhance a book cover image for better readability by Gemini.
    No OCR processing - just image enhancement.
    
    Args:
        image_np: Input image as numpy array
        
    Returns:
        Tuple containing:
        - Enhanced image as numpy array
        - Boolean indicating if the image appears to be a valid book cover
    """
    start_time = time.time()
    
    try:
        # Quick validation
        if image_np is None or image_np.size == 0:
            logger.warning("Invalid image input")
            return image_np, False
            
        # Check if image has reasonable dimensions
        height, width = image_np.shape[:2]
        if height < 200 or width < 200:
            logger.warning(f"Image too small: {width}x{height}")
            return image_np, False
        
        # Make a copy to avoid modifying original
        img_copy = image_np.copy()
        
        # Check for extremely blurry images using Laplacian variance
        gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 10:  # Threshold for blurriness
            logger.warning(f"Image too blurry: {laplacian_var}")
            return image_np, False

        # FAST TRACK - Only essential enhancements for speed
        
        # 1. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)
        
        # 2. Simple color adjustment for the original color image
        # Split the image into color channels
        b, g, r = cv2.split(img_copy)
        
        # Apply CLAHE to each channel
        b_enhanced = clahe.apply(b)
        g_enhanced = clahe.apply(g)
        r_enhanced = clahe.apply(r)
        
        # Merge the enhanced channels
        enhanced_color = cv2.merge([b_enhanced, g_enhanced, r_enhanced])
        
        # 3. Apply sharpening for text clarity
        kernel = np.array([[0, -1, 0],
                          [-1, 5, -1],
                          [0, -1, 0]])
        sharpened = cv2.filter2D(enhanced_color, -1, kernel)
        
        processing_time = time.time() - start_time
        logger.info(f"Image enhancement completed in {processing_time:.2f}s")
        
        return sharpened, True

    except Exception as e:
        logger.error(f"Error during image enhancement: {str(e)}", exc_info=True)
        return image_np, False