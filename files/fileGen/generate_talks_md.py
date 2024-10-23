import os
import re

# Output directory
output_dir = "talks"
os.makedirs(output_dir, exist_ok=True)

# Adjusted regular expression
pattern = re.compile(
    r"(?P<authors>[\w\s\.,&-]+?)\s"
    r"\((?P<year>\d{4}),\s(?P<month>\w+)\)\.\s"
    r"(?P<title>.+?)\.\s"
    r"(?P<type>Talk|Poster)\s"
    r"presented at the\s(?P<venue>.+?),\s"
    r"(?P<location>.+?)(?:\.|$)"
)

# Function to convert month names to numeric format
def convert_month(month_name):
    months = {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    }
    return months.get(month_name, "01")

# Function to generate markdown content and save it
def save_to_markdown(data, filename):
    content = f"""---
title: "{data['title']}"
collection: talks
type: "{data['type']}"
venue: "{data['venue']}"
date: {data['year']}-{convert_month(data['month'])}-01
location: "{data['location']}"
authors: "{data['authors']}"
file_url: "/files/{data['year']}-{convert_month(data['month'])}-{data['authors'].split(",")[0].strip()}.pdf"
#permalink: "https://jov.arvojournals.org/article.aspx?articleid=2801336"
#video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
---
"""
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"File created: {filepath}")

# Collect user input
print("Enter your entries (press Enter twice to finish):")
user_input = ""
while True:
    line = input()
    if not line.strip():
        break
    user_input += line + "\n"

# Check each line with the regex pattern
print("\nChecking input for matches...\n")
for i, line in enumerate(user_input.strip().splitlines(), 1):
    match = pattern.match(line.strip())
    if match:
        print(f"Line {i}: Match found!")
        data = match.groupdict()
        for key, value in data.items():
            print(f"  {key}: {value}")

        # Prepare filename
        first_author_last_name = data['authors'].split(",")[0].strip()
        date = f"{data['year']}-{convert_month(data['month'])}-01"
        filename = f"{date}-{first_author_last_name}.md".replace(" ", "_").strip()

        # Save to markdown
        save_to_markdown(data, filename)
    else:
        print(f"Line {i}: No match found. Please check the format.")

print("\nMarkdown files generation complete!")
