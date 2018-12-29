# coding: utf-8
import struct
import argparse
import os
from gooey import Gooey, GooeyParser
import itertools
from datetime import datetime
import subprocess

#################################
# Utilities
#################################

def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

#################################
# Main
#################################

@Gooey(
    program_name = 'SRB2 Benchmark Tool',
    required_cols = 1,
    optional_cols = 1,
)
def main():
    args = get_args()
    fullcwd = os.path.abspath(os.path.join(os.getcwd(), args.cwd))

    print('SRB2 working directory is {}'.format(fullcwd))

    if not os.path.isdir(fullcwd):
        print('SRB2 working directory {} is invalid.'.format(args.cwd))
        return

    # Test hierarchy:
    # trial number
    # demo name
    # EXE
    # Software/OGL
    # Vidmode
    for i in range(0, args.trials):
        print('Starting trial {}'.format(i+1))

        # Test per demo name
        for demopath in args.demo:
            fulldemopath = os.path.abspath(os.path.join(fullcwd, demopath))

            if not os.path.isfile(fulldemopath):
                print('Demo path {} does not exist; skipping...'.format(fulldemopath))
                continue

            print ('Using demo path {}'.format(demopath))

            # Test per EXE
            for exepath,exeid,exenosoftware,exeopengl in itertools.zip_longest(args.exe, args.id, args.nosoftware, args.opengl):
                fullexepath = os.path.abspath(os.path.join(os.getcwd(), exepath))

                if not is_exe(fullexepath):
                    print('EXE path {} does not exist; skipping...'.format(fullexepath))
                    continue

                exeid = exeid or os.path.basename(exepath)

                execlist = []
                if not exenosoftware:
                    execlist.append('') # empty string to run software without an arg
                if exeopengl:
                    execlist.append('-opengl')

                # Test per software/opengl
                for execarg in execlist:
                    execname = 'software' if execarg == '' else 'opengl' if execarg == '-opengl' else 'na'

                    # Test per vidmode
                    for vidmode in args.vidmode:
                        trialid = '{}_{}'.format( #'{}_{}_{}_{}'.format(
                            exeid,
                            #execname
                            #vidmode,
                            datetime.utcnow().strftime('%Y%m%d%H%M%S'))

                        print('Testing ID {} in {}, vidmode {}'.format(trialid, execname, vidmode))

                        scriptpath = os.path.join(fullcwd, 'srb2benchmark-script.txt')
                        scriptfile = open(scriptpath, 'w', encoding='ascii')
                        scriptfile.write('wait 35\n')
                        scriptfile.write('vid_mode {}\n'.format(vidmode))
                        scriptfile.write('wait 35\n')
                        scriptfile.write('timedemo "{}" -csv "{}" -quit\n'.format(demopath, trialid))
                        scriptfile.close()

                        print('Running {}'.format(fullexepath))

                        o = subprocess.Popen('"{}" {} -win -nomouse -nomusic -nosound -skipintro +exec srb2benchmark-script.txt'.format(fullexepath, execarg),
                            cwd=fullcwd)
                        o.wait()

                        print('Finished testing ID {}'.format(trialid))

                        if os.path.isfile(scriptpath):
                            os.remove(scriptpath)

            print('Finished demo path {}'.format(demopath))

        print('Finished trial {}'.format(i+1))

    print('Finished! See results in {}'.format(os.path.abspath(os.path.join(fullcwd, 'timedemo.csv'))))

    return

#################################
# Arguments
#################################

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_args():
    parser = argparse.ArgumentParser(description='Benchmark SRB2!')

    parser.add_argument('-cwd', type=str, default='..',
        help='Current working directory to start SRB2 from (i.e., your root SRB2 folder)')
    parser.add_argument('-exe', type=str, nargs='+',
        default=' '.join(map(str,
            ['32-bit/srb2win-v2123.exe','64-bit/srb2win-v2123.exe']
            )),
        help='Space-separated list of EXE filenames to test.')
    parser.add_argument('-id', type=str, nargs='+',
        default=' '.join(map(str,
            ['vanilla','vanilla']
            )),
        help='Space-separated list of IDs to associate with the EXEs. # of IDs must match the # of EXEs.')
    parser.add_argument('-nosoftware', type=str2bool, nargs='+',
        default=' '.join(map(str,
            [False, False]
            )),
        help='Do not benchmark Software mode. Space-separated true or false per EXE')
    parser.add_argument('-opengl', type=str2bool, nargs='+',
        default=' '.join(map(str,
            [False, False]
            )),
        help='Benchmark OpenGL mode. Space-separated true or false per EXE')
    parser.add_argument('-vidmode', type=int, nargs='+',
        default=' '.join(map(str,
            [0, 15]
            )),
        help='Space-separated list of vid_modes to test, for all EXEs. 0 = 1920x1200; 9 = 1280x800; 15 = 640x400')

    parser.add_argument('-demo', type=str, nargs='+',
        default=' '.join(map(str,
            ['benchmark/replay/main/MAP01-guest.lmp',
                'benchmark/replay/main/MAP02-guest.lmp']
            )),
        help='Space-separated list of demo filenames to benchmark, relative to the CWD.')
    parser.add_argument('-trials', type=int, default=3,
        help='Number of trials per test')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
