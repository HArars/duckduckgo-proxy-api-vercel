import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Security, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from duckduckgo_search import DDGS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="DuckDuckGo Proxy API",
    description="A proxy API for DuckDuckGo search supporting web, news, images, and videos",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "")
SAFESEARCH = os.getenv("SAFESEARCH", "moderate")


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """Verify Bearer token authentication"""
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY not configured")
    
    if credentials.credentials != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    return True


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "DuckDuckGo Proxy API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search?q=query&max_results=10",
            "news": "/news?q=query&max_results=10",
            "images": "/images?q=query&max_results=10",
            "videos": "/videos?q=query&max_results=10"
        },
        "authentication": "Bearer token required (use SECRET_KEY in Authorization header)"
    }


@app.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """
    Web search endpoint
    
    - **q**: Search query (required)
    - **max_results**: Maximum number of results (1-50, default: 10)
    """
    verify_token(credentials)
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                keywords=q,
                safesearch=SAFESEARCH,
                max_results=max_results
            ))
        
        return {
            "success": True,
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/news")
async def news(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """
    News search endpoint
    
    - **q**: Search query (required)
    - **max_results**: Maximum number of results (1-50, default: 10)
    """
    verify_token(credentials)
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(
                keywords=q,
                safesearch=SAFESEARCH,
                max_results=max_results
            ))
        
        return {
            "success": True,
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News search failed: {str(e)}")


@app.get("/images")
async def images(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """
    Image search endpoint
    
    - **q**: Search query (required)
    - **max_results**: Maximum number of results (1-50, default: 10)
    """
    verify_token(credentials)
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(
                keywords=q,
                safesearch=SAFESEARCH,
                max_results=max_results
            ))
        
        return {
            "success": True,
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image search failed: {str(e)}")


@app.get("/videos")
async def videos(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Dict[str, Any]:
    """
    Video search endpoint
    
    - **q**: Search query (required)
    - **max_results**: Maximum number of results (1-50, default: 10)
    """
    verify_token(credentials)
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.videos(
                keywords=q,
                safesearch=SAFESEARCH,
                max_results=max_results
            ))
        
        return {
            "success": True,
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video search failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
