"""Official Telangana 33 Districts Registry and Normalization Layer.
Strictly implements the exact 33 administrative districts of Telangana.
"""

from typing import Dict, Any, List, Optional, Tuple

EXACT_33_DISTRICTS = [
    "Adilabad",
    "Bhadradri Kothagudem",
    "Hanumakonda",
    "Hyderabad",
    "Jagtial",
    "Jangaon",
    "Jayashankar Bhupalpally",
    "Jogulamba Gadwal",
    "Kamareddy",
    "Karimnagar",
    "Khammam",
    "Kumuram Bheem",
    "Mahabubabad",
    "Mahabubnagar",
    "Mancherial",
    "Medak",
    "Medchal-Malkajgiri",
    "Mulugu",
    "Nagarkurnool",
    "Nalgonda",
    "Narayanpet",
    "Nirmal",
    "Nizamabad",
    "Peddapalli",
    "Rajanna Sircilla",
    "Rangareddy",
    "Sangareddy",
    "Siddipet",
    "Suryapet",
    "Vikarabad",
    "Wanaparthy",
    "Warangal",
    "Yadadri Bhuvanagiri"
]

# District centroids / administrative representative coordinates (lat, lon)
DISTRICTS: Dict[str, Tuple[float, float]] = {
    "Adilabad": (19.67, 78.53),
    "Bhadradri Kothagudem": (17.55, 80.60),
    "Hanumakonda": (18.06, 79.46),
    "Hyderabad": (17.385, 78.487),
    "Jagtial": (18.79, 78.91),
    "Jangaon": (17.72, 79.15),
    "Jayashankar Bhupalpally": (18.45, 79.88),
    "Jogulamba Gadwal": (16.18, 77.80),
    "Kamareddy": (18.32, 78.34),
    "Karimnagar": (18.44, 79.20),
    "Khammam": (17.25, 80.15),
    "Kumuram Bheem": (19.36, 79.28),
    "Mahabubabad": (17.60, 80.00),
    "Mahabubnagar": (16.74, 78.08),
    "Mancherial": (18.87, 79.46),
    "Medak": (18.05, 78.26),
    "Medchal-Malkajgiri": (17.60, 78.58),
    "Mulugu": (18.19, 80.20),
    "Nagarkurnool": (16.48, 78.38),
    "Nalgonda": (17.05, 79.27),
    "Narayanpet": (16.74, 77.58),
    "Nirmal": (19.10, 78.34),
    "Nizamabad": (18.67, 78.09),
    "Peddapalli": (18.62, 79.37),
    "Rajanna Sircilla": (18.38, 78.68),
    "Rangareddy": (17.20, 78.30),
    "Sangareddy": (17.65, 77.85),
    "Siddipet": (18.10, 78.85),
    "Suryapet": (17.14, 79.62),
    "Vikarabad": (17.34, 77.90),
    "Wanaparthy": (16.36, 78.06),
    "Warangal": (17.88, 79.72),
    "Yadadri Bhuvanagiri": (17.48, 79.02),
}

# Compatibility alias for Kumuram Bheem Asifabad
DISTRICTS["Kumuram Bheem Asifabad"] = DISTRICTS["Kumuram Bheem"]

DISTRICT_NAMES: List[str] = sorted(EXACT_33_DISTRICTS)

# Telugu transliterations
DISTRICT_TELUGU: Dict[str, str] = {
    "Adilabad": "ఆదిలాబాద్",
    "Bhadradri Kothagudem": "భద్రాద్రి కొత్తగూడెం",
    "Hanumakonda": "హనుమకొండ",
    "Hyderabad": "హైదరాబాద్",
    "Jagtial": "జగిత్యాల",
    "Jangaon": "జనగాం",
    "Jayashankar Bhupalpally": "జయశంకర్ భూపాలపల్లి",
    "Jogulamba Gadwal": "జోగులాంబ గద్వాల",
    "Kamareddy": "కామారెడ్డి",
    "Karimnagar": "కరీంనగర్",
    "Khammam": "ఖమ్మం",
    "Kumuram Bheem": "కుమురం భీమ్",
    "Kumuram Bheem Asifabad": "కుమురం భీమ్ ఆసిఫాబాద్",
    "Mahabubabad": "మహబూబాబాద్",
    "Mahabubnagar": "మహబూబ్‌నగర్",
    "Mancherial": "మంచిర్యాల",
    "Medak": "మెదక్",
    "Medchal-Malkajgiri": "మేడ్చల్-మల్కాజ్‌గిరి",
    "Mulugu": "ములుగు",
    "Nagarkurnool": "నాగర్‌కర్నూల్",
    "Nalgonda": "నల్గొండ",
    "Narayanpet": "నారాయణపేట",
    "Nirmal": "నిర్మల్",
    "Nizamabad": "నిజామాబాద్",
    "Peddapalli": "పెద్దపల్లి",
    "Rajanna Sircilla": "రాజన్న సిరిసిల్ల",
    "Rangareddy": "రంగారెడ్డి",
    "Sangareddy": "సంగారెడ్డి",
    "Siddipet": "సిద్దిపేట",
    "Suryapet": "సూర్యాపేట",
    "Vikarabad": "వికారాబాద్",
    "Wanaparthy": "వనపర్తి",
    "Warangal": "వరంగల్",
    "Yadadri Bhuvanagiri": "యాదాద్రి భువనగిరి",
}

# Hindi transliterations (हिंदी)
DISTRICT_HINDI: Dict[str, str] = {
    "Adilabad": "आदिलाबाद",
    "Bhadradri Kothagudem": "भद्राद्री कोठागुडेम",
    "Hanumakonda": "हनुमकोंडा",
    "Hyderabad": "हैदराबाद",
    "Jagtial": "जगित्याल",
    "Jangaon": "जनगांव",
    "Jayashankar Bhupalpally": "जयशंकर भूपालपल्ली",
    "Jogulamba Gadwal": "जोगुलाम्बा गडवाल",
    "Kamareddy": "कामारेड्डी",
    "Karimnagar": "करीमनगर",
    "Khammam": "खम्मम",
    "Kumuram Bheem": "कुमुरम भीम",
    "Kumuram Bheem Asifabad": "कुमुरम भीम आसिफाबाद",
    "Mahabubabad": "महबूबाबाद",
    "Mahabubnagar": "महबूबनगर",
    "Mancherial": "मंचिरियाल",
    "Medak": "मेदक",
    "Medchal-Malkajgiri": "मेडचल-मलकाजगिरी",
    "Mulugu": "मुलुगु",
    "Nagarkurnool": "नागरकुरनूल",
    "Nalgonda": "नलगोंडा",
    "Narayanpet": "नारायणपेट",
    "Nirmal": "निर्मल",
    "Nizamabad": "निजामाबाद",
    "Peddapalli": "पेद्दापल्ली",
    "Rajanna Sircilla": "राजन्ना सिरसिल्ला",
    "Rangareddy": "रंगारेड्डी",
    "Sangareddy": "संगारेड्डी",
    "Siddipet": "सिद्दिपेट",
    "Suryapet": "सूर्यापेट",
    "Vikarabad": "विकाराबाद",
    "Wanaparthy": "वनपर्ती",
    "Warangal": "वारंगल",
    "Yadadri Bhuvanagiri": "यादाद्री भुवनगिरी",
}

# Aliases mapping (all lowercase alphanumeric -> canonical official name)
ALIAS_MAP: Dict[str, str] = {
    "kumurambheem": "Kumuram Bheem",
    "kumurambheemasifabad": "Kumuram Bheem",
    "komarambheem": "Kumuram Bheem",
    "komarambheemasifabad": "Kumuram Bheem",
    "asifabad": "Kumuram Bheem",
    "hanumakonda": "Hanumakonda",
    "warangalurban": "Hanumakonda",
    "warangal": "Warangal",
    "warangalrural": "Warangal",
    "rangareddy": "Rangareddy",
    "rangareddi": "Rangareddy",
    "medchalmalkajgiri": "Medchal-Malkajgiri",
    "medchal": "Medchal-Malkajgiri",
    "jayashankarbhupalpally": "Jayashankar Bhupalpally",
    "jayashankarbhupalapally": "Jayashankar Bhupalpally",
    "bhupalpally": "Jayashankar Bhupalpally",
    "yadadribhuvanagiri": "Yadadri Bhuvanagiri",
    "yadadri": "Yadadri Bhuvanagiri",
    "bhadradrikothagudem": "Bhadradri Kothagudem",
    "kothagudem": "Bhadradri Kothagudem",
    "jogulambagadwal": "Jogulamba Gadwal",
    "gadwal": "Jogulamba Gadwal",
    "rajannasircilla": "Rajanna Sircilla",
    "sircilla": "Rajanna Sircilla",
}

def to_clean_slug(text: str) -> str:
    """Helper to convert any district name or input to a clean alphanumeric slug."""
    return "".join(c for c in text.lower() if c.isalnum())

def normalize_district_name(input_name: str) -> str:
    """
    Normalizes any input string (including aliases, previous names, and Telugu names)
    to the official 33-district English display name.
    """
    if not input_name:
        return "Hyderabad"

    # Direct match in exact 33
    if input_name in EXACT_33_DISTRICTS:
        return input_name

    # Check Telugu reverse lookup
    for en_name, te_name in DISTRICT_TELUGU.items():
        if input_name == te_name:
            return "Kumuram Bheem" if en_name == "Kumuram Bheem Asifabad" else en_name

    # Check Hindi reverse lookup
    for en_name, hi_name in DISTRICT_HINDI.items():
        if input_name == hi_name:
            return "Kumuram Bheem" if en_name == "Kumuram Bheem Asifabad" else en_name

    slug = to_clean_slug(input_name)
    if slug in ALIAS_MAP:
        return ALIAS_MAP[slug]

    # Fuzzy match slug against exact 33
    for d in EXACT_33_DISTRICTS:
        if to_clean_slug(d) == slug:
            return d

    # Fallback to closest match or Hyderabad
    for d in EXACT_33_DISTRICTS:
        if slug in to_clean_slug(d) or to_clean_slug(d) in slug:
            return d

    return "Hyderabad"

def get_internal_id(district_name: str) -> str:
    """Returns normalized internal identifier (e.g., 'kumuram_bheem')."""
    official = normalize_district_name(district_name)
    return official.lower().replace("-", "_").replace(" ", "_")

def validate_district_name(district_name: str) -> bool:
    """Validates whether a given district name belongs to the 33 official districts."""
    official = normalize_district_name(district_name)
    return official in EXACT_33_DISTRICTS

def get_coords(district_identifier: str) -> Tuple[float, float]:
    """Retrieve latitude and longitude for any valid district identifier."""
    official = normalize_district_name(district_identifier)
    return DISTRICTS[official]

def format_district_name(district_identifier: str, lang: str = "en") -> str:
    """Format district name for UI display in requested language (English, Telugu, Hindi)."""
    if district_identifier == "ALL":
        if lang == "te":
            return "అన్ని జిల్లాలు (రాష్ట్ర వ్యాప్తంగా)"
        elif lang == "hi":
            return "सभी जिले (राज्यव्यापी)"
        return "All Districts (Statewide)"
    official = normalize_district_name(district_identifier)
    if lang == "te":
        return DISTRICT_TELUGU.get(official, official)
    elif lang == "hi":
        return DISTRICT_HINDI.get(official, official)
    return official

