import sys
import random
import subprocess
import time

dist = ['fixed', 'poisson']
keys = range(1, 6)
orgs = [2]
peers = [1, 2, 3]
exp_root = "./benchmark/exp"
main_file = '/'.join([exp_root, 'main.js'])
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


if len(sys.argv) < 3:
    print("Needs at least 2 arguments")
    sys.exit(1)

start = int(sys.argv[1])
rounds = int(sys.argv[2])
all_config = [(d, k, o, p) for d in dist for k in keys for o in orgs for p in peers]
#print(all_config)
random.shuffle(all_config)

t_start = time.perf_counter()
for trail in range(start, start+rounds):
    for i in range(len(all_config)):
        run_exp(all_config[i], trail)
t_end = time.perf_counter()
print(str(len(all_config) * rounds) + ' experiments finished in ' + str(t_end - t_start) + 's')