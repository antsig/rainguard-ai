def classify_risk(rainfall_mm: float):
    """
    Classify flood risk based on predicted rainfall.
    Rainfall	Risk
    <10 mm	    Low
    10–30 mm	Medium
    >30 mm	    High
    """
    if rainfall_mm < 10.0:
        return "Low"
    elif 10.0 <= rainfall_mm <= 30.0:
        return "Medium"
    else:
        return "High"

def get_recommendations(risk_level: str):
    """
    Provide actionable preparedness tips based on the risk level.
    """
    if risk_level == "High":
        return [
            "Pantau terus ketinggian debit air sungai atau saluran terdekat.",
            "Pindahkan barang-barang berharga dan dokumen ke tempat yang lebih tinggi.",
            "Siapkan Tas Siaga Bencana (Pakaian, Obat, Senter, Dokumen).",
            "Pantau peringatan resmi dari pemerintah/BMKG secara berkala.",
            "Siapkan rute dan rencana evakuasi mandiri."
        ]
    elif risk_level == "Medium":
        return [
            "Bersihkan selokan dan saluran air di sekitar rumah.",
            "Tetap waspada terhadap informasi cuaca terkini.",
            "Hindari bepergian ke daerah dataran rendah/rawan banjir saat hujan deras."
        ]
    else:
        return [
            "Lakukan aktivitas seperti normal.",
            "Tetap jaga kebersihan lingkungan dan saluran air."
        ]

if __name__ == "__main__":
    test_rainfalls = [5.0, 15.0, 35.0]
    for rf in test_rainfalls:
        risk = classify_risk(rf)
        recs = get_recommendations(risk)
        print(f"Rainfall: {rf}mm -> Risk: {risk}")
        for r in recs:
            print(f" - {r}")
