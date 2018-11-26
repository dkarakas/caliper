import sys
import random
import subprocess

dist = ['fixed', 'poisson']
keys = range(1, 6)
orgs = [2]
peers = [1, 2, 3]
exp_root = "./benchmark/exp"
main_file = '/'.join([exp_root, 'main.js'])
res_folder = "./res"

def run_exp(arg_tuple, trail):
    print('Running trail '+ str(trail) + ' exp ' + str(arg_tuple))
    d, k, o, p = arg_tuple
    conf_file = ''.join([exp_root, '/', "exp-", d, '-k', str(k), 'o', str(o), 'p', str(p), '.json'])
    out_file = ''.join([d, '-k', str(k), 'o', str(o), 'p', str(p), '-t', str(trail), '.out'])
    out_file = '/'.join([res_folder, out_file])
    err_file = ''.join([d, '-k', str(k), 'o', str(o), 'p', str(p), '-t', str(trail), '.err'])
    err_file = '/'.join([res_folder, err_file])
    subprocess.call(['node', main_file, '-c', conf_file, '1>'+out_file, '2>'+err_file])


if len(sys.argv) < 3:
    print("Needs at least 2 arguments")
    sys.exit(1)

start = sys.argv[1]
rounds = sys.argv[2]
all_config = [(d, k, o, p) for d in dist for k in keys for o in orgs for p in peers]
print all_config
random.shuffle(all_config)

for trail in range(start, start+rounds):
    for i in range(len(all_config)):
        run_exp(all_config[i], trail)
