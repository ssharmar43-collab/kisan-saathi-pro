"""
╔══════════════════════════════════════════════════════════════════════╗
║   KISAN SAATHI PRO v2.0 — Enhanced Edition                          ║
║   Features: Remember Login, Location Autocomplete, Real-time         ║
║   Weather Forecast, Disease Detection, AI Assistant                  ║
║   pip install customtkinter requests pillow                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import sqlite3
import hashlib
import requests
import json
import threading
import time
from datetime import date, datetime
import os
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ── Palette ────────────────────────────────────────────────────────────────────
G1   = "#00ff88"   # neon green
G2   = "#00c55e"   # mid green
G3   = "#00843d"   # dark green
BG   = "#080d09"   # near-black background
C1   = "#0c1a10"   # card level 1
C2   = "#111f15"   # card level 2
C3   = "#172b1c"   # card level 3
ACC  = "#39ff8f"   # accent
WARN = "#ffb300"   # amber warning
ERR  = "#ff4d6d"   # red error
BLUE = "#38bdf8"   # info blue
TXT  = "#e8f5e9"   # primary text
TXM  = "#81c784"   # muted text

# ── India Location Database ────────────────────────────────────────────────────
INDIA_STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
    "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
    "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
    "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
    "Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
    "Delhi","Jammu and Kashmir","Ladakh","Chandigarh","Puducherry"
]

INDIA_CITIES = {
    "Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946), "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707), "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867), "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714), "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462), "Kanpur": (26.4499, 80.3319),
    "Nagpur": (21.1458, 79.0882), "Patna": (25.5941, 85.1376),
    "Indore": (22.7196, 75.8577), "Bhopal": (23.2599, 77.4126),
    "Ludhiana": (30.9010, 75.8573), "Agra": (27.1767, 78.0081),
    "Varanasi": (25.3176, 82.9739), "Amritsar": (31.6340, 74.8723),
    "Chandigarh": (30.7333, 76.7794), "Surat": (21.1702, 72.8311),
    "Visakhapatnam": (17.6868, 83.2185), "Kochi": (9.9312, 76.2673),
    "Coimbatore": (11.0168, 76.9558), "Madurai": (9.9252, 78.1198),
    "Thiruvananthapuram": (8.5241, 76.9366), "Bhubaneswar": (20.2961, 85.8245),
    "Guwahati": (26.1445, 91.7362), "Dehradun": (30.3165, 78.0322),
    "Jodhpur": (26.2389, 73.0243), "Udaipur": (24.5854, 73.7125),
    "Shimla": (31.1048, 77.1734), "Jammu": (32.7266, 74.8570),
    "Srinagar": (34.0837, 74.7973), "Ranchi": (23.3441, 85.3096),
    "Gwalior": (26.2183, 78.1828), "Jabalpur": (23.1815, 79.9864),
    "Meerut": (28.9845, 77.7064), "Nashik": (19.9975, 73.7898),
    "Aurangabad": (19.8762, 75.3433), "Solapur": (17.6599, 75.9064),
    "Rajkot": (22.3039, 70.8022), "Vadodara": (22.3072, 73.1812),
    "Faridabad": (28.4089, 77.3178), "Gurugram": (28.4595, 77.0266),
    "Noida": (28.5355, 77.3910), "Thane": (19.2183, 72.9781),
    "Navi Mumbai": (19.0330, 73.0297), "Mysuru": (12.2958, 76.6394),
    "Hubli": (15.3647, 75.1240), "Mangaluru": (12.9141, 74.8560),
    "Tiruchirappalli": (10.7905, 78.7047), "Salem": (11.6643, 78.1460),
    "Vijayawada": (16.5062, 80.6480), "Guntur": (16.3067, 80.4365),
    "Warangal": (17.9784, 79.5941), "Nellore": (14.4426, 79.9865),
    "Allahabad": (25.4358, 81.8463), "Prayagraj": (25.4358, 81.8463),
    "Gorakhpur": (26.7606, 83.3732), "Aligarh": (27.8974, 78.0880),
    "Moradabad": (28.8386, 78.7733), "Bareilly": (28.3670, 79.4304),
    "Saharanpur": (29.9680, 77.5510), "Mathura": (27.4924, 77.6737),
    "Hapur": (28.7301, 77.7763), "Rohtak": (28.8955, 76.6066),
    "Hisar": (29.1492, 75.7217), "Karnal": (29.6857, 76.9905),
    "Panipat": (29.3909, 76.9635), "Ambala": (30.3752, 76.7821),
    "Yamunanagar": (30.1290, 77.2674), "Bathinda": (30.2110, 74.9455),
    "Patiala": (30.3398, 76.3869), "Firozpur": (30.9254, 74.6089),
    "Jalandhar": (31.3260, 75.5762), "Pathankot": (32.2643, 75.6421),
    "Hoshiarpur": (31.5143, 75.9116), "Moga": (30.8161, 75.1723),
    "Kota": (25.2138, 75.8648), "Ajmer": (26.4499, 74.6399),
    "Bikaner": (28.0229, 73.3119), "Alwar": (27.5530, 76.6346),
    "Sikar": (27.6094, 75.1399), "Bharatpur": (27.2152, 77.4956),
    "Dhanbad": (23.7957, 86.4304), "Bokaro": (23.6693, 86.1511),
    "Jamshedpur": (22.8046, 86.2029), "Muzaffarpur": (26.1209, 85.3647),
    "Bhagalpur": (25.2425, 86.9842), "Darbhanga": (26.1522, 85.8970),
    "Gaya": (24.7914, 84.9994), "Purnia": (25.7771, 87.4753),
    "Raipur": (21.2514, 81.6296), "Bilaspur": (22.0797, 82.1391),
    "Durg": (21.1904, 81.2849), "Korba": (22.3595, 82.7501),
    "Bhubaneswar": (20.2961, 85.8245), "Cuttack": (20.4625, 85.8830),
    "Rourkela": (22.2604, 84.8536), "Berhampur": (19.3150, 84.7941),
    "Vijaywada": (16.5062, 80.6480), "Tirupati": (13.6288, 79.4192),
    "Kakinada": (16.9891, 82.2475), "Anantapur": (14.6819, 77.6006),
    "Kurnool": (15.8281, 78.0373), "Rajahmundry": (17.0005, 81.8040),
    "Nanded": (19.1383, 77.3210), "Kolhapur": (16.7050, 74.2433),
    "Amravati": (20.9374, 77.7796), "Sangli": (16.8524, 74.5815),
    "Malegaon": (20.5579, 74.5089), "Latur": (18.4088, 76.5604),
    "Dhule": (20.9042, 74.7749), "Ahmednagar": (19.0948, 74.7480),
    "Beed": (18.9890, 75.7595), "Jalgaon": (21.0077, 75.5626),
    "Anand": (22.5645, 72.9289), "Gandhinagar": (23.2156, 72.6369),
    "Junagadh": (21.5222, 70.4579), "Bhavnagar": (21.7645, 72.1519),
    "Jamnagar": (22.4707, 70.0577), "Mehsana": (23.5880, 72.3693),
    "Mangalore": (12.9141, 74.8560), "Davangere": (14.4644, 75.9218),
    "Bellary": (15.1394, 76.9214), "Bijapur": (16.8302, 75.7100),
    "Shimoga": (13.9299, 75.5681), "Tumkur": (13.3379, 77.1173),
    "Bidar": (17.9104, 77.5199), "Raichur": (16.2120, 77.3439),
    "Erode": (11.3410, 77.7172), "Vellore": (12.9165, 79.1325),
    "Thoothukudi": (8.7642, 78.1348), "Tirunelveli": (8.7139, 77.7567),
    "Thanjavur": (10.7870, 79.1378), "Dindigul": (10.3673, 77.9803),
    "Pondicherry": (11.9416, 79.8083), "Cuddalore": (11.7480, 79.7714),
    "Kozhikode": (11.2588, 75.7804), "Thrissur": (10.5276, 76.2144),
    "Kannur": (11.8745, 75.3704), "Kollam": (8.8932, 76.6141),
    "Palakkad": (10.7867, 76.6548), "Malappuram": (11.0510, 76.0711),
    "Ghaziabad": (28.6692, 77.4538), "Muzaffarnagar": (29.4727, 77.7085),
    "Firozabad": (27.1591, 78.3957), "Loni": (28.7500, 77.2900),
}

ALL_CITY_NAMES = sorted(INDIA_CITIES.keys())

# ── Disease Knowledge Base ─────────────────────────────────────────────────────
DISEASE_DB = [
    {
        "name": "Rice Blast",
        "hindi": "धान का झुलसा",
        "crop": "Rice",
        "symptoms": ["grey spots", "diamond shaped lesion", "neck rot", "grey center", "brown border", "leaf blast", "white patch", "blast"],
        "cause": "Fungal – Magnaporthe oryzae",
        "treatment": "Spray Tricyclazole 75WP @ 0.06% or Isoprothiolane 40EC @ 1.5ml/L. Remove infected leaves.",
        "prevention": "Use resistant varieties. Avoid excess nitrogen. Maintain field hygiene.",
        "severity": "High",
        "icon": "🍚"
    },
    {
        "name": "Wheat Yellow Rust",
        "hindi": "गेहूं का पीला रतुआ",
        "crop": "Wheat",
        "symptoms": ["yellow stripe", "yellow pustule", "orange powder", "leaf yellowing", "rust", "stripe rust"],
        "cause": "Fungal – Puccinia striiformis",
        "treatment": "Spray Propiconazole 25EC @ 0.1% or Tebuconazole 250EC. Apply early morning.",
        "prevention": "Plant resistant varieties. Early sowing avoids peak infection period.",
        "severity": "High",
        "icon": "🌾"
    },
    {
        "name": "Late Blight (Potato/Tomato)",
        "hindi": "पछेती अंगमारी",
        "crop": "Potato / Tomato",
        "symptoms": ["water soaked", "dark brown", "white mold", "rapid spread", "leaf curl", "blight", "black patch", "spreading lesion"],
        "cause": "Oomycete – Phytophthora infestans",
        "treatment": "Metalaxyl+Mancozeb @ 0.25% spray. Remove and destroy infected plants. Avoid overhead irrigation.",
        "prevention": "Use certified seed. Ensure good drainage. Spray preventively before monsoon.",
        "severity": "Critical",
        "icon": "🥔"
    },
    {
        "name": "Powdery Mildew",
        "hindi": "चूर्णिल आसिता",
        "crop": "Multiple Crops",
        "symptoms": ["white powder", "powdery coating", "white film", "flour like", "grey white dust", "mildew"],
        "cause": "Fungal – Erysiphe spp.",
        "treatment": "Wettable Sulphur 80WP @ 0.2% or Triadimefon 25WP. Apply 2-3 times at 10-day intervals.",
        "prevention": "Avoid overcrowding. Ensure air circulation. Remove infected plant parts early.",
        "severity": "Medium",
        "icon": "🌿"
    },
    {
        "name": "Brown Plant Hopper (BPH)",
        "hindi": "भूरा फुदका",
        "crop": "Rice",
        "symptoms": ["yellowing base", "hopper burn", "dead circle", "brown small insect", "wilting patch", "bph", "hopper"],
        "cause": "Insect – Nilaparvata lugens",
        "treatment": "Imidacloprid 17.8SL @ 0.3ml/L. Drain field for 3 days. Avoid excess nitrogen.",
        "prevention": "Use BPH resistant varieties. Release natural enemies (Mirid bugs).",
        "severity": "High",
        "icon": "🌾"
    },
    {
        "name": "Stem Borer",
        "hindi": "तना छेदक",
        "crop": "Maize / Rice",
        "symptoms": ["dead heart", "white ear", "stem hole", "borer damage", "frass", "sawdust", "entry hole", "stem borer"],
        "cause": "Insect – Chilo suppressalis / Sesamia inferens",
        "treatment": "Chlorpyriphos 20EC @ 2.5ml/L in whorl. Apply Trichogramma cards (50,000/ha).",
        "prevention": "Crop rotation. Remove and burn stubble after harvest.",
        "severity": "Medium",
        "icon": "🌽"
    },
    {
        "name": "Bacterial Blight",
        "hindi": "जीवाणु अंगमारी",
        "crop": "Rice / Cotton",
        "symptoms": ["water soaked edge", "yellow margin", "wilting", "leaf blight", "yellow leaf edge", "bacterial"],
        "cause": "Bacterial – Xanthomonas oryzae",
        "treatment": "Copper oxychloride 50WP @ 0.3% + Streptomycin 100ppm. Avoid flood irrigation.",
        "prevention": "Use disease-free seeds. Balanced fertilization. Avoid wounding crops.",
        "severity": "High",
        "icon": "🌱"
    },
    {
        "name": "Alternaria Leaf Blight",
        "hindi": "अल्टेरनेरिया पत्ती झुलसा",
        "crop": "Mustard / Potato",
        "symptoms": ["concentric ring", "target board", "dark circle", "brown spot ring", "alternaria", "circular lesion"],
        "cause": "Fungal – Alternaria spp.",
        "treatment": "Mancozeb 75WP @ 0.25% or Iprodione 50WP. Spray at first sign.",
        "prevention": "Crop rotation. Use healthy seeds. Avoid dense planting.",
        "severity": "Medium",
        "icon": "🌻"
    },
    {
        "name": "Fusarium Wilt",
        "hindi": "उकठा रोग",
        "crop": "Tomato / Chickpea / Cotton",
        "symptoms": ["yellowing lower leaf", "wilt", "vascular browning", "collapse", "sudden wilt", "fusarium"],
        "cause": "Fungal – Fusarium oxysporum",
        "treatment": "Drench with Carbendazim 50WP @ 0.1%. Remove infected plants. No effective spray once infected.",
        "prevention": "Resistant varieties. Soil solarisation. Seed treatment with Trichoderma.",
        "severity": "High",
        "icon": "🍅"
    },
    {
        "name": "Red Rot (Sugarcane)",
        "hindi": "लाल सड़न",
        "crop": "Sugarcane",
        "symptoms": ["red inside stalk", "sour smell", "red stalk", "red rot", "wilting cane", "alcohol smell"],
        "cause": "Fungal – Colletotrichum falcatum",
        "treatment": "No effective chemical cure. Remove and destroy infected stalks. Use disease-free setts.",
        "prevention": "Hot water treatment of setts (52°C for 30 min). Use resistant varieties.",
        "severity": "Critical",
        "icon": "🎋"
    },
    {
        "name": "Aphid Infestation",
        "hindi": "माहू कीट",
        "crop": "Multiple Crops",
        "symptoms": ["small green insect", "curling leaf", "sticky honeydew", "sooty mould", "cluster insect", "aphid", "black ant", "tiny insect"],
        "cause": "Insect – Aphis spp.",
        "treatment": "Imidacloprid 17.8SL @ 0.3ml/L or Dimethoate 30EC @ 1.5ml/L. Spray underside of leaves.",
        "prevention": "Encourage ladybirds (natural predators). Avoid excess nitrogen.",
        "severity": "Low",
        "icon": "🌿"
    },
    {
        "name": "Downy Mildew",
        "hindi": "मृदुरोमिल फफूंदी",
        "crop": "Onion / Grapes / Vegetables",
        "symptoms": ["purple grey fuzz", "yellow patch above", "downy growth", "grey fuzz below", "downy mildew"],
        "cause": "Oomycete – Peronospora spp.",
        "treatment": "Metalaxyl 8% + Mancozeb 64% @ 2.5g/L. Spray early morning in cool weather.",
        "prevention": "Avoid excess moisture. Space plants well. Use drip irrigation.",
        "severity": "Medium",
        "icon": "🧅"
    },
]

# AI Assistant knowledge base
AI_KNOWLEDGE = {
    "soil": {
        "loamy": "Loamy soil is ideal for most crops including wheat, rice, maize, vegetables, and fruits. It has good water retention and drainage. Add organic matter annually to maintain fertility.",
        "sandy": "Sandy soil drains quickly. Good for root vegetables like potato, groundnut, and carrot. Needs frequent irrigation and more organic matter. Apply mulching to reduce water loss.",
        "clay": "Clay soil retains water well but can become waterlogged. Suitable for rice and sugarcane. Improve drainage by adding sand and organic matter. Avoid tilling when wet.",
        "black": "Black cotton soil (vertisol) is excellent for cotton, soybean, and wheat. Very fertile but cracks when dry and sticky when wet. Needs careful water management.",
        "red": "Red soil is acidic and low in nutrients. Add lime to raise pH. Good for groundnut, pulses, and millets. Regular fertilization and organic matter addition is essential.",
        "alluvial": "Alluvial soil is highly fertile, found in river plains. Excellent for wheat, rice, sugarcane, and most crops. Maintain organic matter and balanced NPK fertilization.",
    },
    "season": {
        "kharif": "Kharif crops are sown in June-July with monsoon rains and harvested in October-November. Major crops: Rice, Maize, Cotton, Soybean, Jowar, Bajra, Groundnut, Sugarcane.",
        "rabi": "Rabi crops are sown in October-November and harvested in March-April. Major crops: Wheat, Mustard, Chickpea (Chana), Lentil (Masoor), Peas, Barley.",
        "zaid": "Zaid crops are grown in March-June between Rabi and Kharif seasons. Major crops: Watermelon, Muskmelon, Cucumber, Moong Dal, Vegetables.",
    },
    "irrigation": {
        "drip": "Drip irrigation saves 30-50% water compared to flood irrigation. Ideal for vegetables, fruits, and orchards. Government subsidy available under PMKSY scheme.",
        "sprinkler": "Sprinkler irrigation is good for wheat, vegetables, and undulating land. Saves 20-30% water. Useful where drip is not feasible.",
        "flood": "Flood/furrow irrigation is traditional and used for rice. Requires levelled land. High water use. Consider switching to SRI method for rice to save 30% water.",
    },
    "fertilizer": {
        "urea": "Urea (46% N) is the main nitrogen fertilizer. Apply in 2-3 splits. Avoid applying before heavy rain. Use neem-coated urea for slow release and better efficiency.",
        "dap": "DAP (Diammonium Phosphate - 18% N, 46% P2O5) provides nitrogen and phosphorus. Apply at sowing time. 1 bag (50kg) per acre is common recommendation.",
        "potash": "MOP (Muriate of Potash - 60% K2O) improves crop quality and disease resistance. Apply at sowing. Particularly important for potato, sugarcane, and fruits.",
        "organic": "Organic manures (FYM, compost, vermicompost) improve soil health long-term. Apply 4-5 tonnes FYM per acre before sowing. Reduces chemical fertilizer requirement by 20-30%.",
    },
    "schemes": {
        "pmkisan": "PM-KISAN: ₹6,000/year direct income support in 3 installments to all landholding farmers. Register at pmkisan.gov.in with Aadhaar and bank details.",
        "pmfby": "PM Fasal Bima Yojana: Crop insurance at 2% premium for Kharif, 1.5% for Rabi. Covers losses from natural calamities. Register through nearest bank or CSC centre.",
        "kcc": "Kisan Credit Card: Short-term crop loan at 4-7% interest rate up to ₹3 lakh. Apply at any bank with land records and Aadhaar.",
        "solar pump": "PM-KUSUM scheme: 90% subsidy on solar pumps (10% farmer contribution). Apply through state agriculture department.",
        "soil health": "Soil Health Card scheme: Free soil testing and customized fertilizer recommendations every 2 years. Visit your nearest Krishi Vigyan Kendra.",
    }
}

MOTIVATIONAL_QUOTES = [
    "🌱 Every seed you plant is an investment in tomorrow's harvest.",
    "☀️ The farmer is the backbone of the nation. Keep growing!",
    "💪 Hard work in the field today means abundance tomorrow.",
    "🌾 Patience, rain, and care — the three secrets of a great harvest.",
    "🙏 The land never lies to the farmer who respects it.",
    "🌍 Sustainable farming today for a better world tomorrow.",
    "⭐ A good farmer is both a craftsman and a scientist.",
]

WX_ICONS = {
    0:"☀️",1:"🌤️",2:"⛅",3:"☁️",45:"🌫️",48:"🌫️",
    51:"🌦️",53:"🌦️",55:"🌧️",61:"🌧️",63:"🌧️",65:"🌧️",
    71:"❄️",73:"❄️",75:"❄️",80:"🌦️",81:"🌧️",82:"⛈️",
    95:"⛈️",96:"⛈️",99:"⛈️"
}
WX_DESC = {
    0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",
    45:"Foggy",48:"Icy fog",51:"Light drizzle",53:"Drizzle",55:"Heavy drizzle",
    61:"Light rain",63:"Rain",65:"Heavy rain",71:"Light snow",73:"Snow",75:"Heavy snow",
    80:"Rain showers",81:"Heavy showers",82:"Violent showers",95:"Thunderstorm",
    96:"Thunderstorm+hail",99:"Heavy thunderstorm"
}


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTOCOMPLETE ENTRY WIDGET
# ═══════════════════════════════════════════════════════════════════════════════
class AutocompleteEntry(ctk.CTkFrame):
    """Autocomplete dropdown entry widget for location search."""

    def __init__(self, parent, values, placeholder="Search...", width=300, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.all_values  = values
        self.popup_win   = None
        self.listbox     = None
        self._after_id   = None
        self.on_select_callback = None

        self.entry = ctk.CTkEntry(
            self, placeholder_text=placeholder, width=width, height=40,
            fg_color=C2, border_color="#2a4a30", text_color=TXT,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.entry.pack(fill="x")

        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<FocusOut>",   self._schedule_close)
        self.entry.bind("<Escape>",     lambda e: self._close_popup())
        self.entry.bind("<Down>",       self._focus_list)

    def get(self): return self.entry.get()
    def set(self, v): self.entry.delete(0, "end"); self.entry.insert(0, v)

    def _on_key(self, event):
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(120, self._update_list)

    def _update_list(self):
        query = self.entry.get().strip().lower()
        self._close_popup()
        if len(query) < 1:
            return
        matches = [v for v in self.all_values if query in v.lower()][:12]
        if not matches:
            return
        self._show_popup(matches)

    def _show_popup(self, matches):
        try:
            x = self.entry.winfo_rootx()
            y = self.entry.winfo_rooty() + self.entry.winfo_height() + 2
            w = self.entry.winfo_width()
        except Exception:
            return

        self.popup_win = tk.Toplevel(self.winfo_toplevel())
        self.popup_win.wm_overrideredirect(True)
        self.popup_win.wm_geometry(f"{w}x{min(len(matches)*32+4, 320)}+{x}+{y}")
        self.popup_win.configure(bg=C2)
        self.popup_win.lift()
        self.popup_win.attributes("-topmost", True)

        sb = tk.Scrollbar(self.popup_win, orient="vertical", bg=C2)
        self.listbox = tk.Listbox(
            self.popup_win, yscrollcommand=sb.set,
            bg=C2, fg=TXT, selectbackground=G3, selectforeground=G1,
            font=("Segoe UI", 12), borderwidth=0, highlightthickness=1,
            highlightcolor="#2a4a30", activestyle="none", relief="flat",
            cursor="hand2"
        )
        sb.config(command=self.listbox.yview)
        sb.pack(side="right", fill="y") if len(matches) > 10 else None
        self.listbox.pack(fill="both", expand=True, padx=2, pady=2)

        for m in matches:
            self.listbox.insert("end", "  " + m)

        self.listbox.bind("<ButtonRelease-1>", self._on_select)
        self.listbox.bind("<Return>",           self._on_select)
        self.listbox.bind("<Up>", lambda e: self._navigate(-1))
        self.listbox.bind("<Down>", lambda e: self._navigate(1))

    def _navigate(self, direction):
        if not self.listbox: return
        cur = self.listbox.curselection()
        idx = (cur[0] if cur else -1) + direction
        idx = max(0, min(idx, self.listbox.size()-1))
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(idx)
        self.listbox.see(idx)

    def _focus_list(self, event):
        if self.listbox:
            self.listbox.focus_set()
            self.listbox.selection_set(0)

    def _on_select(self, event):
        if not self.listbox: return
        sel = self.listbox.curselection()
        if sel:
            value = self.listbox.get(sel[0]).strip()
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
            self._close_popup()
            if self.on_select_callback:
                self.on_select_callback(value)

    def _schedule_close(self, event):
        self.after(150, self._close_popup)

    def _close_popup(self):
        if self.popup_win:
            try: self.popup_win.destroy()
            except Exception: pass
            self.popup_win = None
            self.listbox   = None


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
class KisanSaathiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌾 Kisan Saathi Pro v2.0")
        self.root.geometry("1280x800")
        self.root.minsize(1100, 700)
        self.root.configure(fg_color=BG)

        self.current_user = None
        self.lang = "en"
        self._content_frame = None

        self.init_db()
        self._try_auto_login()

    # ── Translation ─────────────────────────────────────────────────────────
    def t(self, key):
        texts = {
            "en": {
                "login":"Login","register":"Create Account","email":"Email",
                "password":"Password","name":"Full Name","village":"Village",
                "district":"District","state":"State","farm_size":"Farm Size (acres)",
                "soil":"Soil Type","login_btn":"Login","register_btn":"Create Account",
                "back_btn":"Back to Login","no_account":"No account? Register",
                "dashboard":"Dashboard","crops":"Crop Advisor","weather":"Live Weather",
                "diary":"Farm Diary","disease":"Disease Detection","ai":"AI Assistant",
                "logout":"Logout","welcome":"Welcome","your_crops":"Your Crops",
                "no_crops":"No crops yet","add_crop":"Add Crop","get_weather":"Get Weather",
                "location":"City Name","save":"Save","date":"Date","activity":"Activity",
                "notes":"Notes","history":"History",
            },
            "hi": {
                "login":"लॉगिन","register":"खाता बनाएं","email":"ईमेल",
                "password":"पासवर्ड","name":"पूरा नाम","village":"गाँव",
                "district":"जिला","state":"राज्य","farm_size":"खेत (एकड़)",
                "soil":"मिट्टी","login_btn":"लॉगिन","register_btn":"खाता बनाएं",
                "back_btn":"वापस","no_account":"खाता नहीं? रजिस्टर",
                "dashboard":"डैशबोर्ड","crops":"फसल सलाह","weather":"मौसम",
                "diary":"डायरी","disease":"रोग पहचान","ai":"AI सहायक",
                "logout":"बाहर","welcome":"स्वागत","your_crops":"आपकी फसलें",
                "no_crops":"कोई फसल नहीं","add_crop":"फसल जोड़ें",
                "get_weather":"मौसम देखें","location":"शहर","save":"सहेजें",
                "date":"तारीख","activity":"गतिविधि","notes":"नोट्स","history":"इतिहास",
            }
        }
        return texts[self.lang].get(key, key)

    def toggle_lang(self):
        self.lang = "hi" if self.lang == "en" else "en"
        if self.current_user: self.show_main()
        else: self.show_login()

    # ── Database ────────────────────────────────────────────────────────────
    def init_db(self):
        self.conn = sqlite3.connect('kisansathi_v2.db')
        c = self.conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT UNIQUE, password TEXT,
            village TEXT, district TEXT, state TEXT,
            farm_size REAL, soil_type TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, season TEXT, soil_type TEXT, profit INTEGER
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, crop_name TEXT, planting_date TEXT, field_size REAL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, date TEXT, activity TEXT, notes TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS saved_login (
            id INTEGER PRIMARY KEY, email TEXT, password_hash TEXT, remember INTEGER
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS disease_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, date TEXT, crop TEXT, symptoms TEXT,
            detected TEXT, severity TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ai_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, date TEXT, question TEXT, answer TEXT
        )''')

        # Seed crops
        c.execute("SELECT COUNT(*) FROM crops")
        if c.fetchone()[0] == 0:
            sample = [
                ("Wheat","Rabi","Loamy,Alluvial",25000),
                ("Rice","Kharif","Clay,Alluvial",30000),
                ("Maize","Kharif","Loamy,Sandy",28000),
                ("Potato","Rabi","Sandy,Loamy",45000),
                ("Tomato","Kharif","Loamy,Red",60000),
                ("Onion","Rabi","Loamy,Clay",40000),
                ("Sugarcane","Kharif","Black,Loamy",80000),
                ("Cotton","Kharif","Black,Loamy",35000),
                ("Mustard","Rabi","Loamy,Sandy",22000),
                ("Chickpea","Rabi","Black,Red",28000),
                ("Groundnut","Kharif","Sandy,Red",38000),
                ("Soybean","Kharif","Black,Loamy",26000),
            ]
            c.executemany("INSERT INTO crops (name,season,soil_type,profit) VALUES(?,?,?,?)", sample)
        self.conn.commit()

    def hash_pw(self, pw): return hashlib.sha256(pw.encode()).hexdigest()

    # ── Remember Login ──────────────────────────────────────────────────────
    def _try_auto_login(self):
        """Try to auto-login if remember me was set."""
        c = self.conn.cursor()
        c.execute("SELECT email, password_hash FROM saved_login WHERE remember=1 LIMIT 1")
        row = c.fetchone()
        if row:
            user, err = self._login(row[0], None, pw_hash=row[1])
            if user:
                self.current_user = user
                self.show_main()
                return
        self.show_login()

    def _save_login(self, email, pw_hash, remember):
        c = self.conn.cursor()
        c.execute("DELETE FROM saved_login")
        if remember:
            c.execute("INSERT INTO saved_login (id,email,password_hash,remember) VALUES(1,?,?,1)",
                      (email, pw_hash))
        self.conn.commit()

    def _clear_saved_login(self):
        self.conn.cursor().execute("DELETE FROM saved_login")
        self.conn.commit()

    def _login(self, email, password, pw_hash=None):
        c = self.conn.cursor()
        h = pw_hash if pw_hash else self.hash_pw(password)
        c.execute("SELECT id,name,email,village,district,state,farm_size,soil_type FROM users WHERE email=? AND password=?",
                  (email, h))
        row = c.fetchone()
        if row:
            return {"id":row[0],"name":row[1],"email":row[2],"village":row[3],
                    "district":row[4],"state":row[5],"farm_size":row[6],"soil_type":row[7]}, None
        return None, "Invalid credentials"

    def _register(self, name, email, password, village, district, state, farm_size, soil):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO users (name,email,password,village,district,state,farm_size,soil_type) VALUES(?,?,?,?,?,?,?,?)",
                      (name,email,self.hash_pw(password),village,district,state,float(farm_size),soil))
            self.conn.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    # ─────────────────────────────────────────────────────────────────────────
    #  SCREENS
    # ─────────────────────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ── LOGIN ────────────────────────────────────────────────────────────────
    def show_login(self):
        self._clear()

        # Background texture via gradient frame
        bg = ctk.CTkFrame(self.root, fg_color=BG)
        bg.pack(fill="both", expand=True)

        # Decorative left panel
        left = ctk.CTkFrame(bg, fg_color=C1, width=420, corner_radius=0)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="🌾", font=ctk.CTkFont(size=72)).pack(pady=(80, 10))
        ctk.CTkLabel(left, text="KISAN SAATHI", font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
                     text_color=G1).pack()
        ctk.CTkLabel(left, text="PRO v2.0", font=ctk.CTkFont(size=14),
                     text_color=TXM).pack(pady=(4, 30))

        # Decorative divider
        ctk.CTkFrame(left, height=2, fg_color=G3).pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(left, text="स्मार्ट किसान, समृद्ध भारत",
                     font=ctk.CTkFont(family="Segoe UI", size=13), text_color=TXM).pack(pady=6)
        ctk.CTkLabel(left, text="Smart Farmer, Prosperous India",
                     font=ctk.CTkFont(size=12), text_color=TXM).pack()

        # Quote
        quote = MOTIVATIONAL_QUOTES[datetime.now().day % len(MOTIVATIONAL_QUOTES)]
        ctk.CTkLabel(left, text=quote, font=ctk.CTkFont(size=11),
                     text_color=G2, wraplength=320, justify="center").pack(padx=30, pady=40)

        ctk.CTkButton(left, text="🌐 हिंदी" if self.lang=="en" else "🌐 English",
                      command=self.toggle_lang, fg_color="transparent",
                      border_width=1, border_color=G3, width=140, height=34).pack()

        # Right: Login form
        right = ctk.CTkFrame(bg, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)

        form_wrap = ctk.CTkFrame(right, fg_color="transparent")
        form_wrap.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_wrap, text=f"👋 {self.t('login')}",
                     font=ctk.CTkFont(size=28, weight="bold"), text_color=TXT).pack(pady=(0, 6))
        ctk.CTkLabel(form_wrap, text="Welcome back to your smart farm",
                     font=ctk.CTkFont(size=13), text_color=TXM).pack(pady=(0, 30))

        # Email
        ctk.CTkLabel(form_wrap, text=self.t("email"), font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w")
        self.login_email = ctk.CTkEntry(form_wrap, width=360, height=42,
                                        fg_color=C2, border_color="#2a4a30",
                                        text_color=TXT, placeholder_text="farmer@email.com",
                                        font=ctk.CTkFont(size=13))
        self.login_email.pack(pady=(3, 14))

        # Password
        ctk.CTkLabel(form_wrap, text=self.t("password"), font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w")
        self.login_pass = ctk.CTkEntry(form_wrap, width=360, height=42, show="•",
                                       fg_color=C2, border_color="#2a4a30",
                                       text_color=TXT, placeholder_text="••••••••",
                                       font=ctk.CTkFont(size=13))
        self.login_pass.pack(pady=(3, 10))

        # Remember me checkbox
        self.remember_var = ctk.IntVar(value=0)
        ctk.CTkCheckBox(form_wrap, text="Remember me on this device",
                        variable=self.remember_var, fg_color=G2, hover_color=G3,
                        checkmark_color=BG, text_color=TXM,
                        font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 20))

        # Login button
        ctk.CTkButton(form_wrap, text=self.t("login_btn"), command=self.do_login,
                      width=360, height=44, fg_color=G2, hover_color=G3,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      text_color=BG).pack(pady=(0, 12))

        ctk.CTkButton(form_wrap, text=self.t("no_account"), command=self.show_register,
                      fg_color="transparent", hover_color=C2, text_color=G1,
                      font=ctk.CTkFont(size=13), width=360, height=38,
                      border_width=1, border_color=G3).pack()

        self.login_email.bind("<Return>", lambda e: self.login_pass.focus())
        self.login_pass.bind("<Return>", lambda e: self.do_login())

    def do_login(self):
        email = self.login_email.get().strip()
        pw    = self.login_pass.get().strip()
        if not email or not pw:
            messagebox.showerror("Error", "Please enter email and password")
            return
        user, err = self._login(email, pw)
        if err:
            messagebox.showerror("Login Failed", err)
            return

        self.current_user = user
        remember = bool(self.remember_var.get())
        self._save_login(email, self.hash_pw(pw), remember)

        # Show remember popup
        self._show_remember_popup(user["name"], remember)

    def _show_remember_popup(self, name, already_remembered):
        """Brief welcome popup after login."""
        popup = ctk.CTkToplevel(self.root)
        popup.title("")
        popup.geometry("400x220")
        popup.resizable(False, False)
        popup.configure(fg_color=C1)
        popup.grab_set()
        popup.lift()
        popup.attributes("-topmost", True)

        # Center it
        self.root.update_idletasks()
        px = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        py = self.root.winfo_y() + (self.root.winfo_height() - 220) // 2
        popup.geometry(f"400x220+{px}+{py}")

        ctk.CTkLabel(popup, text="🌾", font=ctk.CTkFont(size=36)).pack(pady=(20, 4))
        ctk.CTkLabel(popup, text=f"Welcome back, {name}!",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color=G1).pack()

        if already_remembered:
            msg = "✅ Login saved — you won't need to login next time."
        else:
            msg = "Check 'Remember me' to skip login next time."
        ctk.CTkLabel(popup, text=msg, font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(pady=8)

        def proceed():
            popup.destroy()
            self.show_main()

        ctk.CTkButton(popup, text="Continue →", command=proceed,
                      fg_color=G2, hover_color=G3, text_color=BG,
                      width=200, height=38, font=ctk.CTkFont(size=13, weight="bold")).pack(pady=10)

        popup.after(3500, lambda: proceed() if popup.winfo_exists() else None)

    # ── REGISTER ─────────────────────────────────────────────────────────────
    def show_register(self):
        self._clear()

        bg = ctk.CTkFrame(self.root, fg_color=BG)
        bg.pack(fill="both", expand=True)

        # Title bar
        bar = ctk.CTkFrame(bg, fg_color=C1, height=60, corner_radius=0)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        ctk.CTkLabel(bar, text="🌾  KISAN SAATHI PRO — Create Account",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color=G1).pack(side="left", padx=24, pady=16)
        ctk.CTkButton(bar, text="← Back", command=self.show_login,
                      fg_color="transparent", text_color=TXM, width=90, height=32).pack(side="right", padx=16)

        # Scrollable form
        scroll = ctk.CTkScrollableFrame(bg, fg_color=BG)
        scroll.pack(fill="both", expand=True, padx=0, pady=0)

        inner = ctk.CTkFrame(scroll, fg_color="transparent")
        inner.pack(expand=True, pady=20)

        # Two-column layout
        cols = ctk.CTkFrame(inner, fg_color="transparent")
        cols.pack()

        # LEFT: Personal info
        left_card = ctk.CTkFrame(cols, fg_color=C1, corner_radius=16)
        left_card.pack(side="left", padx=12, pady=0, fill="y")

        self._sec_label(left_card, "👤 Personal Information")

        self.reg_name    = self._reg_field(left_card, "Full Name", "Enter your full name")
        self.reg_email   = self._reg_field(left_card, "Email Address", "farmer@example.com")
        self.reg_pass    = self._reg_field(left_card, "Password", "Min 4 characters", show="•")
        self.reg_confirm = self._reg_field(left_card, "Confirm Password", "Repeat password", show="•")

        # RIGHT: Farm info
        right_card = ctk.CTkFrame(cols, fg_color=C1, corner_radius=16)
        right_card.pack(side="left", padx=12, pady=0, fill="y")

        self._sec_label(right_card, "🌾 Farm Information")

        # Village
        ctk.CTkLabel(right_card, text="Village Name", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=20, pady=(8, 2))
        self.reg_village = ctk.CTkEntry(right_card, width=300, height=40,
                                        fg_color=C2, border_color="#2a4a30", text_color=TXT,
                                        placeholder_text="Your village")
        self.reg_village.pack(padx=20, pady=(0, 4))

        # District autocomplete
        ctk.CTkLabel(right_card, text="District / City", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=20, pady=(8, 2))
        self.reg_district_ac = AutocompleteEntry(right_card, ALL_CITY_NAMES,
                                                 placeholder="Search district/city...", width=300)
        self.reg_district_ac.pack(padx=20, pady=(0, 4), fill="x")

        # State autocomplete
        ctk.CTkLabel(right_card, text="State", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=20, pady=(8, 2))
        self.reg_state_ac = AutocompleteEntry(right_card, INDIA_STATES,
                                              placeholder="Search state...", width=300)
        self.reg_state_ac.pack(padx=20, pady=(0, 4), fill="x")

        # Farm size
        ctk.CTkLabel(right_card, text="Farm Size (acres)", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=20, pady=(8, 2))
        self.reg_farm = ctk.CTkEntry(right_card, width=300, height=40,
                                     fg_color=C2, border_color="#2a4a30", text_color=TXT,
                                     placeholder_text="e.g. 5.0")
        self.reg_farm.pack(padx=20, pady=(0, 4))

        # Soil type
        ctk.CTkLabel(right_card, text="Soil Type", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=20, pady=(8, 2))
        self.reg_soil = ctk.CTkComboBox(right_card,
                                        values=["Loamy","Sandy","Clay","Black","Red","Alluvial"],
                                        width=300, height=40, fg_color=C2,
                                        border_color="#2a4a30", text_color=TXT,
                                        button_color=G3, dropdown_fg_color=C2,
                                        dropdown_text_color=TXT)
        self.reg_soil.set("Loamy")
        self.reg_soil.pack(padx=20, pady=(0, 20))

        # Buttons row
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(pady=(10, 30))

        ctk.CTkButton(btn_row, text="✅  Create Account", command=self.do_register,
                      width=280, height=48, fg_color=G2, hover_color=G3,
                      font=ctk.CTkFont(size=15, weight="bold"), text_color=BG).pack(side="left", padx=10)
        ctk.CTkButton(btn_row, text="← Back to Login", command=self.show_login,
                      width=200, height=48, fg_color="transparent",
                      border_width=1, border_color=G3, text_color=TXM,
                      font=ctk.CTkFont(size=13)).pack(side="left", padx=10)

    def _sec_label(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=G1).pack(anchor="w", padx=20, pady=(20, 6))
        ctk.CTkFrame(parent, height=1, fg_color=G3).pack(fill="x", padx=20, pady=(0, 8))

    def _reg_field(self, parent, label, placeholder, show=None):
        ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=20, pady=(8, 2))
        kw = dict(width=300, height=40, fg_color=C2, border_color="#2a4a30",
                  text_color=TXT, placeholder_text=placeholder)
        if show: kw["show"] = show
        e = ctk.CTkEntry(parent, **kw)
        e.pack(padx=20, pady=(0, 4))
        return e

    def do_register(self):
        name     = self.reg_name.get().strip()
        email    = self.reg_email.get().strip()
        pw       = self.reg_pass.get().strip()
        confirm  = self.reg_confirm.get().strip()
        village  = self.reg_village.get().strip()
        district = self.reg_district_ac.get().strip()
        state    = self.reg_state_ac.get().strip()
        farm     = self.reg_farm.get().strip()
        soil     = self.reg_soil.get()

        if not all([name, email, pw, village, district, state, farm]):
            messagebox.showerror("Validation Error", "Please fill all fields!"); return
        if pw != confirm:
            messagebox.showerror("Validation Error", "Passwords do not match!"); return
        if len(pw) < 4:
            messagebox.showerror("Validation Error", "Password must be at least 4 characters!"); return

        ok, err = self._register(name, email, pw, village, district, state, farm, soil)
        if ok:
            messagebox.showinfo("✅ Success", f"Account created for {name}!\nPlease login.")
            self.show_login()
        else:
            messagebox.showerror("Registration Failed", err)

    # ── MAIN SHELL ───────────────────────────────────────────────────────────
    def show_main(self):
        self._clear()

        shell = ctk.CTkFrame(self.root, fg_color=BG)
        shell.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ctk.CTkFrame(shell, width=230, fg_color=C1, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo
        logo_f = ctk.CTkFrame(sidebar, fg_color=C2, height=100, corner_radius=0)
        logo_f.pack(fill="x")
        logo_f.pack_propagate(False)
        ctk.CTkLabel(logo_f, text="🌾", font=ctk.CTkFont(size=36)).pack(pady=(14, 2))
        ctk.CTkLabel(logo_f, text="KISAN SAATHI",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=G1).pack()

        # Nav items
        nav = [
            ("🏠", self.t("dashboard"),  self.show_dashboard),
            ("🌾", self.t("crops"),      self.show_crops),
            ("🌤️", self.t("weather"),   self.show_weather),
            ("🦠", self.t("disease"),    self.show_disease),
            ("🤖", self.t("ai"),         self.show_ai),
            ("📖", self.t("diary"),      self.show_diary),
        ]
        ctk.CTkFrame(sidebar, height=1, fg_color=G3).pack(fill="x", padx=16, pady=10)

        self._nav_btns = {}
        for icon, label, cmd in nav:
            key = label
            btn = ctk.CTkButton(
                sidebar, text=f"{icon}  {label}",
                command=lambda c=cmd, k=key: self._nav_click(c, k),
                fg_color="transparent", hover_color=C3, anchor="w",
                height=46, font=ctk.CTkFont(size=13), text_color=TXM,
                corner_radius=8
            )
            btn.pack(fill="x", padx=10, pady=2)
            self._nav_btns[key] = btn

        # User info
        ctk.CTkFrame(sidebar, height=1, fg_color=G3).pack(fill="x", padx=16, pady=10)
        u = self.current_user
        ctk.CTkLabel(sidebar, text=f"👨‍🌾  {u['name']}",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=TXT).pack(padx=16, anchor="w")
        ctk.CTkLabel(sidebar, text=f"📍  {u.get('district','') or u.get('village','')}",
                     font=ctk.CTkFont(size=11), text_color=TXM).pack(padx=16, anchor="w", pady=2)
        ctk.CTkLabel(sidebar, text=f"🌱  {u.get('farm_size',0)} acres · {u.get('soil_type','')} soil",
                     font=ctk.CTkFont(size=11), text_color=TXM).pack(padx=16, anchor="w")

        # Language & logout
        ctk.CTkFrame(sidebar, height=1, fg_color=G3).pack(fill="x", padx=16, pady=10)
        ctk.CTkButton(sidebar, text="🌐  " + ("हिंदी" if self.lang=="en" else "English"),
                      command=self.toggle_lang, fg_color="transparent", hover_color=C2,
                      text_color=TXM, height=36).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(sidebar, text=f"🚪  {self.t('logout')}", command=self.logout,
                      fg_color="transparent", hover_color=C2, text_color=ERR, height=36).pack(fill="x", padx=10, pady=2)

        # Content area
        self._content_frame = ctk.CTkFrame(shell, fg_color=BG)
        self._content_frame.pack(side="right", fill="both", expand=True)

        self.show_dashboard()

    def _nav_click(self, cmd, key):
        for k, btn in self._nav_btns.items():
            if k == key:
                btn.configure(fg_color=G3, text_color=G1)
            else:
                btn.configure(fg_color="transparent", text_color=TXM)
        cmd()

    def _clear_content(self):
        if self._content_frame:
            for w in self._content_frame.winfo_children():
                w.destroy()

    def _content_header(self, title, subtitle=""):
        hdr = ctk.CTkFrame(self._content_frame, fg_color=C1, height=64, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=title, font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=G1).pack(side="left", padx=24, pady=16)
        if subtitle:
            ctk.CTkLabel(hdr, text=subtitle, font=ctk.CTkFont(size=12),
                         text_color=TXM).pack(side="left", pady=22)

    def _card(self, parent, **kwargs):
        return ctk.CTkFrame(parent, fg_color=C1, corner_radius=14, **kwargs)

    # ── DASHBOARD ────────────────────────────────────────────────────────────
    def show_dashboard(self):
        self._clear_content()
        u = self.current_user
        self._content_header(f"🏠  {self.t('welcome')}, {u['name']}!",
                              f"  {date.today().strftime('%A, %d %B %Y')}")

        scroll = ctk.CTkScrollableFrame(self._content_frame, fg_color=BG)
        scroll.pack(fill="both", expand=True, padx=18, pady=14)

        # Stat row
        c_db = self.conn.cursor()
        c_db.execute("SELECT COUNT(*) FROM user_crops WHERE user_id=?", (u['id'],))
        crop_count = c_db.fetchone()[0]
        c_db.execute("SELECT COUNT(*) FROM diary WHERE user_id=?", (u['id'],))
        diary_count = c_db.fetchone()[0]
        c_db.execute("SELECT COUNT(*) FROM disease_log WHERE user_id=?", (u['id'],))
        disease_count = c_db.fetchone()[0]

        stats_row = ctk.CTkFrame(scroll, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 14))

        for icon, val, label, col in [
            ("🌾", str(crop_count), "My Crops", G1),
            ("🦠", str(disease_count), "Disease Checks", WARN),
            ("📖", str(diary_count), "Diary Entries", BLUE),
            ("🌱", f"{u.get('farm_size',0)} ac", "Farm Size", G2),
        ]:
            card = ctk.CTkFrame(stats_row, fg_color=C1, corner_radius=14)
            card.pack(side="left", expand=True, fill="x", padx=5)
            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=30)).pack(pady=(16, 4))
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=22, weight="bold"),
                         text_color=col).pack()
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=11),
                         text_color=TXM).pack(pady=(2, 16))

        # Main content row
        main_row = ctk.CTkFrame(scroll, fg_color="transparent")
        main_row.pack(fill="x")
        main_row.grid_columnconfigure(0, weight=3)
        main_row.grid_columnconfigure(1, weight=2)

        # My crops card
        crops_card = self._card(main_row)
        crops_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        ctk.CTkLabel(crops_card, text=f"🌾  {self.t('your_crops')}",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(14, 6))
        ctk.CTkFrame(crops_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 8))

        c_db.execute("SELECT crop_name, planting_date, field_size FROM user_crops WHERE user_id=? ORDER BY id DESC LIMIT 6",
                     (u['id'],))
        crops = c_db.fetchall()

        if crops:
            for cr in crops:
                row = ctk.CTkFrame(crops_card, fg_color=C2, corner_radius=8)
                row.pack(fill="x", padx=12, pady=3)
                ctk.CTkLabel(row, text=f"🌱  {cr[0]}",
                             font=ctk.CTkFont(size=12, weight="bold"), text_color=TXT).pack(side="left", padx=12, pady=9)
                ctk.CTkLabel(row, text=f"📅 {cr[1]}",
                             font=ctk.CTkFont(size=11), text_color=TXM).pack(side="left")
                ctk.CTkLabel(row, text=f"{cr[2]} ac",
                             font=ctk.CTkFont(size=11), text_color=G2).pack(side="right", padx=12)
        else:
            ctk.CTkLabel(crops_card, text=f"🌱  {self.t('no_crops')}",
                         font=ctk.CTkFont(size=12), text_color=TXM).pack(pady=20)

        ctk.CTkButton(crops_card, text=f"+ {self.t('add_crop')}", command=self.show_crops,
                      fg_color=G3, hover_color=G2, text_color=G1,
                      height=34, width=160).pack(pady=12)

        # Tip card
        tip_card = self._card(main_row)
        tip_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ctk.CTkLabel(tip_card, text="💡  Today's Tip",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(14, 6))
        ctk.CTkFrame(tip_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 12))

        soil = u.get("soil_type", "Loamy")
        tips_map = {
            "Loamy": "Ideal for most crops. Add compost twice a year to keep fertility high. Wheat, rice and vegetables all thrive.",
            "Sandy": "Irrigate more frequently. Mulching helps retain moisture. Add organic matter before sowing.",
            "Clay": "Ensure drainage channels. Don't till when wet. Black gram and sugarcane do well.",
            "Black": "Excellent for cotton and soybean. Needs careful water management — store rainwater!",
            "Red": "Add lime to correct acidity. Groundnut and millets are ideal. Fertilise regularly.",
            "Alluvial": "Highly fertile river soil. Best for wheat, rice, sugarcane. Maintain organic matter."
        }
        ctk.CTkLabel(tip_card, text=tips_map.get(soil, "Keep soil healthy for best yields!"),
                     font=ctk.CTkFont(size=12), text_color=TXT,
                     wraplength=240, justify="left").pack(padx=16, anchor="w")

        ctk.CTkFrame(tip_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=12)
        quote = MOTIVATIONAL_QUOTES[datetime.now().day % len(MOTIVATIONAL_QUOTES)]
        ctk.CTkLabel(tip_card, text=quote, font=ctk.CTkFont(size=11),
                     text_color=G2, wraplength=240, justify="left").pack(padx=16, anchor="w", pady=(0, 16))

    # ── CROP ADVISOR ────────────────────────────────────────────────────────
    def show_crops(self):
        self._clear_content()
        self._content_header(f"🌾  {self.t('crops')}", "  Personalised recommendations for your soil")

        main = ctk.CTkScrollableFrame(self._content_frame, fg_color=BG)
        main.pack(fill="both", expand=True, padx=18, pady=14)

        soil = self.current_user.get("soil_type", "Loamy")
        c = self.conn.cursor()
        c.execute("SELECT name, season, profit FROM crops WHERE soil_type LIKE ?", (f"%{soil}%",))
        crops = c.fetchall()

        ctk.CTkLabel(main, text=f"✅  Crops recommended for {soil} soil",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=G1).pack(anchor="w", pady=(0, 12))

        for name, season, profit in crops:
            card = ctk.CTkFrame(main, fg_color=C1, corner_radius=14)
            card.pack(fill="x", pady=5)

            left_f = ctk.CTkFrame(card, fg_color="transparent")
            left_f.pack(side="left", fill="x", expand=True, padx=16, pady=14)

            ctk.CTkLabel(left_f, text=f"🌾  {name}",
                         font=ctk.CTkFont(size=16, weight="bold"), text_color=TXT).pack(anchor="w")
            ctk.CTkLabel(left_f, text=f"🗓️  Season: {season}",
                         font=ctk.CTkFont(size=12), text_color=TXM).pack(anchor="w", pady=2)
            ctk.CTkLabel(left_f, text=f"💰  Expected Profit: ₹{profit:,} / acre",
                         font=ctk.CTkFont(size=13, weight="bold"), text_color=WARN).pack(anchor="w")

            def make_add(n=name):
                return lambda: self._add_crop_dialog(n)
            ctk.CTkButton(card, text="+ Add to Farm", command=make_add(),
                          fg_color=G3, hover_color=G2, text_color=G1,
                          width=130, height=34).pack(side="right", padx=16, pady=14)

    def _add_crop_dialog(self, crop_name):
        win = ctk.CTkToplevel(self.root)
        win.title(f"Add {crop_name}")
        win.geometry("380x260")
        win.configure(fg_color=C1)
        win.grab_set()
        win.lift()

        ctk.CTkLabel(win, text=f"🌾  Add {crop_name}",
                     font=ctk.CTkFont(size=17, weight="bold"), text_color=G1).pack(pady=(18, 10))

        ctk.CTkLabel(win, text="Field Size (acres):", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=30)
        size_e = ctk.CTkEntry(win, width=280, height=38, fg_color=C2,
                              border_color="#2a4a30", text_color=TXT)
        size_e.insert(0, "1.0")
        size_e.pack(padx=30, pady=(3, 10))

        ctk.CTkLabel(win, text="Planting Date:", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=30)
        date_e = ctk.CTkEntry(win, width=280, height=38, fg_color=C2,
                              border_color="#2a4a30", text_color=TXT)
        date_e.insert(0, str(date.today()))
        date_e.pack(padx=30, pady=(3, 16))

        def save():
            try: size = float(size_e.get())
            except: size = 1.0
            c = self.conn.cursor()
            c.execute("INSERT INTO user_crops (user_id,crop_name,planting_date,field_size) VALUES(?,?,?,?)",
                      (self.current_user['id'], crop_name, date_e.get(), size))
            self.conn.commit()
            messagebox.showinfo("✅", f"{crop_name} added to your farm!")
            win.destroy()
            self.show_dashboard()

        ctk.CTkButton(win, text="✅  Save", command=save,
                      fg_color=G2, hover_color=G3, text_color=BG,
                      width=280, height=40, font=ctk.CTkFont(size=13, weight="bold")).pack()

    # ── LIVE WEATHER ─────────────────────────────────────────────────────────
    def show_weather(self):
        self._clear_content()
        self._content_header(f"🌤️  {self.t('weather')}",
                             "  Real-time forecast powered by Open-Meteo API")

        main = ctk.CTkFrame(self._content_frame, fg_color=BG)
        main.pack(fill="both", expand=True, padx=18, pady=14)

        # Search bar
        search_card = ctk.CTkFrame(main, fg_color=C1, corner_radius=14)
        search_card.pack(fill="x", pady=(0, 14))
        search_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(search_card, text="📍", font=ctk.CTkFont(size=20)).grid(row=0, column=0, padx=(16, 8), pady=14)
        self.wx_city_ac = AutocompleteEntry(search_card, ALL_CITY_NAMES,
                                            placeholder="Search city (e.g. Ludhiana, Jaipur)...",
                                            width=400)
        self.wx_city_ac.grid(row=0, column=1, padx=8, pady=14, sticky="ew")
        user_district = self.current_user.get("district", "")
        if user_district: self.wx_city_ac.set(user_district)

        ctk.CTkButton(search_card, text="🔍  Get Weather", command=self._fetch_weather,
                      fg_color=G2, hover_color=G3, text_color=BG,
                      width=160, height=40, font=ctk.CTkFont(size=13, weight="bold")).grid(
                      row=0, column=2, padx=16, pady=14)

        # Weather display area
        self.wx_display = ctk.CTkScrollableFrame(main, fg_color=BG)
        self.wx_display.pack(fill="both", expand=True)

        ctk.CTkLabel(self.wx_display, text="Search a city above to see live weather forecast.",
                     font=ctk.CTkFont(size=13), text_color=TXM).pack(pady=40)

        # Auto-fetch if district set
        if user_district and user_district in INDIA_CITIES:
            self.root.after(300, self._fetch_weather)

    def _fetch_weather(self):
        city = self.wx_city_ac.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name"); return

        for w in self.wx_display.winfo_children(): w.destroy()
        lbl = ctk.CTkLabel(self.wx_display, text="⏳  Fetching live weather data...",
                           font=ctk.CTkFont(size=14), text_color=TXM)
        lbl.pack(pady=40)
        self.wx_display.update()

        def fetch():
            result, err = self._get_weather_data(city)
            self.root.after(0, lambda: self._render_weather(result, err, city))

        threading.Thread(target=fetch, daemon=True).start()

    def _get_weather_data(self, city):
        # Resolve coordinates
        coords = None
        # Try exact match first
        for name, coord in INDIA_CITIES.items():
            if city.lower() == name.lower():
                coords = coord
                city = name
                break
        # Partial match
        if not coords:
            for name, coord in INDIA_CITIES.items():
                if city.lower() in name.lower() or name.lower() in city.lower():
                    coords = coord
                    city = name
                    break
        # Geocoding API fallback
        if not coords:
            try:
                r = requests.get(
                    f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=3&language=en&format=json",
                    timeout=6)
                data = r.json()
                if data.get("results"):
                    res = data["results"][0]
                    coords = (res["latitude"], res["longitude"])
                    city = res.get("name", city)
            except Exception as e:
                return None, f"Geocoding failed: {e}"
        if not coords:
            return None, f"City '{city}' not found. Try a major city name."

        lat, lon = coords
        try:
            url = (f"https://api.open-meteo.com/v1/forecast"
                   f"?latitude={lat}&longitude={lon}"
                   f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,"
                   f"precipitation,weathercode,apparent_temperature"
                   f"&hourly=temperature_2m,precipitation_probability,weathercode"
                   f"&daily=weathercode,temperature_2m_max,temperature_2m_min,"
                   f"precipitation_sum,sunrise,sunset,uv_index_max"
                   f"&forecast_days=7&timezone=Asia/Kolkata")
            r = requests.get(url, timeout=8)
            data = r.json()
            data["_city"] = city
            return data, None
        except Exception as e:
            return None, f"Weather fetch failed: {e}"

    def _render_weather(self, data, err, city):
        for w in self.wx_display.winfo_children(): w.destroy()

        if err:
            ctk.CTkLabel(self.wx_display, text=f"❌  {err}",
                         font=ctk.CTkFont(size=13), text_color=ERR).pack(pady=40)
            return

        cur   = data.get("current", {})
        daily = data.get("daily", {})
        city_name = data.get("_city", city)

        temp    = cur.get("temperature_2m", "--")
        feels   = cur.get("apparent_temperature", "--")
        hum     = cur.get("relative_humidity_2m", "--")
        wind    = cur.get("wind_speed_10m", "--")
        rain    = cur.get("precipitation", 0)
        wcode   = cur.get("weathercode", 0)
        wx_icon = WX_ICONS.get(wcode, "🌤️")
        wx_desc = WX_DESC.get(wcode, "Partly cloudy")

        # ── Current weather hero card ──
        hero = ctk.CTkFrame(self.wx_display, fg_color=C1, corner_radius=16)
        hero.pack(fill="x", pady=(0, 14))

        left_h = ctk.CTkFrame(hero, fg_color="transparent")
        left_h.pack(side="left", padx=24, pady=20)

        ctk.CTkLabel(left_h, text=wx_icon, font=ctk.CTkFont(size=60)).pack()
        ctk.CTkLabel(left_h, text=wx_desc, font=ctk.CTkFont(size=13),
                     text_color=TXM).pack()

        mid_h = ctk.CTkFrame(hero, fg_color="transparent")
        mid_h.pack(side="left", padx=20, pady=20, expand=True, fill="x")

        ctk.CTkLabel(mid_h, text=f"📍  {city_name.upper()}",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=G1).pack(anchor="w")
        ctk.CTkLabel(mid_h, text=f"{temp}°C",
                     font=ctk.CTkFont(size=52, weight="bold"), text_color=TXT).pack(anchor="w", pady=4)
        ctk.CTkLabel(mid_h, text=f"Feels like {feels}°C",
                     font=ctk.CTkFont(size=13), text_color=TXM).pack(anchor="w")

        right_h = ctk.CTkFrame(hero, fg_color=C2, corner_radius=12)
        right_h.pack(side="right", padx=20, pady=20)

        for icon, label, val in [
            ("💧", "Humidity",    f"{hum}%"),
            ("💨", "Wind",        f"{wind} km/h"),
            ("🌧️", "Rain",       f"{rain} mm"),
        ]:
            stat_row = ctk.CTkFrame(right_h, fg_color="transparent")
            stat_row.pack(padx=20, pady=6, anchor="w")
            ctk.CTkLabel(stat_row, text=f"{icon}  {label}:",
                         font=ctk.CTkFont(size=12), text_color=TXM).pack(side="left")
            ctk.CTkLabel(stat_row, text=f"  {val}",
                         font=ctk.CTkFont(size=12, weight="bold"), text_color=TXT).pack(side="left")

        # ── Farm advisory ──
        adv_card = ctk.CTkFrame(self.wx_display, fg_color=C1, corner_radius=14)
        adv_card.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(adv_card, text="🌾  Farm Advisory",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkFrame(adv_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 8))

        advices = []
        t = float(temp) if isinstance(temp, (int, float)) else 25
        if t > 38: advices.append(("🔴", "Very high temperature! Irrigate early morning (before 7am) or evening (after 6pm). Provide shade for young seedlings."))
        elif t > 32: advices.append(("🟡", "Hot conditions. Water crops more frequently. Watch for heat stress symptoms in sensitive crops."))
        elif t < 8: advices.append(("🔵", "Cold weather ahead! Protect nursery plants with straw or plastic covers. Delay sowing if frost is expected."))
        else: advices.append(("🟢", "Temperature is favourable for field work and most crop growth stages."))

        rr = float(rain) if isinstance(rain, (int, float)) else 0
        if rr > 20: advices.append(("🟡", "Heavy rain forecast. Ensure drainage channels are clear. Avoid applying fertiliser or pesticide before rain."))
        elif rr > 5: advices.append(("🟢", "Moderate rain expected. Good time to apply fertiliser after rain stops."))
        else: advices.append(("🟡", "No significant rain expected. Plan irrigation accordingly."))

        if float(hum) > 80 if isinstance(hum, (int, float)) else False:
            advices.append(("🟠", "High humidity increases disease risk (blast, mildew). Inspect crops closely. Consider preventive fungicide spray."))

        for code, msg in advices:
            row = ctk.CTkFrame(adv_card, fg_color=C2, corner_radius=8)
            row.pack(fill="x", padx=12, pady=3)
            ctk.CTkLabel(row, text=f"{code}  {msg}",
                         font=ctk.CTkFont(size=12), text_color=TXT,
                         wraplength=700, justify="left").pack(padx=14, pady=8, anchor="w")

        ctk.CTkFrame(adv_card, height=6, fg_color="transparent").pack()

        # ── 7-day forecast ──
        fc_days = daily.get("time", [])
        if fc_days:
            forecast_card = ctk.CTkFrame(self.wx_display, fg_color=C1, corner_radius=14)
            forecast_card.pack(fill="x", pady=(0, 14))
            ctk.CTkLabel(forecast_card, text="📅  7-Day Forecast",
                         font=ctk.CTkFont(size=14, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(12, 8))
            ctk.CTkFrame(forecast_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 10))

            row_f = ctk.CTkFrame(forecast_card, fg_color="transparent")
            row_f.pack(fill="x", padx=12, pady=(0, 12))

            max_t = daily.get("temperature_2m_max", [])
            min_t = daily.get("temperature_2m_min", [])
            prec  = daily.get("precipitation_sum", [])
            codes = daily.get("weathercode", [])
            uvs   = daily.get("uv_index_max", [])

            for i, d in enumerate(fc_days[:7]):
                try:
                    dt = datetime.strptime(d, "%Y-%m-%d")
                    day_name = dt.strftime("%a") if i > 0 else "Today"
                    day_num  = dt.strftime("%d")
                except Exception:
                    day_name = d[-5:]; day_num = ""

                dc = ctk.CTkFrame(row_f, fg_color=C2, corner_radius=10)
                dc.pack(side="left", expand=True, fill="x", padx=3)

                c_icon = WX_ICONS.get(codes[i] if i < len(codes) else 0, "🌤️")
                ctk.CTkLabel(dc, text=day_name,
                             font=ctk.CTkFont(size=11, weight="bold"), text_color=G1).pack(pady=(10, 2))
                ctk.CTkLabel(dc, text=day_num, font=ctk.CTkFont(size=10),
                             text_color=TXM).pack()
                ctk.CTkLabel(dc, text=c_icon, font=ctk.CTkFont(size=22)).pack(pady=4)
                mx = f"{max_t[i]:.0f}°" if i < len(max_t) else "--"
                mn = f"{min_t[i]:.0f}°" if i < len(min_t) else "--"
                ctk.CTkLabel(dc, text=mx, font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=ERR).pack()
                ctk.CTkLabel(dc, text=mn, font=ctk.CTkFont(size=11),
                             text_color=BLUE).pack()
                pr = f"💧{prec[i]:.1f}mm" if i < len(prec) else ""
                ctk.CTkLabel(dc, text=pr, font=ctk.CTkFont(size=10),
                             text_color=TXM).pack(pady=(2, 10))

    # ── DISEASE DETECTION ────────────────────────────────────────────────────
    def show_disease(self):
        self._clear_content()
        self._content_header(f"🦠  {self.t('disease')}",
                             "  Describe symptoms to identify crop diseases")

        main = ctk.CTkScrollableFrame(self._content_frame, fg_color=BG)
        main.pack(fill="both", expand=True, padx=18, pady=14)

        top_row = ctk.CTkFrame(main, fg_color="transparent")
        top_row.pack(fill="x")
        top_row.grid_columnconfigure(0, weight=1)
        top_row.grid_columnconfigure(1, weight=1)

        # Input card
        inp_card = ctk.CTkFrame(top_row, fg_color=C1, corner_radius=14)
        inp_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ctk.CTkLabel(inp_card, text="🔍  Describe Symptoms",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(14, 6))
        ctk.CTkFrame(inp_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 10))

        # Crop selection
        ctk.CTkLabel(inp_card, text="Crop (optional):", font=ctk.CTkFont(size=12),
                     text_color=TXM).pack(anchor="w", padx=16)
        self.dis_crop_box = ctk.CTkComboBox(inp_card,
            values=["Any crop","Wheat","Rice","Maize","Potato","Tomato","Onion","Sugarcane","Cotton","Mustard","Soybean"],
            width=280, height=36, fg_color=C2, border_color="#2a4a30", text_color=TXT,
            button_color=G3, dropdown_fg_color=C2, dropdown_text_color=TXT)
        self.dis_crop_box.set("Any crop")
        self.dis_crop_box.pack(anchor="w", padx=16, pady=(4, 10))

        ctk.CTkLabel(inp_card, text="Symptoms (describe what you see):",
                     font=ctk.CTkFont(size=12), text_color=TXM).pack(anchor="w", padx=16)
        ctk.CTkLabel(inp_card,
                     text="e.g: yellow stripes on leaves, white powder coating, brown spots with rings",
                     font=ctk.CTkFont(size=11), text_color="#4a7a52").pack(anchor="w", padx=16, pady=(2, 4))

        self.dis_symptoms = ctk.CTkTextbox(inp_card, height=100, width=340,
                                           fg_color=C2, border_color="#2a4a30", text_color=TXT,
                                           font=ctk.CTkFont(size=12))
        self.dis_symptoms.pack(padx=16, pady=(0, 14))

        ctk.CTkButton(inp_card, text="🔬  Detect Disease", command=self._detect_disease,
                      fg_color=G2, hover_color=G3, text_color=BG,
                      height=42, font=ctk.CTkFont(size=13, weight="bold")).pack(padx=16, pady=(0, 14))

        # Quick reference
        ref_card = ctk.CTkFrame(top_row, fg_color=C1, corner_radius=14)
        ref_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ctk.CTkLabel(ref_card, text="📚  Common Disease Reference",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(14, 6))
        ctk.CTkFrame(ref_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 10))

        ref_scroll = ctk.CTkScrollableFrame(ref_card, fg_color="transparent", height=200)
        ref_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        for d in DISEASE_DB[:7]:
            sev_col = ERR if d["severity"]=="Critical" else WARN if d["severity"]=="High" else G2
            row = ctk.CTkFrame(ref_scroll, fg_color=C2, corner_radius=8)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"{d['icon']}  {d['name']}",
                         font=ctk.CTkFont(size=12, weight="bold"), text_color=TXT).pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(row, text=d["severity"],
                         font=ctk.CTkFont(size=11), text_color=sev_col).pack(side="right", padx=12)

        # Result area
        self.dis_result = ctk.CTkFrame(main, fg_color="transparent")
        self.dis_result.pack(fill="x", pady=(14, 0))

    def _detect_disease(self):
        for w in self.dis_result.winfo_children(): w.destroy()

        symptoms_text = self.dis_symptoms.get("1.0", "end").strip().lower()
        crop_filter   = self.dis_crop_box.get()
        if not symptoms_text:
            messagebox.showerror("Error", "Please describe the symptoms first!"); return

        # Keyword matching
        words = re.split(r'[,\s]+', symptoms_text)
        best, best_score = None, 0
        for d in DISEASE_DB:
            score = 0
            for kw in d["symptoms"]:
                if any(kw in w or w in kw for w in words):
                    score += 1
                if kw in symptoms_text:
                    score += 1
            if crop_filter != "Any crop" and crop_filter.lower() in d["crop"].lower():
                score += 3
            if score > best_score:
                best_score = score
                best = d

        result_card = ctk.CTkFrame(self.dis_result, fg_color=C1, corner_radius=14)
        result_card.pack(fill="x")

        ctk.CTkLabel(result_card, text="🔬  Detection Result",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(14, 6))
        ctk.CTkFrame(result_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 10))

        if best and best_score >= 1:
            sev_col = ERR if best["severity"]=="Critical" else WARN if best["severity"]=="High" else G2
            conf = min(95, 50 + best_score * 10)

            top_f = ctk.CTkFrame(result_card, fg_color=C2, corner_radius=10)
            top_f.pack(fill="x", padx=14, pady=(0, 8))

            ctk.CTkLabel(top_f, text=f"✅  {best['icon']}  {best['name']}  ({best['hindi']})",
                         font=ctk.CTkFont(size=16, weight="bold"), text_color=TXT).pack(anchor="w", padx=14, pady=(12, 4))
            ctk.CTkLabel(top_f, text=f"Affects: {best['crop']}   |   Confidence: {conf}%   |   Severity: {best['severity']}",
                         font=ctk.CTkFont(size=12), text_color=sev_col).pack(anchor="w", padx=14, pady=(0, 4))
            ctk.CTkLabel(top_f, text=f"Cause: {best['cause']}",
                         font=ctk.CTkFont(size=12), text_color=TXM).pack(anchor="w", padx=14, pady=(0, 12))

            cols_d = ctk.CTkFrame(result_card, fg_color="transparent")
            cols_d.pack(fill="x", padx=14, pady=(0, 14))

            for heading, text, col in [
                ("💊  Treatment", best["treatment"], WARN),
                ("🛡️  Prevention",  best["prevention"], BLUE),
            ]:
                box = ctk.CTkFrame(cols_d, fg_color=C2, corner_radius=10)
                box.pack(side="left", expand=True, fill="x", padx=5)
                ctk.CTkLabel(box, text=heading, font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=col).pack(anchor="w", padx=14, pady=(10, 4))
                ctk.CTkLabel(box, text=text, font=ctk.CTkFont(size=11),
                             text_color=TXT, wraplength=300, justify="left").pack(anchor="w", padx=14, pady=(0, 12))

            # Log it
            c = self.conn.cursor()
            c.execute("INSERT INTO disease_log (user_id,date,crop,symptoms,detected,severity) VALUES(?,?,?,?,?,?)",
                      (self.current_user['id'], str(date.today()), crop_filter,
                       symptoms_text[:200], best['name'], best['severity']))
            self.conn.commit()
        else:
            ctk.CTkLabel(result_card,
                         text="❓  No exact match found. Please describe symptoms more specifically.\n"
                              "    Try: leaf color, spot shape, area affected, smell, crop name.",
                         font=ctk.CTkFont(size=13), text_color=TXM).pack(padx=16, pady=20, anchor="w")

    # ── AI ASSISTANT ─────────────────────────────────────────────────────────
    def show_ai(self):
        self._clear_content()
        self._content_header(f"🤖  {self.t('ai')}",
                             "  Smart farming assistant — ask anything!")

        main = ctk.CTkFrame(self._content_frame, fg_color=BG)
        main.pack(fill="both", expand=True, padx=18, pady=14)

        # Chat history
        chat_card = ctk.CTkFrame(main, fg_color=C1, corner_radius=14)
        chat_card.pack(fill="both", expand=True, pady=(0, 10))

        self.ai_chat_scroll = ctk.CTkScrollableFrame(chat_card, fg_color="transparent")
        self.ai_chat_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Welcome message
        self._ai_add_msg("bot",
            "🌾 Namaste! I'm your Kisan Saathi AI assistant.\n\n"
            "I can help you with:\n"
            "• 🌱 Soil & crop selection advice\n"
            "• 💧 Irrigation & fertilizer guidance\n"
            "• 📅 Season-wise farming calendar\n"
            "• 🏛️ Government schemes (PM-KISAN, KCC, PMFBY)\n"
            "• 🦠 Disease identification tips\n"
            "• 💰 Profit estimation\n\n"
            "Type your question below in English or Hindi!")

        # Quick questions
        quick_f = ctk.CTkFrame(main, fg_color=C1, corner_radius=14)
        quick_f.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(quick_f, text="💡 Quick Questions:",
                     font=ctk.CTkFont(size=12), text_color=TXM).pack(side="left", padx=14, pady=10)

        quick_qs = [
            "Best crops for Loamy soil?",
            "How to apply urea?",
            "PM-KISAN benefits?",
            "Drip irrigation subsidy?",
        ]
        for q in quick_qs:
            def make_q(qtext=q): return lambda: self._ask_ai(qtext)
            ctk.CTkButton(quick_f, text=q, command=make_q(),
                          fg_color=C3, hover_color=G3, text_color=TXM,
                          height=30, width=170, font=ctk.CTkFont(size=11)).pack(side="left", padx=4, pady=10)

        # Input row
        inp_row = ctk.CTkFrame(main, fg_color=C1, corner_radius=14)
        inp_row.pack(fill="x")

        self.ai_input = ctk.CTkEntry(inp_row, placeholder_text="Ask me anything about farming...",
                                     height=44, fg_color=C2, border_color="#2a4a30",
                                     text_color=TXT, font=ctk.CTkFont(size=13))
        self.ai_input.pack(side="left", fill="x", expand=True, padx=14, pady=12)
        self.ai_input.bind("<Return>", lambda e: self._ask_ai_from_input())

        ctk.CTkButton(inp_row, text="Send ➤", command=self._ask_ai_from_input,
                      fg_color=G2, hover_color=G3, text_color=BG,
                      width=100, height=40, font=ctk.CTkFont(size=13, weight="bold")).pack(side="right", padx=14)

    def _ai_add_msg(self, role, text):
        is_bot = (role == "bot")
        bg_col = C2 if is_bot else C3
        align  = "w" if is_bot else "e"
        prefix = "🤖 " if is_bot else "👨‍🌾 "

        bubble = ctk.CTkFrame(self.ai_chat_scroll, fg_color=bg_col, corner_radius=12)
        bubble.pack(anchor=align, pady=4, padx=8, fill="x" if is_bot else None)

        ctk.CTkLabel(bubble, text=prefix + text, font=ctk.CTkFont(size=12),
                     text_color=TXT if is_bot else G1,
                     wraplength=580, justify="left").pack(padx=14, pady=10, anchor="w")
        # Auto-scroll
        self.ai_chat_scroll.after(100, lambda: self.ai_chat_scroll._parent_canvas.yview_moveto(1.0))

    def _ask_ai_from_input(self):
        q = self.ai_input.get().strip()
        if not q: return
        self.ai_input.delete(0, "end")
        self._ask_ai(q)

    def _ask_ai(self, question):
        self._ai_add_msg("user", question)
        answer = self._generate_ai_answer(question)
        self._ai_add_msg("bot", answer)

        # Log to DB
        c = self.conn.cursor()
        c.execute("INSERT INTO ai_chat (user_id,date,question,answer) VALUES(?,?,?,?)",
                  (self.current_user['id'], str(date.today()), question, answer[:500]))
        self.conn.commit()

    def _generate_ai_answer(self, q):
        """Rule-based AI using knowledge base."""
        q_low = q.lower()
        u = self.current_user

        # Soil queries
        for soil_key, info in AI_KNOWLEDGE["soil"].items():
            if soil_key in q_low or (soil_key == u.get("soil_type","").lower() and "soil" in q_low):
                return f"🌱 {soil_key.capitalize()} Soil Advice:\n\n{info}"

        if "soil" in q_low:
            soil = u.get("soil_type","Loamy").lower()
            info = AI_KNOWLEDGE["soil"].get(soil, "Keep soil healthy by adding organic matter.")
            return f"🌱 Based on your {soil} soil:\n\n{info}"

        # Season queries
        for season, info in AI_KNOWLEDGE["season"].items():
            if season in q_low:
                return f"📅 {season.capitalize()} Season:\n\n{info}"

        if "season" in q_low or "when to sow" in q_low or "kab" in q_low:
            return ("📅 Indian Farming Seasons:\n\n"
                    + AI_KNOWLEDGE["season"]["kharif"] + "\n\n"
                    + AI_KNOWLEDGE["season"]["rabi"] + "\n\n"
                    + AI_KNOWLEDGE["season"]["zaid"])

        # Irrigation
        for irr_key, info in AI_KNOWLEDGE["irrigation"].items():
            if irr_key in q_low or "irrigation" in q_low:
                return f"💧 Irrigation Advice:\n\n{info}"

        if "water" in q_low or "sinchaii" in q_low or "irrigation" in q_low:
            return "💧 Irrigation Tips:\n\n" + AI_KNOWLEDGE["irrigation"]["drip"]

        # Fertilizer
        for fert_key, info in AI_KNOWLEDGE["fertilizer"].items():
            if fert_key in q_low or "khad" in q_low:
                return f"🧪 Fertilizer Info ({fert_key}):\n\n{info}"

        if "fertilizer" in q_low or "urea" in q_low or "dap" in q_low or "khad" in q_low:
            return "🧪 Fertilizer Guide:\n\n" + AI_KNOWLEDGE["fertilizer"]["urea"]

        # Schemes
        for scheme_key, info in AI_KNOWLEDGE["schemes"].items():
            if scheme_key in q_low or "scheme" in q_low or "yojana" in q_low:
                return f"🏛️ Government Scheme:\n\n{info}"

        if "pm-kisan" in q_low or "pmkisan" in q_low or "₹6000" in q_low or "income support" in q_low:
            return "🏛️ PM-KISAN:\n\n" + AI_KNOWLEDGE["schemes"]["pmkisan"]

        if "kcc" in q_low or "credit card" in q_low or "loan" in q_low or "karj" in q_low:
            return "🏛️ Kisan Credit Card:\n\n" + AI_KNOWLEDGE["schemes"]["kcc"]

        if "insurance" in q_low or "bima" in q_low or "pmfby" in q_low:
            return "🏛️ PM Fasal Bima Yojana:\n\n" + AI_KNOWLEDGE["schemes"]["pmfby"]

        if "solar" in q_low or "pump" in q_low or "kusum" in q_low:
            return "🏛️ Solar Pump Scheme:\n\n" + AI_KNOWLEDGE["schemes"]["solar pump"]

        # Crop specific
        c_db = self.conn.cursor()
        c_db.execute("SELECT name, season, soil_type, profit FROM crops")
        all_crops = c_db.fetchall()
        for name, season, soil_types, profit in all_crops:
            if name.lower() in q_low:
                return (f"🌾 {name} Information:\n\n"
                        f"📅 Season: {season}\n"
                        f"🌱 Suitable Soil: {soil_types}\n"
                        f"💰 Expected Profit: ₹{profit:,} per acre\n\n"
                        f"Ask me about sowing time, fertilizers, or diseases for {name}!")

        # Profit queries
        if "profit" in q_low or "income" in q_low or "earn" in q_low or "kamai" in q_low:
            soil = u.get("soil_type", "Loamy")
            c_db.execute("SELECT name, profit FROM crops WHERE soil_type LIKE ? ORDER BY profit DESC LIMIT 3",
                         (f"%{soil}%",))
            top_crops = c_db.fetchall()
            if top_crops:
                lines = "\n".join([f"  🌾 {n}: ₹{p:,}/acre" for n, p in top_crops])
                return f"💰 Top profitable crops for your {soil} soil:\n\n{lines}\n\nProfit depends on local market prices. Consider crop diversification!"
            return "💰 To maximise profit: choose crops suited to your soil, reduce input costs with organic farming, and sell at the right time!"

        # Weather advice
        if "weather" in q_low or "mausam" in q_low or "rain" in q_low or "barish" in q_low:
            return "🌤️ For live weather: go to the Weather tab and search your city. I recommend checking weather before irrigation and spraying schedules!"

        # Disease queries
        if "disease" in q_low or "bimari" in q_low or "rog" in q_low:
            return ("🦠 For disease detection: go to the Disease Detection tab and describe what you see.\n\n"
                    "Common symptoms to describe:\n• Leaf color changes\n• Spot shapes\n"
                    "• Powdery coatings\n• Wilting patterns\n• Insect presence")

        # Greetings
        if any(g in q_low for g in ["hello","hi","namaste","namaskar","helo"]):
            return f"🙏 Namaste {u['name']}! I'm ready to help you with your {u.get('farm_size',0)}-acre farm.\n\nWhat would you like to know today?"

        if "thank" in q_low or "shukriya" in q_low or "dhanyavad" in q_low:
            return "🙏 You're welcome! Happy farming! May your harvest be plentiful! 🌾"

        # Default helpful response
        return (f"🤔 I'm not sure about that specific question. Here's what I can help with:\n\n"
                f"• Type 'soil' — advice for your {u.get('soil_type','loamy')} soil\n"
                f"• Type 'kharif' or 'rabi' — season crop lists\n"
                f"• Type a crop name — specific crop info\n"
                f"• Type 'PM-KISAN' — government scheme details\n"
                f"• Type 'urea' / 'DAP' — fertilizer guidance\n"
                f"• Type 'drip' — irrigation advice\n\n"
                f"Please try rephrasing or use the Disease Detection tab for plant health issues!")

    # ── FARM DIARY ───────────────────────────────────────────────────────────
    def show_diary(self):
        self._clear_content()
        self._content_header(f"📖  {self.t('diary')}",
                             "  Keep track of all farm activities")

        main = ctk.CTkFrame(self._content_frame, fg_color=BG)
        main.pack(fill="both", expand=True, padx=18, pady=14)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Add entry
        add_card = ctk.CTkFrame(main, fg_color=C1, corner_radius=14)
        add_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ctk.CTkLabel(add_card, text="✍️  New Entry",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(14, 6))
        ctk.CTkFrame(add_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(add_card, text="Date:", font=ctk.CTkFont(size=12), text_color=TXM).pack(anchor="w", padx=16)
        self.diary_date = ctk.CTkEntry(add_card, width=290, height=38,
                                       fg_color=C2, border_color="#2a4a30", text_color=TXT)
        self.diary_date.insert(0, str(date.today()))
        self.diary_date.pack(padx=16, pady=(3, 10))

        ctk.CTkLabel(add_card, text="Activity:", font=ctk.CTkFont(size=12), text_color=TXM).pack(anchor="w", padx=16)
        self.diary_act = ctk.CTkComboBox(add_card,
            values=["Sowing","Irrigation","Fertilizer","Pesticide","Weeding","Harvest","Soil Test","Market Visit","Other"],
            width=290, height=38, fg_color=C2, border_color="#2a4a30", text_color=TXT,
            button_color=G3, dropdown_fg_color=C2, dropdown_text_color=TXT)
        self.diary_act.set("Sowing")
        self.diary_act.pack(padx=16, pady=(3, 10))

        ctk.CTkLabel(add_card, text="Notes:", font=ctk.CTkFont(size=12), text_color=TXM).pack(anchor="w", padx=16)
        self.diary_notes = ctk.CTkTextbox(add_card, height=120, width=290,
                                          fg_color=C2, border_color="#2a4a30", text_color=TXT,
                                          font=ctk.CTkFont(size=12))
        self.diary_notes.pack(padx=16, pady=(3, 14))

        ctk.CTkButton(add_card, text=f"💾  {self.t('save')}", command=self._save_diary,
                      fg_color=G2, hover_color=G3, text_color=BG,
                      height=42, font=ctk.CTkFont(size=13, weight="bold")).pack(padx=16, pady=(0, 16))

        # History
        hist_card = ctk.CTkFrame(main, fg_color=C1, corner_radius=14)
        hist_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ctk.CTkLabel(hist_card, text=f"📋  {self.t('history')}",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=G1).pack(anchor="w", padx=16, pady=(14, 6))
        ctk.CTkFrame(hist_card, height=1, fg_color=G3).pack(fill="x", padx=16, pady=(0, 10))

        self.diary_list = ctk.CTkScrollableFrame(hist_card, fg_color="transparent")
        self.diary_list.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._refresh_diary()

    def _save_diary(self):
        d = self.diary_date.get().strip()
        a = self.diary_act.get()
        n = self.diary_notes.get("1.0", "end").strip()
        if not a: messagebox.showerror("Error", "Please select an activity"); return
        c = self.conn.cursor()
        c.execute("INSERT INTO diary (user_id,date,activity,notes) VALUES(?,?,?,?)",
                  (self.current_user['id'], d, a, n))
        self.conn.commit()
        self.diary_notes.delete("1.0", "end")
        messagebox.showinfo("✅", "Diary entry saved!")
        self._refresh_diary()

    def _refresh_diary(self):
        for w in self.diary_list.winfo_children(): w.destroy()
        c = self.conn.cursor()
        c.execute("SELECT date, activity, notes FROM diary WHERE user_id=? ORDER BY id DESC LIMIT 25",
                  (self.current_user['id'],))
        entries = c.fetchall()
        if not entries:
            ctk.CTkLabel(self.diary_list, text="No entries yet. Add your first activity!",
                         font=ctk.CTkFont(size=12), text_color=TXM).pack(pady=20)
            return

        act_icons = {"Sowing":"🌱","Irrigation":"💧","Fertilizer":"🧪","Pesticide":"💊",
                     "Weeding":"🌿","Harvest":"🌾","Soil Test":"🔬","Market Visit":"🏪","Other":"📝"}
        for d, a, n in entries:
            row = ctk.CTkFrame(self.diary_list, fg_color=C2, corner_radius=8)
            row.pack(fill="x", pady=3)
            icon = act_icons.get(a, "📝")
            ctk.CTkLabel(row, text=f"{icon}  {a}",
                         font=ctk.CTkFont(size=12, weight="bold"), text_color=G1).pack(anchor="w", padx=12, pady=(6, 1))
            ctk.CTkLabel(row, text=f"📅 {d}",
                         font=ctk.CTkFont(size=11), text_color=TXM).pack(anchor="w", padx=12)
            if n:
                ctk.CTkLabel(row, text=n[:90] + ("..." if len(n)>90 else ""),
                             font=ctk.CTkFont(size=11), text_color=TXT,
                             wraplength=340, justify="left").pack(anchor="w", padx=12, pady=(0, 6))
            else:
                ctk.CTkFrame(row, height=4, fg_color="transparent").pack()

    # ── LOGOUT ───────────────────────────────────────────────────────────────
    def logout(self):
        self._clear_saved_login()
        self.current_user = None
        self.show_login()


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = ctk.CTk()
    app = KisanSaathiApp(root)
    root.mainloop()
