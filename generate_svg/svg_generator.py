import sys
import subprocess
from collections import defaultdict
import os

def generate_commit_percentage_svg(token, repository, branch="main"):
    """
    Generates a commit percentage dashboard SVG for users with @smartone.ai email addresses.
    :param token: Personal access token or GitHub Actions token for authentication.
    :param repository: Repository in the format 'owner/repo'.
    :param branch: Branch name to fetch logs from.
    """
    repo_url = f"https://{token}@github.com/{repository}.git"
    
    # Clone the repository using the token
    repo_dir = "temp_repo"
    if os.path.exists(repo_dir):
        subprocess.run(["rm", "-rf", repo_dir])  # Clean up if the directory already exists
    subprocess.run(["git", "clone", "--branch", branch, repo_url, repo_dir])

    # Move to the cloned repository
    os.chdir(repo_dir)

    # Fetch commit logs
    result = subprocess.run(["git", "log", "--pretty=format:%an <%ae>"], capture_output=True, text=True)
    commit_logs = result.stdout.splitlines()

    # Process logs for users with @smartone.ai email addresses
    email_to_name = {}
    commit_count = defaultdict(int)

    for log in commit_logs:
        name, email = log.rsplit(" <", 1)
        email = email.rstrip(">")
        if email.endswith("@smartone.ai"):  # Filter emails
            commit_count[email] += 1
            email_to_name[email] = name

    # Calculate percentages
    total_commits = sum(commit_count.values())
    percentages = {email: (count / total_commits) * 100 for email, count in commit_count.items()}

    # Generate SVG
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

    # Write SVG to output directory
    os.makedirs("output", exist_ok=True)
    with open("../output/commit_percentage.svg", "w") as f:  # Save outside the temp_repo
        f.write(svg_content)

    print("SVG generated successfully!")

    # Clean up cloned repo
    os.chdir("..")
    subprocess.run(["rm", "-rf", repo_dir])

# Entry point for the script
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m generate_svg.svg_generator <TOKEN> <REPOSITORY>")
        sys.exit(1)

    TOKEN = sys.argv[1]
    REPOSITORY = sys.argv[2]
    generate_commit_percentage_svg(TOKEN, REPOSITORY)
