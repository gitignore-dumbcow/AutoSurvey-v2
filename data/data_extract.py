from bs4 import BeautifulSoup

# Read the HTML file
with open(r'place.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

options = soup.find_all('option')

result = []
for opt in options:
    code = opt.get('value', '').strip()
    label = opt.get('label', '').strip()
    if code and label:
        result.append({'code': code, 'label': label})

# Print or save the result
for item in result:
    
    import json
    with open('place_options.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)