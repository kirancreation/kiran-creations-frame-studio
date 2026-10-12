#!/usr/bin/env python3
'Local Wi-Fi photo upload server for Kiran Creations Frame Studio Pro.'
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from email.parser import BytesParser
from email.policy import default
import json, socket, mimetypes, urllib.parse, uuid, os, io
import qrcode
from qrcode.image.svg import SvgPathImage

ROOT = Path(__file__).resolve().parent
UPLOADS = ROOT / "uploads"
UPLOADS.mkdir(exist_ok=True)
PORT = 8000
ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".heic", ".avif"}

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80)); return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally: s.close()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, fmt, *args):
        print("[server] " + (fmt % args))
    def send_bytes(self, status, body, content_type="text/html; charset=utf-8"):
        self.send_response(status); self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        path=urllib.parse.urlparse(self.path).path
        if path == "/mobile":
            done = "?done=1" in self.path
            msg = '<p class="ok">Upload complete! You can choose more photos.</p>' if done else ''
            page = f'''<!doctype html><html lang="bn"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kiran Creations — Photo Upload</title><style>body{{font:16px Arial,sans-serif;background:#f3f5fa;margin:0;padding:20px;color:#20243a}}main{{max-width:480px;margin:20px auto;background:white;padding:22px;border-radius:16px;box-shadow:0 5px 25px #0001}}h1{{font-size:22px}}input,button{{width:100%;margin:12px 0;padding:13px;box-sizing:border-box}}button{{background:#6544df;color:white;border:0;border-radius:9px;font-weight:bold}}.ok{{background:#e2f7ed;padding:12px;border-radius:8px}}small{{color:#697187;line-height:1.5}}</style><main><h1>📷 Kiran Creations Photo Upload</h1><p>আপনার মোবাইল থেকে একসঙ্গে একাধিক ছবি বেছে আপলোড করুন। আপলোড শেষ হলে ছবি কম্পিউটারের Photo Gallery-তে দেখা যাবে।</p>{msg}<form method="post" action="/upload" enctype="multipart/form-data"><input type="file" name="photos" accept="image/*" multiple required><button type="submit">ছবি আপলোড করুন</button></form><small>নোট: মোবাইল ও কম্পিউটার একই Wi-Fi নেটওয়ার্কে থাকতে হবে। শুধু ছবির ফাইল গ্রহণ করা হয়।</small></main></html>'''
            return self.send_bytes(200,page.encode())
        if path == "/api/info":
            body=json.dumps({"phone_url":f"http://{lan_ip()}:{PORT}/mobile"}).encode()
            return self.send_bytes(200,body,"application/json; charset=utf-8")
        if path == "/api/qr":
            # Generate a real QR locally for this computer's current Wi-Fi upload URL.
            url=f"http://{lan_ip()}:{PORT}/mobile"
            qr=qrcode.QRCode(box_size=8,border=3,error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(url); qr.make(fit=True)
            image=qr.make_image(image_factory=SvgPathImage)
            buf=io.BytesIO(); image.save(buf)
            return self.send_bytes(200,buf.getvalue(),"image/svg+xml; charset=utf-8")
        if path == "/api/uploads":
            items=[]
            for p in sorted(UPLOADS.iterdir(),key=lambda x:x.stat().st_mtime):
                if p.is_file() and p.suffix.lower() in ALLOWED:
                    items.append({"name":p.name,"url":"/uploads/"+urllib.parse.quote(p.name)})
            return self.send_bytes(200,json.dumps(items).encode(),"application/json; charset=utf-8")
        return super().do_GET()
    def do_POST(self):
        if urllib.parse.urlparse(self.path).path != "/upload":
            return self.send_bytes(404,b"Not found")
        try:
            length=int(self.headers.get("Content-Length","0"))
            if length<=0 or length>300*1024*1024: return self.send_bytes(413,b"Upload too large or empty")
            content_type=self.headers.get("Content-Type","")
            raw=(f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n").encode()+self.rfile.read(length)
            msg=BytesParser(policy=default).parsebytes(raw)
            saved=0
            for part in msg.iter_parts() if msg.is_multipart() else []:
                filename=part.get_filename()
                if not filename: continue
                ext=Path(filename).suffix.lower()
                data=part.get_payload(decode=True) or b""
                ctype=part.get_content_type()
                if ext not in ALLOWED or not ctype.startswith("image/") or not data: continue
                safe=Path(filename).name.replace("\\","_").replace("/","_")
                target=UPLOADS/(uuid.uuid4().hex[:8]+"_"+safe)
                target.write_bytes(data); saved+=1
            if saved:
                self.send_response(303);self.send_header("Location","/mobile?done=1");self.send_header("Content-Length","0");self.end_headers()
            else: self.send_bytes(400,b"No valid image files received")
        except Exception as exc:
            print("Upload error:",exc);self.send_bytes(500,b"Upload failed")

if __name__ == "__main__":
    ip=lan_ip()
    print("\nKiran Creations Frame Studio Pro is running.")
    print(f"On this computer: http://127.0.0.1:{PORT}")
    print(f"On your phone (same Wi-Fi): http://{ip}:{PORT}/mobile")
    print("Keep this window open while using mobile upload. Press Ctrl+C to stop.\n")
    try: ThreadingHTTPServer(("0.0.0.0",PORT),Handler).serve_forever()
    except KeyboardInterrupt: print("\nServer stopped.")
