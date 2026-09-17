import re

with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

js_ids = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js))
html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))

missing = js_ids - html_ids
print("Total IDs referenced in JS:", len(js_ids))
print("Total IDs defined in HTML:", len(html_ids))
print("Missing IDs:", sorted(list(missing)))

# Also check lines where missing IDs are used:
for m in sorted(list(missing)):
    for line_num, line in enumerate(js.splitlines(), 1):
        if f'getElementById("{m}")' in line or f"getElementById('{m}')" in line:
            print(f"  Missing '{m}' used at line {line_num}: {line.strip()}")
