# Bootcamp Python

Todo lo que fui haciendo durante el bootcamp de Python. El recorrido completo con los datos: bajarlos de APIs, guardarlos en MongoDB, analizarlos con consultas y pipelines, y publicarlos como datasets en Zenodo.

## Contenido por días

- **Dia 2 a 4**: fundamentos de Python, lectura y escritura de ficheros (TXT, CSV, JSON) y primeras peticiones HTTP con requests.
- **Dia 5**: mini proyecto semana 1, un extractor universal de APIs que filtra los datos y los exporta a CSV.
- **Dia 6 y 7**: conexión a MongoDB Atlas y CRUD básico con menú interactivo.
- **Dia 8 a 10**: consultas avanzadas y pipelines de agregación, con una consola de análisis meteorológico.
- **Dia 12 a 15**: la API de Zenodo, descargar ficheros, subir datos y metadatos, versionar depósitos y un menú interactivo que lo unifica todo.
- **Dia 16 a 19**: ingesta automática de Zenodo a MongoDB, control de errores con logging y consultas sobre los datos ingeridos.

## Cómo instalarlo

Crea un entorno virtual, instala las dependencias que aparecen en el archivo requirements.txt y crea el archivo .env con tus credenciales.

```bash
python -m venv env
pip install -r requirements.txt
```

El .env va en la raiz y necesita dos variables (esta en .gitignore, asi que no se sube al repo):

```env
MONGO_URI=mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?appName=<cluster>
Token_Zenodo_Sandbox=<tu-token-de-zenodo-sandbox>
```

## Cómo ejecutarlo

Desde la raiz, por ejemplo:

```bash
python "Dia 5/mini_proyecto_semana_1.py"
python "Dia 15/script_final.py"
```

Los archivos generados con cada script serán almacenados en la ruta desde la cual ejecutes el codigo, en este caso, en la raiz, por lo que puede ser conveniente ejecutar cada codigo desde su pertinente carpeta.

Los dias de MongoDB necesitan la variable MONGO_URI y el cluster accesible. Los dias 12 en adelante necesitan el token de Zenodo Sandbox.

## Autor

Saul Jiménez Vela, Universidad de Extremadura.