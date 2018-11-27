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

if len(sys.argv) != 2:
    print('This script needs 1 argument!')
    sys.exit(1)

if __name__ ==  '__main__':
    filename = sys.argv[1]
    start = time.perf_counter()
    count = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line == '\n':
                continue
            count += 1
            args = line.strip().split(' ')
            run_exp((args[0], args[1], args[2], args[3]), args[4])
    end = time.perf_counter()
    print(str(count) + ' experiment finished in ' + str(end - start) + 's')
