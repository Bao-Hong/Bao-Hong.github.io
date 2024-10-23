import os
import re

# Input string with multiple entries
input_text = """
Hong, B., Chen, J., & Li, L. (2024, May). Temporal dynamics of serial dependence in ocular tracking. Talk presented at the 2024 Annual Meeting of the Vision Sciences Society, Florida, USA.
Hong, B., Huang, W.J., Li, E., Chen, J., & Li, L. (2023, August). Ocular tracking abilities in preadolescent children. Talk presented at the 5th China Vision Science Conference (CVSC2023), Wenzhou, Zhejiang, China
Hong, B., Huang, W. J., Li, E., Chen, J., & Li, L. (2023, April). Ocular tracking abilities in preadolescent children. Poster presented the 2023 Annual Meeting of the General Psychology and Experimental Psychology of the Chinese Psychological Association, Jinhua, Zhejiang, China
Huang, W. J., Hong, B., Chen, J., & Li, L. (2024, October). Brain Structural Correlates of Ocular Tracking in Preadolescent Children and Young Adults. Poster presented at the 2024 Annual Meeting of Society for Neuroscience, Chicago, USA.
Huang, W. J., Hong, B., Wu, J. H., Chen, J., & Li, L. (2023, August). Investigating brain structural correlates of ocular tracking in preadolescent children and young adults. Poster presented at the 5th China Vision Science Conference (CVSC2023), Wenzhou, Zhejiang, China
"""

# Output directory
output_dir = "talks"
os.makedirs(output_dir, exist_ok=True)

# Regular expression to extract details from each entry
pattern = re.compile(
    r"(?P<authors>(\w+),\s.+?)\s\((?P<year>\d{4}),\s(?P<month>\w+)\)\.\s"
    r"(?P<title>.+?)\.\s(?P<type>(Talk|Poster))\s"
    r"presented at the\s(?P<venue>.+?),\s(?P<location>.+?)\."
)

# Function to convert month names to numeric format
def convert_month(month_name):
    months = {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    }
    return months.get(month_name, "01")

# Generate markdown content and save to individual .md files
for match in pattern.finditer(input_text):
    data = match.groupdict()

    # Extract the first author's last name
    first_author_last_name = data['authors'].split(",")[0]

    # Prepare date in YYYY-MM-DD format
    date = f"{data['year']}-{convert_month(data['month'])}-01"

    # Generate markdown content
    content = f"""---
title: "{data['title']}"
collection: talks
type: "{data['type']}"
venue: "{data['venue']}"
date: {date}
location: "{data['location']}"
file_url: "/files/{data['title'].replace(' ', '_')}.pdf"
---
"""

    # Create filename in the format YYYY-MM-DD-LastName.md
    filename = f"{date}-{first_author_last_name}.md"
    filepath = os.path.join(output_dir, filename)

    # Write the content to a markdown file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Markdown files generated successfully!")
