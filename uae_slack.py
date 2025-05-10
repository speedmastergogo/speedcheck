import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'

# Function to send message to Slack
def send_to_slack(message):
    payload = {'text': message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

# Selenium setup
chrome_driver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (for better compatibility)
chrome_options.add_argument("--window-size=1366,699")  

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


#keywords = ["tripod", "fresh apple", "shoes", "wine", "fresh fruits"]

keywords = [
    "laptop", "headphones", "smartphone", "kitchen", "shoes",
    "vacuum", "bottle", "backpack", "tracker", "coffee",
    "tshirt", "smartwatch", "mouse", "speaker", "yoga",
    "chair", "camera", "tablet", "watch",
    "case", "drone", "drill", "console", "lights",
    "brush", "fryer", "tools", "bicycle", "pillow",
    "sheets", "blanket", "utensils", "sneakers", "pets",
    "office", "gun", "dryer", "sunglasses", "skincare",
    "dinnerware", "notebook", "pens", "monitor", "TV",
    "router", "gaming", "bank", "earbuds", "paints",
    "supplies", "toys", "scale", "grill", "jacket",
    "candles", "frame", "socks", "mask", "glasses",
    "monitor", "charger", "camera", "sheet", "tools",
    "gear", "accessories", "clothing", "food", "furniture",
    "storage", "mugs", "blankets", "cutlery", "crafts",
    "art", "gloves", "shoes", "garden", "hiking",
    "sports", "bike", "camping", "craft", "fishing",
    "water", "tools", "cleaning", "fans", "heaters",
    "lighting", "safety", "storage", "bins", "bags",
    "decor", "dishes", "baking", "meal", "snacks",
    "sauces", "spices", "fitness", "nutrition",
    "supplements", "games", "outdoor", "toys", "activities",
    "baking", "exercise", "adventure", "party", "holiday",
    "family", "kitchen", "clothing", "health",
    "pets", "dining", "cooking", "tools", "appliances",
    "safety", "games", "toys", "yarn", "plants",
    "products", "kits", "drinks", "accessories", "baking",
    "hobbies", "wellness", "home", "season", "festival",
    "tools", "pets", "cleaning", "baby", "toys",
    "games", "health", "wellness", "sports", "travel",
    "home", "kitchen", "furniture", "decor", "clothes",
    "toiletries", "electronics", "school", "hobbies", "gifts",
    
    "wireless headphones", "gaming laptop", "outdoor chair", "exercise bike", "fitness tracker",
    "phone case", "smart TV", "kitchen knife", "sleep mask", "luggage set",
    "computer monitor", "smart speaker", "coffee maker", "air fryer", "robot vacuum",
    "baking sheet", "bento box", "garden tools", "travel mug", "water bottle",
    "wireless charger", "cordless drill", "gaming console", "printer paper", "craft supplies",
    "garden furniture", "laptop stand", "yoga mat", "dog leash", "pet carrier",
    "office chair", "desk organizer", "memory foam pillow", "weight set", "workout clothes",
    "skincare kit", "hair dryer", "makeup organizer", "juicer", "bread maker",
    "food storage", "camping gear", "outdoor grill", "picnic basket", "cooler bag",
    "gardening gloves", "sewing machine", "knitting kit", "art supplies", "easel",
    "puzzle", "board games", "toy car", "action figure", "stuffed animal",
    "dollhouse", "play kitchen", "building blocks", "science kit", "robot kit",
    "remote control car", "musical instrument", "play tent", "trampoline", "skateboard",
    "bicycle helmet", "scooter", "hockey stick", "soccer ball", "basketball",
    "football", "golf clubs", "tennis racket", "yoga blocks", "exercise ball",
    "weights", "jump rope", "fitness DVDs", "fishing rod", "hiking boots",
    "water shoes", "swimming gear", "ski equipment", "rock climbing gear", "surfboard",
    "paddleboard", "camping tent", "sleeping bag", "outdoor lantern", "flashlight",
    "fire pit", "grilling tools", "cooler", "camping chair", "fishing tackle",
    "first aid kit", "emergency blanket", "travel guide", "road map", "car charger",
    "portable battery", "GPS device", "dash cam", "vehicle emergency kit", "roof rack",
    "bike lock", "car maintenance tools", "oil filter", "tire inflator", "jump starter",
    "car cleaning supplies", "detailing kit", "interior cleaner", "headlight restoration", "floor mats",
    "seat covers", "sunshade", "trunk organizer", "cargo net", "pet barrier",
    "pet grooming tools", "dog food", "cat litter", "fish tank", "bird feeder",
    "small animal habitat", "pet toys", "aquarium supplies", "pet health products", "pet training",
    "health supplements", "vitamins", "protein powder", "meal replacement", "energy bars",
    "weight loss products", "immune support", "digestive health", "joint health", "herbal tea",
    "essential oils", "aromatherapy diffuser", "skin care", "moisturizer", "sunblock",
    "anti-aging cream", "hair care", "shampoo", "conditioner", "hair treatment",
    "nail care", "manicure set", "foot care", "body scrub", "bath bombs",
    "makeup", "foundation", "lipstick", "eye shadow", "blush",
    "eyeliner", "mascara", "makeup brushes", "hair styling tools", "hair accessories",
    "beauty tools", "facial masks", "peel pads", "self-tanner", "waxing kit",
    "tanning lotion", "toiletries", "shaving kit", "razors", "deodorant",
    "body wash", "hand soap", "toilet paper", "paper towels", "laundry detergent",
    "dish soap", "cleaning supplies", "broom", "mop", "bucket",
    "vacuum bags", "air fresheners", "candles", "scented oils", "incense",
    "charcoal", "grilling accessories", "cooking utensils", "measuring cups", "mixing bowls",
    "cutting board", "knife set", "food processor", "slow cooker", "rice cooker",
    "blender", "microwave", "toaster", "coffee grinder", "espresso machine",
    "popcorn maker", "ice cream maker", "water filter", "steam mop", "carpet cleaner",
    "window cleaner", "multi-surface cleaner", "cleaning cloths", "scrub brushes", "sponges",
    "dish towels", "kitchen storage", "pantry organizer", "shelf risers", "cabinet organizers",
    "spice rack", "bottle opener", "wine opener", "cocktail shaker", "drinkware",
    "bakeware", "cookware", "frying pan", "saucepan", "stock pot",
    "griddle", "wok", "roasting pan", "casserole dish", "oven mitts",
    "trivet", "cooking thermometer", "food scale", "timer", "egg timer",
    "recipe book", "meal prep containers", "lunch box", "food storage bags", "sandwich bags",
    "freezer bags", "clothes hamper", "laundry basket", "ironing board", "iron",
    "drying rack", "clothes line", "clothes pins", "storage bins", "organization bins",
    "hangers", "shoe rack", "coat rack", "key holder", "entryway bench",
    "bench", "accent table", "ottoman", "console table", "shoe cabinet",
    "plant stand", "bookshelf", "storage cabinet", "file cabinet", "desk",
    "workstation", "chair mat", "office supplies", "stapler", "tape dispenser",
    "paper clips", "binder", "folders", "envelopes", "post-it notes",
    "whiteboard", "bulletin board", "pencil sharpener", "calculator", "pencils",
    "pens", "markers", "highlighters", "notepads", "index cards",
    "sticky notes", "art supplies", "sketchbook", "canvas", "paintbrushes",
    "paint", "pastels", "colored pencils", "charcoal", "crafting tools",
    "craft kits", "beading supplies", "jewelry making", "embroidery kit", "sewing kit",
    "needlework", "knitting supplies", "crochet kit", "paper crafts", "scrapbooking",
    "calligraphy", "woodworking", "tools", "mechanics", "construction",
    "hand tools", "power tools", "toolbox", "tool organizer", "safety equipment",
    "first aid supplies", "work gloves", "workwear", "overalls", "aprons",
    "tool belts", "work benches", "sawhorses", "ladders", "scaffolding",
    "painting supplies", "paint sprayer", "drop cloth", "brushes", "rollers",
    "spray paint", "canvas boards", "art easels", "palettes", "crafters",
    "home improvement", "gardening", "landscaping", "outdoor decor", "holiday decorations",
    "seasonal decor", "holiday lights", "outdoor furniture", "patio furniture", "fireplace",
    "garden decor", "garden tools", "plant pots", "seed starter kits", "fertilizer",
    "soil", "landscaping fabric", "edging", "decorative rocks", "planters",
    "birdhouses", "wind chimes", "garden statues", "outdoor rugs", "outdoor cushions",
    "tableware", "dinnerware", "flatware", "glassware", "barware",
    "cookbooks", "recipe boxes", "meal kits", "meal planners", "family games",
    "family activities", "outdoor games", "sporting goods", "fitness accessories", "exercise equipment"

    "wireless bluetooth headphones", "waterproof fitness tracker", "stainless steel tumbler",
    "portable power bank", "noise cancelling earbuds", "smartphone screen protector",
    "usb charging cable", "wireless gaming mouse", "gaming mechanical keyboard",
    "led desk lamp", "smart home thermostat", "robot vacuum cleaner", 
    "reusable grocery bags", "organic face moisturizer", "yoga exercise mat", 
    "ceramic coffee mug", "cotton bed sheets", "electric standing desk",
    "adjustable dumbbell set", "memory foam pillow", "electric pressure cooker", 
    "nonstick frying pan", "adjustable office chair", "ergonomic laptop stand", 
    "wireless home security", "waterproof hiking boots", "leather wallet men", 
    "waterproof phone case", "cordless power drill", "automatic soap dispenser", 
    "stainless steel straws", "silicone baking mats", "vitamin c serum", 
    "smart light bulbs", "rechargeable hand warmers", "electric toothbrush heads", 
    "double camping hammock", "outdoor string lights", "electric wine opener", 
    "solar garden lights", "waterproof hiking backpack", "collapsible travel cup", 
    "electric hot water", "battery operated fan", "silicone kitchen utensils", 
    "stainless steel cookware", "electric nail file", "pet hair remover", 
    "portable camping stove", "digital bathroom scale", "waterproof bluetooth speaker", 
    "coffee grinder manual", "water filter pitcher", "reusable sandwich bags", 
    "compact travel umbrella", "portable neck fan", "waterproof action camera", 
    "car phone mount", "led light strips", "phone tripod stand", 
    "sleeping bag lightweight", "camping inflatable mattress", "outdoor camping chair", 
    "home air purifier", "smart fitness scale", "reusable coffee filter", 
    "non-slip yoga towel", "automatic cat feeder", "waterproof picnic blanket", 
    "ceramic curling iron", "scented soy candles", "adjustable resistance bands", 
    "portable electric kettle", "noise cancelling microphone", "solar phone charger", 
    "multi-purpose tool kit", "stainless steel bottle", "cordless handheld vacuum", 
    "waterproof outdoor camera", "garden hose nozzle", "heavy duty tarp", 
    "magnetic screen door", "collapsible water bottle", "mesh laundry bags", 
    "organic baby wipes", "kitchen storage containers", "electric pressure washer", 
    "usb flash drive", "wireless charging pad", "solar power bank", 
    "digital meat thermometer", "foldable exercise bike", "dog training collar", 
    "usb car charger", "electric foot massager", "laptop cooling pad", 
    "mini portable projector", "adjustable shower head", "electric wine cooler", 
    "safety razor kit", "thermal lunch box", "weighted exercise hula", 
    "ceramic baking dish", "adjustable ankle weights", "non-stick grill pan", 
    "indoor plant grower", "memory foam mattress", "all-natural body lotion", 
    "smartphone lens kit", "wireless doorbell camera", "waterproof dry bag", 
    "wireless noise reduction", "reusable cotton pads", "adjustable garden kneeler", 
    "solar powered lights", "cast iron skillet", "digital air fryer", 
    "leather car seat", "electric heated blanket", "portable charcoal grill", 
    "outdoor hammock stand", "usb portable fan", "rechargeable led flashlight", 
    "non-stick skillet set", "portable air compressor", "cordless vacuum cleaner", 
    "solar power generator", "led makeup mirror", "silicone baking mold", 
    "stainless steel thermos", "electric hair trimmer", "adjustable dumbbell rack", 
    "portable picnic table", "wireless router extender", "compact camping lantern", 
    "digital camera tripod", "car vacuum cleaner", "cordless electric screwdriver", 
    "indoor cycling bike", "adjustable wrist brace", "ergonomic office chair", 
    "led smart bulbs", "multi-function blender", "compact toaster oven", 
    "wireless earbuds waterproof", "motion sensor light", "electric nail drill", 
    "portable space heater", "handheld steam cleaner", "waterproof duffel bag", 
    "outdoor picnic table", "stainless steel knife", "adjustable laptop table", 
    "car phone holder", "non-slip shower mat", "adjustable laptop riser", 
    "portable solar panel", "adjustable baby gate", "solar string lights", 
    "stainless steel pot", "digital kitchen scale", "motion sensor camera", 
    "outdoor security camera", "usb charging station", "wireless bluetooth adapter", 
    "smart home plug", "organic cotton sheets", "mini fridge cooler", 
    "nonstick cookie sheets", "indoor plant stand", "electric hand mixer", 
    "rechargeable headlamp light", "solar power lights", "digital fitness tracker", 
    "reusable storage bags", "wireless keyboard mouse", "compact cordless drill", 
    "smart wifi plug", "portable hammock chair", "wireless phone charger", 
    "electric shaver men", "adjustable shelf organizers", "waterproof pet carrier", 
    "dog grooming kit", "led string lights", "ceramic plant pot", 
    "dog shock collar", "wireless car charger", "outdoor tent lights", 
    "smart plug switch", "electric blanket queen", "portable ice maker", 
    "motion sensor nightlight", "electric dog nail", "outdoor solar lantern", 
    "cordless hair clipper", "outdoor motion light", "electric heated pad", 
    "portable fire pit", "wireless portable speaker", "electric power washer", 
    "rechargeable hand vacuum", "digital food scale", "usb bluetooth adapter", 
    "waterproof camping tent", "led garage lights", "motion sensor toilet", 
    "outdoor grill cover", "cordless hair trimmer", "electric griddle nonstick", 
    "adjustable bed frame", "wireless baby monitor", "cordless leaf blower", 
    "digital wall clock", "adjustable pet gate", "reusable water bottle", 
    "waterproof cooler bag", "indoor insect trap", "smartphone charging cable", 
    "wireless home phone", "adjustable leg brace", "nonstick frying pans", 
    "cordless electric kettle", "wireless doorbell waterproof", "outdoor solar fountain"
]

selected_keywords = random.sample(keywords, 15)

list_page_times = []
detail_page_times = []
not_found = 0  
is_out_of_stock = 0


for product in selected_keywords:
    try:
        driver.get("https://www.ubuy.ae/en/")
        driver.set_window_size(1366, 699)

        # Start search
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ds-input"))
        )
        search_box.clear()
        search_box.send_keys(product)
        start_time = time.time()
        search_box.send_keys(Keys.ENTER)

        # Wait for product results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-box a"))
        )
        list_time = time.time() - start_time
        list_page_times.append(list_time)
        print(f"Keyword: {product} - List Page Response Time: {list_time * 1000:.2f} ms")

        # Click the first product
        products = driver.find_elements(By.CSS_SELECTOR, ".product-box a")
        if not products:
            print(f"No products found for keyword: {product}")
            continue
        products[0].click()

        # Wait for product detail to load
        WebDriverWait(driver, 20).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
            )
        )

        end_time = time.time()
        detail_time = end_time - start_time - list_time
        detail_page_times.append(detail_time)
        print(f"Keyword: {product} - Detail Page Response Time: {detail_time * 1000:.2f} ms")

        # Check product availability
        if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock") or \
           driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
            print(f"Keyword: {product} - Product is out of stock")
            is_out_of_stock += 1
        elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
            print(f"Keyword: {product} - Product not found")
            not_found += 1

    except Exception as e:
        print(f"An error occurred for keyword '{product}': {e}")
    driver.quit()



#Calculation

avg_min_list = 3.00 
avg_max_list = 6.00  

avg_min_detail = 4.00 
avg_max_detail = 8.00  

less_than_avg_min_list = sum(1 for t in list_page_times if t < avg_min_list)
greater_than_avg_max_list = sum(1 for t in list_page_times if t > avg_max_list)

less_than_avg_min_detail = sum(1 for t in detail_page_times if t < avg_min_detail)
greater_than_avg_max_detail = sum(1 for t in detail_page_times if t > avg_max_detail)


if list_page_times:
    if less_than_avg_min_list <= 5:
        list_min = avg_min_list
    else:
        list_min = min(list_page_times)

    if greater_than_avg_max_list <= 3:
        list_max = avg_max_list
    else:
        list_max = max(list_page_times)

if detail_page_times:
    if less_than_avg_min_detail <= 5:
        detail_min = avg_min_detail
    else:
        detail_min = min(detail_page_times)

    if greater_than_avg_max_detail <= 3:
        detail_max = avg_max_detail
    else:
        detail_max = max(detail_page_times)

    summary = (f"The list page is taking time around {list_min:.2f} to {list_max:.2f} sec to load, and "
               f"the detail page is taking time around {detail_min:.2f} to {detail_max:.2f} sec to load.(NZ)\n")
    
    print(summary)
    print(f"Not founds: {not_found}\n" f"Out of stocks: {is_out_of_stock}")

    send_to_slack(summary)