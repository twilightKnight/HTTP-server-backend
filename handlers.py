from http.server import BaseHTTPRequestHandler
from services import handle_request


class CityByIdHandler(BaseHTTPRequestHandler):
    """Request handler class serving all get requests for the task"""

    def do_GET(self):
        response, error = handle_request(self.path)
        if error is not None:
            self.send_response(error['Code'], error['Description'])
            self.end_headers()
        else:
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(response).encode('UTF-8'))
