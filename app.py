import time
import random
import requests
import streamlit as st 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_driver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--window-size=1366,699") 

service = Service(executable_path=chrome_driver_path)

st.title('Ubuy Speed Check')

# Button selection for country
#location = st.radio("Select a location:", ('NZ', 'KW', 'UAE'))

selected_location = None

# Check if a location has been selected
if selected_location:
    st.write(f"Calculating at: {selected_location}")
else:
    st.write("Please select a domain.")

# Display buttons for location selection
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('QA'):
        selected_location = 'QA'

with col2:
    if st.button('KW'):
        selected_location = 'KW'

with col3:
    if st.button('UAE'):
        selected_location = 'UAE'



keywords = [
    "fashion accessory item", "fun group activity", "exciting outdoor trip", "home kitchen tool", "creative wall decor",
"newborn care gear", "school travel bag", "carry-on travel gear", "bakeware and utensils", "financial savings tool",
"two-wheel road transport", "mountain ride gear", "storage organization box", "soft bed cover", "cozy bed throw",
"hydration travel container", "personal care brush", "digital photo device", "outdoor shelter gear", "aromatic wax light",
"phone safety case", "ergonomic sitting chair", "portable power supply", "household sanitation product", "casual fashion wear",
"everyday wear clothing", "hot beverage maker", "video gaming device", "food preparation gear", "DIY craft supplies",
"handmade art projects", "cutting eating tools", "home interior accents", "table meal setup", "ceramic plate set",
"kitchen hole cutter", "flavored cold beverages", "aerial filming robot", "small stereo earbuds", "home tech devices",
"home workout routine", "air cooling fans", "relatives bonding time", "holiday event celebration", "water sport hobby",
"personal health training", "daily meal food", "photo display frame", "oil-free cook machine", "indoor seating unit",
"fun leisure activity", "outdoor green area", "multiplayer online platform", "travel hiking supplies", "gift wrapping supplies",
"holiday surprise gift", "sunlight vision wear", "warm handwear accessory", "charcoal barbecue grill", "personal safety tool",
"creative pastimes activity", "seasonal festive gift", "body health supplies", "home heating device", "nature trail gear",
"indoor living space", "winter clothing gear", "cooking preparation space", "educational build kits", "portable computer device",
"ambient string lights", "room lamp fixture", "protective face mask", "cooked food portion", "computer display screen",
"handheld control device", "hot drink container", "school writing pad", "balanced food intake", "corporate workspace furniture",
"camping outdoor gear", "art painting tools", "event party decor", "ballpoint ink pens", "domestic animal care",
"bedtime neck support", "green home decoration", "consumer retail goods", "internet modem router", "protective home equipment",
"cooking condiment bottles", "body weight checker", "education learning tools", "changing seasonal theme", "bedding sleep linen",
"cozy sleep blankets", "footwear fashion shoes", "facial care products", "mobile cell device", "digital fitness watch",
"athletic sports sneakers", "tasty food snacks", "comfortable foot socks", "portable sound speaker", "kitchen flavor spices",
"team physical games", "closet storage drawers", "art supply materials", "UV blocking shades", "diet health pills",
"media play tablet", "personal wash items", "hand repair tools", "kids play objects", "activity fitness tracker",
"airline weekend travel", "graphic print tshirt", "entertainment smart TV", "eating steel utensils", "floor cleaning vacuum",
"wrist timepiece watch", "clean bottled water", "mental health wellness", "knitting fiber yarn", "indoor yoga mat",
    
  "wireless audio headphones", "gaming high-performance laptop", "outdoor foldable chair", 
    "indoor exercise bike", "advanced fitness tracker", "phone protection case", "4K smart TV", 
    "kitchen chef knife", "comfortable sleep mask", "travel luggage set", "HD computer monitor", 
    "voice activated speaker", "coffee brewing maker", "compact air fryer", "robot vacuum cleaner", 
    "nonstick baking sheet", "portable bento box", "gardening hand tools", "insulated travel mug", 
    "reusable water bottle", "wireless charging pad", "cordless power drill", "modern gaming console", 
    "premium printer paper", "crafting hobby supplies", "outdoor garden furniture", "adjustable laptop stand", 
    "soft yoga mat", "durable dog leash", "travel pet carrier", "ergonomic office chair", "desk storage organizer", 
    "memory foam pillow", "adjustable weight set", "athletic workout clothes", "luxury skincare kit", 
    "professional hair dryer", "makeup cosmetic organizer", "high-speed juicer", "automatic bread maker", 
    "airtight food storage", "essential camping gear", "portable outdoor grill", "wicker picnic basket", 
    "insulated cooler bag", "protective gardening gloves", "sewing machine kit", "beginner knitting kit", 
    "essential art supplies", "wooden artist easel", "challenging jigsaw puzzle", "family board games", 
    "toy car replica", "action figure set", "plush stuffed animal", "mini dollhouse set", "toy play kitchen", 
    "educational building blocks", "science experiment kit", "robot building kit", "remote control car", 
    "musical instrument kit", "kids play tent", "outdoor trampoline fun", "adult skateboard deck", 
    "safety bicycle helmet", "folding scooter ride", "hockey practice stick", "inflatable soccer ball", 
    "regulation basketball hoop", "official football gear", "golf club set", "professional tennis racket", 
    "balance yoga blocks", "inflatable exercise ball", "adjustable dumbbell weights", "jump rope workout", 
    "fitness DVD collection", "lightweight fishing rod", "durable hiking boots", "waterproof water shoes", 
    "comfortable swimming gear", "high-performance ski equipment", "climbing rock gear", "surfboard riding board", 
    "paddleboard accessory kit", "compact camping tent", "warm sleeping bag", "LED outdoor lantern", 
    "handheld flashlight tool", "portable fire pit", "grilling barbecue tools", "camping cooler bag", 
    "foldable camping chair", "professional fishing tackle", "first aid kit", "emergency thermal blanket", 
    "travel adventure guide", "folding road map", "vehicle USB charger", "portable battery pack", "GPS navigation device", 
    "car dash cam", "vehicle emergency kit", "roof rack carrier", "bike lock security", "basic car maintenance tools", 
    "oil change filter", "emergency tire inflator", "compact jump starter", "car detailing supplies", "professional detailing kit", 
    "vehicle interior cleaner", "headlight restoration kit", "floor mat protector", "comfortable seat covers", 
    "car window sunshade", "trunk storage organizer", "secure cargo net", "dog pet barrier", "pet grooming tools", 
    "nutritious dog food", "odorless cat litter", "aquarium fish tank", "automatic bird feeder", "small animal habitat", 
    "interactive pet toys", "aquarium cleaning supplies", "pet health products", "basic pet training", "health supplements", 
    "muscle vitamins pack", "protein powder supplement", "meal replacement shake", "energy protein bars", "weight loss plan", 
    "immune system support", "digestive health probiotics", "joint health supplements", "organic herbal tea", 
    "aromatherapy essential oils", "relaxing diffuser kit", "luxury skin care", "hydrating moisturizer", 
    "protective sunblock lotion", "anti-aging cream", "natural hair care", "shampoo conditioner set", 
    "restorative hair treatment", "nail care kit", "manicure pedicure set", "foot care tools", "gentle body scrub", 
    "luxury bath bombs", "relaxing makeup remover",
    "makeup", "foundation", "lipstick", "eye shadow", "blush",
    "eyeliner", "mascara", "makeup brushes", "hair styling tools", "hair accessories",
    "beauty tools", "facial masks", "peel pads", "self-tanner", "waxing kit",
    "tanning lotion", "toiletries", "shaving kit", "razors", "deodorant",
    "body wash", "hand soap", "toilet paper", "paper towels", "laundry detergent",
    "dish soap", "cleaning supplies", "broom", "mop", "bucket",
    "vacuum bags", "air fresheners", "scented oils", "incense",
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


selected_keywords = random.sample(keywords, 12)

list_page_times = []
detail_page_times = []
not_found = 0
is_out_of_stock = 0

def run_tests_nz(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(QA)"

    for product in selected_keywords:
        try:
            driver.get("https://www.ubuy.qa/en/")
            driver.set_window_size(1366, 699)
            search_box = driver.find_element(By.CSS_SELECTOR, ".ds-input")
            search_box.clear()  
            search_box.send_keys(product)
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)


            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1) .product-title"))
            )
            #WebDriverWait(driver, 10).until(
             #   EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-lg-3:nth-child(3) .img-detail img"))
            #).click()

            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)

            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            
            driver.find_element(By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1)").click()


            try:
                WebDriverWait(driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                
                end_time = time.time()
                response_time_detail = (end_time - start_time - response_time_list)
                detail_page_times.append(response_time_detail)
                

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1500:.2f} ms")
            except:
                st.write(f"Keyword: {product} - timeout.")
        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")
        finally:
           driver.get("https://www.ubuy.qa/en/")
           driver.set_window_size(1366, 699) 
def run_tests_kw(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(KW)"
    for product in selected_keywords:
        try:
            driver.get("https://www.a.ubuy.com.kw/en/")
            driver.set_window_size(1366, 699)

            search_box = driver.find_element(By.CSS_SELECTOR, ".ds-input")
            search_box.clear()  
            search_box.send_keys(product)
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)


            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1) .product-title"))
            )
            #WebDriverWait(driver, 10).until(
             #   EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-lg-3:nth-child(3) .img-detail img"))
            #).click()

            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)

            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            
            driver.find_element(By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1)").click()

    #Main (detail)
            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                
                end_time = time.time()
                response_time_detail = (end_time - start_time - response_time_list)
                detail_page_times.append(response_time_detail)
                

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1500:.2f} ms")

            except:
                st.write(f"Keyword: {product} - timeout.")


        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")

        finally:
            driver.get("https://www.a.ubuy.com.kw/en/")
            driver.set_window_size(1366, 699)


def run_tests_uae(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(UAE)"

    for product in selected_keywords:
        try:
            driver.get("https://www.ubuy.ae/en/")
            driver.set_window_size(1366, 699)

            search_box = driver.find_element(By.CSS_SELECTOR, ".ds-input")
            search_box.clear()  
            search_box.send_keys(product)
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)


            WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1) .product-title"))
            )
            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)

            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            
            driver.find_element(By.CSS_SELECTOR, "div.product-inner-list:nth-of-type(1)").click()

    #Main (detail)
            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                
                end_time = time.time()
                response_time_detail = (end_time - start_time - response_time_list)
                detail_page_times.append(response_time_detail)
                

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")

            except:
                st.write(f"Keyword: {product} - timeout.")


        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")

        finally:
            driver.get("https://www.ubuy.ae/en/")
            driver.set_window_size(1366, 699)


# Main logic to run tests
def main():
    driver = webdriver.Chrome(service=service, options=chrome_options)

    if selected_location == 'QA':
        run_tests_nz(driver, selected_keywords)
    elif selected_location == 'KW':
        run_tests_kw(driver, selected_keywords)
    elif selected_location == 'UAE':
        run_tests_uae(driver, selected_keywords)

    driver.quit()

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
                f"the detail page is taking time around {detail_min:.2f} to {detail_max:.2f} sec to load.({selected_location})\n")
        
        st.write(summary)
        st.write(f"Not founds: {not_found}\n" f"Out of stocks: {is_out_of_stock}")

if __name__ == "__main__":
    main()