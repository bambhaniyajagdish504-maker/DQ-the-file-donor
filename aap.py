from aiohttp import web
import asyncio

async def health(request):
    return web.Response(text="OK")

def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)

    async def start():
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8000)
        await site.start()

    loop = asyncio.get_event_loop()
    loop.create_task(start())