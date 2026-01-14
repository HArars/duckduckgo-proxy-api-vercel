import os
from ddgs import DDGS
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="DuckDuckGo Search API", version="2.0.0")

# 添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从环境变量获取配置
SECRET_KEY = os.getenv('SECRET_KEY')
SAFESEARCH = os.getenv('SAFESEARCH', 'moderate')

# 启动时验证
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

print('✅ Environment variables loaded:')
print(f'   - SECRET_KEY: {SECRET_KEY[:4]}****')
print(f'   - SAFESEARCH: {SAFESEARCH}')

# 中间件:请求日志
@app.middleware("http")
async def log_requests(request: Request, call_next):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# 授权检查函数
def check_authorization(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header != f'Bearer {SECRET_KEY}':
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return True

# 解析请求体
async def parse_request_body(request: Request):
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    
    keywords = data.get('q', '')
    max_results = int(data.get('max_results', 10))
    
    if not keywords:
        raise HTTPException(status_code=400, detail="Missing required parameter: q")
    
    if max_results < 1 or max_results > 100:
        raise HTTPException(status_code=400, detail="max_results must be between 1 and 100")
    
    return keywords, max_results

# 通用搜索处理函数
async def handle_search(request: Request, search_type: str, search_func):
    """通用搜索处理逻辑"""
    check_authorization(request)
    keywords, max_results = await parse_request_body(request)
    
    print(f'>> {search_type} search for: {keywords}')
    
    try:
        with DDGS() as ddgs:
            results = list(search_func(ddgs, keywords, max_results))
            return JSONResponse(content={'results': results})
    except Exception as e:
        print(f'❌ {search_type} search error: {str(e)}')
        raise HTTPException(status_code=500, detail=f"{search_type} search failed: {str(e)}")

# 健康检查端点
@app.get('/health')
@app.get('/api/health')
async def health_check():
    """健康检查端点"""
    return JSONResponse(content={
        'status': 'ok',
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'version': '2.0.0',
        'library': 'ddgs',
        'safesearch': SAFESEARCH
    })

# 网页搜索端点
@app.post('/search')
@app.post('/api/search')
async def search(request: Request):
    """网页搜索"""
    return await handle_search(
        request, 
        'Web',
        lambda ddgs, kw, max_r: ddgs.text(kw, safesearch=SAFESEARCH, max_results=max_r)
    )

# 新闻搜索端点
@app.post('/searchNews')
@app.post('/api/searchNews')
async def search_news(request: Request):
    """新闻搜索"""
    return await handle_search(
        request,
        'News',
        lambda ddgs, kw, max_r: ddgs.news(kw, safesearch=SAFESEARCH, max_results=max_r)
    )

# 答案搜索端点
@app.post('/searchAnswers')
@app.post('/api/searchAnswers')
async def search_answers(request: Request):
    """答案搜索（返回第一条搜索结果）"""
    check_authorization(request)
    keywords, _ = await parse_request_body(request)
    
    print(f'>> Answers search for: {keywords}')
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(keywords, safesearch=SAFESEARCH, max_results=1))
            answer = results[0] if results else None
            return JSONResponse(content={'results': answer})
    except Exception as e:
        print(f'❌ Answers search error: {str(e)}')
        raise HTTPException(status_code=500, detail=f"Answers search failed: {str(e)}")

# 图片搜索端点
@app.post('/searchImages')
@app.post('/api/searchImages')
async def search_images(request: Request):
    """图片搜索"""
    return await handle_search(
        request,
        'Image',
        lambda ddgs, kw, max_r: ddgs.images(kw, safesearch=SAFESEARCH, max_results=max_r)
    )

# 视频搜索端点
@app.post('/searchVideos')
@app.post('/api/searchVideos')
async def search_videos(request: Request):
    """视频搜索"""
    return await handle_search(
        request,
        'Video',
        lambda ddgs, kw, max_r: ddgs.videos(kw, safesearch=SAFESEARCH, max_results=max_r)
    )

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f'❌ Unhandled error: {str(exc)}')
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    )
