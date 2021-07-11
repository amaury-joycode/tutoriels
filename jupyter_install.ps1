pip install -r jupyter-requirements.txt
jupyter contrib nbextension install
jupyter-nbextension install rise --py --sys-prefix
jupyter-nbextension enable rise --py --sys-prefix
jt -t monokai -T -N -kl