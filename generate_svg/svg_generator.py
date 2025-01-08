import subprocess
from collections import defaultdict
import os

def generate_commit_percentage_svg():
    """
    Generates a commit percentage dashboard SVG for users with @smartone.ai email addresses.
    """
    result = subprocess.run(["git", "log", "--pretty=format:%an <%ae>"], capture_output=True, text=True)
    commit_logs = result.stdout.splitlines()

    email_to_name = {}
    commit_count = defaultdict(int)

    for log in commit_logs:
        name, email = log.rsplit(" <", 1)
        email = email.rstrip(">")
        if email.endswith("@smartone.ai"):  # Filter emails
            commit_count[email] += 1
            email_to_name[email] = name

    total_commits = sum(commit_count.values())
    percentages = {email: (count / total_commits) * 100 for email, count in commit_count.items()}

    svg_width = 600
    bar_width = 400
    bar_height = 20
    padding = 10
    text_padding = 5
    svg_height = len(percentages) * (bar_height + padding) + 80

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">
    <style>
      .title {{ font: bold 18px sans-serif; fill: #333; }}
      .subtitle {{ font: bold 14px sans-serif; fill: #666; }}
      .text {{ font: 14px sans-serif; fill: #555; }}
      .bar {{ fill: #4caf50; }}
      .bg-bar {{ fill: #e0e0e0; }}
    </style>
    <text x="20" y="30" class="title">Commit Percentage Dashboard</text>
    """

    y_offset = 80
    for email, percent in percentages.items():
        username = email_to_name[email]
        bar_length = (percent / 100) * bar_width

        svg_content += f"""
        <rect x="20" y="{y_offset}" width="{bar_width}" height="{bar_height}" class="bg-bar"></rect>
        <rect x="20" y="{y_offset}" width="{bar_length}" height="{bar_height}" class="bar"></rect>
        <text x="{bar_width + 30}" y="{y_offset + bar_height - text_padding}" class="text">{percent:.2f}%</text>
        <text x="25" y="{y_offset - text_padding + 20}" class="text">{username}</text>
        """
        y_offset += bar_height + padding

    svg_content += "</svg>"

    os.makedirs("output", exist_ok=True)
    with open("output/commit_percentage.svg", "w") as f:
        f.write(svg_content)

    print("SVG generated successfully!")

# Calling the function to generate the SVG
if __name__ == "__main__":
    generate_commit_percentage_svg()