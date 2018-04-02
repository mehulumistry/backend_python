import simplejson as simplejson
import tornado
from sqlalchemy import create_engine
from tornado import web
from tornado.ioloop import IOLoop

from python_backend.setting import *

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_recycle=3600)
conn = engine.connect()


class BaseHandler(tornado.web.RequestHandler):
     def set_default_headers(self):
          self.set_header("Access-Control-Allow-Origin", "*")
          self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST")
          self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By,If-Modified-Since, X-File-Name,Cache-Control")


class queryHandler(BaseHandler):

    @web.asynchronous
    def get(self, *args):
        snapshotOrderBook()




class displayOrderBook(BaseHandler):

    @web.asynchronous
    def get(self, *args):


        conn = engine.connect()


        rows_ask = conn.execute("SELECT * FROM orderBooks where type = 'ask' ORDER BY id DESC LIMIT 30 ")
        rows_bid = conn.execute("SELECT * FROM orderBooks where type = 'bid' ORDER BY id DESC LIMIT 30 ")



        asks_as_dict = []

        for ask in rows_bid:
            ask_as_dict = {
                'type': 'bid',
                'price': ask.price,
                'amount': ask.amount,
                'count': ask.count,
                'exchange': ask.exchange,
                'pairname': ask.pairname

            }
            asks_as_dict.append(ask_as_dict)

        bids_as_dict = []

        for bid in rows_ask:
            bid_as_dict = {
                'type': 'ask',
                'price': bid.price,
                'amount': bid.amount,
                'count': bid.count,
                'exchange': bid.exchange,
                'pairname': bid.pairname

            }
            bids_as_dict.append(bid_as_dict)


        snapshot_orderbook = []
        snapshot_orderbook.append(asks_as_dict)
        snapshot_orderbook.append(bids_as_dict)


        self.write(simplejson.dumps(snapshot_orderbook))
        self.flush()
        self.finish()
        conn.close()

class snapshotOrderBook(BaseHandler):

    @web.asynchronous
    def get(self, *args):
        price = "0"
        try:
            price = self.get_argument("price")
        except:
            print("No price value")

        try:
            exchange = self.get_argument("exchange")
        except:
            print("No exchange value")

        try:
            pairname = self.get_argument("pairname")
        except:
            print("No pairname value")


        print(price + " " + exchange + " " + pairname)

        # SELECT * FROM table WHERE column LIKE "%" use wildcard at client side when seleting every values

        rows_ask = conn.execute("SELECT * FROM orderBooks WHERE type = 'ask' AND price > "+price+" AND exchange = '"+exchange+"' AND pairname = '"+pairname+"' ORDER BY id DESC LIMIT 30 ")
        rows_bid = conn.execute("SELECT * FROM orderBooks WHERE type = 'bid' AND price > "+price+" AND exchange = '"+exchange+"' AND pairname = '"+pairname+"' ORDER BY id DESC LIMIT 30 ")

        asks_as_dict = []

        for ask in rows_bid:
            ask_as_dict = {
                'type': 'bid',
                'price': ask.price,
                'amount': ask.amount,
                'count': ask.count,
                'exchange': ask.exchange,
                'pairname': ask.pairname

            }
            asks_as_dict.append(ask_as_dict)

        bids_as_dict = []

        for bid in rows_ask:
            bid_as_dict = {
                'type': 'ask',
                'price': bid.price,
                'amount': bid.amount,
                'count': bid.count,
                'exchange': bid.exchange,
                'pairname': bid.pairname

            }
            bids_as_dict.append(bid_as_dict)

        snapshot_orderbook = []
        snapshot_orderbook.append(asks_as_dict)
        snapshot_orderbook.append(bids_as_dict)

        self.write(simplejson.dumps(snapshot_orderbook))
        self.flush()
        self.finish()
        conn.close()

app = web.Application([
    (r'/noble-markets-realtime-order-book', displayOrderBook),
    (r'/noble-markets-order-book-snapshot', snapshotOrderBook),
    (r'/', queryHandler),
])

if __name__ == '__main__':
    app.listen(9505)
    IOLoop.instance().start()
