import os

possible_links = {}
for root, dirs, files in os.walk('docs'):
        for file in files:
            if file.endswith('.html'):
                pth = os.path.join(root, file).replace('docs/', '')
                year = pth.split('/')[0]
                month = pth.split('/')[1]
                title = pth.split('/')[-1]
                if year not in possible_links:
                    possible_links[year] = {}
                if month not in possible_links[year]:
                    possible_links[year][month] = []
                possible_links[year][month].append(title)

with open('docs/index.html', 'w+') as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css">
</head>
<body>
""")
    for year in [str(i) for i in range(2007, 2023)]:
        f.write(f'<h1 class="year">{year}</h1>\n')
        for month in possible_links[year]:
            f.write(f'<h2 class="month">{month}</h2>\n')
            for title in possible_links[year][month]:
                f.write(f'<a href="{year}/{month}/{title}">{title.replace(".html","").replace("_"," ")}</a><br>\n')
    f.write("</body></html>")
                