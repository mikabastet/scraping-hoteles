import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import HtmlResponse
import time

class HotelesNetSpider(scrapy.Spider):
    name = "hoteles_net"
    start_urls = ['https://www.hoteles.net/madrid/']

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def parse(self, response):
        self.logger.info(f"Accediendo a: {self.start_urls[0]}")
        
        try:
            self.driver.get(self.start_urls[0])
            self.logger.info("✓ Página cargada con Selenium")
            
            # Espera a que se cargue el contenido dinámico - 10 segundos máximo
            wait = WebDriverWait(self.driver, 10)
            try:
                # Espera a que aparezcan elementos de hotel (cualquier enlace con href que contenga 'madrid')
                wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'a[href*="/madrid/"]')
                ))
                self.logger.info("✓ Contenido dinámico cargado")
            except:
                self.logger.warning("⚠ Timeout esperando contenido, continuando...")
            
            # Espera adicional
            time.sleep(2)
            
            # Guarda HTML
            html_path = r'C:\Users\mika\Desktop\scraping\alojamientos\alojamientoscd\spiders\page_debug.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            self.logger.info(f"✓ HTML guardado en {html_path}")
            
            page_html = self.driver.page_source
            response = HtmlResponse(
                url=self.driver.current_url,
                body=page_html.encode('utf-8')
            )
            
            # Busca todos los enlaces que contengan madrid
            hoteles_a = response.css('a[href*="/madrid/"]')
            self.logger.info(f"Elementos con /madrid/: {len(hoteles_a)}")
            
            contador = 0
            for enlace in hoteles_a:
                nombre = enlace.css('::text').get()
                url = enlace.css('::attr(href)').get()
                
                if nombre and url and 'hotel' in url.lower():
                    yield {
                        'nombre': nombre.strip(),
                        'url': url.strip()
                    }
                    contador += 1
                    self.logger.info(f"✓ Hotel: {nombre.strip()}")
            
            self.logger.info(f"✓ Total: {contador} hoteles extraídos")
            
        except Exception as e:
            self.logger.error(f"❌ Error: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

    def closed(self, reason):
        self.driver.quit()
        self.logger.info("✓ Navegador cerrado")