import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
from screeninfo import get_monitors
import time
from urllib.parse import quote
import re
from bs4 import BeautifulSoup

class BibliaApp:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = tk.Tk()
        self.root.title("Control de Versículos Bíblicos - RV1960")
        self.root.geometry("800x600")
        
        # Configuración de la web para scraping
        self.base_url = "https://mibibliavirtual.com/RV1960"
        self.search_url = f"{self.base_url}/search.php"
        
        # Detectar monitores
        self.detectar_pantallas()
        
        # Caché local para versículos
        self.biblia_cache = {}
        
        # Lista de versículos a mostrar
        self.lista_versiculos = []
        self.indice_actual = 0
        
        # Último libro usado (para búsquedas parciales como "1:1")
        self.ultimo_libro = "Génesis"
        self.ultimo_capitulo = 1
        
        # Ventana secundaria (pantalla de proyección)
        self.pantalla_secundaria = None
        self.texto_versiculo = None
        self.tamano_fuente = 48  # Tamaño de fuente inicial
        
        # Mapeo de libros de la Biblia y sus capítulos
        self.libros = self.crear_mapeo_libros()
        
        # Lista de libros para el combobox
        self.lista_libros_nombres = sorted([libro.title() for libro in self.libros.keys()])
        
        self.crear_interfaz_principal()
    
    def crear_mapeo_libros(self):
        """Crea el mapeo de libros de la Biblia y sus capítulos"""
        return {
            # Antiguo Testamento
            'génesis': {'archivo': 'Genesis', 'capitulos': 50, 'testamento': 'AntiguoTestamento'},
            'éxodo': {'archivo': 'Exodo', 'capitulos': 40, 'testamento': 'AntiguoTestamento'},
            'levítico': {'archivo': 'Levitico', 'capitulos': 27, 'testamento': 'AntiguoTestamento'},
            'números': {'archivo': 'Numeros', 'capitulos': 36, 'testamento': 'AntiguoTestamento'},
            'deuteronomio': {'archivo': 'Deuteronomio', 'capitulos': 34, 'testamento': 'AntiguoTestamento'},
            'josué': {'archivo': 'Josue', 'capitulos': 24, 'testamento': 'AntiguoTestamento'},
            'jueces': {'archivo': 'Jueces', 'capitulos': 21, 'testamento': 'AntiguoTestamento'},
            'rut': {'archivo': 'Rut', 'capitulos': 4, 'testamento': 'AntiguoTestamento'},
            '1 samuel': {'archivo': '1Samuel', 'capitulos': 31, 'testamento': 'AntiguoTestamento'},
            '2 samuel': {'archivo': '2Samuel', 'capitulos': 24, 'testamento': 'AntiguoTestamento'},
            '1 reyes': {'archivo': '1Reyes', 'capitulos': 22, 'testamento': 'AntiguoTestamento'},
            '2 reyes': {'archivo': '2Reyes', 'capitulos': 25, 'testamento': 'AntiguoTestamento'},
            '1 crónicas': {'archivo': '1Cronicas', 'capitulos': 29, 'testamento': 'AntiguoTestamento'},
            '2 crónicas': {'archivo': '2Cronicas', 'capitulos': 36, 'testamento': 'AntiguoTestamento'},
            'esdras': {'archivo': 'Esdras', 'capitulos': 10, 'testamento': 'AntiguoTestamento'},
            'nehemías': {'archivo': 'Nehemias', 'capitulos': 13, 'testamento': 'AntiguoTestamento'},
            'ester': {'archivo': 'Ester', 'capitulos': 10, 'testamento': 'AntiguoTestamento'},
            'job': {'archivo': 'Job', 'capitulos': 42, 'testamento': 'AntiguoTestamento'},
            'salmos': {'archivo': 'Salmos', 'capitulos': 150, 'testamento': 'AntiguoTestamento'},
            'proverbios': {'archivo': 'Proverbios', 'capitulos': 31, 'testamento': 'AntiguoTestamento'},
            'eclesiastés': {'archivo': 'Eclesiastes', 'capitulos': 12, 'testamento': 'AntiguoTestamento'},
            'cantares': {'archivo': 'Cantares', 'capitulos': 8, 'testamento': 'AntiguoTestamento'},
            'isaías': {'archivo': 'Isaias', 'capitulos': 66, 'testamento': 'AntiguoTestamento'},
            'jeremías': {'archivo': 'Jeremias', 'capitulos': 52, 'testamento': 'AntiguoTestamento'},
            'lamentaciones': {'archivo': 'Lamentaciones', 'capitulos': 5, 'testamento': 'AntiguoTestamento'},
            'ezequiel': {'archivo': 'Ezequiel', 'capitulos': 48, 'testamento': 'AntiguoTestamento'},
            'daniel': {'archivo': 'Daniel', 'capitulos': 12, 'testamento': 'AntiguoTestamento'},
            'oseas': {'archivo': 'Oseas', 'capitulos': 14, 'testamento': 'AntiguoTestamento'},
            'joel': {'archivo': 'Joel', 'capitulos': 3, 'testamento': 'AntiguoTestamento'},
            'amós': {'archivo': 'Amos', 'capitulos': 9, 'testamento': 'AntiguoTestamento'},
            'abdías': {'archivo': 'Abdias', 'capitulos': 1, 'testamento': 'AntiguoTestamento'},
            'jonás': {'archivo': 'Jonas', 'capitulos': 4, 'testamento': 'AntiguoTestamento'},
            'miqueas': {'archivo': 'Miqueas', 'capitulos': 7, 'testamento': 'AntiguoTestamento'},
            'nahúm': {'archivo': 'Nahum', 'capitulos': 3, 'testamento': 'AntiguoTestamento'},
            'habacuc': {'archivo': 'Habacuc', 'capitulos': 3, 'testamento': 'AntiguoTestamento'},
            'sofonías': {'archivo': 'Sofonias', 'capitulos': 3, 'testamento': 'AntiguoTestamento'},
            'hageo': {'archivo': 'Hageo', 'capitulos': 2, 'testamento': 'AntiguoTestamento'},
            'zacarías': {'archivo': 'Zacarias', 'capitulos': 14, 'testamento': 'AntiguoTestamento'},
            'malaquías': {'archivo': 'Malaquias', 'capitulos': 4, 'testamento': 'AntiguoTestamento'},
            
            # Nuevo Testamento
            'mateo': {'archivo': 'Mateo', 'capitulos': 28, 'testamento': 'NuevoTestamento'},
            'marcos': {'archivo': 'Marcos', 'capitulos': 16, 'testamento': 'NuevoTestamento'},
            'lucas': {'archivo': 'Lucas', 'capitulos': 24, 'testamento': 'NuevoTestamento'},
            'juan': {'archivo': 'Juan', 'capitulos': 21, 'testamento': 'NuevoTestamento'},
            'hechos': {'archivo': 'Hechos', 'capitulos': 28, 'testamento': 'NuevoTestamento'},
            'romanos': {'archivo': 'Romanos', 'capitulos': 16, 'testamento': 'NuevoTestamento'},
            '1 corintios': {'archivo': '1Corintios', 'capitulos': 16, 'testamento': 'NuevoTestamento'},
            '2 corintios': {'archivo': '2Corintios', 'capitulos': 13, 'testamento': 'NuevoTestamento'},
            'gálatas': {'archivo': 'Galatas', 'capitulos': 6, 'testamento': 'NuevoTestamento'},
            'efesios': {'archivo': 'Efesios', 'capitulos': 6, 'testamento': 'NuevoTestamento'},
            'filipenses': {'archivo': 'Filipenses', 'capitulos': 4, 'testamento': 'NuevoTestamento'},
            'colosenses': {'archivo': 'Colosenses', 'capitulos': 4, 'testamento': 'NuevoTestamento'},
            '1 tesalonicenses': {'archivo': '1Tesalonicenses', 'capitulos': 5, 'testamento': 'NuevoTestamento'},
            '2 tesalonicenses': {'archivo': '2Tesalonicenses', 'capitulos': 3, 'testamento': 'NuevoTestamento'},
            '1 timoteo': {'archivo': '1Timoteo', 'capitulos': 6, 'testamento': 'NuevoTestamento'},
            '2 timoteo': {'archivo': '2Timoteo', 'capitulos': 4, 'testamento': 'NuevoTestamento'},
            'tito': {'archivo': 'Tito', 'capitulos': 3, 'testamento': 'NuevoTestamento'},
            'filemón': {'archivo': 'Filemon', 'capitulos': 1, 'testamento': 'NuevoTestamento'},
            'hebreos': {'archivo': 'Hebreos', 'capitulos': 13, 'testamento': 'NuevoTestamento'},
            'santiago': {'archivo': 'Santiago', 'capitulos': 5, 'testamento': 'NuevoTestamento'},
            '1 pedro': {'archivo': '1Pedro', 'capitulos': 5, 'testamento': 'NuevoTestamento'},
            '2 pedro': {'archivo': '2Pedro', 'capitulos': 3, 'testamento': 'NuevoTestamento'},
            '1 juan': {'archivo': '1Juan', 'capitulos': 5, 'testamento': 'NuevoTestamento'},
            '2 juan': {'archivo': '2Juan', 'capitulos': 1, 'testamento': 'NuevoTestamento'},
            '3 juan': {'archivo': '3Juan', 'capitulos': 1, 'testamento': 'NuevoTestamento'},
            'judas': {'archivo': 'Judas', 'capitulos': 1, 'testamento': 'NuevoTestamento'},
            'apocalipsis': {'archivo': 'Apocalipsis', 'capitulos': 22, 'testamento': 'NuevoTestamento'}
        }
    
    def detectar_pantallas(self):
        """Detecta las pantallas disponibles"""
        try:
            self.monitores = get_monitors()
            if len(self.monitores) > 1:
                self.pantalla_proyeccion = self.monitores[1]
                print(f"Pantalla secundaria detectada: {self.pantalla_proyeccion}")
            else:
                self.pantalla_proyeccion = self.monitores[0]
                print("Solo se detectó una pantalla. Usando la misma para proyección.")
        except Exception as e:
            print(f"Error detectando pantallas: {e}")
            self.pantalla_proyeccion = None
    
    def normalizar_referencia(self, referencia):
        """Normaliza la referencia para diferentes formatos"""
        referencia = referencia.strip()
        
        # Mapa de abreviaturas comunes
        abreviaturas = {
            'gn': 'génesis', 'ex': 'éxodo', 'lv': 'levítico', 'nm': 'números',
            'dt': 'deuteronomio', 'jos': 'josué', 'jue': 'jueces', 'rt': 'rut',
            '1s': '1 samuel', '2s': '2 samuel', '1r': '1 reyes', '2r': '2 reyes',
            '1cr': '1 crónicas', '2cr': '2 crónicas', 'esd': 'esdras', 'neh': 'nehemías',
            'est': 'ester', 'job': 'job', 'sal': 'salmos', 'pr': 'proverbios',
            'ec': 'eclesiastés', 'cnt': 'cantares', 'is': 'isaías', 'jer': 'jeremías',
            'lam': 'lamentaciones', 'ez': 'ezequiel', 'dn': 'daniel', 'os': 'oseas',
            'jl': 'joel', 'am': 'amós', 'abd': 'abdías', 'jon': 'jonás',
            'miq': 'miqueas', 'nah': 'nahúm', 'hab': 'habacuc', 'sof': 'sofonías',
            'hag': 'hageo', 'zac': 'zacarías', 'mal': 'malaquías',
            'mt': 'mateo', 'mc': 'marcos', 'lc': 'lucas', 'jn': 'juan',
            'juan': 'juan', 'hch': 'hechos', 'rom': 'romanos', 'ro': 'romanos',
            '1co': '1 corintios', '2co': '2 corintios', 'ga': 'gálatas',
            'ef': 'efesios', 'fil': 'filipenses', 'col': 'colosenses',
            '1ts': '1 tesalonicenses', '2ts': '2 tesalonicenses', '1ti': '1 timoteo',
            '2ti': '2 timoteo', 'tit': 'tito', 'flm': 'filemón', 'heb': 'hebreos',
            'stg': 'santiago', '1p': '1 pedro', '2p': '2 pedro', '1jn': '1 juan',
            '2jn': '2 juan', '3jn': '3 juan', 'jud': 'judas', 'ap': 'apocalipsis'
        }
        
        # Separar libro del resto
        partes = referencia.split()
        if len(partes) >= 2:
            libro = partes[0].lower()
            resto = ' '.join(partes[1:])
            
            # Verificar si es abreviatura
            if libro in abreviaturas:
                return f"{abreviaturas[libro]} {resto}"
        
        return referencia.lower()
    
    def parsear_referencia(self, referencia):
        """Parsea una referencia bíblica y devuelve (libro, capitulo, versiculo)"""
        referencia = referencia.strip()
        
        # Patrones posibles:
        # 1. "Génesis 1:1" - libro completo
        # 2. "Gn 1:1" - abreviatura
        # 3. "1:1" - solo capítulo y versículo (usa último libro)
        # 4. "Juan 3" - solo capítulo (sin versículo)
        
        # Patrón para "libro capítulo:versículo" o "libro capítulo"
        patron_completo = r'^([a-zA-Z0-9\s]+?)\s*(\d+)(?::(\d+))?$'
        match = re.match(patron_completo, referencia, re.IGNORECASE)
        
        if match:
            libro = match.group(1).strip().lower()
            capitulo = int(match.group(2))
            versiculo = int(match.group(3)) if match.group(3) else None
            return libro, capitulo, versiculo
        
        # Patrón para solo "capítulo:versículo" (ej: "1:1")
        patron_solo = r'^(\d+):(\d+)$'
        match = re.match(patron_solo, referencia)
        
        if match:
            capitulo = int(match.group(1))
            versiculo = int(match.group(2))
            # Usar el último libro usado
            return self.ultimo_libro.lower(), capitulo, versiculo
        
        return None, None, None
    
    def obtener_texto_biblico_scraping(self, referencia):
        """Obtiene el texto bíblico mediante web scraping de mibibliavirtual.com"""
        # Parsear la referencia
        libro, capitulo, versiculo = self.parsear_referencia(referencia)
        
        if not libro:
            return None
        
        # Actualizar último libro usado
        self.ultimo_libro = libro
        if capitulo:
            self.ultimo_capitulo = capitulo
        
        # Crear clave de caché
        if versiculo:
            cache_key = f"{libro}_{capitulo}_{versiculo}"
            referencia_completa = f"{libro.title()} {capitulo}:{versiculo}"
        else:
            cache_key = f"{libro}_{capitulo}"
            referencia_completa = f"{libro.title()} {capitulo}"
        
        # Verificar caché
        if cache_key in self.biblia_cache:
            print(f"Usando caché para: {referencia_completa}")
            return self.biblia_cache[cache_key]
        
        try:
            # Buscar el libro en el mapeo
            libro_info = None
            libro_nombre = None
            for key, info in self.libros.items():
                if libro in key or key in libro:
                    libro_info = info
                    libro_nombre = key
                    break
            
            if not libro_info:
                print(f"Libro no encontrado: {libro}")
                return None
            
            # Construir URL del capítulo
            if capitulo <= libro_info['capitulos']:
                url = f"{self.base_url}/{libro_info['testamento']}/{libro_info['archivo']}/{libro_info['archivo']}{capitulo}.htm"
                
                print(f"Accediendo a capítulo: {url}")
                
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    if versiculo:
                        # Buscar el versículo específico
                        texto_encontrado = self.buscar_versiculo_en_html(soup, versiculo)
                        
                        if texto_encontrado:
                            texto_completo = f"{texto_encontrado}\n\n{libro_nombre.title()} {capitulo}:{versiculo} (RV1960)"
                            self.biblia_cache[cache_key] = texto_completo
                            return texto_completo
                        else:
                            # Si no encuentra el versículo exacto, mostrar mensaje
                            return f"Versículo {versiculo} no encontrado en {libro_nombre.title()} {capitulo}"
                    else:
                        # Mostrar todo el capítulo (primeros versículos)
                        return self.obtener_capitulo_completo(soup, libro_nombre, capitulo)
                else:
                    print(f"Error al obtener capítulo: {response.status_code}")
                    return None
            else:
                print(f"Capítulo {capitulo} no existe en {libro_nombre}")
                return None
                
        except Exception as e:
            print(f"Error en obtener_texto_biblico_scraping: {e}")
            return None
    
    def buscar_versiculo_en_html(self, soup, versiculo_buscado):
        """Busca un versículo específico en el HTML del capítulo"""
        # Buscar por el número del versículo
        # En mibibliavirtual, los versículos suelen estar en párrafos o divs
        
        # Método 1: Buscar elementos que contengan el número del versículo
        patron_versiculo = re.compile(rf'^{versiculo_buscado}\s+|[{versiculo_buscado}]\s+')
        
        for elemento in soup.find_all(['p', 'div', 'span', 'font']):
            texto = elemento.get_text().strip()
            
            # Verificar si el elemento contiene el versículo
            if re.search(patron_versiculo, texto):
                # Limpiar el texto
                texto_limpio = re.sub(r'^\s*\d+\s*', '', texto)  # Quitar número al inicio
                texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
                
                if texto_limpio:
                    return texto_limpio[0].upper() + texto_limpio[1:]
            
            # También buscar en elementos hijos
            for hijo in elemento.find_all(['b', 'strong', 'a']):
                if hijo.get_text().strip() == str(versiculo_buscado):
                    # Encontró el número, buscar el texto siguiente
                    texto_completo = elemento.get_text().strip()
                    texto_limpio = re.sub(r'^\s*\d+\s*', '', texto_completo)
                    texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
                    if texto_limpio:
                        return texto_limpio[0].upper() + texto_limpio[1:]
        
        # Método 2: Buscar por patrones en todo el texto
        texto_completo = soup.get_text()
        lineas = texto_completo.split('\n')
        
        for linea in lineas:
            if re.search(rf'^{versiculo_buscado}\s', linea.strip()):
                texto_limpio = re.sub(r'^\s*\d+\s*', '', linea.strip())
                if texto_limpio:
                    return texto_limpio[0].upper() + texto_limpio[1:]
        
        return None
    
    def obtener_capitulo_completo(self, soup, libro_nombre, capitulo):
        """Obtiene el texto completo del capítulo (primeros versículos)"""
        versiculos = []
        
        # Buscar todos los versículos
        for i in range(1, 11):  # Primeros 10 versículos como muestra
            texto = self.buscar_versiculo_en_html(soup, i)
            if texto:
                versiculos.append(f"{i}. {texto}")
            else:
                break
        
        if versiculos:
            texto_capitulo = '\n\n'.join(versiculos)
            if len(versiculos) < 10:
                texto_completo = f"{texto_capitulo}\n\n{libro_nombre.title()} {capitulo} (RV1960)"
            else:
                texto_completo = f"{texto_capitulo}\n...\n\n{libro_nombre.title()} {capitulo} (RV1960 - Primeros versículos)"
            
            cache_key = f"{libro_nombre}_{capitulo}"
            self.biblia_cache[cache_key] = texto_completo
            return texto_completo
        
        return None
    
    def buscar_versiculo(self):
        """Busca y muestra un versículo"""
        referencia = self.entrada_versiculo.get().strip()
        if not referencia:
            messagebox.showwarning("Advertencia", "Por favor ingresa una referencia bíblica.")
            return
        
        # Deshabilitar botón mientras busca
        self.btn_buscar.config(state='disabled', text="Buscando...")
        self.estado_label.config(text="🔍 Buscando versículo...", foreground='orange')
        
        # Buscar en segundo plano
        thread = threading.Thread(target=self._buscar_versiculo_thread, args=(referencia,))
        thread.daemon = True
        thread.start()
    
    def _buscar_versiculo_thread(self, referencia):
        """Hilo para buscar versículo"""
        texto = self.obtener_texto_biblico_scraping(referencia)
        
        # Actualizar UI en el hilo principal
        self.root.after(0, self._mostrar_resultado, referencia, texto)
    
    def _mostrar_resultado(self, referencia, texto):
        """Muestra el resultado de la búsqueda"""
        # Rehabilitar botón
        self.btn_buscar.config(state='normal', text="Buscar y Mostrar")
        
        if texto is None:
            self.estado_label.config(text="❌ No se encontró el versículo", foreground='red')
            
            # Mostrar sugerencias
            libro, capitulo, versiculo = self.parsear_referencia(referencia)
            if libro and capitulo and not versiculo:
                sugerencia = f"{libro.title()} {capitulo}:1"
            elif libro and not capitulo:
                sugerencia = f"{libro.title()} 1:1"
            else:
                sugerencia = "Génesis 1:1"
            
            messagebox.showerror(
                "Error", 
                f"No se pudo encontrar '{referencia}'.\n\n"
                f"Prueba con:\n"
                f"• {sugerencia}\n"
                f"• Juan 3:16\n"
                f"• Salmos 23\n"
                f"• O usa el selector de libros"
            )
            return
        
        # Formatear texto completo
        texto_completo = texto
        
        # Guardar el último versículo buscado
        self.ultimo_versiculo = {
            'referencia': referencia,
            'texto_completo': texto_completo
        }
        
        self.estado_label.config(text="✅ Versículo encontrado", foreground='green')
        
        # Actualizar selector de libro
        libro, capitulo, versiculo = self.parsear_referencia(referencia)
        if libro:
            libro_titulo = libro.title()
            if libro_titulo in self.lista_libros_nombres:
                self.libro_var.set(libro_titulo)
            if capitulo:
                self.capitulo_var.set(str(capitulo))
        
        # Mostrar en pantalla secundaria si está activa
        if self.pantalla_secundaria and self.pantalla_secundaria.winfo_exists():
            self.actualizar_pantalla_secundaria(texto_completo)
        else:
            messagebox.showinfo("Éxito", "Versículo encontrado. Inicia la pantalla secundaria para verlo.")
    
    def buscar_por_selector(self):
        """Busca usando el selector de libro y capítulo"""
        libro = self.libro_var.get()
        capitulo = self.capitulo_var.get()
        
        if not libro or not capitulo:
            messagebox.showwarning("Advertencia", "Selecciona un libro y capítulo.")
            return
        
        referencia = f"{libro} {capitulo}"
        self.entrada_versiculo.delete(0, tk.END)
        self.entrada_versiculo.insert(0, referencia)
        self.buscar_versiculo()
    
    def crear_interfaz_principal(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Control de Versículos Bíblicos\nReina Valera 1960", 
            font=('Arial', 16, 'bold'),
            justify='center'
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Info del scraping
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky='ew')
        
        ttk.Label(
            info_frame, 
            text="📖 Usando mibibliavirtual.com (RV1960) - Sin límites de API",
            font=('Arial', 9),
            foreground='green'
        ).pack()
        
        # Selector de libro y capítulo
        selector_frame = ttk.LabelFrame(main_frame, text="Selector Rápido", padding="5")
        selector_frame.grid(row=2, column=0, columnspan=4, sticky='ew', pady=5)
        
        ttk.Label(selector_frame, text="Libro:").grid(row=0, column=0, padx=5)
        self.libro_var = tk.StringVar()
        self.libro_combo = ttk.Combobox(
            selector_frame, 
            textvariable=self.libro_var,
            values=self.lista_libros_nombres,
            width=20,
            state='readonly'
        )
        self.libro_combo.grid(row=0, column=1, padx=5)
        self.libro_combo.set('Génesis')
        
        ttk.Label(selector_frame, text="Capítulo:").grid(row=0, column=2, padx=5)
        self.capitulo_var = tk.StringVar()
        self.capitulo_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.capitulo_var,
            values=[str(i) for i in range(1, 151)],
            width=10,
            state='readonly'
        )
        self.capitulo_combo.grid(row=0, column=3, padx=5)
        self.capitulo_combo.set('1')
        
        ttk.Button(
            selector_frame,
            text="Ir",
            command=self.buscar_por_selector
        ).grid(row=0, column=4, padx=5)
        
        # Entrada de versículo
        ttk.Label(main_frame, text="Ingresa el versículo:", 
                 font=('Arial', 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.entrada_versiculo = ttk.Entry(main_frame, width=30, font=('Arial', 11))
        self.entrada_versiculo.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        self.entrada_versiculo.bind('<Return>', lambda e: self.buscar_versiculo())
        
        # Botones principales
        self.btn_buscar = ttk.Button(
            main_frame, 
            text="Buscar", 
            command=self.buscar_versiculo
        )
        self.btn_buscar.grid(row=3, column=3, padx=5, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Agregar a Lista", 
            command=self.agregar_a_lista
        ).grid(row=4, column=2, padx=5, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Iniciar Pantalla", 
            command=self.iniciar_pantalla_secundaria
        ).grid(row=4, column=3, padx=5, pady=5)
        
        # Frame para la lista de versículos
        lista_frame = ttk.LabelFrame(main_frame, text="Lista de Versículos", padding="5")
        lista_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Listbox con scrollbar
        listbox_frame = ttk.Frame(lista_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lista_box = tk.Listbox(
            listbox_frame, 
            height=8, 
            yscrollcommand=scrollbar.set,
            font=('Arial', 10)
        )
        self.lista_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.lista_box.yview)
        
        # Botones para controlar la lista
        control_frame = ttk.Frame(lista_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            control_frame, 
            text="← Anterior", 
            command=self.versiculo_anterior
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Siguiente →", 
            command=self.versiculo_siguiente
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Eliminar", 
            command=self.eliminar_de_lista
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame, 
            text="Limpiar", 
            command=self.limpiar_lista
        ).pack(side=tk.LEFT, padx=5)
        
        # Estado del scraping
        self.estado_label = ttk.Label(
            main_frame, 
            text="✅ Conectado a mibibliavirtual.com",
            font=('Arial', 9),
            foreground='green'
        )
        self.estado_label.grid(row=6, column=0, columnspan=4, pady=5)
        
        # Ejemplos de uso
        ejemplos_frame = ttk.LabelFrame(main_frame, text="Ejemplos - Prueba escribir:", padding="5")
        ejemplos_frame.grid(row=7, column=0, columnspan=4, sticky='ew', pady=5)
        
        ejemplos = [
            "Génesis 1:1", "Juan 3:16", "Salmos 23",
            "1:1", "Romanos 8", "Mateo 5:3"
        ]
        
        for i, ejemplo in enumerate(ejemplos):
            btn_ejemplo = ttk.Button(
                ejemplos_frame, 
                text=ejemplo,
                command=lambda e=ejemplo: self.usar_ejemplo(e)
            )
            btn_ejemplo.grid(row=0, column=i, padx=2, pady=2)
        
        # Nota sobre búsquedas parciales
        nota_label = ttk.Label(
            main_frame,
            text="💡 Tip: Escribe '1:1' para ver el versículo 1 del capítulo 1 del último libro usado",
            font=('Arial', 8, 'italic'),
            foreground='blue'
        )
        nota_label.grid(row=8, column=0, columnspan=4, pady=2)
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Bind para selección en lista
        self.lista_box.bind('<<ListboxSelect>>', self.seleccionar_versiculo)
    
    def usar_ejemplo(self, ejemplo):
        """Usa un ejemplo de búsqueda"""
        self.entrada_versiculo.delete(0, tk.END)
        self.entrada_versiculo.insert(0, ejemplo)
        self.buscar_versiculo()
    
    def agregar_a_lista(self):
        """Agrega el versículo actual a la lista"""
        if not hasattr(self, 'ultimo_versiculo'):
            messagebox.showwarning("Advertencia", "Primero busca un versículo.")
            return
        
        # Agregar a la lista
        self.lista_versiculos.append(self.ultimo_versiculo.copy())
        
        # Actualizar Listbox
        ref = self.ultimo_versiculo['referencia']
        self.lista_box.insert(tk.END, f"{ref} (RV1960)")
        
        # Limpiar entrada
        self.entrada_versiculo.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", f"'{ref}' agregado a la lista.")
    
    def versiculo_siguiente(self):
        """Muestra el siguiente versículo de la lista"""
        if not self.lista_versiculos:
            return
        
        self.indice_actual = (self.indice_actual + 1) % len(self.lista_versiculos)
        self.mostrar_versiculo_actual()
    
    def versiculo_anterior(self):
        """Muestra el versículo anterior de la lista"""
        if not self.lista_versiculos:
            return
        
        self.indice_actual = (self.indice_actual - 1) % len(self.lista_versiculos)
        self.mostrar_versiculo_actual()
    
    def mostrar_versiculo_actual(self):
        """Muestra el versículo actual en la pantalla secundaria"""
        if self.lista_versiculos and self.indice_actual < len(self.lista_versiculos):
            versiculo = self.lista_versiculos[self.indice_actual]
            if self.pantalla_secundaria and self.pantalla_secundaria.winfo_exists():
                self.actualizar_pantalla_secundaria(versiculo['texto_completo'])
            
            # Seleccionar en la lista
            self.lista_box.selection_clear(0, tk.END)
            self.lista_box.selection_set(self.indice_actual)
            self.lista_box.see(self.indice_actual)
    
    def seleccionar_versiculo(self, event):
        """Maneja la selección de un versículo en la lista"""
        seleccion = self.lista_box.curselection()
        if seleccion:
            self.indice_actual = seleccion[0]
            self.mostrar_versiculo_actual()
    
    def eliminar_de_lista(self):
        """Elimina el versículo seleccionado de la lista"""
        seleccion = self.lista_box.curselection()
        if seleccion:
            indice = seleccion[0]
            self.lista_box.delete(indice)
            del self.lista_versiculos[indice]
            
            if self.lista_versiculos:
                if indice >= len(self.lista_versiculos):
                    self.indice_actual = len(self.lista_versiculos) - 1
                else:
                    self.indice_actual = indice
                self.mostrar_versiculo_actual()
            else:
                if self.pantalla_secundaria and self.pantalla_secundaria.winfo_exists():
                    self.actualizar_pantalla_secundaria("")
    
    def limpiar_lista(self):
        """Limpia toda la lista de versículos"""
        self.lista_box.delete(0, tk.END)
        self.lista_versiculos.clear()
        self.indice_actual = 0
        
        if self.pantalla_secundaria and self.pantalla_secundaria.winfo_exists():
            self.actualizar_pantalla_secundaria("")
    
    def iniciar_pantalla_secundaria(self):
        """Inicia la ventana en la segunda pantalla"""
        if self.pantalla_secundaria and self.pantalla_secundaria.winfo_exists():
            self.pantalla_secundaria.lift()
            return
        
        # Crear nueva ventana
        self.pantalla_secundaria = tk.Toplevel(self.root)
        self.pantalla_secundaria.title("Versículo Bíblico - RV1960")
        
        # Configurar para segunda pantalla
        if hasattr(self, 'pantalla_proyeccion') and self.pantalla_proyeccion:
            x = self.pantalla_proyeccion.x
            y = self.pantalla_proyeccion.y
            width = self.pantalla_proyeccion.width
            height = self.pantalla_proyeccion.height
            self.pantalla_secundaria.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configurar modo pantalla completa
        self.pantalla_secundaria.attributes('-fullscreen', True)
        self.pantalla_secundaria.configure(bg='black')
        
        # Frame para el versículo
        frame_versiculo = tk.Frame(self.pantalla_secundaria, bg='black')
        frame_versiculo.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Texto del versículo
        self.texto_versiculo = tk.Text(
            frame_versiculo, 
            wrap=tk.WORD,
            bg='black',
            fg='white',
            font=('Arial', self.tamano_fuente, 'bold'),
            insertbackground='white',
            relief=tk.FLAT,
            padx=30,
            pady=30
        )
        self.texto_versiculo.pack(fill=tk.BOTH, expand=True)
        
        # Panel de control en la pantalla secundaria
        control_panel = tk.Frame(self.pantalla_secundaria, bg='#333333')
        control_panel.place(relx=0.5, rely=0.95, anchor='center')
        
        tk.Button(
            control_panel,
            text="← Anterior",
            bg='#444444',
            fg='white',
            font=('Arial', 12),
            command=self.versiculo_anterior
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(
            control_panel,
            text="Siguiente →",
            bg='#444444',
            fg='white',
            font=('Arial', 12),
            command=self.versiculo_siguiente
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(
            control_panel,
            text="A+",
            bg='#444444',
            fg='white',
            font=('Arial', 12, 'bold'),
            command=self.aumentar_fuente
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(
            control_panel,
            text="A-",
            bg='#444444',
            fg='white',
            font=('Arial', 12, 'bold'),
            command=self.disminuir_fuente
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(
            control_panel,
            text="✕ Salir",
            bg='#c0392b',
            fg='white',
            font=('Arial', 12),
            command=self.salir_pantalla_completa
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Bind teclas de navegación
        self.pantalla_secundaria.bind('<Escape>', lambda e: self.salir_pantalla_completa())
        self.pantalla_secundaria.bind('<Right>', lambda e: self.versiculo_siguiente())
        self.pantalla_secundaria.bind('<Left>', lambda e: self.versiculo_anterior())
        self.pantalla_secundaria.bind('<plus>', lambda e: self.aumentar_fuente())
        self.pantalla_secundaria.bind('<minus>', lambda e: self.disminuir_fuente())
        
        # Mostrar versículo actual si existe
        if self.lista_versiculos:
            self.mostrar_versiculo_actual()
    
    def aumentar_fuente(self):
        """Aumenta el tamaño de la fuente"""
        self.tamano_fuente = min(120, self.tamano_fuente + 4)
        if self.texto_versiculo:
            self.texto_versiculo.config(font=('Arial', self.tamano_fuente, 'bold'))
    
    def disminuir_fuente(self):
        """Disminuye el tamaño de la fuente"""
        self.tamano_fuente = max(20, self.tamano_fuente - 4)
        if self.texto_versiculo:
            self.texto_versiculo.config(font=('Arial', self.tamano_fuente, 'bold'))
    
    def actualizar_pantalla_secundaria(self, texto):
        """Actualiza el texto en la pantalla secundaria"""
        if self.texto_versiculo and self.texto_versiculo.winfo_exists():
            self.texto_versiculo.delete(1.0, tk.END)
            self.texto_versiculo.insert(1.0, texto)
            self.texto_versiculo.see(1.0)
    
    def salir_pantalla_completa(self):
        """Sale del modo pantalla completa"""
        if self.pantalla_secundaria:
            self.pantalla_secundaria.destroy()
            self.pantalla_secundaria = None
            self.texto_versiculo = None
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BibliaApp()
    app.run()
