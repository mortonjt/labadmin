from os.path import dirname, join
from base64 import b64encode
from uuid import uuid4

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

from knimin import config
from knimin.handlers.base import MainHandler, NoPageHandler
from knimin.handlers.auth_handlers import AuthLoginHandler, AuthLogoutHandler
from knimin.handlers.ag_search import AGSearchHandler
from knimin.handlers.logged_in_index import LoggedInIndexHandler
from knimin.handlers.barcode_util import BarcodeUtilHandler
from knimin.handlers.ag_stats import AGStatsHandler
from knimin.handlers.ag_edit_participant import AGEditParticipantHandler
from knimin.handlers.ag_new_kit import AGNewKitHandler, AGNewKitDLHandler
from knimin.handlers.ag_edit_kit import AGEditKitHandler
from knimin.handlers.ag_new_barcode import (AGNewBarcodeHandler,
                                            AGBarcodePrintoutHandler,
                                            AGBarcodeAssignedHandler)
from knimin.handlers.ag_edit_barcode import AGEditBarcodeHandler
from knimin.handlers.ag_update_geocode import AGUpdateGeocodeHandler
from knimin.handlers.ag_pulldown import AGPulldownHandler, AGPulldownDLHandler
from knimin.handlers.ag_add_barcode_kit import AGAddBarcodeKitHandler
from knimin.handlers.ag_get_participant_names import (AGNamesHandler,
                                                      AGNamesDLHandler)
define("port", default=config.http_port, type=int)


DIRNAME = dirname(__file__)
STATIC_PATH = join(DIRNAME, "static")
TEMPLATE_PATH = join(DIRNAME, "templates")  # base folder for webpages
COOKIE_SECRET = b64encode(uuid4().bytes + uuid4().bytes)


class WebApplication(Application):
    def __init__(self):
        handlers = [
            (r"/results/(.*)", StaticFileHandler,
                {"path": '/tmp/'}),
            (r"/static/(.*)", StaticFileHandler, {"path": STATIC_PATH}),
            (r"/", MainHandler),
            (r"/auth/login/", AuthLoginHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r"/logged_in_index/", LoggedInIndexHandler),
            (r"/ag_search/", AGSearchHandler),
            (r"/barcode_util/", BarcodeUtilHandler),
            (r"/ag_add_barcode_kit/", AGAddBarcodeKitHandler),
            (r"/ag_stats/", AGStatsHandler),
            (r"/ag_edit_participant/", AGEditParticipantHandler),
            (r"/ag_new_kit/", AGNewKitHandler),
            (r"/ag_new_kit/download/", AGNewKitDLHandler),
            (r"/ag_edit_kit/", AGEditKitHandler),
            (r"/ag_new_barcode/", AGNewBarcodeHandler),
            (r"/ag_update_geocode/", AGUpdateGeocodeHandler),
            (r"/ag_edit_barcode/", AGEditBarcodeHandler),
            (r"/ag_pulldown/", AGPulldownHandler),
            (r"/ag_pulldown/download/", AGPulldownDLHandler),
            (r"/ag_participant_names/", AGNamesHandler),
            (r"/ag_participant_names/download/", AGNamesDLHandler),
            (r"/ag_new_barcode/download/", AGBarcodePrintoutHandler),
            (r"/ag_new_barcode/assigned/", AGBarcodeAssignedHandler),
            (r".*", NoPageHandler)
        ]
        settings = {
            "template_path": TEMPLATE_PATH,
            "debug": config.debug,
            "cookie_secret": COOKIE_SECRET,
            "login_url": "/login/",
        }
        super(WebApplication, self).__init__(handlers, **settings)


def main():
    parse_command_line()
    http_server = HTTPServer(WebApplication())
    http_server.listen(options.port)
    print("Tornado started on port %d" % options.port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
