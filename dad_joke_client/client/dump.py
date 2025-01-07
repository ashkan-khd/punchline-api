import httpx
import asyncio

# List of URLs to request
urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
]

# Asynchronous function to fetch a single URL
async def fetch_url(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()  # Parse JSON response

# Asynchronous function to fetch multiple URLs concurrently
async def fetch_all_urls(urls):
    tasks = [fetch_url(url) for url in urls]  # Create a list of tasks
    results = await asyncio.gather(*tasks)  # Gather results
    print("Type of results:")
    print(type(results))
    print(type(results[0]))
    return results

# Run the event loop
async def main():
    responses = await fetch_all_urls(urls)
    for i, response in enumerate(responses):
        print(f"Response {i + 1}: {response}")

# Start the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
