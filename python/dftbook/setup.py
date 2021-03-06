import subprocess
import time
import os

def setup_ase_espresso():
    print('Installing ASE')
    subprocess.run(['pip', 'install', 'ase'])

    print('Installing ase-espresso')
    subprocess.run(['pip', 'install', '--upgrade', 'git+git://github.com/ulissigroup/ase-espresso'])

    print('Installing pseudopotentials')
    subprocess.run(['mkdir', 'gbrv_pseudopotentials'])
    subprocess.run(['wget', '-P', './gbrv_pseudopotentials/', 'https://www.physics.rutgers.edu/gbrv/all_pbe_UPF_v1.5.tar.gz'])
    subprocess.run(['tar', 'xf', 'gbrv_pseudopotentials/all_pbe_UPF_v1.5.tar.gz', '-C', './gbrv_pseudopotentials/'])

    print('Renaming pseudopotentials')
    #Rename the GBRV pseudopotentials to Cu.UPF etc
    import glob
    import shutil
    import os
    ppfiles = glob.glob('gbrv_pseudopotentials/*_*.UPF')
    for ppfile in ppfiles:
        dir_name = os.path.dirname(ppfile)
        old_name = os.path.basename(ppfile)
        new_name = old_name.split('_')[0].capitalize() + '.UPF'

        shutil.move(ppfile, os.path.join(dir_name, new_name))

    #Tell ase-espresso where to get the pseudopotentials
    print('Almost there, setting environment pseudopotential path')
    os.environ['ESP_PSP_PATH'] = '/content/gbrv_pseudopotentials/'
    print('Done setting up ase, ase-espresso and the pseudopotentials')


def setup_colab():
    '''Setup a colab environment.
    Installs quantum-espresso, ase, the QE python wrapper,
    '''
    t0 = time.time()
    print('Please be patient. This takes about 30 seconds.')

    setup_ase_espresso()

    if os.environ['COLAB_GPU']=='1': #we have a gpu
        print('Found a GPU, installing the GPU Quantum Espresso version')
        print("Installing MKL")
        subprocess.run(["sh", "-c", "'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'"])
        subprocess.run(["wget", "https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB"])
        subprocess.run(["apt-key", "add", "GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB"])
        subprocess.run(['sh', '-c', "'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'"])
        subprocess.run(['apt', 'update'])
        subprocess.run(['apt', 'install', 'intel-mkl-2020.0-088'])

        print('Getting the GPU pw.x executable')
        subprocess.run(['pip', 'install', 'gdown'])
        url = 'https://drive.google.com/uc?id=1aWPj1yTXENx2tES_CVQxYFqhXQwqoHvI'
        import gdown
        gdown.download(url, '/usr/local/bin/pw.x', quiet=True)
        subprocess.run(['chmod', '+x', '/usr/local/bin/pw.x'])
        print('Done installing GPU version of Quantum Espresso')

    else: #cpu-only colab
        print('Installing quantum espresso for CPU')
        subprocess.run(['apt-get', 'install', 'quantum-espresso'])

    print('Setup is complete. Please visit https://github.com/jkitchin/dft-book-espresso to find the tutorials.')
    print(f'Installation took {time.time() - t0:1.1f} seconds')

# def setup_ubuntu():
#     '''Setup an Ubuntu environment.
#     I have nowhere to test this.
#     I assume you can just add "sudo" to the beginning of each command above.
#     Alternatively, we can make it a script in the package that you just run at the command line.
#     This probably needs some logic to not install every time it is run if not needed.
#     Maybe also
#     '''
#     raise NotImplementedError('This is not supported yet. Can you help?')


# def setup_nersc():
#     '''Good idea?'''
#     raise NotImplementedError('This is not supported yet. Can you help?')
