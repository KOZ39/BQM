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
        source_hca_list = {hca.track.name.split('_', 1)[1]: hca.binary for hca in parse_acb(f)}

    with open(target, 'rb') as f:
        target_hca_list = {hca.track.name.split('_', 1)[1]: str(hca.track.cue_id) for hca in parse_acb(f)}

    subprocess.call(['bin/AcbEditor.exe', target])

    for i in source_hca_list.keys():
        if i in target_hca_list.keys():
            with open(os.path.join(target.split('.')[0], target_hca_list[i].zfill(5)) + '.hca', 'wb') as f:
                f.write(source_hca_list[i])

    '''
    target_hca_list.keys() - source_hca_list.keys()
    for i in abc:
        shutil.copy2('dummy.hca', os.path.join(target.split('.')[0], target_hca_list[i].zfill(5)) + '.hca')
    '''

    mute(source)
