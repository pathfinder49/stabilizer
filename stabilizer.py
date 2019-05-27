import json
import asyncio
from collections import OrderedDict
import logging

import numpy as np

logger = logging.getLogger()


class StabilizerError(Exception):
    pass


class StabilizerConfig:
    async def connect(self, host, port=1235):
        self.reader, self.writer = await asyncio.open_connection(host, port)

    async def set(self, channel, iir):
        up = OrderedDict([("channel", channel), ("iir", iir.as_dict())])
        s = json.dumps(up, separators=(",", ":"))
        assert "\n" not in s
        logger.debug("send %s", s)
        self.writer.write(s.encode() + b"\n")
        r = (await self.reader.readline()).decode()
        logger.debug("recv %s", r)
        ret = json.loads(r, object_pairs_hook=OrderedDict)
        if ret["code"] != 200:
            raise StabilizerError(ret)
        return ret


class IIR:
    t_update = 2e-6

    def __init__(self):
        self.ba = np.zeros(5, np.float32)
        self.y_offset = 0.
        self.y_min = -float(1 << 15)
        self.y_max = float(1 << 15) - 1

    def as_dict(self):
        iir = OrderedDict()
        iir["ba"] = [float(_) for _ in self.ba]
        iir["y_offset"] = self.y_offset
        iir["y_min"] = self.y_min
        iir["y_max"] = self.y_max
        return iir

    def configure_pi(self, kp, ki, g=0.):
        ki = np.copysign(ki, kp)*self.t_update*2
        g = np.copysign(g, kp)
        eps = np.finfo(np.float32).eps
        if abs(ki) < eps:
            a1, b0, b1 = 0., kp, 0.
        else:
            if abs(g) < eps:
                c = 1.
            else:
                c = 1./(1. + ki/g)
            a1 = 2*c - 1.
            b0 = ki*c + kp
            b1 = ki*c - a1*kp
            if abs(b0 + b1) < eps:
                raise ValueError("low integrator gain and/or gain limit")
        self.ba[0] = b0
        self.ba[1] = b1
        self.ba[2] = 0.
        self.ba[3] = a1
        self.ba[4] = 0.

    def set_x_offset(self, o):
        b = self.ba[:3].sum()
        self.y_offset = b*o


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--stabilizer", default="10.0.16.99")
    p.add_argument("-c", "--channel", default=0, type=int,
                   help="Stabilizer channel to configure")
    p.add_argument("-o", "--offset", default=0., type=float,
                   help="X offset, in ADC LSB")
    p.add_argument("-p", "--proportional-gain", default=1., type=float,
                   help="Proportional gain, in DAC LSB/ADC LSB")
    p.add_argument("-i", "--integral-gain", default=0., type=float,
                   help="Integral gain, in DAC LSB/(ADC LSB*s)")

    args = p.parse_args()

    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    logging.basicConfig(level=logging.DEBUG)

    async def main():
        i = IIR()
        i.configure_pi(args.proportional_gain, args.integral_gain)
        i.set_x_offset(args.offset)
        s = StabilizerConfig()
        await s.connect(args.stabilizer)
        r = await s.set(0, i)

    loop.run_until_complete(main())
