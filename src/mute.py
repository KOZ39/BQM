import io
from collections import namedtuple

from sub import acb


def parse_acb(acb_file):
    utf = acb.UTFTable(acb_file)
    cue = acb.TrackList(utf)
    embedded_awb = io.BytesIO(utf.rows[0]['AwbFile'])
    data_source = acb.AFSArchive(embedded_awb)

    acb_format = namedtuple('acb_format', 'track, binary')

    return [
        acb_format(
            track = track,
            binary = data_source.file_data_for_cue_id(track.memory_wav_id)
        ) 
        for track in cue.tracks
    ]


def crc16(data):
    poly = 0x8005
    init = 0x0000
    xorout = 0x0000

    for x in data:
        init ^= x << 8
        for _ in range(8):
            if init & 0x8000:
                init = ((init << 1) ^ poly) & 0xffff
            else:
                init = (init << 1) & 0xffff

    return (init ^ xorout).to_bytes(2, 'big')


def mute(acb_file, and_save=True):
    with open(acb_file, 'rb+') as f:
        hca_list = [i.binary for i in parse_acb(f)]
        f.seek(0)
        data = f.read()

        for hca in hca_list:
            header_size = int.from_bytes(hca[6:8], 'big')
            frame_count = int.from_bytes(hca[16:20], 'big')
            frame_size = int.from_bytes(hca[28:30], 'big')

            block = b'\xff\xff' + (b'\x00' * (frame_size - 4))
            block += crc16(block)

            data = data.replace(hca, hca[:header_size] + (frame_count * block))

        if and_save:
            f.seek(0)
            f.write(data)


if __name__ == "__main__":
    import argparse
    import glob
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="ACB file or directory", nargs='+')
    args = parser.parse_args()

    for i in args.path:
        if os.path.isfile(i):
            mute(i)
        elif os.path.isdir(i):
            for file in glob.iglob(i + '/*.acb*'):
                mute(file)
