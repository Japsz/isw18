# isw18
Instalacion(fedora):

Dependencias:
npm install

Exportar variable de entorno PYTHONPATH:
export PYTHONPATH=$PYTHONPATH:/home/usuario/lib/python3.6/site-packages/

Agregar el ejecutable de python a la variable path (en node_module/python-shell/index.js):


Instalar paquetes de python:
python3 setup.py install --prefix=/home/usuario

Instalar paquetes de numpy y scpi:
python3 -m pip install --user numpy scipy

Testing:
