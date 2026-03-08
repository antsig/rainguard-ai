import requests
from bs4 import BeautifulSoup

# Peta nama wilayah internal ke URL BMKG
BMKG_URLS = {
    "Jakarta": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml",
    "Bandung": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaBarat.xml",
    "Surabaya": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml",
    "Yogyakarta": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DIYogyakarta.xml",
    "Semarang": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTengah.xml"
}

# Mapping kode cuaca BMKG ke teks deskriptif
WEATHER_CODES = {
    "0": "Cerah", "1": "Cerah Berawan", "2": "Cerah Berawan", "3": "Berawan",
    "4": "Berawan Tebal", "5": "Udara Kabur", "10": "Asap", "45": "Kabut",
    "60": "Hujan Ringan", "61": "Hujan Sedang", "63": "Hujan Lebat", "80": "Hujan Lokal",
    "95": "Hujan Petir", "97": "Hujan Petir"
}

def get_realtime_weather(region: str) -> dict:
    """
    Mengambil data cuaca real-time dari API publik BMKG untuk wilayah yang dipilih.
    """
    if region not in BMKG_URLS:
        return {"error": "Wilayah tidak didukung BMKG"}

    try:
        url = BMKG_URLS[region]
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return {"error": "Gagal terhubung ke BMKG"}
            
        # Parse XML dengan xml agar tag yang error dilewati
        soup = BeautifulSoup(response.content, features="xml")
        
        # Cari area yang sesuai
        target_area = None
        for area in soup.find_all('area'):
            desc = area.get('description', '')
            if region.lower() in desc.lower():
                target_area = area
                break
                
        if target_area is None:
            # Fallback area pertama
            target_area = soup.find('area')
            
        if target_area is None:
            return {
                "source": "BMKG Real-time (Fallback)",
                "weather_desc": "Berawan",
                "weather_code": "3",
                "temperature_c": "28",
                "humidity_percent": "75"
            }

        # Extract values
        weather_param = target_area.find('parameter', attrs={'id': 'weather'})
        t_param = target_area.find('parameter', attrs={'id': 't'})
        hu_param = target_area.find('parameter', attrs={'id': 'hu'})
        
        weather_val = weather_param.find('value').text if weather_param and weather_param.find('value') else "0"
        
        # Temperature usually has child value inside timerange but some has unit='C'
        # We find the first <value> regardless, but try to find the one inside timerange
        temp_val = "N/A"
        if t_param:
            for val in t_param.find_all('value'):
                temp_val = val.text
                break
                    
        hu_val = "80"
        if hu_param:
            hu_val_node = hu_param.find('value')
            if hu_val_node: hu_val = hu_val_node.text
            
        desc = WEATHER_CODES.get(weather_val, "Berawan")
        
        return {
            "source": "BMKG Terkini",
            "weather_desc": desc,
            "weather_code": weather_val,
            "temperature_c": temp_val,
            "humidity_percent": hu_val
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(get_realtime_weather("Jakarta"))
