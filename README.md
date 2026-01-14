# DuckDuckGo Proxy API

基于 FastAPI 和 DuckDuckGo 搜索库的代理 API，支持网页、新闻、图片、视频等多种搜索。

## 快速部署

点击下方按钮一键部署到 Vercel：

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/YOUR_USERNAME/duckduckgo-proxy-api-vercel)

**环境变量配置：**
- `SECRET_KEY`：API 授权密钥（必需）
- `SAFESEARCH`：搜索安全级别，默认 `moderate`（可选）

部署后在 Vercel 项目设置中添加环境变量，或使用命令：
```bash
vercel env add SECRET_KEY
```

## API 端点

所有端点需要在请求头中携带：`Authorization: Bearer YOUR_SECRET_KEY`

- `GET /api/health` - 健康检查
- `POST /api/search` - 网页搜索
- `POST /api/searchNews` - 新闻搜索
- `POST /api/searchImages` - 图片搜索
- `POST /api/searchVideos` - 视频搜索
- `POST /api/searchAnswers` - 答案搜索

**请求参数：**
```json
{
  "q": "搜索关键词",
  "max_results": 10
}
```

## 使用示例

```bash
curl -X POST "https://your-app.vercel.app/api/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_secret_key" \
  -d '{"q": "Python", "max_results": 5}'
```

## 本地开发

```bash
git clone https://github.com/YOUR_USERNAME/duckduckgo-proxy-api-vercel.git
cd duckduckgo-proxy-api-vercel
pip install -r requirements.txt

# 创建 .env 文件并配置 SECRET_KEY
uvicorn api.index:app --reload --port 8000
```

## License

MIT
