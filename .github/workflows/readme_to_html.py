#!/usr/bin/env python3

import markdown
from pygments.formatters import HtmlFormatter

# Read README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()

# Configure markdown with extensions
md = markdown.Markdown(
    extensions=[
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.sane_lists'
    ],
    extension_configs={
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'use_pygments': True
        }
    }
)

# Convert markdown to HTML
html_content = md.convert(readme_content)

# Get syntax highlighting CSS
formatter = HtmlFormatter(style='default')
pygments_css = formatter.get_style_defs('.highlight')

# Create complete HTML document
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README</title>
    <style>
{pygments_css}
body {{
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}}
th, td {{
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}}
th {{
    background-color: #f5f5f5;
    font-weight: bold;
}}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

# Write to index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("✅ README.md converted to index.html")
