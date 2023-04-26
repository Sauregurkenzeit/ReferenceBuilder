import requests


def search_articles(keywords, result_limit=10):
    base_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
    query = ' '.join(keywords)
    params = {
        'query': query,
        'format': 'json',
        'resulttype': 'core',
        'pageSize': result_limit
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()['resultList']['result']
    else:
        print(f"Error {response.status_code}: Unable to fetch articles.")
        return None


def generate_reference_list(articles):
    reference_list = []
    for article in articles:
        authors = ', '.join([author['fullName'] for author in article['authorList']['author']])
        title = article['title']
        journal = article['journalInfo']['journal']['title']
        year = article['pubYear']
        volume = article.get('journalInfo', {}).get('volume', '')
        issue = article.get('journalInfo', {}).get('issue', '')
        pages = article.get('pageInfo', '')
        doi = article.get('doi', '')

        reference = f"{authors} ({year}). {title}. {journal}, {volume}({issue}), {pages}. https://doi.org/{doi}"
        reference_list.append(reference)

    return reference_list


def main():
    keywords = input("Enter the keywords separated by space: ").split()
    result_limit = int(input("Enter the number of results to fetch: "))
    articles = search_articles(keywords, result_limit)

    if articles:
        reference_list = generate_reference_list(articles)
        print("\nReference List:")
        for idx, reference in enumerate(reference_list, start=1):
            print(f"{idx}. {reference}")


if __name__ == '__main__':
    main()
