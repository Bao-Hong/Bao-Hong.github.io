import re

# Regular expression to parse the input text
pattern = re.compile(
    r"(?P<authors>.+?)\s\((?P<status>In review|To be submitted|\d{4})\)\.\s"
    r"(?P<title>.+?)(?:\.\s(?P<venue>.*?)(?:\s(?P<url>https?://\S+))?)?$"
)

# Separate entries into two categories
preprints = []
published = []

# Prompt the user to input their publications
print("Enter your list of publications (press Enter twice to finish):")

# Collect user input line by line
input_text = ""
while True:
    line = input()
    if not line:  # Stop when the user presses Enter on an empty line
        break
    input_text += line + "\n"

# Process the input text line by line
for line in input_text.strip().splitlines():
    match = pattern.match(line.strip())
    if match:
        data = match.groupdict()
        if data["status"].isdigit():  # Published work
            published.append(data)
        else:  # In review or To be submitted
            data['venue'] = data.get('venue', '')
            data['url'] = data.get('url', '')
            preprints.append(data)

# Function to generate HTML list
def generate_html_list(entries):
    html_list = "  <ul>\n"
    for entry in entries:
        url = f'<a href="{entry["url"]}">[PDF]</a>' if entry["url"] else ""
        venue = f"<i>{entry['venue']}</i>" if entry["venue"] else ""
        html_list += (
            f"    <li>\n"
            f"      {entry['authors']} ({entry['status']}).\n"
            f"      {entry['title']}.\n"
            f"      {venue} {url}\n"
            f"    </li>\n"
        )
    html_list += "  </ul>\n"
    return html_list

# Generate the final HTML content without unnecessary newlines
html_content = (
    "---\n"
    "layout: archive\n"
    "title: \"Publications\"\n"
    "permalink: /publications/\n"
    "author_profile: true\n"
    "---\n\n"
    "{% if site.author.googlescholar %}\n"
    "  <div class=\"wordwrap\">\n"
    "    You can also find my articles on"
    " <a href=\"{{ site.author.googlescholar }}\">my Google Scholar</a>.\n"
    "  </div>\n"
    "{% endif %}\n\n"
    "{% include base_path %}\n\n"
    "<h2>Published Works:</h2>\n"
    f"{generate_html_list(published)}"
    "<h2>Manuscripts Submitted or in Preparation:</h2>\n"
    f"{generate_html_list(preprints)}\n"
)

# Save the generated HTML to publications.html
output_path = "../../_pages/publications.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content.strip())  # Use strip() to remove any leading/trailing whitespace

print(f"\nGenerated {output_path} successfully!")
