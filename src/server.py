import pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

BASE_DIR = pathlib.Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR.parent / "pages"
ROUTES = {
    "/": "index.html",
    "/catalog": "catalog.html",
    "/category": "category.html",
    "/contacts": "contacts.html",
}


def read_html(name: str) -> bytes:
    return (PAGES_DIR / name).read_bytes()


class Handler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов: возвращает HTML-страницы и принимает POST-данные."""

    def _send_html(self, data: bytes, status=200):
        """Отправка HTML-страницы с заданным статусом."""
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        """Обработка GET-запроса: возвращает HTML-страницу на основе маршрута."""
        path = self.path.split("?", 1)[0]
        file_name = ROUTES.get(path, "contacts.html")
        self._send_html(read_html(file_name))

    def do_POST(self):
        """Обработка POST-запроса: выводит данные формы в консоль и редиректит на /contacts."""
        ln = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(ln).decode()
        print("[POST]", parse_qs(body, keep_blank_values=True))
        self.send_response(302)
        self.send_header("Location", "/contacts")
        self.end_headers()


if __name__ == "__main__":
    print("📡  http://127.0.0.1:8000")
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
