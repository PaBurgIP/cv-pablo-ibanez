# CV público de Pablo Ibáñez-Porras

La web se genera desde el libro de actividades situado en la carpeta hermana
`Certificados Académicos`. Si existen `Actividades.xlsx` y
`Actividades.actualizado.xlsx`, se usa automáticamente el modificado más
recientemente. El timeline de Formación y Experiencia sigue siendo manual y el
generador verifica que no cambie.

## Actualizar el HTML

1. Editar el Excel y guardar los cambios.
2. Instalar una vez la dependencia: `python -m pip install -r scripts/requirements.txt`.
3. Desde esta carpeta, ejecutar: `python scripts/generar_cv.py`.

El script actualiza publicaciones, formación continua, actividad académica,
docencia, divulgación y reconocimientos. A continuación genera automáticamente
`index-en.html` a partir de `index.html`, usando el catálogo de traducciones de
`scripts/traducir_cv.py`. Los textos del campo `Detalle` tienen prioridad sobre
los resúmenes provisionales incluidos en el código.

En la misma ejecución crea también los PDF A4 en ambos idiomas mediante
Microsoft Edge o Google Chrome:

- `CV Pablo Ibáñez-Porras.pdf`
- `CV Pablo Ibáñez-Porras EN.pdf`

En Windows también se puede hacer doble clic en `Actualizar CV.bat`; el archivo
comprueba la dependencia de Python y ejecuta el proceso completo.

Si se añade contenido nuevo en español que todavía no figure en el catálogo,
el generador avisa de las traducciones pendientes para revisarlas sin romper la
página inglesa.

Para probar con otro libro o crear una salida aparte:

```powershell
python scripts/generar_cv.py --excel "ruta\Actividades.xlsx" --output "index-prueba.html"
```

También es posible regenerar únicamente la traducción:

```powershell
python scripts/traducir_cv.py
```

Para regenerar solo los HTML y omitir temporalmente los PDF:

```powershell
python scripts/generar_cv.py --skip-pdf
```

La página se publica mediante GitHub Pages desde la rama `main` y la carpeta
raíz. Los archivos de `assets/` son necesarios: incluyen las fuentes, la foto y
el efecto topográfico del hero.
