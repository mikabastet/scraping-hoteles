# 🏨 Web Scraper de Hoteles - Madrid

Web scraper desarrollado en Python que extrae información de hoteles en Madrid desde **hoteles.net** usando **Selenium** para renderizar contenido dinámico (JavaScript).

## 📋 Descripción

Este proyecto identifica y extrae datos de hoteles que **NO tienen página web propia**, útil para:
- 📊 Análisis de mercado turístico
- 🎯 Prospección de clientes
- 📧 Campañas de email marketing
- 🔍 Investigación del sector hotelero

## ✨ Características

- ✅ Extrae información de hoteles desde hoteles.net
- ✅ Filtra solo hoteles SIN web propia
- ✅ Maneja sitios con contenido dinámico (JavaScript)
- ✅ Exporta datos a CSV
- ✅ Evita errores de elementos obsoletos (stale element reference)
- ✅ ChromeDriver automático

## 🛠️ Tecnologías

- **Python 3.12+**
- **Selenium 4.15.2** - Automatización de navegador Chrome
- **webdriver-manager 4.0.1** - Gestión automática del ChromeDriver
- **Scrapy 2.14.1** - Framework base
- **CSV** - Exportación de datos

## 📦 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/scraping-hoteles.git
cd scraping
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🚀 Uso

```bash
python alojamientos/alojamientoscd/spiders/scraping_hoteles.py
```

**Resultado:** Archivo `hoteles.madrid.csv` con 46+ hoteles sin web propia.

## 📊 Salida

Archivo CSV con las siguientes columnas:

```csv
nombre,url_hoteles_net
Hotel Axor Feria,https://www.hoteles.net/madrid/hotel-axor-feria.html
Apartahotel Be Smart Madrid Albufera,https://www.hoteles.net/madrid/apartahotel-be-smart-madrid-albufera.html
Hotel City House Florida Norte,https://www.hoteles.net/madrid/hotel-city-house-florida-norte.html
```

## 📁 Estructura

```
scraping/
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
├── .gitignore                # Archivos ignorados
└── alojamientos/
    ├── scrapy.cfg
    └── alojamientoscd/
        ├── settings.py
        └── spiders/
            ├── scraping_hoteles.py     # Script principal
            ├── hoteles.madrid.csv      # Resultado
            └── page_debug.html         # Debug (HTML capturado)
```

## ⚙️ Cómo funciona

1. Abre Chrome automáticamente
2. Accede a `hoteles.net/madrid/`
3. Extrae lista de ~50 hoteles
4. Para cada hotel:
   - Navega a su página
   - Busca enlaces a web propia
   - Filtra redes sociales y agregadores
5. Guarda solo los que **NO tienen web**
6. Exporta a CSV

## 🔧 Adaptar a otras ciudades

Edita la línea en `scraping_hoteles.py`:

```python
url = 'https://www.hoteles.net/barcelona/'  # Cambiar la ciudad
```

## ⚠️ Consideraciones Importantes

- ⏱️ Tiempo de ejecución: 5-10 minutos (navegación realista)
- 🤖 Respeta `robots.txt` del sitio
- 🔗 No hagas requests muy frecuentes
- 🖥️ Requiere Chrome instalado en el sistema

## 🐛 Solución de problemas

**Error "stale element reference":**
```
→ Ya solucionado: El script extrae URLs primero y luego las procesa
```

**ChromeDriver no encontrado:**
```
→ Instala: pip install --upgrade webdriver-manager
```

## 📈 Próximas mejoras

- [ ] Soportar múltiples ciudades
- [ ] Añadir información de contacto
- [ ] Exportar a Excel
- [ ] Scheduling automático (cron)
- [ ] Base de datos para historial

## 📄 Licencia

Proyecto de código abierto para fines educativos y personales.

## 👤 Autor

**Tu nombre** | [LinkedIn](https://linkedin.com/in/tu-usuario)

---

⭐ Si te resulta útil, dale una estrella en GitHub 🌟
