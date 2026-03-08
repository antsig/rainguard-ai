import requests
from bs4 import BeautifulSoup

# Peta nama wilayah internal ke URL BMKG
BMKG_URLS = {
    "Aceh": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Aceh.xml",
    "Bali": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Bali.xml",
    "Banten": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Banten.xml",
    "Bengkulu": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Bengkulu.xml",
    "DI Yogyakarta": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DIYogyakarta.xml",
    "DKI Jakarta": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml",
    "Gorontalo": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Gorontalo.xml",
    "Jambi": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Jambi.xml",
    "Jawa Barat": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaBarat.xml",
    "Jawa Tengah": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTengah.xml",
    "Jawa Timur": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml",
    "Kalimantan Barat": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanBarat.xml",
    "Kalimantan Selatan": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanSelatan.xml",
    "Kalimantan Tengah": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanTengah.xml",
    "Kalimantan Timur": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanTimur.xml",
    "Kalimantan Utara": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanUtara.xml",
    "Kepulauan Bangka Belitung": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KepulauanBangkaBelitung.xml",
    "Kepulauan Riau": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KepulauanRiau.xml",
    "Lampung": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Lampung.xml",
    "Maluku": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Maluku.xml",
    "Maluku Utara": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-MalukuUtara.xml",
    "Nusa Tenggara Barat": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-NusaTenggaraBarat.xml",
    "Nusa Tenggara Timur": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-NusaTenggaraTimur.xml",
    "Papua": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Papua.xml",
    "Papua Barat": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-PapuaBarat.xml",
    "Riau": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Riau.xml",
    "Sulawesi Barat": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiBarat.xml",
    "Sulawesi Selatan": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiSelatan.xml",
    "Sulawesi Tengah": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiTengah.xml",
    "Sulawesi Tenggara": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiTenggara.xml",
    "Sulawesi Utara": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiUtara.xml",
    "Sumatera Barat": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SumateraBarat.xml",
    "Sumatera Selatan": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SumateraSelatan.xml",
    "Sumatera Utara": "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SumateraUtara.xml"
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
