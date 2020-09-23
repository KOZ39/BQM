from mute import *

if __name__ == "__main__":
    import argparse
    import os
    import shutil
    import subprocess
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('source', help="")
    parser.add_argument('target', help="")
    args = parser.parse_args()

    if os.path.getsize(source := args.source) > os.path.getsize(target := args.target):
        # print('!')
        sys.exit()

    with open(source, 'rb') as f:
        source_hca_dict = {hca.track.name.split('_', 1)[1]: hca.binary for hca in parse_acb(f)}

    with open(target, 'rb') as f:
        target_hca_dict = {hca.track.name.split('_', 1)[1]: str(hca.track.cue_id) for hca in parse_acb(f)}

    subprocess.call(['../bin/AcbEditor.exe', target])

    target = target.split('.')[0]

    for i in source_hca_dict.keys():
        if i in target_hca_dict.keys():
            with open(os.path.join(target, target_hca_dict[i].zfill(5)) + '.hca', 'wb') as f:
                f.write(source_hca_dict[i])

    for i in target_hca_dict.keys() - source_hca_dict.keys():
        shutil.copy2('dummy.hca', os.path.join(target, target_hca_dict[i].zfill(5)) + '.hca')

    subprocess.call(['../bin/AcbEditor.exe', target])

    '''
    with open(target + '.acb.bytes', 'ab') as f:
        f.write(* b'\x00')
    '''

    mute(source)
