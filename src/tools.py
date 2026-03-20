from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search(query: str) -> str:
    contents = []
    search_response = tavily_client.search(query)
    for searched in search_response["results"][:3]:
        contents.append(searched["content"])
    return "\n".join(contents)
def finish(answer: str) -> str:
    return answer
TOOLS = {"search": search, "finish": finish}
if __name__ == "__main__":
    result = search("capital of France")
    print(result)