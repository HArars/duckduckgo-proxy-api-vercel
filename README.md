# DuckDuckGo Proxy API

A DuckDuckGo proxy API built with FastAPI, supporting web search, news, images, and videos. One-click deploy to Vercel with Bearer token authentication.

## Features

- 🔍 **Web Search** - Search the web using DuckDuckGo
- 📰 **News Search** - Find news articles
- 🖼️ **Image Search** - Search for images
- 🎥 **Video Search** - Find videos
- 🔒 **Bearer Token Authentication** - Secure your API with token-based auth
- 🌐 **CORS Support** - Cross-Origin Resource Sharing enabled
- ⚙️ **SafeSearch** - Configurable content filtering
- 🚀 **Vercel Ready** - One-click deployment to Vercel

## Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/HArars/duckduckgo-proxy-api-vercel)

After deployment, remember to set your environment variables in Vercel:
- `SECRET_KEY`: Your API authentication token
- `SAFESEARCH`: Content filtering level (`on`, `moderate`, or `off`)

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/HArars/duckduckgo-proxy-api-vercel.git
cd duckduckgo-proxy-api-vercel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Edit `.env` and set your `SECRET_KEY`:
```env
SECRET_KEY=your-secret-key-here
SAFESEARCH=moderate
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### Authentication

All endpoints (except root) require Bearer token authentication. Include your `SECRET_KEY` in the Authorization header:

```bash
Authorization: Bearer your-secret-key-here
```

### Endpoints

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "name": "DuckDuckGo Proxy API",
  "version": "1.0.0",
  "endpoints": {
    "search": "/search?q=query&max_results=10",
    "news": "/news?q=query&max_results=10",
    "images": "/images?q=query&max_results=10",
    "videos": "/videos?q=query&max_results=10"
  }
}
```

#### `GET /search`
Web search endpoint.

**Parameters:**
- `q` (required): Search query
- `max_results` (optional): Number of results (1-50, default: 10)

**Example:**
```bash
curl -H "Authorization: Bearer your-secret-key" \
  "http://localhost:8000/search?q=python&max_results=5"
```

**Response:**
```json
{
  "success": true,
  "query": "python",
  "results": [
    {
      "title": "Welcome to Python.org",
      "href": "https://www.python.org/",
      "body": "The official home of the Python Programming Language..."
    }
  ],
  "count": 5
}
```

#### `GET /news`
News search endpoint.

**Parameters:**
- `q` (required): Search query
- `max_results` (optional): Number of results (1-50, default: 10)

**Example:**
```bash
curl -H "Authorization: Bearer your-secret-key" \
  "http://localhost:8000/news?q=technology&max_results=5"
```

#### `GET /images`
Image search endpoint.

**Parameters:**
- `q` (required): Search query
- `max_results` (optional): Number of results (1-50, default: 10)

**Example:**
```bash
curl -H "Authorization: Bearer your-secret-key" \
  "http://localhost:8000/images?q=cats&max_results=5"
```

#### `GET /videos`
Video search endpoint.

**Parameters:**
- `q` (required): Search query
- `max_results` (optional): Number of results (1-50, default: 10)

**Example:**
```bash
curl -H "Authorization: Bearer your-secret-key" \
  "http://localhost:8000/videos?q=tutorial&max_results=5"
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Bearer token for API authentication | - | Yes |
| `SAFESEARCH` | SafeSearch level: `on`, `moderate`, or `off` | `moderate` | No |

## Deployment to Vercel

### Using Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables:
```bash
vercel env add SECRET_KEY
vercel env add SAFESEARCH
```

### Using Vercel Dashboard

1. Import your repository on Vercel
2. Add environment variables:
   - `SECRET_KEY`: Your API authentication token
   - `SAFESEARCH`: Content filtering level

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [duckduckgo-search](https://github.com/deedy5/duckduckgo_search) - DuckDuckGo search library
- [Uvicorn](https://www.uvicorn.org/) - ASGI server
- [Vercel](https://vercel.com/) - Serverless deployment platform

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This is an unofficial API and is not affiliated with DuckDuckGo. Use responsibly and in accordance with DuckDuckGo's terms of service.
