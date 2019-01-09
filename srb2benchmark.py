# coding: utf-8
import struct
import argparse
import os
# When running `pyinstaller build-cmd.spec`, comment out this below line
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

# When running `pyinstaller build-cmd.spec`, comment out this @Gooey(...) statement
@Gooey(
    program_name = 'SRB2 Benchmark Tool',
    required_cols = 1,
    optional_cols = 1,
)
def main():
    args = get_args()
    xargs = args.xargs
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
            for exepath,exeid,exenosoftware,exeopengl,exeperargs in itertools.zip_longest(args.exe, args.id, args.nosoftware, args.opengl, args.perargs):
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
                        trialtime = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                        trialtimeread = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')

                        trialid = '{}{}{}'.format( #'{}_{}_{}_{}'.format(
                            exeid,
                            #execname
                            #vidmode,
                            '_{}'.format(i) if not args.noidtrialnum else '',
                            '_{}'.format(trialtime) if args.unique else '')

                        print('Testing ID {} in {}, vidmode {} - {}'.format(trialid, execname, vidmode, trialtimeread))

                        scriptpath = os.path.join(fullcwd, 'srb2benchmark-script.txt')
                        scriptfile = open(scriptpath, 'w', encoding='ascii')
                        scriptfile.write('wait 35\n')
                        scriptfile.write('vid_mode {}\n'.format(vidmode))
                        scriptfile.write('wait 35\n')
                        scriptfile.write('timedemo "{}" -csv "{}" -quit\n'.format(demopath, trialid))
                        scriptfile.close()

                        print('Running {}'.format(fullexepath))

                        o = subprocess.Popen('"{}" {} {} {} -skipintro +exec srb2benchmark-script.txt'.format(fullexepath, exeperargs if isinstance(exeperargs, str) else '', xargs if isinstance(xargs, str) else '', execarg),
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
        default=['32-bit/srb2win-v2123.exe','64-bit/srb2win-v2123.exe'],
        help='Space-separated list of EXE filenames to test.')
    parser.add_argument('-id', type=str, nargs='+',
        default=['vanilla','vanilla'],
        help='Space-separated list of IDs to associate with the EXEs. # of IDs must match the # of EXEs.')
    parser.add_argument('-nosoftware', type=str2bool, nargs='+',
        default=[False, False],
        help='Do not benchmark Software mode. Space-separated true or false per EXE')
    parser.add_argument('-opengl', type=str2bool, nargs='+',
        default=[False, False],
        help='Benchmark OpenGL mode. Space-separated true or false per EXE')
    parser.add_argument('-perargs', type=str, nargs='+',
        default=['""','""'],
        help='Command line arguments to add. Space-separated, quoted strings per EXE.')

    parser.add_argument('-vidmode', type=int, nargs='+',
        default=[0, 15],
        help='Space-separated list of vid_modes to test, for all EXEs. 0 = 1920x1200; 9 = 1280x800; 15 = 640x400')
    parser.add_argument('-demo', type=str, nargs='+',
        default=['benchmark/replay/main/MAP01-guest.lmp',
                'benchmark/replay/main/MAP02-guest.lmp'],
        help='Space-separated list of demo filenames to benchmark, relative to the CWD.')
    parser.add_argument('-trials', type=int, default=3,
        help='Number of trials per test')
    parser.add_argument('-xargs', type=str, default='-win -nomouse -nomusic -nosound',
        help='Command line arguments to add to every run.')

    parser.add_argument('-noidtrialnum', action='store_true', default=False,
        help='Do not add trial number to ID')
    parser.add_argument('-unique', action='store_true', default=False,
        help='Make trial IDs unique (add UTC datetime to ID string)')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
