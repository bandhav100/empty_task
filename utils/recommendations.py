"""Citizen action recommendations for water stress and air quality in English and Telugu."""

from typing import List, Dict

CITIZEN_WATER_RECOMMENDATIONS = {
    0: {  # Low Risk
        "en": [
            "Maintain sustainable water habits: regular aerator cleaning and mindful tap usage.",
            "Prime window for rooftop rainwater harvesting: clean filters and inspect recharge pits before the monsoon.",
            "Verify household plumbing: fix silent toilet cistern leaks to prevent monthly water loss.",
            "Re-check the outlook monthly: ocean anomalies can shift seasonal rainfall patterns within weeks."
        ],
        "te": [
            "సాధారణ నీటి పొదుపు అలవాట్లను కొనసాగించండి: కుళాయిల వాడకంలో జాగ్రత్త వహించండి.",
            "పైకప్పు వర్షపు నీటి సేకరణకు ఇదే సరైన సమయం: వర్షాకాలం రాకముందే ఫిల్టర్లు, ఇంకుడు గుంతలను శుభ్రం చేయండి.",
            "ఇంటి ప్లంబింగ్‌ను తనిఖీ చేయండి: నిశ్శబ్దంగా కారే టాయిలెట్ లీకులను వెంటనే సరిచేయండి.",
            "ప్రతి నెలా ఈ సలహాదారును పరిశీలించండి: సముద్ర ఉష్ణోగ్రతల మార్పుల వల్ల కొన్ని వారాల్లోనే పరిస్థితులు మారవచ్చు."
        ],
        "hi": [
            "जल संरक्षण की स्थायी आदतें बनाए रखें: नियमित नल एरेटर की सफाई और सतर्क जल उपयोग।",
            "छत पर वर्षा जल संचयन (RWH) का उत्तम समय: मानसून से पहले फिल्टर और रीचार्ज गड्ढों की सफाई करें।",
            "घरेलू प्लंबिंग की जांच करें: टॉयलेट सिस्टर्न लीकेज को तुरंत ठीक कर मासिक पानी की बर्बादी रोकें।",
            "हर महीने परिदृश्य की समीक्षा करें: महासागरीय विसंगतियां कुछ ही हफ्तों में मौसमी वर्षा बदल सकती हैं।"
        ]
    },
    1: {  # Medium Risk
        "en": [
            "Implement a 10% to 15% reduction in domestic water consumption: take shorter bucket showers and only run full washing loads.",
            "Inspect and repair all dripping faucets, overhead tank float valves, and municipal pipeline connections.",
            "Establish a 48-hour household emergency drinking water buffer in clean covered food-grade containers.",
            "Adopt graywater reuse: divert rinse water from clothes or vegetables to household plants and floor cleaning.",
            "Stay informed on municipal supply schedules from HMWSSB or Mission Bhagiratha local water distribution."
        ],
        "te": [
            "రోజువారీ నీటి వాడకాన్ని 10% నుండి 15% వరకు తగ్గించండి: బకెట్ స్నానం చేయండి, పూర్తి లోడ్ ఉన్నప్పుడే బట్టలు ఉతకండి.",
            "కారే కుళాయిలు, ఓవర్‌హెడ్ ట్యాంక్ ఫ్లోట్ వాల్వ్‌లు, పైపులను వెంటనే మరమ్మతు చేయండి.",
            "పరిశుభ్రమైన పాత్రలలో కనీసం 2 రోజులకు సరిపడా తాగునీటిని నిల్వ ఉంచండి.",
            "ఉతికిన నీటిని లేదా కూరగాయలు కడిగిన నీటిని మొక్కలకు, ఇంటి శుభ్రతకు మళ్ళీ ఉపయోగించండి.",
            "స్థానిక మున్సిపల్ / మిషన్ భగీరథ నీటి సరఫరా షెడ్యూల్ నోటీసులను గమనించండి."
        ],
        "hi": [
            "घरेलू पानी के उपयोग में 10% से 15% की कमी लाएं: बाल्टी से स्नान करें और केवल पूरी लोड पर कपड़े धोएं।",
            "टपकते नलों, ओवरहेड टैंक फ्लोट वाल्व और पाइपलाइन कनेक्शनों की तुरंत मरम्मत करें।",
            "साफ, ढके हुए बर्तनों में 48 घंटे के लिए आपातकालीन पेयजल का सुरक्षित भंडारण रखें।",
            "ग्रे-वाटर का पुन: उपयोग: कपड़े या सब्जी धोने के पानी को पौधों और फर्श की सफाई में लगाएं।",
            "स्थानीय HMWSSB या मिशन भगीरथ जलापूर्ति कार्यक्रम से अपडेट रहें।"
        ]
    },
    2: {  # High Risk
        "en": [
            "Secure drinking water reserves for 3 to 4 days; do not wait until local pressure collapses.",
            "Preemptively coordinate residential water tanker or 20-liter bubble-top supply before peak shortage surcharges.",
            "Strictly eliminate discretionary water usage: suspend garden hose watering, car washing, and courtyard washing.",
            "Monitor sump and borewell drawdown weekly; install a dry-run protector on domestic water pumps.",
            "Prioritize community water pooling and ensure vulnerable elderly or infant neighbors have reliable potable water.",
            "Clean and repair rooftop catchment channels to capture every drop of unseasonal or sudden downpours."
        ],
        "te": [
            "కనీసం 3 నుండి 4 రోజులకు సరిపడా తాగునీటిని ముందుగానే నిల్వ చేసుకోండి; కొరత మొదలయ్యే వరకు ఆగవద్దు.",
            "పీక్ సమయంలో ట్యాంకర్ల కొరత రాకముందే రెసిడెన్షియల్ వాటర్ ట్యాంకర్ లేదా 20 లీటర్ల క్యాన్ల సరఫరాను సిద్ధం చేసుకోండి.",
            "పైపులతో కార్లు కడగడం, ప్రాంగణం కడగడం, తోటలకు నీరు పోయడం వంటి అనవసర నీటి వాడకాన్ని తక్షణమే నిలిపివేయండి.",
            "సంప్ మరియు బోరుబావి నీటి మట్టాలను వారానికోసారి గమనించండి; మోటార్ డ్రై-రన్ ప్రొటెక్టర్ ఏర్పాటు చేసుకోండి.",
            "అపార్ట్‌మెంట్లు, బస్తీలలో నీటి వాడకాన్ని పంచుకోండి; వృద్ధులు, పసిపిల్లలు ఉన్న ఇళ్లకు తాగునీటి లభ్యతను నిర్ధారించండి.",
            "ఆకస్మిక వర్షపు నీటిని ఒడిసిపట్టడానికి పైకప్పు పైపులు, ఇంకుడు గుంతలను సిద్ధంగా ఉంచండి."
        ],
        "hi": [
            "कम से कम 3 से 4 दिनों के लिए पेयजल सुरक्षित रखें; आपूर्ति दबाव गिरने तक प्रतीक्षा न करें।",
            "अत्यधिक कमी से पहले ही आवासीय पानी के टैंकर या 20-लीटर जार आपूर्ति का पूर्व-प्रबंध करें।",
            "अनावश्यक जल उपयोग पूरी तरह बंद करें: होज़ पाइप से कार धोना, आंगन धोना और लॉन में पानी देना रोकें।",
            "सम्प और बोरवेल के जलस्तर पर साप्ताहिक नजर रखें; घरेलू पंपों पर ड्राई-रन प्रोटेक्टर लगवाएं।",
            "समुदाय में जल सहयोग सुनिश्चित करें; बुजुर्गों और छोटे बच्चों वाले परिवारों के लिए पेयजल प्राथमिकता दें।",
            "अचानक होने वाली बारिश की हर बूंद संचित करने के लिए छत के पाइप और जल संचयन गड्ढों को तैयार रखें।"
        ]
    }
}

def get_water_recommendations(risk_level: int, lang: str = "en") -> List[str]:
    """Retrieve actionable water recommendations for the given risk level."""
    rec_dict = CITIZEN_WATER_RECOMMENDATIONS.get(risk_level, CITIZEN_WATER_RECOMMENDATIONS[0])
    return rec_dict.get(lang, rec_dict["en"])


# ----------------- EL NIÑO CITIZEN & FARMER PRECAUTIONS -----------------
EL_NINO_PRECAUTIONS = [
    {
        "id": "agriculture",
        "icon": "🌾",
        "color": "#16a34a",
        "title": {
            "en": "Farming & Agriculture Safeguards",
            "te": "వ్యవసాయం & పంటల భద్రతా చర్యలు",
            "hi": "कृषि एवं फसल सुरक्षा उपाय"
        },
        "precautions": {
            "en": [
                "Avoid sowing immediately after early sporadic showers; wait for steady monsoon rainfall to prevent seed and input loss.",
                "Switch from water-intensive crops (paddy, sugarcane) to drought-resilient millets (Jowar, Bajra, Ragi), pulses (red gram, green gram), and oilseeds.",
                "Adopt micro-irrigation (drip / sprinkler) and organic mulching to conserve root-zone soil moisture by 30% to 40%.",
                "Enroll early in state and central crop insurance programs (PMFBY / Rythu Bima) before notified cut-off dates to buffer against dry-spell failure.",
                "Construct or desilt on-farm ponds (Panta Kuntalu) to store runoff for critical life-saving supplemental irrigation."
            ],
            "te": [
                "తొలకరి మొదటి చినుకులు పడగానే తొందరపడి విత్తనాలు వేయకండి; రుతుపవనాలు స్థిరపడే వరకు వేచి ఉండండి.",
                "ఎక్కువ నీరు అవసరమయ్యే వరి, చెరకు వంటి పంటలకు బదులుగా చిరుధాన్యాలు (జొన్నలు, సజ్జలు, రాగులు), పప్పుధాన్యాలు, నూనెగింజలు సాగు చేయండి.",
                "నేలలో తేమను కాపాడుకోవడానికి బిందు, తుంపర (డ్రిప్, స్ప్రింక్లర్) సేద్యం మరియు మల్చింగ్ పద్ధతులను అనుసరించండి (30-40% నీరు ఆదా అవుతుంది).",
                "వర్షాభావ పరిస్థితుల నుంచి రక్షణ కోసం నోటిఫై చేసిన తేదీలలోపే పంటల బీమా (PMFBY / రైతు బీమా) చేయించుకోండి.",
                "వర్షపు నీటిని నిల్వ ఉంచేందుకు వ్యవసాయ క్షేత్రాల్లో పంట కుంటలు (ఫార్మ్ పాండ్స్) ఏర్పాటు చేసుకోండి."
            ],
            "hi": [
                "शुरुआती छिटपुट बारिश के तुरंत बाद बुवाई न करें; बीज के नुकसान से बचने के लिए मानसून के स्थिर होने तक प्रतीक्षा करें।",
                "अधिक पानी वाली फसलों (धान, गन्ना) के स्थान पर सूखा-प्रतिरोधी मोटे अनाज (ज्वार, बाजरा, रागी), दलहन (अरहर, मूंग) और तिलहन लगाएं।",
                "मिट्टी की नमी वाष्पीकरण को 30-40% कम करने के लिए सूक्ष्म सिंचाई (ड्रिप/स्प्रिंकलर) और मल्चिंग तकनीक अपनाएं।",
                "सूखे के जोखिम से सुरक्षा के लिए समय रहते फसल बीमा (PMFBY / रायथु बीमा) में पंजीकरण कराएं।",
                "अंतिम चरण की जीवनरक्षक सिंचाई के लिए खेत में जल संचयन तालाब (फार्म पॉन्ड) तैयार रखें।"
            ]
        }
    },
    {
        "id": "groundwater",
        "icon": "💧",
        "color": "#0284c7",
        "title": {
            "en": "Groundwater & Drinking Water Protection",
            "te": "భూగర్భ జలాలు & తాగునీటి రక్షణ",
            "hi": "भूजल एवं घरेलू पेयजल सुरक्षा"
        },
        "precautions": {
            "en": [
                "Install automated dry-run protectors and phase sensors on agricultural and domestic borewells to prevent motor burnout under deep drawdown.",
                "Deepen, clean, and desilt rooftop rainwater harvesting recharge pits (ఇంకుడు గుంతలు) ahead of erratic high-intensity showers.",
                "Maintain a 3-to-4 day emergency drinking water buffer in clean, covered food-grade containers.",
                "Practice systematic domestic graywater reuse: divert vegetable rinse and RO reject water to household plants, flushing, and floor cleaning.",
                "Coordinate with local Mission Bhagiratha / HMWSSB officials and report pipeline leakages or pressure drops promptly."
            ],
            "te": [
                "బోరుబావులలో నీటి మట్టం తగ్గినప్పుడు మోటార్లు కాలిపోకుండా ఆటోమేటిక్ డ్రై-రన్ ప్రొటెక్టర్లను ఏర్పాటు చేయండి.",
                "తీవ్రమైన ఆకస్మిక వర్షపు నీరు భూమిలోకి ఇంకేలా ఇంటి పైకప్పు వర్షపు నీటి ఇంకుడు గుంతలను ముందే శుభ్రం చేసి సిద్ధంగా ఉంచండి.",
                "పరిశుభ్రమైన, మూత ఉన్న పాత్రలలో కనీసం 3 నుండి 4 రోజులకు సరిపడా తాగునీటిని నిల్వ ఉంచుకోండి.",
                "కూరగాయలు కడిగిన నీరు, RO ఫిల్టర్ వ్యర్థ నీటిని మొక్కలకు, ఇంటి శుభ్రతకు మళ్ళీ ఉపయోగించండి (గ్రే-వాటర్ రీసైక్లింగ్).",
                "స్థానిక మిషన్ భగీరథ లేదా HMWSSB అధికారులతో సంప్రదించి, పైపుల లీకేజీలు ఉంటే వెంటనే ఫిర్యాదు చేయండి."
            ],
            "hi": [
                "जलस्तर गिरने पर मोटर जलने से बचाने के लिए बोरवेल पंपों पर ड्राई-रन प्रोटेक्टर और फेज सेंसर लगाएं।",
                "अचानक तेज बारिश के पानी को भूमिगत करने के लिए छत के वर्षा जल संचयन और रीचार्ज गड्ढों की सफाई करें।",
                "साफ और ढके हुए बर्तनों में कम से कम 3 से 4 दिनों के लिए आपातकालीन पेयजल सुरक्षित रखें।",
                "घरेलू ग्रे-वाटर का पुन: उपयोग: सब्जी धोने और आरओ रिजेक्ट पानी को बागवानी और फ्लशिंग में लगाएं।",
                "स्थानीय मिशन भगीरथ या HMWSSB अधिकारियों के संपर्क में रहें और पाइपलाइन लीकेज की तुरंत सूचना दें।"
            ]
        }
    },
    {
        "id": "heatwave",
        "icon": "☀️",
        "color": "#ea580c",
        "title": {
            "en": "Heatwave, Citizen Health & Outdoor Safety",
            "te": "వడగాల్పులు, ప్రజారోగ్యం & భద్రతా జాగ్రత్తలు",
            "hi": "लू, नागरिक स्वास्थ्य एवं धूप से सुरक्षा"
        },
        "precautions": {
            "en": [
                "Avoid strenuous outdoor activity and direct sun exposure between 11:00 AM and 4:00 PM during prolonged summer heatwaves.",
                "Stay consistently hydrated: consume oral rehydration salts (ORS), buttermilk (మజ్జిగ), tender coconut water, and lemon water frequently.",
                "Prioritize care for high-risk individuals: keep infants, pregnant women, and elderly family members in cool, ventilated rooms.",
                "Wear light-colored, loose cotton clothing and use umbrellas or wide-brimmed head coverings when outdoors.",
                "Recognize early symptoms of heat stroke (dizziness, nausea, cessation of sweating, high pulse) and seek immediate medical assistance."
            ],
            "te": [
                "వేసవిలో తీవ్ర ఎండలు, వడగాల్పుల సమయంలో ఉదయం 11:00 గంటల నుండి సాయంత్రం 4:00 గంటల వరకు బయట తిరగకండి.",
                "శరీరం డీహైడ్రేట్ కాకుండా తరచూ మజ్జిగ, ఓఆర్ఎస్ (ORS), కొబ్బరి నీళ్ళు, నిమ్మరసం పుష్కలంగా తాగండి.",
                "వృద్ధులు, గర్భిణీలు, చిన్న పిల్లల విషయంలో ప్రత్యేక జాగ్రత్తలు తీసుకోండి; వారిని చల్లని ప్రదేశాలలో ఉంచండి.",
                "లేత రంగు కాటన్ దుస్తులు ధరించండి; ఎండలో వెళ్ళేటప్పుడు గొడుగు లేదా తలపాగా తప్పనిసరిగా వాడండి.",
                "వడదెబ్బ లక్షణాలు (తలతిరగడం, వాంతులు, నాడి వేగంగా కొట్టుకోవడం) కనిపిస్తే వెంటనే సమీప వైద్యుడిని సంప్రదించండి."
            ],
            "hi": [
                "अल नीनो प्रेरित तीव्र गर्मी में सुबह 11:00 बजे से शाम 4:00 बजे तक सीधी धूप और भारी काम से बचें।",
                "शरीर में पानी की कमी न होने दें: ओआरएस (ORS), छाछ, नारियल पानी और नींबू पानी का नियमित सेवन करें।",
                "छोटे बच्चों, गर्भवती महिलाओं और बुजुर्गों का विशेष ध्यान रखें; उन्हें ठंडे और हवादार कमरों में रखें।",
                "हल्के रंग के ढीले सूती कपड़े पहनें और बाहर निकलते समय छाता या सिर पर कपड़ा अवश्य रखें।",
                "लू के लक्षण (चक्कर आना, जी मिचलाना, तेज नाड़ी) दिखने पर तुरंत नजदीकी स्वास्थ्य केंद्र से संपर्क करें।"
            ]
        }
    },
    {
        "id": "livestock",
        "icon": "🐄",
        "color": "#9333ea",
        "title": {
            "en": "Livestock, Fodder & Veterinary Protection",
            "te": "పశు సంరక్షణ & ఎండు మేత యాజమాన్యం",
            "hi": "पशुधन, सूखा चारा एवं पशु स्वास्थ्य"
        },
        "precautions": {
            "en": [
                "Pre-stock and store dry fodder (paddy straw, maize silage) in moisture-proof sheds ahead of drought-induced green fodder scarcity.",
                "Provide thatched roof shading, wet gunny bags, or mist sprinklers in cattle sheds to reduce thermal stress.",
                "Ensure clean drinking water with mineral mixture and electrolytes is accessible to livestock around the clock.",
                "Complete timely livestock vaccinations against seasonal foot-and-mouth disease (FMD) and hemorrhagic septicemia.",
                "Graze cattle only during early morning or late evening hours to prevent thermal exhaustion."
            ],
            "te": [
                "పచ్చిమేత కొరత రాకముందే ఎండు గడ్డి, మొక్కజొన్న సైలేజ్ వంటి ఎండు మేతను ముందుగానే నిల్వ చేసుకోండి.",
                "పశువుల కొట్టాలకు తడి గోనె సంచులు, తుంపరలు (స్ప్రింక్లర్లు) ఏర్పాటు చేసి ఎండ వేడిమి నుంచి ఉపశమనం కల్పించండి.",
                "పశువులకు 24 గంటలూ శుభ్రమైన తాగునీరు అందుబాటులో ఉంచండి; నీటిలో మినరల్ మిశ్రమం మరియు ఎలక్ట్రోలైట్స్ కలపండి.",
                "వర్షాకాలం ముందు వేసే గాలికుంటు వ్యాధి, గొంతువాపు నివారణ టీకాలను పశుసంవర్ధక శాఖ ద్వారా వేయించండి.",
                "ఎండ ఎక్కువగా ఉన్నప్పుడు కాకుండా తెల్లవారుజామున లేదా సాయంత్రం వేళల్లోనే పశువులను మేతకు తీసుకెళ్లండి."
            ],
            "hi": [
                "सूखे के कारण हरे चारे की कमी से पहले ही सूखे चारे (भूसा, पुआल, साइलेज) का पर्याप्त भंडारण कर लें।",
                "पशु बाड़ों में छायादार छप्पर, गीली बोरियां या फव्वारे लगाकर पशुओं को अत्यधिक गर्मी से बचाएं।",
                "पशुओं के लिए 24 घंटे स्वच्छ पेयजल उपलब्ध रखें; पानी में खनिज मिश्रण व इलेक्ट्रोलाइट्स मिलाएं।",
                "मौसम बदलने से पहले खुरपका-मुंहपका (FMD) और गलाघोंटू जैसी बीमारियों के टीके समय पर लगवाएं।",
                "पशुओं को चराने केवल सुबह जल्दी या शाम के ठंडे समय में ही ले जाएं।"
            ]
        }
    },
    {
        "id": "community",
        "icon": "🏛️",
        "color": "#d97706",
        "title": {
            "en": "Community, RWA & Civic Water Governance",
            "te": "సామాజిక, అపార్ట్‌మెంట్ & గ్రామీణ నీటి నిర్వహణ",
            "hi": "सामुदायिक, RWA एवं शहरी जल प्रबंधन"
        },
        "precautions": {
            "en": [
                "Resident Welfare Associations (RWAs) and Gram Panchayats should enforce equitable water ration schedules and ban hose pipe car washing.",
                "Register early with verified municipal water tanker suppliers (HMWSSB / Urban Local Bodies) to avert predatory private tanker cartels.",
                "Conduct community audits of residential overhead tanks, sumps, and distribution valves to arrest distribution losses.",
                "Establish neighborhood check-ins to verify that vulnerable elderly and lower-income households have potable water access.",
                "Promptly report broken civic water pipelines and illegal groundwater extraction to local municipal helpline numbers."
            ],
            "te": [
                "అపార్ట్‌మెంట్లు, కాలనీ సంక్షేమ సంఘాలు (RWAs), గ్రామ పంచాయతీలు సమాన నీటి పంపిణీ నియమాలను అమలు చేయాలి; పైపులతో వాహనాలు కడగడం నిషేధించాలి.",
                "ప్రైవేట్ ట్యాంకర్ల అధిక ధరల దోపిడీ నుంచి తప్పించుకోవడానికి అధికారిక మున్సిపల్ ట్యాంకర్ల వద్ద ముందే రిజిస్టర్ చేసుకోండి.",
                "కాలనీ సంపులు, ఓవర్‌హెడ్ ట్యాంకులు, గేట్ వాల్వ్‌లను తనిఖీ చేసి నీరు వృథా కాకుండా చూడండి.",
                "ఒంటరి వృద్ధులు, బలహీన వర్గాల కుటుంబాలకు తాగునీరు అందుతోందో లేదో స్థానికంగా గమనించి సహాయం అందించండి.",
                "రోడ్లపై పైపులైన్ లీకేజీలు లేదా అక్రమ బోర్ల తవ్వకాలు ఉంటే వెంటనే మున్సిపల్ టోల్ ఫ్రీ నంబర్లకు తెలియజేయండి."
            ],
            "hi": [
                "रेजिडेंट वेलफेयर एसोसिएशन (RWA) और ग्राम पंचायतें समान जल वितरण समय सारणी बनाएं और होज पाइप से धुलाई बंद करें।",
                "निजी टैंकर माफिया की लूट से बचने के लिए सरकारी/नगरपालिका टैंकर सेवा में पहले से पंजीकरण कराएं।",
                "सोसायटी के ओवरहेड टैंकों और भूमिगत सम्प की लीकेज जांच कर पानी की बर्बादी रोकें।",
                "बुजुर्गों और कमजोर परिवारों के लिए पीने के पानी की उपलब्धता सुनिश्चित करने के लिए पड़ोस में सहयोग करें।",
                "सड़क पर पाइपलाइन लीकेज और अवैध जल दोहन की सूचना तत्काल नगर निगम हेल्पलाइन पर दर्ज कराएं।"
            ]
        }
    }
]


def get_el_nino_precautions(lang: str = "en") -> List[Dict]:
    """Retrieve categorized El Niño precautions in the requested language."""
    target_lang = lang if lang in ("en", "te", "hi") else "en"
    result = []
    for cat in EL_NINO_PRECAUTIONS:
        result.append({
            "id": cat["id"],
            "icon": cat["icon"],
            "color": cat["color"],
            "title": cat["title"].get(target_lang, cat["title"]["en"]),
            "precautions": cat["precautions"].get(target_lang, cat["precautions"]["en"])
        })
    return result

