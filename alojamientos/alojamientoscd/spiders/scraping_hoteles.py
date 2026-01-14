#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def get_website_from_hotel_page(driver, url_hotel):
    """Extrae la web oficial del hotel desde su página en hoteles.net"""
    try:
        driver.get(url_hotel)
        time.sleep(2)  # Espera más tiempo
        
        # Busca todos los enlaces que NO sean de hoteles.net
        try:
            enlaces = driver.find_elements(By.CSS_SELECTOR, 'a[href*="http"]')
        except:
            return None
        
        for enlace in enlaces:
            try:
                href = enlace.get_attribute('href')
                
                # Si es un enlace externo (no de hoteles.net) y parece ser un sitio web
                if href and 'hoteles.net' not in href and 'http' in href:
                    # Filtra enlaces de redes sociales y otros
                    if not any(x in href.lower() for x in ['facebook', 'instagram', 'twitter', 'tripadvisor', 'booking', 'google', 'maps', 'youtube']):
                        return href
            except:
                pass
        
        return None
        
    except Exception as e:
        return None

def scrape_hoteles():
    """Scraped hoteles de Madrid usando Selenium y filtra por web propia"""
    
    print("=" * 60)
    print("SCRAPING DE HOTELES MADRID - SIN WEB PROPIA")
    print("=" * 60)
    
    print("\nIniciando navegador Chrome...")
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_argument('--no-sandbox')
    
    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        url = 'https://www.hoteles.net/madrid/'
        print(f"\nAccediendo a: {url}")
        driver.get(url)
        
        print("Esperando contenido (5 segundos)...")
        time.sleep(5)
        
        # Guarda HTML para debug
        html_path = r'C:\Users\mika\Desktop\scraping\alojamientos\alojamientoscd\spiders\page_debug.html'
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"✓ HTML guardado en {html_path}")
        except:
            pass
        
        # PASO 1: Extrae TODOS los URLs primero (evita stale element reference)
        print("\nBuscando hoteles...")
        try:
            todos_enlaces = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/madrid/"]')
        except:
            todos_enlaces = []
        
        print(f"Total de enlaces encontrados: {len(todos_enlaces)}")
        
        # Guarda los datos antes de navegar (evita stale element)
        urls_hoteles = []
        for enlace in todos_enlaces:
            try:
                nombre = enlace.text.strip()
                url_hotel = enlace.get_attribute('href')
                if nombre and url_hotel and url_hotel.endswith('.html'):
                    urls_hoteles.append((nombre, url_hotel))
            except:
                pass
        
        print(f"Total de hoteles extraídos: {len(urls_hoteles)}\n")
        
        # PASO 2: Ahora procesa cada URL (no el elemento DOM)
        hoteles = []
        
        for contador, (nombre, url_hotel) in enumerate(urls_hoteles, 1):
            try:
                print(f"[{contador}/{len(urls_hoteles)}] Procesando: {nombre}")
                
                # Obtén la web oficial del hotel
                website = get_website_from_hotel_page(driver, url_hotel)
                
                if website:
                    print(f"     → Con web propia: {website[:60]}... (IGNORADO)")
                else:
                    print(f"     → SIN web propia (GUARDADO)")
                    hoteles.append({
                        'nombre': nombre,
                        'url_hoteles_net': url_hotel
                    })
                    
            except Exception as e:
                print(f"     → Error: {e}")
        
        print(f"\n{'=' * 60}")
        print(f"✓ Total: {len(hoteles)} hoteles SIN web propia")
        print(f"{'=' * 60}")
        
        # Guarda en CSV
        csv_path = r'C:\Users\mika\Desktop\scraping\alojamientos\alojamientoscd\spiders\hoteles.madrid.csv'
        
        if hoteles:
            try:
                with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['nombre', 'url_hoteles_net'])
                    writer.writeheader()
                    writer.writerows(hoteles)
                print(f"\n✓ Datos guardados en: {csv_path}")
            except Exception as e:
                print(f"\n❌ Error guardando CSV: {e}")
        else:
            print("\n⚠ No se encontraron hoteles sin web propia")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        print(traceback.format_exc())
    
    finally:
        if driver:
            driver.quit()
            print("\n✓ Navegador cerrado")

if __name__ == '__main__':
    scrape_hoteles()

