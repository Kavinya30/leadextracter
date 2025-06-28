import requests
import pandas as pd
import json
import time
import random

# --- CONFIGURATION (Replace with your actual API Key and Endpoint) ---
# IMPORTANT: In a real-world scenario, you would replace these with the actual
# API details from your chosen legitimate B2B data provider that offers LinkedIn data
# AND Google Business Profile related website information.
# These values are purely illustrative and for demonstration purposes.
FICTIONAL_B2B_API_KEY = "YOUR_REAL_B2B_DATA_PROVIDER_API_KEY" # Replace this!
FICTIONAL_B2B_API_URL = "https://api.example-b2b-provider.com/v1/contacts" # Replace with actual API endpoint for contacts

class MockB2BContactAPI:
    """
    A mock class to simulate a legitimate B2B Data Provider API that includes LinkedIn profiles
    and a simulated Google Business Profile website field.
    In a real application, this would be actual HTTP calls to a service like Apollo.io, ZoomInfo, etc.
    """
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        print("Mock B2B Contact API initialized. (Remember to use a real provider!)")

    def _generate_mock_contacts(self, company_industry, company_country, count):
        """
        Generates mock contact data, including LinkedIn profiles and a simulated
        Google Business Profile website field.
        """
        mock_contacts = []
        for i in range(count):
            first_name = random.choice(["Alice", "Bob", "Charlie", "Diana", "Eve"])
            last_name = random.choice(["Smith", "Jones", "Williams", "Brown", "Davis"])
            full_name = f"{first_name} {last_name}"
            
            mock_company_name = f"Company {random.randint(1, 100)} {company_industry.title() if company_industry else ''}"
            mock_title = random.choice(["CEO", "Marketing Manager", "Sales Representative", "Software Engineer", "HR Director"])
            mock_country = company_country.title() if company_country else random.choice(["USA", "India", "Germany", "Canada"])
            
            # Simulate LinkedIn profile URL presence
            has_linkedin = random.random() > 0.1 # 90% chance to have a LinkedIn profile URL
            linkedin_url = f"https://www.linkedin.com/in/{first_name.lower()}{last_name.lower()}{random.randint(1,99)}" if has_linkedin else None

            # Simulate a general website for the company (from any source)
            has_general_website = random.random() > 0.3 # 70% chance to have a general website
            general_website_url = f"http://www.{mock_company_name.lower().replace(' ', '')}.com" if has_general_website else None

            # Simulate Google Business Profile website presence independently
            # This is the key addition to address your specific GMB requirement
            # Set a higher chance (60%) for no GMB website to generate more target leads
            has_gmb_website = random.random() > 0.6 
            gmb_website_url = f"http://gmb.website/{mock_company_name.lower().replace(' ', '')}{random.randint(1,99)}.com" if has_gmb_website else None

            mock_contacts.append({
                "id": f"contact_{random.randint(100000, 999999)}",
                "name": full_name,
                "title": mock_title,
                "company_name": mock_company_name,
                "industry": company_industry,
                "country": mock_country,
                "email": f"{first_name.lower()}.{last_name.lower()}@{mock_company_name.lower().replace(' ', '')}.com",
                "phone": f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
                "linkedin_profile_url": linkedin_url,
                "general_website_url": general_website_url, # General website, for context
                "google_business_profile_website": gmb_website_url # Specific GMB website status
            })
        return mock_contacts

    def get_contacts(self, industry=None, country=None, limit=50, page=1):
        """
        Simulates fetching contact data from a B2B data provider's API.
        In a real scenario, this would involve `requests.get()` to the actual API endpoint.
        """
        print(f"Mock API Call: Fetching contacts for industry='{industry}', country='{country}', limit={limit}, page={page}")
        
        # Simulate API call delay
        time.sleep(1 + random.random() * 0.5) 

        # Generate mock data. In a real scenario, this would be the API's actual response.
        mock_data = self._generate_mock_contacts(industry, country, limit)
        
        response_data = {
            "data": mock_data,
            "total_results": 1000, # Fictional total results
            "current_page": page,
            "per_page": limit
        }
        
        return response_data

class LinkedInLeadsExtractor:
    def __init__(self, api_client):
        self.api_client = api_client
        self.filtered_leads = [] # Renamed for clarity, will hold the final filtered leads

    def extract_and_filter_gmb_no_website(self, industry=None, country=None):
        """
        Extracts leads using the provided API client and filters them
        based on the criteria:
        1. Country filter
        2. Industry filter
        3. No website listed in their Google Business Profile (simulated)
        """
        all_raw_contacts = []
        page = 1
        has_more_data = True

        while has_more_data:
            print(f"Requesting page {page} from API...")
            try:
                # Fetch a batch of contacts from the API
                api_response = self.api_client.get_contacts(
                    industry=industry,
                    country=country,
                    limit=50, # Most APIs have a default/max limit per request for contacts
                    page=page
                )
                
                current_batch_contacts = api_response.get("data", [])
                
                if not current_batch_contacts:
                    has_more_data = False
                else:
                    all_raw_contacts.extend(current_batch_contacts)
                    # For this mock, we'll simulate stopping after a few pages or if a batch is small
                    if len(current_batch_contacts) < 50 or page >= 5: # Max 5 pages for demo to get more data
                        has_more_data = False
                    page += 1

            except requests.exceptions.RequestException as e:
                print(f"API call failed: {e}. Stopping extraction.")
                has_more_data = False
            
            time.sleep(random.uniform(0.5, 2.0)) # Be polite to the API

        print(f"\nTotal raw contacts fetched: {len(all_raw_contacts)}")

        # Now, apply the 'no Google Business Profile website' filter
        self.filtered_leads = []
        for contact in all_raw_contacts:
            # This is the crucial filter: Check if 'google_business_profile_website' is missing or empty
            gmb_website = contact.get("google_business_profile_website")
            
            if not gmb_website: # If the GMB website field is None, empty string, etc.
                self.filtered_leads.append(contact)
        
        return self.filtered_leads

# --- Main Application Logic ---
if __name__ == "__main__":
    # 1. Initialize the API Client (replace MockB2BContactAPI with a real client)
    api_client = MockB2BContactAPI(FICTIONAL_B2B_API_KEY, FICTIONAL_B2B_API_URL)
    
    # 2. Initialize the Leads Extractor
    leads_extractor = LinkedInLeadsExtractor(api_client) # Renamed to be more general as it's not just LinkedIn now

    # 3. Get User Input
    print("--- Legitimate Leads Extractor (with Simulated GMB Website Filter) ---")
    print("This tool simulates fetching professional contacts from a B2B data provider API.")
    print("It filters for contacts whose company does NOT have a website listed in their Google Business Profile (simulated).")
    print("-" * 80)

    industry_filter = input("Enter industry to filter by (e.g., 'Software', 'Healthcare', leave blank for any): ").strip()
    country_filter = input("Enter country to filter by (e.g., 'USA', 'UK', 'Australia', leave blank for any): ").strip()

    # Convert empty strings to None for the API calls
    industry_filter = industry_filter if industry_filter else None
    country_filter = country_filter if country_filter else None

    # 4. Execute Extraction and Filtering
    print(f"\nStarting extraction for Industry: '{industry_filter if industry_filter else 'Any'}', Country: '{country_filter if country_filter else 'Any'}'...")
    
    start_time = time.time()
    
    # Call the modified extraction method
    final_filtered_leads = leads_extractor.extract_and_filter_gmb_no_website(
        industry=industry_filter,
        country=country_filter
    )
    
    end_time = time.time()
    
    # 5. Display Results and Save to CSV
    if final_filtered_leads:
        print(f"\nExtraction complete! Found {len(final_filtered_leads)} leads whose companies lack a Google Business Profile website (simulated).")
        print(f"Total time taken: {end_time - start_time:.2f} seconds.")

        # Create a DataFrame for better presentation and CSV export
        df = pd.DataFrame(final_filtered_leads)
        
        # Define the columns you want to display/save (adjust based on actual API response)
        # Include general_website_url and google_business_profile_website for clarity
        display_columns = [
            'name', 'title', 'company_name', 'industry', 'country',
            'email', 'phone', 'linkedin_profile_url',
            'general_website_url', 'google_business_profile_website'
        ]
        
        # Ensure only existing columns are selected
        final_df = df[[col for col in display_columns if col in df.columns]]

        # Generate a descriptive filename
        output_filename = f"gmb_no_website_leads_{industry_filter if industry_filter else 'any_industry'}_{country_filter if country_filter else 'any_country'}.csv"
        
        final_df.to_csv(output_filename, index=False)
        print(f"\nFiltered leads saved to '{output_filename}'")
        
        print("\n--- First 10 Filtered Leads (with GMB Website Status) ---")
        print(final_df.head(10).to_string())
    else:
        print("\nNo leads found matching the criteria or an error occurred during extraction.")
        print(f"Total time taken: {end_time - start_time:.2f} seconds.")