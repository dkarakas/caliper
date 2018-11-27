import sys
import subprocess
import time

res_folder = "./res"
bash_script = './run_single.sh'

def run_exp(arg_tuple, trail):
    print('Running trail '+ str(trail) + ' exp ' + str(arg_tuple))
    d, k, o, p = arg_tuple
    conf_file = ''.join(["exp-", d, '-k', str(k), 'o', str(o), 'p', str(p), '.json'])
    out_file = ''.join([d, '-k', str(k), 'o', str(o), 'p', str(p), '-t', str(trail), '.out'])
    out_file = '/'.join([res_folder, out_file])
    err_file = ''.join([d, '-k', str(k), 'o', str(o), 'p', str(p), '-t', str(trail), '.err'])
    err_file = '/'.join([res_folder, err_file])
    subprocess.call([bash_script, conf_file, out_file, err_file])

if len(sys.argv) != 6:
    print('This script needs 5 arguments!')
    sys.exit(1)

if __name__ ==  '__main__':
    dist = sys.argv[1]
    key = int(sys.argv[2])
    org = int(sys.argv[3])
    peer = int(sys.argv[4])
    trail = int(sys.argv[5])
    start = time.perf_counter()
    run_exp((dist, key, org, peer), trail)
    end = time.perf_counter()
    print('1 experiment finished in ' + str(end - start) + 's')
