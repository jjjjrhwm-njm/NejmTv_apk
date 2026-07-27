import os
import aiohttp
from aiohttp import web

# قراءة المتغيرات من بيئة Render
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # توكن Bot B

# السيرفر يعمل على المنفذ 8080 (Render يتوقع هذا)
PORT = int(os.getenv("PORT", 8080))

async def handle_get_file(request):
    """
    هذا الـ endpoint يقلد api.telegram.org
    لكنه يعالج الملفات الكبيرة
    """
    try:
        data = await request.json()
        file_id = data.get("file_id")
        
        if not file_id:
            return web.json_response({"ok": False, "error": "missing file_id"}, status=400)

        # الاتصال بـ Telegram API مباشرة
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                result = await resp.json()
                
                if not result.get("ok"):
                    return web.json_response(result, status=400)
                
                # إرجاع النتيجة كما هي (بدون تخزين محلي)
                return web.json_response(result)
                
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)}, status=500)

async def handle_health(request):
    # لإبقاء السيرفر حيًا (Uptime)
    return web.json_response({"status": "ok"})

def main():
    app = web.Application()
    app.router.add_post("/bot{token}/getFile", handle_get_file)
    app.router.add_get("/health", handle_health)
    
    # يمكنك إضافة endpoint إضافي للاختبار
    app.router.add_get("/", lambda r: web.json_response({"message": "Nejm TV Bot API is running"}))
    
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
