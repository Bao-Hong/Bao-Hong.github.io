import re

# Input: Your plain text list of publications
input_text = """
Hong, B.+, Chen J.+, Huang, W.J., & Li L.* (In review). Serial dependence in smooth pursuit eye movements of preadolescent children and adults
Hong, B., Chen J., & Li L.* (To be submitted). Temporal dynamics of serial dependence in ocular tracking
Huang, W.J.+, Chen J.+, Hong, B., Wang, Y., S., Zuo, X., N.*, & Li, L.* (To be submitted). Investigating Brain Structural Correlates of Ocular Tracking in Preadolescent Children and Young Adults.
Hong, B., Zhang, L., & Sun, H. (2019). Measurement of the Vertical Spatial Metaphor of Power Concepts Using the Implicit Relational Assessment Procedure. Frontiers in Psychology, 10, 1422. https://doi.org/10.3389/fpsyg.2019.01422
"""

# Regular expression to parse the input text
pattern = re.compile(
    r"(?P<authors>.+?)\s\((?P<status>In review|To be submitted|\d{4})\)\.\s"
    r"(?P<title>.+?)(?:\.\s(?P<venue>.*?)(?:\s(?P<url>https?://\S+))?)?$"
)

# Separate entries into two categories
preprints = []
published = []

# Process the input text line by line
for line in input_text.strip().splitlines():
    match = pattern.match(line.strip())
    if match:
        data = match.groupdict()
        if data["status"].isdigit():  # Published work
            published.append(data)
        else:  # In review or To be submitted
            # Fill in venue and URL as None if not present
            data['venue'] = data.get('venue', None)
            data['url'] = data.get('url', None)
            preprints.append(data)

# Debug: Print out categorized publications
print("Preprints:")
for entry in preprints:
    print(entry)

print("\nPublished Works:")
for entry in published:
    print(entry)

# Function to generate an HTML list for a given category
def generate_html_list(entries):
    html_list = "<ul>\n"
    for entry in entries:
        url = f'<a href="{entry["url"]}">[PDF]</a>' if entry["url"] else ""
        venue = f"<i>{entry['venue']}</i>" if entry["venue"] else ""
        html_list += f'<li>{entry["authors"]} ({entry["status"]}). {entry["title"]}. {venue} {url}</li>\n'
    html_list += "</ul>\n"
    return html_list

# Generate the final HTML content
html_content = f"""
---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{{% if site.author.googlescholar %}}
  <div class="wordwrap">You can also find my articles on <a href="{{{{ site.author.googlescholar }}}}">my Google Scholar profile</a>.</div>
{{% endif %}}

<h2>Preprints & Manuscripts submitted or in preparation:</h2>
{generate_html_list(preprints)}

<h2>Published Works:</h2>
{generate_html_list(published)}
"""

# Save the generated HTML to publications.html
output_path = "publications.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\nGenerated {output_path} successfully!")
