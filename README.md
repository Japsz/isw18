# isw18
Instalacion:

FEDORA

	Instalar dependencias:
	npm install

	Agregar el ejecutable de python a la variable path (en node_module/python-shell/index.js):
	var pythonPath = options.pythonPath || 'python3';

	Exportar variable de entorno PYTHONPATH:
	export PYTHONPATH=$PYTHONPATH:/home/nombre_usuario/lib/python3.6/site-packages/

	Ejecutar exe de python:
	python3 setup.py install --prefix=/home/nombre_usuario

	Instalar paquetes de numpy y scpi:
	python3 -m pip install --user numpy scipy

Testing:
