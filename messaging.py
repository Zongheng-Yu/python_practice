#!/usr/bin/python
from log import *
from abc import abstractmethod, ABCMeta
from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack, calcsize
from Queue import Queue
from threading import Thread


class Packable(object):
    __metaclass__ = ABCMeta
    PACK_FORMAT = None

    def __init__(self):
        self.payload = None

    @abstractmethod
    def pack(self):
        return self.payload

    @abstractmethod
    def unpack_header(self, packed_string):
        pass


class Message(Packable):
    MAGIC = 0x45454545
    DMX_TYPE = 0
    JSON_TYPE = 1
    UNKNOWN_TYPE = 99
    PACK_FORMAT = "!III"
    HEAD_LENGTH = calcsize(PACK_FORMAT)

    def __init__(self, payload=None, msg_type=UNKNOWN_TYPE):
        super(Message, self).__init__()
        if payload:
            self.payload_len = len(payload)
        else:
            self.payload_len = 0
        self.magic = self.MAGIC
        self.type = msg_type
        self.payload = payload

    def __str__(self):
        return "Message instance: payload length: 0x%d, magic: %x, type: %d, payload: %s"\
               % (self.payload_len, self.magic, self.type, self.payload)

    def pack(self):
        return pack(self.PACK_FORMAT, self.payload_len, self.magic, self.type) + self.payload

    def unpack_header(self, packed_string):
        self.payload_len, self.magic, self.type = unpack(self.PACK_FORMAT, packed_string)
        return calcsize(self.PACK_FORMAT)


class DmxMessage(Packable):
    PACK_FORMAT = '!HHHHB3s'
    HEAD_LENGTH = calcsize(PACK_FORMAT)
    IWC_PRB_FAMILY = 0x0b4c

    def __init__(self, payload=None):
        super(DmxMessage, self).__init__()
        self.msg_id = 0
        self.v2_computer = 9
        self.family = self.IWC_PRB_FAMILY
        self.process = 0
        self.focus = 0
        self.spare = '000'
        self.payload = payload

    def __str__(self):
        return "dmx message: msg ID: %x, computer: %d, family: %d, process: %d, focus: %d" \
               % (self.msg_id, self.v2_computer, self.family, self.process, self.focus)

    def pack(self):
        if not self.payload:
            self.payload = pack('I', 12)
        return pack(self.PACK_FORMAT,
                    self.msg_id, self.v2_computer, self.family, self.process, self.focus, self.spare) + self.payload

    def unpack_header(self, packed_string):
        self.msg_id, self.v2_computer, self.family, self.process, self.focus, self.spare =\
            unpack(self.PACK_FORMAT, packed_string)
        return calcsize(self.PACK_FORMAT)


class JsonMessage(Packable):
    def __init__(self, payload=None):
        super(JsonMessage, self).__init__()
        self.payload = payload

    def __str__(self):
        return "json message: " + self.payload

    def pack(self):
        return self.payload

    def unpack_header(self, packed_string):
        return 0


class Connection(object):
    def __init__(self, raw_conn, message_handler=None):
        if message_handler is not None:
            if callable(message_handler):
                self._rx_handler = message_handler
                self._rx = None
            else:
                raise TypeError("message_handler is not callabe")
        else:
            self._rx = Queue()
            self._rx_handler = None
        self._tx = Queue()
        self._thread_r = None
        self._thread_t = None
        self._raw_conn = raw_conn

    def start(self):
        self._thread_r = Thread(target=self._receive_forever, args=())
        self._thread_r.setDaemon(True)
        self._thread_r.start()
        self._thread_t = Thread(target=self._send_forever, args=())
        self._thread_t.setDaemon(True)
        self._thread_t.start()

    def _send_forever(self):
        while True:
            raw_msg = self._tx.get()
            logger.debug("send msg: " + str(raw_msg))
            if isinstance(raw_msg, DmxMessage):
                msg_s = Message(raw_msg.pack(), Message.DMX_TYPE)
            elif isinstance(raw_msg, JsonMessage):
                msg_s = Message(raw_msg.pack(), Message.JSON_TYPE)
            else:
                continue
            self._raw_conn.sendall(msg_s.pack())

    def _receive_until_len(self, len_r):
        if not len_r:
            return
        data = ''
        while len(data) < len_r:
            data += self._raw_conn.recv(len_r - len(data))
            if len(data) == 0:
                exit()
        return data

    def _rx_handle_message(self, msg):
        logger.debug("receive message: " + str(msg))
        if self._rx_handler:
            self._rx_handler(msg)
        else:
            self._rx.put(msg)

    def _receive_forever(self):
        while True:
            if self._raw_conn:
                packed_data = self._receive_until_len(Message.HEAD_LENGTH)
                msg_r = Message()
                msg_r.unpack_header(packed_data)
                if msg_r.magic != msg_r.MAGIC:
                    raise IOError("unexpected data received from socket: magic:%x" % msg_r.magic)
                unpacked_data = self._receive_until_len(msg_r.payload_len)
                if msg_r.type == msg_r.DMX_TYPE:
                    dmx = DmxMessage()
                    dmx.unpack_header(unpacked_data[:DmxMessage.HEAD_LENGTH])
                    dmx.payload = unpacked_data[DmxMessage.HEAD_LENGTH:]
                    self._rx_handle_message(dmx)
                elif msg_r.type == msg_r.JSON_TYPE:
                    self._rx_handle_message(JsonMessage(unpacked_data))
                else:
                    raise IOError("unexpected message type received from socket: type:%d" % msg_r.type)

    def receive(self, tmo=None):
        if self._rx:
            return self._rx.get(timeout=tmo)

    def send(self, raw_msg):
        if isinstance(raw_msg, DmxMessage) or isinstance(raw_msg, JsonMessage):
            self._tx.put(raw_msg)
        else:
            raise TypeError("Not a DMX or JASON message")

    def is_alive(self):
        return self._thread_r.is_alive() and self._thread_t.is_alive()

    def close(self):
        self._raw_conn.close()


class Server(object):
    def __init__(self, local):
        self._local = local
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind(self._local)
        self._socket.listen(5)

    def wait_for_new_connection(self, message_handler=None):
        raw_conn, addr = self._socket.accept()
        connection = Connection(raw_conn, message_handler)
        connection.start()
        return connection, addr


class Client(object):
    def __init__(self, remote, message_handler=None):
        self._remote = remote
        self._connection = None
        self._message_handler = message_handler

    def start(self):
        raw_conn = socket(AF_INET, SOCK_STREAM)
        raw_conn.connect(self._remote)
        self._connection = Connection(raw_conn, self._message_handler)
        self._connection.start()

    def receive(self, tmo=None):
        return self._connection.receive(tmo)

    def send(self, msg):
        return self._connection.send(msg)

    def close(self):
        self._connection.close()

    def is_alive(self):
        return self._connection.is_alive()


if __name__ == '__main__':
    pass
