import streamlit as st
import urllib.request
import json
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

isco08_dict = {'Armed forces occupations': 0, 'Commissioned armed forces officers': 110, 'Non-commissioned armed forces officers': 210, 'Armed forces occupations, other ranks': 310, 'Managers': 1000, 'Chief executives, senior officials and legislators': 1100, 'Legislators and senior officials': 1110, 'Legislators': 1111, 'Senior government officials': 1112, 'Traditional chiefs and heads of village': 1113, 'Senior officials of special-interest organizations': 1114, 'Managing directors and chief executives': 1120, 'Administrative and commercial managers': 1200, 'Business services and administration managers': 1210, 'Finance managers': 1211, 'Human resource managers': 1212, 'Policy and planning managers': 1213, 'Business services and administration managers not elsewhere classified': 1219, 'Sales, marketing and development managers': 1220, 'Sales and marketing managers': 1221, 'Advertising and public relations managers': 1222, 'Research and development managers': 1223, 'Production and specialised services managers': 1300, 'Production managers in agriculture, forestry and fisheries': 1310, 'Agricultural and forestry production managers': 1311, 'Aquaculture and fisheries production managers': 1312, 'Manufacturing, mining, construction, and distribution managers': 1320, 'Manufacturing managers': 1321, 'Mining managers': 1322, 'Construction managers': 1323, 'Supply, distribution and related managers': 1324, 'Information and communications technology service managers': 1330, 'Professional services managers': 1340, 'Child care services managers': 1341, 'Health services managers': 1342, 'Aged care services managers': 1343, 'Social welfare managers': 1344, 'Education managers': 1345, 'Financial and insurance services branch managers': 1346, 'Professional services managers not elsewhere classified': 1349, 'Hospitality, retail and other services managers': 1400, 'Hotel and restaurant managers': 1410, 'Hotel managers': 1411, 'Restaurant managers': 1412, 'Retail and wholesale trade managers': 1420, 'Other services managers': 1430, 'Sports, recreation and cultural centre managers': 1431, 'Services managers not elsewhere classified': 1439, 'Professionals': 2000, 'Science and engineering professionals': 2100, 'Physical and earth science professionals': 2110, 'Physicists and astronomers': 2111, 'Meteorologists': 2112, 'Chemists': 2113, 'Geologists and geophysicists': 2114, 'Mathematicians, actuaries and statisticians': 2120, 'Life science professionals': 2130, 'Biologists, botanists, zoologists and related professionals': 2131, 'Farming, forestry and fisheries advisers': 2132, 'Environmental protection professionals': 2133, 'Engineering professionals (excluding electrotechnology)': 2140, 'Industrial and production engineers': 2141, 'Civil engineers': 2142, 'Environmental engineers': 2143, 'Mechanical engineers': 2144, 'Chemical engineers': 2145, 'Mining engineers, metallurgists and related professionals': 2146, 'Engineering professionals not elsewhere classified': 2149, 'Electrotechnology engineers': 2150, 'Electrical engineers': 2151, 'Electronics engineers': 2152, 'Telecommunications engineers': 2153, 'Architects, planners, surveyors and designers': 2160, 'Building architects': 2161, 'Landscape architects': 2162, 'Product and garment designers': 2163, 'Town and traffic planners': 2164, 'Cartographers and surveyors': 2165, 'Graphic and multimedia designers': 2166, 'Health professionals': 2200, 'Medical doctors': 2210, 'Generalist medical practitioners': 2211, 'Specialist medical practitioners': 2212, 'Nursing and midwifery professionals': 2220, 'Nursing professionals': 2221, 'Midwifery professionals': 2222, 'Traditional and complementary medicine professionals': 2230, 'Paramedical practitioners': 2240, 'Veterinarians': 2250, 'Other health professionals': 2260, 'Dentists': 2261, 'Pharmacists': 2262, 'Environmental and occupational health and hygiene professionals': 2263, 'Physiotherapists': 2264, 'Dieticians and nutritionists': 2265, 'Audiologists and speech therapists': 2266, 'Optometrists and ophthalmic opticians': 2267, 'Health professionals not elsewhere classified': 2269, 'Teaching professionals': 2300, 'University and higher education teachers': 2310, 'Vocational education teachers': 2320, 'Secondary education teachers': 2330, 'Primary school and early childhood teachers': 2340, 'Primary school teachers': 2341, 'Early childhood educators': 2342, 'Other teaching professionals': 2350, 'Education methods specialists': 2351, 'Special needs teachers': 2352, 'Other language teachers': 2353, 'Other music teachers': 2354, 'Other arts teachers': 2355, 'Information technology trainers': 2356, 'Teaching professionals not elsewhere classified': 2359, 'Business and administration professionals': 2400, 'Finance professionals': 2410, 'Accountants': 2411, 'Financial and investment advisers': 2412, 'Financial analysts': 2413, 'Administration professionals': 2420, 'Management and organization analysts': 2421, 'Policy administration professionals': 2422, 'Personnel and careers professionals': 2423, 'Training and staff development professionals': 2424, 'Sales, marketing and public relations professionals': 2430, 'Advertising and marketing professionals': 2431, 'Public relations professionals': 2432, 'Technical and medical sales professionals (excluding ICT)': 2433, 'Information and communications technology sales professionals': 2434, 'Information and communications technology professionals': 2500, 'Software and applications developers and analysts': 2510, 'Systems analysts': 2511, 'Software developers': 2512, 'Web and multimedia developers': 2513, 'Applications programmers': 2514, 'Software and applications developers and analysts not elsewhere classified': 2519, 'Database and network professionals': 2520, 'Database designers and administrators': 2521, 'Systems administrators': 2522, 'Computer network professionals': 2523, 'Database and network professionals not elsewhere classified': 2529, 'Legal, social and cultural professionals': 2600, 'Legal professionals': 2610, 'Lawyers': 2611, 'Judges': 2612, 'Legal professionals not elsewhere classified': 2619, 'Librarians, archivists and curators': 2620, 'Archivists and curators': 2621, 'Librarians and related information professionals': 2622, 'Social and religious professionals': 2630, 'Economists': 2631, 'Sociologists, anthropologists and related professionals': 2632, 'Philosophers, historians and political scientists': 2633, 'Psychologists': 2634, 'Social work and counselling professionals': 2635, 'Religious professionals': 2636, 'Authors, journalists and linguists': 2640, 'Authors and related writers': 2641, 'Journalists': 2642, 'Translators, interpreters and other linguists': 2643, 'Creative and performing artists': 2650, 'Visual artists': 2651, 'Musicians, singers and composers': 2652, 'Dancers and choreographers': 2653, 'Film, stage and related directors and producers': 2654, 'Actors': 2655, 'Announcers on radio, television and other media': 2656, 'Creative and performing artists not elsewhere classified': 2659, 'Technicians and associate professionals': 3000, 'Science and engineering associate professionals': 3100, 'Physical and engineering science technicians': 3110, 'Chemical and physical science technicians': 3111, 'Civil engineering technicians': 3112, 'Electrical engineering technicians': 3113, 'Electronics engineering technicians': 3114, 'Mechanical engineering technicians': 3115, 'Chemical engineering technicians': 3116, 'Mining and metallurgical technicians': 3117, 'Draughtspersons': 3118, 'Physical and engineering science technicians not elsewhere classified': 3119, 'Mining, manufacturing and construction supervisors': 3120, 'Mining supervisors': 3121, 'Manufacturing supervisors': 3122, 'Construction supervisors': 3123, 'Process control technicians': 3130, 'Power production plant operators': 3131, 'Incinerator and water treatment plant operators': 3132, 'Chemical processing plant controllers': 3133, 'Petroleum and natural gas refining plant operators': 3134, 'Metal production process controllers': 3135, 'Process control technicians not elsewhere classified': 3139, 'Life science technicians and related associate professionals': 3140, 'Life science technicians (excluding medical)': 3141, 'Agricultural technicians': 3142, 'Forestry technicians': 3143, 'Ship and aircraft controllers and technicians': 3150, "Ships' engineers": 3151, "Ships' deck officers and pilots": 3152, 'Aircraft pilots and related associate professionals': 3153, 'Air traffic controllers': 3154, 'Air traffic safety electronics technicians': 3155, 'Health associate professionals': 3200, 'Medical and pharmaceutical technicians': 3210, 'Medical imaging and therapeutic equipment technicians': 3211, 'Medical and pathology laboratory technicians': 3212, 'Pharmaceutical technicians and assistants': 3213, 'Medical and dental prosthetic technicians': 3214, 'Nursing and midwifery associate professionals': 3220, 'Nursing associate professionals': 3221, 'Midwifery associate professionals': 3222, 'Traditional and complementary medicine associate professionals': 3230, 'Veterinary technicians and assistants': 3240, 'Other health associate professionals': 3250, 'Dental assistants and therapists': 3251, 'Medical records and health information technicians': 3252, 'Community health workers': 3253, 'Dispensing opticians': 3254, 'Physiotherapy technicians and assistants': 3255, 'Medical assistants': 3256, 'Environmental and occupational health inspectors and associates': 3257, 'Ambulance workers': 3258, 'Health associate professionals not elsewhere classified': 3259, 'Business and administration associate professionals': 3300, 'Financial and mathematical associate professionals': 3310, 'Securities and finance dealers and brokers': 3311, 'Credit and loans officers': 3312, 'Accounting associate professionals': 3313, 'Statistical, mathematical and related associate professionals': 3314, 'Valuers and loss assessors': 3315, 'Sales and purchasing agents and brokers': 3320, 'Insurance representatives': 3321, 'Commercial sales representatives': 3322, 'Buyers': 3323, 'Trade brokers': 3324, 'Business services agents': 3330, 'Clearing and forwarding agents': 3331, 'Conference and event planners': 3332, 'Employment agents and contractors': 3333, 'Real estate agents and property managers': 3334, 'Business services agents not elsewhere classified': 3339, 'Administrative and specialised secretaries': 3340, 'Office supervisors': 3341, 'Legal secretaries': 3342, 'Administrative and executive secretaries': 3343, 'Medical secretaries': 3344, 'Regulatory government associate professionals': 3350, 'Customs and border inspectors': 3351, 'Government tax and excise officials': 3352, 'Government social benefits officials': 3353, 'Government licensing officials': 3354, 'Police inspectors and detectives': 3411, 'Regulatory government associate professionals not elsewhere classified': 3359, 'Legal, social, cultural and related associate professionals': 3400, 'Legal, social and religious associate professionals': 3410, 'Social work associate professionals': 3412, 'Religious associate professionals': 3413, 'Sports and fitness workers': 3420, 'Athletes and sports players': 3421, 'Sports coaches, instructors and officials': 3422, 'Fitness and recreation instructors and program leaders': 3423, 'Artistic, cultural and culinary associate professionals': 3430, 'Photographers': 3431, 'Interior designers and decorators': 3432, 'Gallery, museum and library technicians': 3433, 'Chefs': 3434, 'Other artistic and cultural associate professionals': 3435, 'Information and communications technicians': 3500, 'Information and communications technology operations and user support technicians': 3510, 'Information and communications technology operations technicians': 3511, 'Information and communications technology user support technicians': 3512, 'Computer network and systems technicians': 3513, 'Web technicians': 3514, 'Telecommunications and broadcasting technicians': 3520, 'Broadcasting and audio-visual technicians': 3521, 'Telecommunications engineering technicians': 3522, 'Clerical support workers': 4000, 'General and keyboard clerks': 4100, 'General office clerks': 4110, 'Secretaries (general)': 4120, 'Keyboard operators': 4130, 'Typists and word processing operators': 4131, 'Data entry clerks': 4132, 'Customer services clerks': 4200, 'Tellers, money collectors and related clerks': 4210, 'Bank tellers and related clerks': 4211, 'Bookmakers, croupiers and related gaming workers': 4212, 'Pawnbrokers and money-lenders': 4213, 'Debt-collectors and related workers': 4214, 'Client information workers': 4220, 'Travel consultants and clerks': 4221, 'Contact centre information clerks': 4222, 'Telephone switchboard operators': 4223, 'Hotel receptionists': 4224, 'Enquiry clerks': 4225, 'Receptionists (general)': 4226, 'Survey and market research interviewers': 4227, 'Client information workers not elsewhere classified': 4229, 'Numerical and material recording clerks': 4300, 'Numerical clerks': 4310, 'Accounting and bookkeeping clerks': 4311, 'Statistical, finance and insurance clerks': 4312, 'Payroll clerks': 4313, 'Material-recording and transport clerks': 4320, 'Stock clerks': 4321, 'Production clerks': 4322, 'Transport clerks': 4323, 'Other clerical support workers': 4410, 'Library clerks': 4411, 'Mail carriers and sorting clerks': 4412, 'Coding, proof-reading and related clerks': 4413, 'Scribes and related workers': 4414, 'Filing and copying clerks': 4415, 'Personnel clerks': 4416, 'Clerical support workers not elsewhere classified': 4419, 'Service and sales workers': 5000, 'Personal service workers': 5100, 'Travel attendants, conductors and guides': 5110, 'Travel attendants and travel stewards': 5111, 'Transport conductors': 5112, 'Travel guides': 5113, 'Cooks': 5120, 'Waiters and bartenders': 5130, 'Waiters': 5131, 'Bartenders': 5132, 'Hairdressers, beauticians and related workers': 5140, 'Hairdressers': 5141, 'Beauticians and related workers': 5142, 'Building and housekeeping supervisors': 5150, 'Cleaning and housekeeping supervisors in offices, hotels and other establishments': 5151, 'Domestic housekeepers': 5152, 'Building caretakers': 5153, 'Other personal services workers': 5160, 'Astrologers, fortune-tellers and related workers': 5161, 'Companions and valets': 5162, 'Undertakers and embalmers': 5163, 'Pet groomers and animal care workers': 5164, 'Driving instructors': 5165, 'Personal services workers not elsewhere classified': 5169, 'Sales workers': 5200, 'Street and market salespersons': 5210, 'Stall and market salespersons': 5211, 'Street food salespersons': 5212, 'Shop salespersons': 5220, 'Shop keepers': 5221, 'Shop supervisors': 5222, 'Shop sales assistants': 5223, 'Cashiers and ticket clerks': 5230, 'Other sales workers': 5240, 'Fashion and other models': 5241, 'Sales demonstrators': 5242, 'Door to door salespersons': 5243, 'Contact centre salespersons': 5244, 'Service station attendants': 5245, 'Food service counter attendants': 5246, 'Sales workers not elsewhere classified': 5249, 'Personal care workers': 5300, "Child care workers and teachers' aides": 5310, 'Child care workers': 5311, "Teachers' aides": 5312, 'Personal care workers in health services': 5320, 'Health care assistants': 5321, 'Home-based personal care workers': 5322, 'Personal care workers in health services not elsewhere classified': 5329, 'Protective services workers': 5410, 'Fire-fighters': 5411, 'Police officers': 5412, 'Prison guards': 5413, 'Security guards': 5414, 'Protective services workers not elsewhere classified': 5419, 'Skilled agricultural, forestry and fishery workers': 6000, 'Market-oriented skilled agricultural workers': 6100, 'Market gardeners and crop growers': 6110, 'Field crop and vegetable growers': 6111, 'Tree and shrub crop growers': 6112, 'Gardeners, horticultural and nursery growers': 6113, 'Mixed crop growers': 6114, 'Animal producers': 6120, 'Livestock and dairy producers': 6121, 'Poultry producers': 6122, 'Apiarists and sericulturists': 6123, 'Animal producers not elsewhere classified': 6129, 'Mixed crop and animal producers': 6130, 'Market-oriented skilled forestry, fishery and hunting workers': 6200, 'Forestry and related workers': 6210, 'Fishery workers, hunters and trappers': 6220, 'Aquaculture workers': 6221, 'Inland and coastal waters fishery workers': 6222, 'Deep-sea fishery workers': 6223, 'Hunters and trappers': 6224, 'Subsistence farmers, fishers, hunters and gatherers': 6300, 'Subsistence crop farmers': 6310, 'Subsistence livestock farmers': 6320, 'Subsistence mixed crop and livestock farmers': 6330, 'Subsistence fishers, hunters, trappers and gatherers': 6340, 'Craft and related trades workers': 7000, 'Building and related trades workers, excluding electricians': 7100, 'Building frame and related trades workers': 7110, 'House builders': 7111, 'Bricklayers and related workers': 7112, 'Stonemasons, stone cutters, splitters and carvers': 7113, 'Concrete placers, concrete finishers and related workers': 7114, 'Carpenters and joiners': 7115, 'Building frame and related trades workers not elsewhere classified': 7119, 'Building finishers and related trades workers': 7120, 'Roofers': 7121, 'Floor layers and tile setters': 7122, 'Plasterers': 7123, 'Insulation workers': 7124, 'Glaziers': 7125, 'Plumbers and pipe fitters': 7126, 'Air conditioning and refrigeration mechanics': 7127, 'Painters, building structure cleaners and related trades workers': 7130, 'Painters and related workers': 7131, 'Spray painters and varnishers': 7132, 'Building structure cleaners': 7133, 'Metal, machinery and related trades workers': 7200, 'Sheet and structural metal workers, moulders and welders, and related workers': 7210, 'Metal moulders and coremakers': 7211, 'Welders and flamecutters': 7212, 'Sheet-metal workers': 7213, 'Structural-metal preparers and erectors': 7214, 'Riggers and cable splicers': 7215, 'Blacksmiths, toolmakers and related trades workers': 7220, 'Blacksmiths, hammersmiths and forging press workers': 7221, 'Toolmakers and related workers': 7222, 'Metal working machine tool setters and operators': 7223, 'Metal polishers, wheel grinders and tool sharpeners': 7224, 'Machinery mechanics and repairers': 7230, 'Motor vehicle mechanics and repairers': 7231, 'Aircraft engine mechanics and repairers': 7232, 'Agricultural and industrial machinery mechanics and repairers': 7233, 'Bicycle and related repairers': 7234, 'Handicraft and printing workers': 7300, 'Handicraft workers': 7310, 'Precision-instrument makers and repairers': 7311, 'Musical instrument makers and tuners': 7312, 'Jewellery and precious-metal workers': 7313, 'Potters and related workers': 7314, 'Glass makers, cutters, grinders and finishers': 7315, 'Sign writers, decorative painters, engravers and etchers': 7316, 'Handicraft workers in wood, basketry and related materials': 7317, 'Handicraft workers in textile, leather and related materials': 7318, 'Handicraft workers not elsewhere classified': 7319, 'Printing trades workers': 7320, 'Pre-press technicians': 7321, 'Printers': 7322, 'Print finishing and binding workers': 7323, 'Electrical and electronic trades workers': 7400, 'Electrical equipment installers and repairers': 7410, 'Building and related electricians': 7411, 'Electrical mechanics and fitters': 7412, 'Electrical line installers and repairers': 7413, 'Electronics and telecommunications installers and repairers': 7420, 'Electronics mechanics and servicers': 7421, 'Information and communications technology installers and servicers': 7422, 'Food processing, wood working, garment and other craft and related trades workers': 7500, 'Food processing and related trades workers': 7510, 'Butchers, fishmongers and related food preparers': 7511, 'Bakers, pastry-cooks and confectionery makers': 7512, 'Dairy-products makers': 7513, 'Fruit, vegetable and related preservers': 7514, 'Food and beverage tasters and graders': 7515, 'Tobacco preparers and tobacco products makers': 7516, 'Wood treaters, cabinet-makers and related trades workers': 7520, 'Wood treaters': 7521, 'Cabinet-makers and related workers': 7522, 'Woodworking-machine tool setters and operators': 7523, 'Garment and related trades workers': 7530, 'Tailors, dressmakers, furriers and hatters': 7531, 'Garment and related pattern-makers and cutters': 7532, 'Sewing, embroidery and related workers': 7533, 'Upholsterers and related workers': 7534, 'Pelt dressers, tanners and fellmongers': 7535, 'Shoemakers and related workers': 7536, 'Other craft and related workers': 7540, 'Underwater divers': 7541, 'Shotfirers and blasters': 7542, 'Product graders and testers (excluding foods and beverages)': 7543, 'Fumigators and other pest and weed controllers': 7544, 'Craft and related workers not elsewhere classified': 7549, 'Plant and machine operators, and assemblers': 8000, 'Stationary plant and machine operators': 8100, 'Mining and mineral processing plant operators': 8110, 'Miners and quarriers': 8111, 'Mineral and stone processing plant operators': 8112, 'Well drillers and borers and related workers': 8113, 'Cement, stone and other mineral products machine operators': 8114, 'Metal processing and finishing plant operators': 8120, 'Metal processing plant operators': 8121, 'Metal finishing, plating and coating machine operators': 8122, 'Chemical and photographic products plant and machine operators': 8130, 'Chemical products plant and machine operators': 8131, 'Photographic products machine operators': 8132, 'Rubber, plastic and paper products machine operators': 8140, 'Rubber products machine operators': 8141, 'Plastic products machine operators': 8142, 'Paper products machine operators': 8143, 'Textile, fur and leather products machine operators': 8150, 'Fibre preparing, spinning and winding machine operators': 8151, 'Weaving and knitting machine operators': 8152, 'Sewing machine operators': 8153, 'Bleaching, dyeing and fabric cleaning machine operators': 8154, 'Fur and leather preparing machine operators': 8155, 'Shoemaking and related machine operators': 8156, 'Laundry machine operators': 8157, 'Textile, fur and leather products machine operators not elsewhere classified': 8159, 'Food and related products machine operators': 8160, 'Wood processing and papermaking plant operators': 8170, 'Pulp and papermaking plant operators': 8171, 'Wood processing plant operators': 8172, 'Other stationary plant and machine operators': 8180, 'Glass and ceramics plant operators': 8181, 'Steam engine and boiler operators': 8182, 'Packing, bottling and labelling machine operators': 8183, 'Stationary plant and machine operators not elsewhere classified': 8189, 'Assemblers': 8210, 'Mechanical machinery assemblers': 8211, 'Electrical and electronic equipment assemblers': 8212, 'Assemblers not elsewhere classified': 8219, 'Drivers and mobile plant operators': 8300, 'Locomotive engine drivers and related workers': 8310, 'Locomotive engine drivers': 8311, 'Railway brake, signal and switch operators': 8312, 'Car, van and motorcycle drivers': 8320, 'Motorcycle drivers': 8321, 'Car, taxi and van drivers': 8322, 'Heavy truck and bus drivers': 8330, 'Bus and tram drivers': 8331, 'Heavy truck and lorry drivers': 8332, 'Mobile plant operators': 8340, 'Mobile farm and forestry plant operators': 8341, 'Earthmoving and related plant operators': 8342, 'Crane, hoist and related plant operators': 8343, 'Lifting truck operators': 8344, "Ships' deck crews and related workers": 8350, 'Elementary occupations': 9000, 'Cleaners and helpers': 9100, 'Domestic, hotel and office cleaners and helpers': 9110, 'Domestic cleaners and helpers': 9111, 'Cleaners and helpers in offices, hotels and other establishments': 9112, 'Vehicle, window, laundry and other hand cleaning workers': 9120, 'Hand launderers and pressers': 9121, 'Vehicle cleaners': 9122, 'Window cleaners': 9123, 'Other cleaning workers': 9129, 'Agricultural, forestry and fishery labourers': 9210, 'Crop farm labourers': 9211, 'Livestock farm labourers': 9212, 'Mixed crop and livestock farm labourers': 9213, 'Garden and horticultural labourers': 9214, 'Forestry labourers': 9215, 'Fishery and aquaculture labourers': 9216, 'Labourers in mining, construction, manufacturing and transport': 9300, 'Mining and construction labourers': 9310, 'Mining and quarrying labourers': 9311, 'Civil engineering labourers': 9312, 'Building construction labourers': 9313, 'Manufacturing labourers': 9320, 'Hand packers': 9321, 'Manufacturing labourers not elsewhere classified': 9329, 'Transport and storage labourers': 9330, 'Hand and pedal vehicle drivers': 9331, 'Drivers of animal-drawn vehicles and machinery': 9332, 'Freight handlers': 9333, 'Shelf fillers': 9334, 'Food preparation assistants': 9410, 'Fast food preparers': 9411, 'Kitchen helpers': 9412, 'Street and related sales and service workers': 9500, 'Street and related service workers': 9510, 'Street vendors (excluding food)': 9520, 'Refuse workers and other elementary workers': 9600, 'Refuse workers': 9610, 'Garbage and recycling collectors': 9611, 'Refuse sorters': 9612, 'Sweepers and related labourers': 9613, 'Other elementary workers': 9620, 'Messengers, package deliverers and luggage porters': 9621, 'Odd job persons': 9622, 'Meter readers and vending-machine collectors': 9623, 'Water and firewood collectors': 9624, 'Elementary workers not elsewhere classified': 9629, 'Refusal': 77777, "Don't know": 88888, 'No answer': 99999, 'Not valid': 00000}
inverted_dict = {v: k for k, v in isco08_dict.items()}


# bypass the server certificate verification on client side
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) 

# Add title, image and header
st.title('ISCO-08 Code Generator')
st.image("assets/ess.png", width=150)
st.header('Enter your job details:')

# Questions for the user
job_title = st.text_input('1. What is the name or title of your main job?')
job_work = st.text_input('2. In your main job, what kind of work do you do most of the time?')
job_qualifications = st.text_input('3. What training or qualifications are needed for the job?')

# Request headers and URL
api_key = os.getenv('api_key')
url = 'https://isco08-testing.westeurope.inference.ml.azure.com/score'
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'isco08-testing-1' }

button_clicked = st.button('Generate ISCO-08 code')

if button_clicked:
    if job_title and job_work and job_qualifications:
        # Request data goes here
        data = {'idno':1000.0, 'language':'unknown', 'job_title': job_title, 'job_kind_of_work': job_work, 
                'job_qualifications': job_qualifications}

        body = str.encode(json.dumps(data))
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            st.write(f"The proposed ISCO-08 code is {result['isco08']} '{inverted_dict[result['isco08']]}'.")
        except urllib.error.HTTPError as error:
            st.write("The request failed with status code: " + str(error.code))
            st.write(error.info())
            st.write(json.loads(error.read()))
    else:
        st.warning("Please answer all the questions to generate the output.")

# Footer with second image
st.markdown('---')
st.markdown(
    """
    This application was developed by Benjamin Beuster for AI testing at Sikt.
    """
)
st.image("assets/sikt.jpg", width=200)