import os
import re

# Input references as a single string
input_text = """
Hong, B.+, Chen J.+, Huang, W.J., & Li L.* (In review). Serial dependence in smooth pursuit eye movements of preadolescent children and adults.
Hong, B., Chen J., & Li L.* (To be submitted). Temporal dynamics of serial dependence in ocular tracking.
Huang, W.J.+, Chen J.+, Hong, B., Wang, Y., S., Zuo, X., N.*, & Li, L.* (To be submitted). Investigating Brain Structural Correlates of Ocular Tracking in Preadolescent Children and Young Adults.
Hong, B., Zhang, L., & Sun, H. (2019). Measurement of the Vertical Spatial Metaphor of Power Concepts Using the Implicit Relational Assessment Procedure. Frontiers in Psychology, 10, 1422. https://doi.org/10.3389/fpsyg.2019.01422
"""

# Output directory
output_dir = "publications"
os.makedirs(output_dir, exist_ok=True)

# Regular expression to extract details
pattern = re.compile(
    r"(?P<authors>.+?)\s\((?P<status>(In review|To be submitted|\d{4}))\)\.\s"
    r"(?P<title>.+?)\.\s(?P<venue>[^.,]*)"
    r"(?:,\s(?P<volume_issue>\d+,\s?\d+))?"
    r"(?:\.\s(?P<doi>https?://[^\s]+))?"
)

# Generate markdown content and save to individual .md files
for match in pattern.finditer(input_text):
    data = match.groupdict()

    # Determine the date or status
    if data["status"].isdigit():
        date = f"{data['status']}-01-01"
    else:
        date = "TBD"

    # Generate permalink and filename from the title
    title_slug = data['title'].replace(' ', '-').lower()
    filename = f"{date}-{title_slug}.md"
    permalink = f"/publication/{filename[:-3]}"

    # Prepare venue and citation
    venue = data["venue"] or "Unpublished"
    citation = f"{data['authors']} ({data['status']}). {data['title']}."

    # Generate markdown content
    content = f"""---
title: "{data['title']}"
collection: publications
category: conferences
permalink: {permalink}
excerpt: 'This paper is about {data["title"]}.'
date: {date}
venue: '{venue}'
paperurl: ''
citation: '{citation}'
---
"""

    # Save each entry as an .md file
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Markdown files generated successfully!")
