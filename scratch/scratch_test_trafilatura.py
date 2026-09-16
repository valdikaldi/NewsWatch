import trafilatura
import json

# Define the path to your local HTML file
html_file_path = "Canada invited to become first 'associate member' of the EU _ Euronews.html"  


try:
    #  Read the local HTML content
    with open(html_file_path, "r", encoding="utf-8") as file:
        raw_html = file.read()

    #  Extract as JSON with metadata enabled
    json_output = trafilatura.extract(
        raw_html, 
        output_format="json", 
        with_metadata=True,
        include_comments=False
    )

    if json_output:
        #  Convert the JSON string into a Python dictionary
        article_data = json.loads(json_output)
        
        #  Grab the fields (using .get() prevents errors if a field is missing)
        title = article_data.get("title")
        summary = article_data.get("excerpt")  # Trafilatura names the brief summary 'excerpt'
        article_text = article_data.get("text")
        date = article_data.get("date")

        #  Display the results
        print(f"TITLE:\n{title}\n")
        print(f"PUBLICATION DATE:\n{date}\n")
        print(f"SUMMARY / EXCERPT:\n{summary}\n")
        print(f"ARTICLE TEXT (First 300 chars):\n{article_text[:300]}...")
        
    else:
        print("Trafilatura failed to extract structural data from this HTML.")

except FileNotFoundError:
    print(f"Error: The file '{html_file_path}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")