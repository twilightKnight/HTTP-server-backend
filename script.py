from http.server import HTTPServer, BaseHTTPRequestHandler
from handlers import CityByIdHandler
from services import parse_file, parse_timezones
from settings import TIMEZONES_FILE, FILE_NAME, IP, PORT


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """Runs server with Base build-in handler"""

    server_address = (IP, PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
    """Module main function"""

    try:
        parse_file(FILE_NAME)
        parse_timezones(TIMEZONES_FILE)
    except FileNotFoundError:
        print('File not found.')
    else:
        print('Files successfully parsed.')
        print(f'Server hosted on {IP}:{PORT}')
        run(handler_class=CityByIdHandler)


if __name__ == '__main__':
    main()


