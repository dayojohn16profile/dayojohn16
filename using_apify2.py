from apify_client import ApifyClient

# 1️⃣ Initialize the client with your token
client = ApifyClient("YOUR_API_TOKEN_HERE")

# 2️⃣ Set up the input
run_input = {
    "profileUrls": [
        "https://www.linkedin.com/in/williamhgates",
        "https://www.linkedin.com/in/jeannie-wyrick-b4760710a",
    ],
    "searchFilters": {
        "currentCompany": None,        # leave None if you don’t want to filter by company
        "currentTitle": None,          # leave None if you don’t filter by title
        "industries": ["Information Technology & Services"],  # filter to Technology
    },
    "resultsLimit": 10  # maximum number of profiles to return
}

# 3️⃣ Run the actor
actor_run = client.actors.run(
    actor_id="dev_fusion/linkedin-profile-scraper",  # your actor ID
    run_input=run_input,
    wait_for_finish=True
)

# 4️⃣ Fetch the dataset items (the results)
dataset_items = client.dataset(actor_run["defaultDatasetId"]).list_items()
for item in dataset_items.items:
    print(item)
