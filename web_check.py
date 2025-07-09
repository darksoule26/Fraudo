from duckduckgo_search import DDGS

def search_company_info(company_name):
    try:
        query = f"{company_name} official website"
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(query, region='in-en', safesearch='Moderate', max_results=5)

            for r in search_results:
                link = r.get("href")
                if link:
                    results.append(link)

        return {
            "found": bool(results),
            "top_links": results,
            "trust_summary": "Company website and info found online." if results else "No reliable links found for the company."
        }

    except Exception as e:
        return {
            "found": False,
            "top_links": [],
            "trust_summary": f"Search error: {str(e)}"
        }
