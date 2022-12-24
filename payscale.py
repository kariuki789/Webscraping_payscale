import requests
from bs4 import BeautifulSoup
import pandas as pd

# Create an empty list to store the data
data = []

# Set the base URL and the number of pages to scrape
base_url = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
num_pages = 34  # change this value to specify the number of pages to scrape

# Scrape data from each page
for page in range(1, num_pages+1):
    # Make a request to the website and parse the HTML content
    response = requests.get(f"{base_url}/page/{page}")
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the element that contains the data you want to scrape
    data_element = soup.find("table", {"class": "data-table"})

    # Extract the data you want from the element
    for row in data_element.find_all("tr"):
        cells = row.find_all("td")
        if cells:
            major = cells[1].text.split(":")[1]
            Degree_Type=cells[2].text.split(":")[1]
            Early_Career_pay = cells[3].text.split(":")[1]
            Mid_Career_pay = cells[4].text.split(":")[1]
            High_meaning = cells[5].text.split(":")[1]
            Early_Career_pay = float(Early_Career_pay.replace("$", "").replace(",", ""))
            Mid_Career_pay = float(Mid_Career_pay.replace("$", "").replace(",", ""))
            if High_meaning == "-":
                High_meaning = 0
            else:
                High_meaning = float(High_meaning.replace("%", "").replace(",", "")) / 100
            data.append({"Major": major,"Degree_type":Degree_Type, "Early Career Pay": Early_Career_pay, "Mid Career Pay": Mid_Career_pay, "% High Meaning": High_meaning})
# Create a DataFrame from the list of data
df = pd.DataFrame(data)

# Define a function to classify the Major column as STEM,SSH or OTHER FIELDS
def classify_field(major):
    stem_keywords = ["engineering", "Aeronautics & Astronautics","Aerospace Studies",
"computer science", "math", "statistics", "physical sciences", "life sciences", "health professions"]
    ssh_keywords = ["social sciences", "humanities"]
    business_keywords = ["accounting", "business"]
    for keyword in stem_keywords:
        if keyword in major.lower():
            return "STEM"
    for keyword in ssh_keywords:
        if keyword in major.lower():
            return "SSH"
    for keyword in business_keywords:
        if keyword in major.lower():
            return "BUSINESS"
    return "OTHER FIELDS"

# Apply the classify_field function to the Major column
df["Field Type"] = df["Major"].apply(classify_field)

df.to_csv("pay_scale.csv")
# Print the resulting DataFrame
print(df.head())
