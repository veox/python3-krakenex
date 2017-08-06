# This file is part of krakenex.
#
# krakenex is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# krakenex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser
# General Public LICENSE along with krakenex. If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt>.


"""Kraken.com cryptocurrency Exchange API."""


import json
import urllib.request
import urllib.parse
import urllib.error

# private query nonce
import time

# private query signing
import hashlib
import hmac
import base64

from . import connection
from . import response


class API(object):
    """ Maps a key/secret pair to a connection.

    Specifying either the pair or the connection is optional.

    .. note::
       If a connection is not set, a new one will be opened on
       first query. If a connection is set, during creation or as a result
       of a previous query, it will be reused for subsequent queries.
       However, its state is not checked.

    .. note::
       No timeout handling or query rate limiting is performed.

    .. note::
       If a private query is performed without setting a key/secret
       pair, the effects are undefined.

    """
    def __init__(self, key='', secret='', conn=None):
        """ Create an object with authentication information.

        :param key: key required to make queries to the API
        :type key: str
        :param secret: private key used to sign API messages
        :type secret: str
        :param conn: existing connection object to use
        :type conn: krakenex.Connection
        :returns: None

        """
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.conn = conn
        return

    def load_key(self, path):
        """ Load key and secret from file.

        Expected file format is key and secret on separate lines.

        :param path: path to keyfile
        :type path: str
        :returns: None

        """
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()
        return

    # DEPRECATE: just access directly, e.g. k.conn = krakenex.Connection()
    def set_connection(self, conn):
        """ Set an existing connection to be used as a default in queries.

        .. deprecated:: 1.0.0
           Access the object's :py:attr:`conn` attribute directly.

        :param conn: existing connection object to use
        :type conn: krakenex.Connection
        :returns: None

        """
        self.conn = conn
        return

    def _query(self, urlpath, req, conn=None, headers=None):
        """ Low-level query handling.

        If a connection object is provided, attempts to use that
        specific connection.

        If it is not provided, attempts to reuse a connection from the
        previous query.

        If this is the first ever query, opens a new connection, and
        keeps it as a fallback for future queries.

        Connection state is not checked.

        .. warning::
           The fallback connection will be re-used for both public and
           private queries.

        .. note::
           Preferably use :py:meth:`query_private` or
           :py:meth:`query_public` instead.

        :param urlpath: API URL path sans host
        :type urlpath: str
        :param req: API request parameters
        :type req: dict
        :param conn: (optional) existing connection object to use
        :type conn: krakenex.Connection
        :param headers: (optional) HTTPS headers
        :type headers: dict
        :returns: :py:func:`json.loads`-deserialised Python object

        """

        # TODO: monitor call rate

        url = self.uri + urlpath

        if conn is None:
            if self.conn is None:
                self.conn = connection.Connection()
            conn = self.conn

        if headers is None:
            headers = {}

        ret = conn._request(url, req, headers)
        return response.Response(json.loads(ret))

    def query_public(self, method, req=None, conn=None):
        """ API queries that do not require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object

        """
        urlpath = '/' + self.apiversion + '/public/' + method

        if req is None:
            req = {}

        return self._query(urlpath, req, conn)

    def query_private(self, method, req=None, conn=None):
        """ API queries that require a valid key/secret pair.

        :param method: API method name
        :type method: str
        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object

        """

        if req is None:
            req = {}

        # TODO: check if self.{key,secret} are set
        urlpath = '/' + self.apiversion + '/private/' + method

        req['nonce'] = int(1000 * time.time())
        postdata = urllib.parse.urlencode(req)

        # Unicode-objects must be encoded before hashing
        encoded = (str(req['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        headers = {
            'API-Key': self.key,
            'API-Sign': sigdigest.decode()
        }

        return self._query(urlpath, req, conn, headers)

    def get_server_time(self, req=None, conn=None):
        """Public API method.
        Get current server time

        Input:
            None
        Result:
            unixtime =  as unix timestamp
            rfc1123 = as RFC 1123 time format

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        t = self.query_public('Time', req=req, conn=conn)
        return t

    def get_asset_info(self, req=None, conn=None):
        """Public API method.
        Get an array of asset names and their info

        Input:
            info = info to retrieve (optional):
                info = all info (default)
            aclass = asset class (optional):
                currency (default)
            asset = comma delimited list of assets to get info on (optional.  default = all for given asset class)
        Result:
            <asset_name> = asset name
                altname = alternate name
                aclass = asset class
                decimals = scaling decimal places for record keeping
                display_decimals = scaling decimal places for output display

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        assets = self.query_public('Assets', req=req, conn=conn)
        return assets

    def get_asset_pair_info(self, req=None, conn=None):
        """Public API method.
        Get an array of asset pair names and their info

        Input:
            info = info to retrieve (optional):
                info = all info (default)
                leverage = leverage info
                fees = fees schedule
                margin = margin info
            pair = comma delimited list of asset pairs to get info on (optional.  default = all)
        Result:
            <pair_name> = pair name
                altname = alternate pair name
                aclass_base = asset class of base component
                base = asset id of base component
                aclass_quote = asset class of quote component
                quote = asset id of quote component
                lot = volume lot size
                pair_decimals = scaling decimal places for pair
                lot_decimals = scaling decimal places for volume
                lot_multiplier = amount to multiply lot volume by to get currency volume
                leverage_buy = array of leverage amounts available when buying
                leverage_sell = array of leverage amounts available when selling
                fees = fee schedule array in [volume, percent fee] tuples
                fees_maker = maker fee schedule array in [volume, percent fee] tuples (if on maker/taker)
                fee_volume_currency = volume discount currency
                margin_call = margin call level
                margin_stop = stop-out/liquidation margin level

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        asset_pairs = self.query_public('AssetPairs', req=req, conn=conn)
        return asset_pairs

    def get_ticker_info(self, req=None, conn=None):
        """Public API method.
        Get an array of pair names and their ticker info

        Input:
            pair = comma delimited list of asset pairs to get info on
        Result:
            <pair_name> = pair name
                a = ask array(<price>, <whole lot volume>, <lot volume>),
                b = bid array(<price>, <whole lot volume>, <lot volume>),
                c = last trade closed array(<price>, <lot volume>),
                v = volume array(<today>, <last 24 hours>),
                p = volume weighted average price array(<today>, <last 24 hours>),
                t = number of trades array(<today>, <last 24 hours>),
                l = low array(<today>, <last 24 hours>),
                h = high array(<today>, <last 24 hours>),
    o = today's opening price

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        info = self.query_public('Ticker', req=req, conn=conn)
        return info

    def get_ohlc_data(self, req=None, conn=None):
        """Public API method.
        Get an array of pair name and OHLC data

        Input:
            pair = asset pair to get OHLC data for
            interval = time frame interval in minutes (optional):
                1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600
            since = return committed OHLC data since given id (optional.  exclusive)
        Result:
            <pair_name> = pair name
                array of array entries(<time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>)
            last = id to be used as since when polling for new, committed OHLC data

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        ohlc = self.query_public('OHLC', req=req, conn=conn)
        return ohlc

    def get_order_book(self, req=None, conn=None):
        """Public API method.
        Get an array of pair name and market depth

        Input:
            pair = asset pair to get market depth for
            count = maximum number of asks/bids (optional)
        Result:
            <pair_name> = pair name
                asks = ask side array of array entries(<price>, <volume>, <timestamp>)
                bids = bid side array of array entries(<price>, <volume>, <timestamp>)

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        depth = self.query_public('Depth', req=req, conn=conn)
        return depth

    def get_recent_trades(self, req=None, conn=None):
        """Public API method.
        Get an array of pair name and recent trade data

        Input:
            pair = asset pair to get trade data for
            since = return trade data since given id (optional.  exclusive)
        Result:
            <pair_name> = pair name
                array of array entries(<price>, <volume>, <time>, <buy/sell>, <market/limit>, <miscellaneous>)
            last = id to be used as since when polling for new trade data

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        trades = self.query_public('Trades', req=req, conn=conn)
        return trades

    def get_spread_data(self, req=None, conn=None):
        """Public API method.
        Get an array of pair name and recent spread data

        Input:
            pair = asset pair to get spread data for
            since = return spread data since given id (optional.  inclusive)
        Result:
            <pair_name> = pair name
                array of array entries(<time>, <bid>, <ask>)
            last = id to be used as since when polling for new spread data

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        spread = self.query_public('Spread', req=req, conn=conn)
        return spread

    def get_account_balance(self, req=None, conn=None):
        """Private API method.
        Get an array of asset names and balance amount

        Input:
            None
        Result:
            an array of asset names and balance amount

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        balance = self.query_private('Balance', req=req, conn=conn)
        return balance

    def get_trade_balance(self, req=None, conn=None):
        """Private API method.
        Get an array of trade balance info

        Input:
            aclass = asset class (optional):
                currency (default)
            asset = base asset used to determine balance (default = ZUSD)
        Result:
            eb = equivalent balance (combined balance of all currencies)
            tb = trade balance (combined balance of all equity currencies)
            m = margin amount of open positions
            n = unrealized net profit/loss of open positions
            c = cost basis of open positions
            v = current floating valuation of open positions
            e = equity = trade balance + unrealized net profit/loss
            mf = free margin = equity - initial margin (maximum margin available to open new positions)
            ml = margin level = (equity / initial margin) * 100

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        balance = self.query_private('TradeBalance', req=req, conn=conn)
        return balance

    def get_open_orders(self, req=None, conn=None):
        """Private API method.
        Get an array of order info in open array with txid as the key

        Input:
            trades = whether or not to include trades in output (optional.  default = false)
            userref = restrict results to given user reference id (optional)
        Result:
            refid = Referral order transaction id that created this order
            userref = user reference id
            status = status of order:
                pending = order pending book entry
                open = open order
                closed = closed order
                canceled = order canceled
                expired = order expired
            opentm = unix timestamp of when order was placed
            starttm = unix timestamp of order start time (or 0 if not set)
            expiretm = unix timestamp of order end time (or 0 if not set)
            descr = order description info
                pair = asset pair
                type = type of order (buy/sell)
                ordertype = order type (See Add standard order)
                price = primary price
                price2 = secondary price
                leverage = amount of leverage
                order = order description
                close = conditional close order description (if conditional close set)
            vol = volume of order (base currency unless viqc set in oflags)
            vol_exec = volume executed (base currency unless viqc set in oflags)
            cost = total cost (quote currency unless unless viqc set in oflags)
            fee = total fee (quote currency)
            price = average price (quote currency unless viqc set in oflags)
            stopprice = stop price (quote currency, for trailing stops)
            limitprice = triggered limit price (quote currency, when limit based order type triggered)
            misc = comma delimited list of miscellaneous info
                stopped = triggered by stop price
                touched = triggered by touch price
                liquidated = liquidation
                partial = partial fill
            oflags = comma delimited list of order flags
                viqc = volume in quote currency
                fcib = prefer fee in base currency (default if selling)
                fciq = prefer fee in quote currency (default if buying)
                nompp = no market price protection
            trades = array of trade ids related to order (if trades info requested and data available)

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        orders = self.query_private('OpenOrders', req=req, conn=conn)
        return orders

    def get_closed_orders(self, req=None, conn=None):
        """Private API method.
        Get an array of order info

        Input:
            trades = whether or not to include trades in output (optional.  default = false)
            userref = restrict results to given user reference id (optional)
            start = starting unix timestamp or order tx id of results (optional.  exclusive)
            end = ending unix timestamp or order tx id of results (optional.  inclusive)
            ofs = result offset
            closetime = which time to use (optional)
                open
                close
                both (default)
        Result:
            closed = array of order info.  See Get open orders.  Additional fields:
                closetm = unix timestamp of when order was closed
                reason = additional info on status (if any)
            count = amount of available order info matching criteria

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        orders = self.query_private('ClosedOrders', req=req, conn=conn)
        return orders

    def query_orders_info(self, req=None, conn=None):
        """Private API method.
        Get an associative array of orders info

        Input:
            trades = whether or not to include trades in output (optional.  default = false)
            userref = restrict results to given user reference id (optional)
            txid = comma delimited list of transaction ids to query info about (20 maximum)
        Result:
            <order_txid> = order info.  See Get open orders/Get closed orders

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        orders = self.query_private('QueryOrders', req=req, conn=conn)
        return orders

    def get_trades_history(self, req=None, conn=None):
        """Private API method.
        Get an array of trade info

        Input:
            type = type of trade (optional)
                all = all types (default)
                any position = any position (open or closed)
                closed position = positions that have been closed
                closing position = any trade closing all or part of a position
                no position = non-positional trades
            trades = whether or not to include trades related to position in output (optional.  default = false)
            start = starting unix timestamp or trade tx id of results (optional.  exclusive)
            end = ending unix timestamp or trade tx id of results (optional.  inclusive)
            ofs = result offset
        Result:
            trades = array of trade info with txid as the key
                ordertxid = order responsible for execution of trade
                pair = asset pair
                time = unix timestamp of trade
                type = type of order (buy/sell)
                ordertype = order type
                price = average price order was executed at (quote currency)
                cost = total cost of order (quote currency)
                fee = total fee (quote currency)
                vol = volume (base currency)
                margin = initial margin (quote currency)
                misc = comma delimited list of miscellaneous info
                    closing = trade closes all or part of a position
            count = amount of available trades info matching criteria
        If the trade opened a position, the follow fields are also present in the trade info:
                 posstatus = position status (open/closed)
                cprice = average price of closed portion of position (quote currency)
                ccost = total cost of closed portion of position (quote currency)
                cfee = total fee of closed portion of position (quote currency)
                cvol = total fee of closed portion of position (quote currency)
                cmargin = total margin freed in closed portion of position (quote currency)
                net = net profit/loss of closed portion of position (quote currency, quote currency scale)
                trades = list of closing trades for position (if available)

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        history = self.query_private('TradesHistory', req=req, conn=conn)
        return history

    def query_trades_info(self, req=None, conn=None):
        """Private API method.
        Get an associative array of trades info

        Input:
            txid = comma delimited list of transaction ids to query info about (20 maximum)
            trades = whether or not to include trades related to position in output (optional.  default = false)
        Result:
            <trade_txid> = trade info.

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        info = self.query_private('QueryTrades', req=req, conn=conn)
        return info

    def get_open_positions(self, req=None, conn=None):
        """Private API method.
        Get an associative array of open position info

        Input:
            txid = comma delimited list of transaction ids to restrict output to
            docalcs = whether or not to include profit/loss calculations (optional.  default = false)
        Result:
            <position_txid> = open position info
                ordertxid = order responsible for execution of trade
                pair = asset pair
                time = unix timestamp of trade
                type = type of order used to open position (buy/sell)
                ordertype = order type used to open position
                cost = opening cost of position (quote currency unless viqc set in oflags)
                fee = opening fee of position (quote currency)
                vol = position volume (base currency unless viqc set in oflags)
                vol_closed = position volume closed (base currency unless viqc set in oflags)
                margin = initial margin (quote currency)
                value = current value of remaining position (if docalcs requested.  quote currency)
                net = unrealized profit/loss of remaining position (if docalcs requested.  quote currency, quote currency scale)
                misc = comma delimited list of miscellaneous info
                oflags = comma delimited list of order flags
                    viqc = volume in quote currency

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        positions = self.query_private('OpenPositions', req=req, conn=conn)
        return positions

    def get_ledgers_info(self, req=None, conn=None):
        """Private API method.
        Get an associative array of ledgers info

        Input:
            aclass = asset class (optional):
                currency (default)
            asset = comma delimited list of assets to restrict output to (optional.  default = all)
            type = type of ledger to retrieve (optional):
                all (default)
                deposit
                withdrawal
                trade
                margin
            start = starting unix timestamp or ledger id of results (optional.  exclusive)
            end = ending unix timestamp or ledger id of results (optional.  inclusive)
            ofs = result offset
        Result:
            <ledger_id> = ledger info
                refid = reference id
                time = unx timestamp of ledger
                type = type of ledger entry
                aclass = asset class
                asset = asset
                amount = transaction amount
                fee = transaction fee
                balance = resulting balance

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        ledgers = self.query_private('Ledgers', req=req, conn=conn)
        return ledgers

    def query_ledgers(self, req=None, conn=None):
        """Private API method.
        Get an associative array of ledgers info

        Input:
            id = comma delimited list of ledger ids to query info about (20 maximum)
        Result:
            <ledger_id> = ledger info.

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        ledgers = self.query_private('QueryLedgers', req=req, conn=conn)
        return ledgers

    def get_trade_volume(self, req=None, conn=None):
        """Private API method.
        Get an associative array of trade volumes

        Input:
            pair = comma delimited list of asset pairs to get fee info on (optional)
            fee-info = whether or not to include fee info in results (optional)
        Result:
            currency = volume currency
            volume = current discount volume
            fees = array of asset pairs and fee tier info (if requested)
                fee = current fee in percent
                minfee = minimum fee for pair (if not fixed fee)
                maxfee = maximum fee for pair (if not fixed fee)
                nextfee = next tier's fee for pair (if not fixed fee.  nil if at lowest fee tier)
                nextvolume = volume level of next tier (if not fixed fee.  nil if at lowest fee tier)
                tiervolume = volume level of current tier (if not fixed fee.  nil if at lowest fee tier)
            fees_maker = array of asset pairs and maker fee tier info (if requested) for any pairs on maker/taker schedule
                fee = current fee in percent
                minfee = minimum fee for pair (if not fixed fee)
                maxfee = maximum fee for pair (if not fixed fee)
                nextfee = next tier's fee for pair (if not fixed fee.  nil if at lowest fee tier)
                nextvolume = volume level of next tier (if not fixed fee.  nil if at lowest fee tier)
                tiervolume = volume level of current tier (if not fixed fee.  nil if at lowest fee tier)

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        volume = self.query_private('Trade=Volume', req=req, conn=conn)
        return volume

    def add_standard_order(self, req=None, conn=None):
        """Private API method.
        Add a standard order

        Input:
            pair = asset pair
            type = type of order (buy/sell)
            ordertype = order type:
                market
                limit (price = limit price)
                stop-loss (price = stop loss price)
                take-profit (price = take profit price)
                stop-loss-profit (price = stop loss price, price2 = take profit price)
                stop-loss-profit-limit (price = stop loss price, price2 = take profit price)
                stop-loss-limit (price = stop loss trigger price, price2 = triggered limit price)
                take-profit-limit (price = take profit trigger price, price2 = triggered limit price)
                trailing-stop (price = trailing stop offset)
                trailing-stop-limit (price = trailing stop offset, price2 = triggered limit offset)
                stop-loss-and-limit (price = stop loss price, price2 = limit price)
                settle-position
            price = price (optional.  dependent upon ordertype)
            price2 = secondary price (optional.  dependent upon ordertype)
            volume = order volume in lots
            leverage = amount of leverage desired (optional.  default = none)
            oflags = comma delimited list of order flags (optional):
                viqc = volume in quote currency (not available for leveraged orders)
                fcib = prefer fee in base currency
                fciq = prefer fee in quote currency
                nompp = no market price protection
                post = post only order (available when ordertype = limit)
            starttm = scheduled start time (optional):
                0 = now (default)
                +<n> = schedule start time <n> seconds from now
                <n> = unix timestamp of start time
            expiretm = expiration time (optional):
                0 = no expiration (default)
                +<n> = expire <n> seconds from now
                <n> = unix timestamp of expiration time
            userref = user reference id.  32-bit signed number.  (optional)
            validate = validate inputs only.  do not submit order (optional)

            optional closing order to add to system when order gets filled:
                close[ordertype] = order type
                close[price] = price
                close[price2] = secondary price
        Result:
            descr = order description info
                order = order description
                close = conditional close order description (if conditional close set)
            txid = array of transaction ids for order (if order was added successfully)
        Errors:
            EGeneral:Invalid arguments
            EService:Unavailable
            ETrade:Invalid request
            EOrder:Cannot open position
            EOrder:Cannot open opposing position
            EOrder:Margin allowance exceeded
            EOrder:Margin level too low
            EOrder:Insufficient margin (exchange does not have sufficient funds to allow margin trading)
            EOrder:Insufficient funds (insufficient user funds)
            EOrder:Order minimum not met (volume too low)
            EOrder:Orders limit exceeded
            EOrder:Positions limit exceeded
            EOrder:Rate limit exceeded
            EOrder:Scheduled orders limit exceeded
            EOrder:Unknown position

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        order = self.query_private('AddOrder', req=req, conn=conn)
        return order

    def cancel_open_order(self, req=None, conn=None):
        """Private API method.
        Cancel an existing order

        Input:
            txid = transaction id
        Result:
            count = number of orders canceled
            pending = if set, order(s) is/are pending cancellation

        :param req: (optional) API request parameters
        :type req: dict
        :param conn: (optional) connection object to use
        :type conn: krakenex.Connection
        :returns: :py:func:`json.loads`-deserialised Python object
        """
        order = self.query_private('CancelOrder', req=req, conn=conn)
        return order
