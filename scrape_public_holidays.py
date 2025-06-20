import datetime
import requests
from bs4 import BeautifulSoup
import csv

COUNTRY_SLUGS = {
    "afghanistan": "Afghanistan",
    "albania": "Albania",
    "algeria": "Algeria",
    "andorra": "Andorra",
    "angola": "Angola",
    "anguilla": "Anguilla",
    "antigua-and-barbuda": "Antigua and Barbuda",
    "argentina": "Argentina",
    "armenia": "Armenia",
    "aruba": "Aruba",
    "australia": "Australia",
    "austria": "Austria",
    "azerbaijan": "Azerbaijan",
    "bahamas": "Bahamas",
    "bahrain": "Bahrain",
    "bangladesh": "Bangladesh",
    "barbados": "Barbados",
    "belarus": "Belarus",
    "belgium": "Belgium",
    "belize": "Belize",
    "benin": "Benin",
    "bermuda": "Bermuda",
    "bhutan": "Bhutan",
    "bolivia": "Bolivia",
    "bosnia": "Bosnia and Herzegovina",
    "botswana": "Botswana",
    "brazil": "Brazil",
    "british-virgin-islands": "British Virgin Islands",
    "brunei": "Brunei",
    "bulgaria": "Bulgarian",
    "burkina-faso": "Burkina Faso",
    "burundi": "Burundi",
    "cambodia": "Cambodia",
    "cameroon": "Cameroon",
    "canada": "Canada",
    "cape-verde": "Cape Verde",
    "cayman-islands": "Cayman Islands",
    "central-african-republic": "Central African Republic",
    "chad": "Chad",
    "chile": "Chile",
    "china": "China",
    "colombia": "Colombia",
    "comores": "Comoros",
    "dr-congo": "Congo DR",
    "cook-islands": "Cook Islands",
    "costa-rica": "Costa Rica",
    "croatia": "Croatia",
    "cuba": "Cuba",
    "curacao": "Curaçao",
    "cyprus": "Cyprus",
    "czech": "Czechia",
    "denmark": "Denmark",
    "djibouti": "Djibouti",
    "dominica": "Dominica",
    "dominican-republic": "Dominican Republic",
    "ecuador": "Ecuador",
    "egypt": "Egypt",
    "el-salvador": "El Salvador",
    "guineaecuatorial": "Equatorial Guinea",
    "eritrea": "Eritrea",
    "estonia": "Estonia",
    "ethiopia": "Ethiopia",
    "falkland-islands": "Falkland Islands",
    "faroe-islands": "Faroe Islands",
    "fiji": "Fiji",
    "finland": "Finland",
    "france": "France",
    "gabon": "Gabon",
    "gambia": "Gambia",
    "georgia": "Georgia",
    "germany": "Germany",
    "ghana": "Ghana",
    "gibraltar": "Gibraltar",
    "greece": "Greece",
    "greenland": "Greenland",
    "grenada": "Grenada",
    "guam": "Guam",
    "guatemala": "Guatemala",
    "guernsey": "Guernsey",
    "guinea": "Guinea",
    "guinea-bissau": "Guinea-Bissau",
    "guyana": "Guyana",
    "haiti": "Haiti",
    "honduras": "Honduras",
    "hong-kong": "Hong Kong",
    "hungary": "Hungary",
    "iceland": "Iceland",
    "india": "India",
    "indonesia": "Indonesia",
    "iran": "Iran",
    "iraq": "Iraq",
    "ireland": "Ireland",
    "isle-of-man": "Isle of Man",
    "israel": "Israel",
    "italy": "Italy",
    "ivory-coast": "Ivory Coast",
    "jamaica": "Jamaica",
    "japan": "Japan",
    "jersey": "Jersey",
    "jordan": "Jordan",
    "kazakhstan": "Kazakhstan",
    "kenya": "Kenya",
    "kiribati": "Kiribati",
    "kosovo": "Kosovo",
    "kuwait": "Kuwait",
    "kyrgyzstan": "Kyrgyzstan",
    "laos": "Laos",
    "latvia": "Latvia",
    "lebanon": "Lebanon",
    "lesotho": "Lesotho",
    "liberia": "Liberia",
    "libya": "Libya",
    "liechtenstein": "Liechtenstein",
    "lithuania": "Lithuania",
    "luxembourg": "Luxembourg",
    "macau": "Macau",
    "madagascar": "Madagascar",
    "malawi": "Malawi",
    "malaysia": "Malaysia",
    "maldives": "Maldives",
    "mali": "Mali",
    "malta": "Malta",
    "marshall-islands": "Marshall Islands",
    "martinique": "Martinique",
    "mauritania": "Mauritania",
    "mauritius": "Mauritius",
    "mayotte": "Mayotte",
    "mexico": "Mexico",
    "micronesia": "Micronesia",
    "moldova": "Moldova",
    "monaco": "Monaco",
    "mongolia": "Mongolia",
    "montenegro": "Montenegro",
    "montserrat": "Montserrat",
    "morocco": "Morocco",
    "mozambique": "Mozambique",
    "myanmar": "Myanmar",
    "namibia": "Namibia",
    "nauru": "Nauru",
    "nepal": "Nepal",
    "netherlands": "The Netherlands",
    "new-caledonia": "New Caledonia",
    "new-zealand": "New Zealand",
    "nicaragua": "Nicaragua",
    "niger": "Niger",
    "nigeria": "Nigeria",
    "norfolk-island": "Norfolk Island",
    "north-korea": "North Korea",
    "macedonia": "North Macedonia",
    "northern-mariana-islands": "Northern Mariana Islands",
    "norway": "Norway",
    "oman": "Oman",
    "pakistan": "Pakistan",
    "palau": "Palau",
    "panama": "Panama",
    "papua-new-guinea": "Papua New Guinea",
    "paraguay": "Paraguay",
    "peru": "Peru",
    "philippines": "Philippines",
    "poland": "Poland",
    "portugal": "Portugal",
    "puerto-rico": "Puerto Rico",
    "qatar": "Qatar",
    "romania": "Romania",
    "russia": "Russia",
    "rwanda": "Rwanda",
    "saint-barthelemy": "Saint Barthélemy",
    "saint-helena": "Saint Helena",
    "saint-kitts-and-nevis": "Saint Kitts and Nevis",
    "saint-lucia": "Saint Lucia",
    "saint-martin": "Saint Martin",
    "saint-pierre-and-miquelon": "Saint Pierre and Miquelon",
    "saint-vincent-and-the-grenadines": "Saint Vincent and the Grenadines",
    "samoa": "Samoa",
    "san-marino": "San Marino",
    "sao-tome-and-principe": "São Tomé and Príncipe",
    "saudi-arabia": "Saudi Arabia",
    "senegal": "Senegal",
    "serbia": "Serbia",
    "seychelles": "Seychelles",
    "sierra-leone": "Sierra Leone",
    "singapore": "Singapore",
    "sint-maarten": "Sint Maarten",
    "slovakia": "Slovakia",
    "slovenia": "Slovenia",
    "solomon-islands": "Solomon Islands",
    "somalia": "Somalia",
    "south-africa": "South Africa",
    "south-korea": "South Korea",
    "south-sudan": "South Sudan",
    "spain": "Spain",
    "sri-lanka": "Sri Lanka",
    "sudan": "Sudan",
    "suriname": "Suriname",
    "swaziland": "Swaziland",
    "sweden": "Sweden",
    "switzerland": "Switzerland",
    "syria": "Syria",
    "taiwan": "Taiwan",
    "tajikistan": "Tajikistan",
    "tanzania": "Tanzania",
    "thailand": "Thailand",
    "timor-leste": "Timor-Leste",
    "togo": "Togo",
    "tonga": "Tonga",
    "trinidad": "Trinidad and Tobago",
    "tunisia": "Tunisia",
    "turkey": "Turkey",
    "turkmenistan": "Turkmenistan",
    "turks-and-caicos-islands": "Turks and Caicos Islands",
    "tuvalu": "Tuvalu",
    "united-states-virgin-islands": "U.S. Virgin Islands",
    "uganda": "Uganda",
    "ukraine": "Ukraine",
    "united-arab-emirates": "United Arab Emirates",
    "uk": "United Kingdom",
    "us": "United States",
    "uruguay": "Uruguay",
    "uzbekistan": "Uzbekistan",
    "vanuatu": "Vanuatu",
    "vatican-city-state": "Vatican City",
    "venezuela": "Venezuela",
    "vietnam": "Vietnam",
    "wallis-and-futuna": "Wallis and Futuna",
    "yemen": "Yemen",
    "zambia": "Zambia",
    "zimbabwe": "Zimbabwe"
}

def prompt_for_country():
    first_letter = input("Enter the first letter of the country: ").strip().lower()
    matches = [(slug, name) for slug, name in COUNTRY_SLUGS.items() if name.lower().startswith(first_letter)]

    if not matches:
        print("No countries found with that starting letter.")
        return None

    print("\nMatching countries:")
    for i, (slug, name) in enumerate(matches):
        print(f"{i + 1}. {name}")

    while True:
        try:
            choice = int(input("Select a country by number: "))
            if 1 <= choice <= len(matches):
                return matches[choice - 1][0]  # Return the selected slug
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Enter a valid number.")

def scrape_public_holidays(slug, year):
    url = f"https://www.timeanddate.com/holidays/{slug}/{year}"
    print(f"Scraping URL: {url}")  # ← this line prints the URL being scraped

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
    }
    today_date_str = datetime.datetime.now().strftime("%d/%m/%Y")
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Error fetching {url}: {resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", id="holidays-table")
    if not table:
        print(f"No holidays table at {url}")
        return []

    tbody = table.find("tbody")
    if not tbody:
        print(f"No table body at {url}")
        return []

    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }

    public = []
    for row in tbody.find_all("tr"):
        cols = row.find_all(["th", "td"])
        if len(cols) < 4:
            continue
        holiday_type = cols[3].get_text(strip=True)
        if not any(term in holiday_type for term in ["National", "Government", "Public"]):
            continue

        date_text = cols[0].get_text(strip=True)
        parts = date_text.split()
        if len(parts) != 2:
            continue
        day_str = parts[0].zfill(2)
        mon_str = parts[1]
        mon_num = month_map.get(mon_str, "??")

        full_date = f"{day_str}/{mon_num}/{year}"

        holiday_name = cols[2].get_text(strip=True)
        final_name = f"Verified, {holiday_name}. DBM. {today_date_str}"

        public.append({"date": full_date, "name": final_name})

    return public


if __name__ == "__main__":
    slug = prompt_for_country()
    if not slug:
        exit()

    start_year = int(input("Enter the start year (YYYY): "))
    current_year = datetime.datetime.now().year

    all_holidays = []
    for yr in range(start_year, current_year + 1):
        print(f"\nScraping {slug}/{yr} …")
        all_holidays.extend(scrape_public_holidays(slug, yr))

    csv_file = f"{slug}_national_holidays_{start_year}_to_{current_year}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "name"])
        writer.writeheader()
        for rec in all_holidays:
            writer.writerow(rec)

    print(f"Saved {len(all_holidays)} holidays to {csv_file}")
