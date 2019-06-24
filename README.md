leapMotion
==========

Version 1.0 23/06/2019
----------------------

# Configuración leapMotion
1. Abrir una terminal y ejecutar servicio del leap motion con el siguiente comando.	
```
	sudo leapd
```
2. Abrir otra terminal y ejecutar el panel de control que ofrece leap motion
```
	sudo LeapControlPanel
```
![Alt text](demos/configuracion.png "Captura configuracion")

# Instalación dependencias para ejecutar demos
1. Ejecutar solo una vez.
```
sudo apt-get install scrot
virtualenv --python=python2 env
source env/bin/activate
pip install -r requirements.txt
```

# Demos desarrolladas para el leap motion

* Ejecutar demo pizarra
-----------------------

1. Abrir una terminal y ejecutar servicio del leap motion con el siguiente comando.	
```
	sudo leapd
```

2. Abrir otra terminal 
```
	source env/bin/activate
	cd LeapSDK_mauricio/leap_motion/src/
```

3. Ejecutar script de pizarra
```
	python pizarra.py
```

Capturas demo pizarra
---------------------
![Alt text](demos/demo_pizarra_1.png "Captura demo 1")
![Alt text](demos/demo_pizarra_2.png "Captura demo 2")
![Output sample](demos/demoPizarra.gif)


* Ejecutar demo predicción digitos
----------------------------------

1. Abrir una terminal y ejecutar servicio del leap motion con el siguiente comando.	
```
	sudo leapd
```

1. Abrir otra terminal y ejecutar
```
	source env/bin/activate
	cd LeapSDK_mauricio/leap_motion/src/
```

2. Ejecutar script de predicción
```
	python prediccion.py
```
Capturas demo predicción digitos
--------------------------------

![Alt text](demos/demo_prediccion_1.png "Captura demo 1")
![Alt text](demos/demo_prediccion_2.png "Captura demo 2")
![Alt text](demos/demo_prediccion_3.png "Captura demo 3")
![Alt text](demos/demo_prediccion_4.png "Captura demo 4")
