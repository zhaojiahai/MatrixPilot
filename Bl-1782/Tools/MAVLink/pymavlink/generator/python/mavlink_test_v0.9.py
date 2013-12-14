'''
MAVLink protocol implementation (auto-generated by mavgen.py)

Generated from: test.xml

Note: this file has been auto-generated. DO NOT EDIT
'''

import struct, array, mavutil, time

WIRE_PROTOCOL_VERSION = "0.9"

class MAVLink_header(object):
    '''MAVLink message header'''
    def __init__(self, msgId, mlen=0, seq=0, srcSystem=0, srcComponent=0):
        self.mlen = mlen
        self.seq = seq
        self.srcSystem = srcSystem
        self.srcComponent = srcComponent
        self.msgId = msgId

    def pack(self):
        return struct.pack('BBBBBB', 85, self.mlen, self.seq,
                          self.srcSystem, self.srcComponent, self.msgId)

class MAVLink_message(object):
    '''base MAVLink message class'''
    def __init__(self, msgId, name):
        self._header     = MAVLink_header(msgId)
        self._payload    = None
        self._msgbuf     = None
        self._crc        = None
        self._fieldnames = []
        self._type       = name

    def get_msgbuf(self):
        return self._msgbuf

    def get_header(self):
        return self._header

    def get_payload(self):
        return self._payload

    def get_crc(self):
        return self._crc

    def get_fieldnames(self):
        return self._fieldnames

    def get_type(self):
        return self._type

    def get_msgId(self):
        return self._header.msgId

    def get_srcSystem(self):
        return self._header.srcSystem

    def get_srcComponent(self):
        return self._header.srcComponent

    def get_seq(self):
        return self._header.seq

    def __str__(self):
        ret = '%s {' % self._type
        for a in self._fieldnames:
            v = getattr(self, a)
            ret += '%s : %s, ' % (a, v)
        ret = ret[0:-2] + '}'
        return ret            

    def pack(self, mav, crc_extra, payload):
        self._payload = payload
        self._header  = MAVLink_header(self._header.msgId, len(payload), mav.seq,
                                       mav.srcSystem, mav.srcComponent)
        self._msgbuf = self._header.pack() + payload
        crc = mavutil.x25crc(self._msgbuf[1:])
        if False: # using CRC extra
            crc.accumulate(chr(crc_extra))
        self._crc = crc.crc
        self._msgbuf += struct.pack('<H', self._crc)
        return self._msgbuf


# enums

# message IDs
MAVLINK_MSG_ID_BAD_DATA = -1
MAVLINK_MSG_ID_TEST_TYPES = 0

class MAVLink_test_types_message(MAVLink_message):
        '''
        Test all field types
        '''
        def __init__(self, c, s, u8, u16, u32, u64, s8, s16, s32, s64, f, d, u8_array, u16_array, u32_array, u64_array, s8_array, s16_array, s32_array, s64_array, f_array, d_array):
                MAVLink_message.__init__(self, MAVLINK_MSG_ID_TEST_TYPES, 'TEST_TYPES')
                self._fieldnames = ['c', 's', 'u8', 'u16', 'u32', 'u64', 's8', 's16', 's32', 's64', 'f', 'd', 'u8_array', 'u16_array', 'u32_array', 'u64_array', 's8_array', 's16_array', 's32_array', 's64_array', 'f_array', 'd_array']
                self.c = c
                self.s = s
                self.u8 = u8
                self.u16 = u16
                self.u32 = u32
                self.u64 = u64
                self.s8 = s8
                self.s16 = s16
                self.s32 = s32
                self.s64 = s64
                self.f = f
                self.d = d
                self.u8_array = u8_array
                self.u16_array = u16_array
                self.u32_array = u32_array
                self.u64_array = u64_array
                self.s8_array = s8_array
                self.s16_array = s16_array
                self.s32_array = s32_array
                self.s64_array = s64_array
                self.f_array = f_array
                self.d_array = d_array

        def pack(self, mav):
                return MAVLink_message.pack(self, mav, 91, struct.pack('>c10sBHIQbhiqfd3s3H3I3Q3s3h3i3q3f3d', self.c, self.s, self.u8, self.u16, self.u32, self.u64, self.s8, self.s16, self.s32, self.s64, self.f, self.d, self.u8_array, self.u16_array, self.u32_array, self.u64_array, self.s8_array, self.s16_array, self.s32_array, self.s64_array, self.f_array, self.d_array))


mavlink_map = {
        MAVLINK_MSG_ID_TEST_TYPES : ( '>c10sBHIQbhiqfd3s3H3I3Q3s3h3i3q3f3d', MAVLink_test_types_message, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], 91 ),
}

class MAVError(Exception):
        '''MAVLink error class'''
        def __init__(self, msg):
            Exception.__init__(self, msg)
            self.message = msg

class MAVString(str):
        '''NUL terminated string'''
        def __init__(self, s):
                str.__init__(self)
        def __str__(self):
            i = self.find(chr(0))
            if i == -1:
                return self[:]
            return self[0:i]

class MAVLink_bad_data(MAVLink_message):
        '''
        a piece of bad data in a mavlink stream
        '''
        def __init__(self, data, reason):
                MAVLink_message.__init__(self, MAVLINK_MSG_ID_BAD_DATA, 'BAD_DATA')
                self._fieldnames = ['data', 'reason']
                self.data = data
                self.reason = reason
                self._msgbuf = data
            
class MAVLink(object):
        '''MAVLink protocol handling class'''
        def __init__(self, file, srcSystem=0, srcComponent=0):
                self.seq = 0
                self.file = file
                self.srcSystem = srcSystem
                self.srcComponent = srcComponent
                self.callback = None
                self.callback_args = None
                self.callback_kwargs = None
                self.buf = array.array('B')
                self.expected_length = 6
                self.have_prefix_error = False
                self.robust_parsing = False
                self.protocol_marker = 85
                self.little_endian = False
                self.crc_extra = False
                self.sort_fields = False
                self.total_packets_sent = 0
                self.total_bytes_sent = 0
                self.total_packets_received = 0
                self.total_bytes_received = 0
                self.total_receive_errors = 0
                self.startup_time = time.time()

        def set_callback(self, callback, *args, **kwargs):
            self.callback = callback
            self.callback_args = args
            self.callback_kwargs = kwargs
            
        def send(self, mavmsg):
                '''send a MAVLink message'''
                buf = mavmsg.pack(self)
                self.file.write(buf)
                self.seq = (self.seq + 1) % 255
                self.total_packets_sent += 1
                self.total_bytes_sent += len(buf)

        def bytes_needed(self):
            '''return number of bytes needed for next parsing stage'''
            ret = self.expected_length - len(self.buf)
            if ret <= 0:
                return 1
            return ret

        def parse_char(self, c):
            '''input some data bytes, possibly returning a new message'''
            if isinstance(c, str):
                self.buf.fromstring(c)
            else:
                self.buf.extend(c)
            self.total_bytes_received += len(c)
            if len(self.buf) >= 1 and self.buf[0] != 85:
                magic = self.buf[0]
                self.buf = self.buf[1:]
                if self.robust_parsing:
                    m = MAVLink_bad_data(chr(magic), "Bad prefix")
                    if self.callback:
                        self.callback(m, *self.callback_args, **self.callback_kwargs)
                    self.expected_length = 6
                    self.total_receive_errors += 1
                    return m
                if self.have_prefix_error:
                    return None
                self.have_prefix_error = True
                self.total_receive_errors += 1
                raise MAVError("invalid MAVLink prefix '%s'" % magic) 
            self.have_prefix_error = False
            if len(self.buf) >= 2:
                (magic, self.expected_length) = struct.unpack('BB', self.buf[0:2])
                self.expected_length += 8
            if self.expected_length >= 8 and len(self.buf) >= self.expected_length:
                mbuf = self.buf[0:self.expected_length]
                self.buf = self.buf[self.expected_length:]
                self.expected_length = 6
                if self.robust_parsing:
                    try:
                        m = self.decode(mbuf)
                        self.total_packets_received += 1
                    except MAVError as reason:
                        m = MAVLink_bad_data(mbuf, reason.message)
                        self.total_receive_errors += 1
                else:
                    m = self.decode(mbuf)
                    self.total_packets_received += 1
                if self.callback:
                    self.callback(m, *self.callback_args, **self.callback_kwargs)
                return m
            return None

        def parse_buffer(self, s):
            '''input some data bytes, possibly returning a list of new messages'''
            m = self.parse_char(s)
            if m is None:
                return None
            ret = [m]
            while True:
                m = self.parse_char("")
                if m is None:
                    return ret
                ret.append(m)
            return ret

        def decode(self, msgbuf):
                '''decode a buffer as a MAVLink message'''
                # decode the header
                try:
                    magic, mlen, seq, srcSystem, srcComponent, msgId = struct.unpack('cBBBBB', msgbuf[:6])
                except struct.error as emsg:
                    raise MAVError('Unable to unpack MAVLink header: %s' % emsg)
                if ord(magic) != 85:
                    raise MAVError("invalid MAVLink prefix '%s'" % magic)
                if mlen != len(msgbuf)-8:
                    raise MAVError('invalid MAVLink message length. Got %u expected %u, msgId=%u' % (len(msgbuf)-8, mlen, msgId))

                if not msgId in mavlink_map:
                    raise MAVError('unknown MAVLink message ID %u' % msgId)

                # decode the payload
                (fmt, type, order_map, crc_extra) = mavlink_map[msgId]

                # decode the checksum
                try:
                    crc, = struct.unpack('<H', msgbuf[-2:])
                except struct.error as emsg:
                    raise MAVError('Unable to unpack MAVLink CRC: %s' % emsg)
                crc2 = mavutil.x25crc(msgbuf[1:-2])
                if False: # using CRC extra 
                    crc2.accumulate(chr(crc_extra))
                if crc != crc2.crc:
                    raise MAVError('invalid MAVLink CRC in msgID %u 0x%04x should be 0x%04x' % (msgId, crc, crc2.crc))

                try:
                    t = struct.unpack(fmt, msgbuf[6:-2])
                except struct.error as emsg:
                    raise MAVError('Unable to unpack MAVLink payload type=%s fmt=%s payloadLength=%u: %s' % (
                        type, fmt, len(msgbuf[6:-2]), emsg))

                tlist = list(t)
                # handle sorted fields
                if False:
                    t = tlist[:]
                    for i in range(0, len(tlist)):
                        tlist[i] = t[order_map[i]]

                # terminate any strings
                for i in range(0, len(tlist)):
                    if isinstance(tlist[i], str):
                        tlist[i] = MAVString(tlist[i])
                t = tuple(tlist)
                # construct the message object
                try:
                    m = type(*t)
                except Exception as emsg:
                    raise MAVError('Unable to instantiate MAVLink message of type %s : %s' % (type, emsg))
                m._msgbuf = msgbuf
                m._payload = msgbuf[6:-2]
                m._crc = crc
                m._header = MAVLink_header(msgId, mlen, seq, srcSystem, srcComponent)
                return m
        def test_types_encode(self, c, s, u8, u16, u32, u64, s8, s16, s32, s64, f, d, u8_array, u16_array, u32_array, u64_array, s8_array, s16_array, s32_array, s64_array, f_array, d_array):
                '''
                Test all field types

                c                         : char (char)
                s                         : string (char)
                u8                        : uint8_t (uint8_t)
                u16                       : uint16_t (uint16_t)
                u32                       : uint32_t (uint32_t)
                u64                       : uint64_t (uint64_t)
                s8                        : int8_t (int8_t)
                s16                       : int16_t (int16_t)
                s32                       : int32_t (int32_t)
                s64                       : int64_t (int64_t)
                f                         : float (float)
                d                         : double (double)
                u8_array                  : uint8_t_array (uint8_t)
                u16_array                 : uint16_t_array (uint16_t)
                u32_array                 : uint32_t_array (uint32_t)
                u64_array                 : uint64_t_array (uint64_t)
                s8_array                  : int8_t_array (int8_t)
                s16_array                 : int16_t_array (int16_t)
                s32_array                 : int32_t_array (int32_t)
                s64_array                 : int64_t_array (int64_t)
                f_array                   : float_array (float)
                d_array                   : double_array (double)

                '''
                msg = MAVLink_test_types_message(c, s, u8, u16, u32, u64, s8, s16, s32, s64, f, d, u8_array, u16_array, u32_array, u64_array, s8_array, s16_array, s32_array, s64_array, f_array, d_array)
                msg.pack(self)
                return msg
            
        def test_types_send(self, c, s, u8, u16, u32, u64, s8, s16, s32, s64, f, d, u8_array, u16_array, u32_array, u64_array, s8_array, s16_array, s32_array, s64_array, f_array, d_array):
                '''
                Test all field types

                c                         : char (char)
                s                         : string (char)
                u8                        : uint8_t (uint8_t)
                u16                       : uint16_t (uint16_t)
                u32                       : uint32_t (uint32_t)
                u64                       : uint64_t (uint64_t)
                s8                        : int8_t (int8_t)
                s16                       : int16_t (int16_t)
                s32                       : int32_t (int32_t)
                s64                       : int64_t (int64_t)
                f                         : float (float)
                d                         : double (double)
                u8_array                  : uint8_t_array (uint8_t)
                u16_array                 : uint16_t_array (uint16_t)
                u32_array                 : uint32_t_array (uint32_t)
                u64_array                 : uint64_t_array (uint64_t)
                s8_array                  : int8_t_array (int8_t)
                s16_array                 : int16_t_array (int16_t)
                s32_array                 : int32_t_array (int32_t)
                s64_array                 : int64_t_array (int64_t)
                f_array                   : float_array (float)
                d_array                   : double_array (double)

                '''
                return self.send(self.test_types_encode(c, s, u8, u16, u32, u64, s8, s16, s32, s64, f, d, u8_array, u16_array, u32_array, u64_array, s8_array, s16_array, s32_array, s64_array, f_array, d_array))
            
