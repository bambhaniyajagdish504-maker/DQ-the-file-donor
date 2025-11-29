from aiohttp import web

async def health(request):
    return web.Response(text="OK")

def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    web.run_app(app, port=8000)