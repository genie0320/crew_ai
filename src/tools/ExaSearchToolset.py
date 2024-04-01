"""
# Requirements for the Tools
- description : 도구의 이름표와 설명서 (agent는 이걸 읽어보고 사용한다.)
- input : 이를테면... api 설명서의 input 같은 것.
- result : 이를테면... api 설명서의 result 같은 것.
"""

from dataclasses import dataclass
from dotenv import load_dotenv
from exa_py import Exa
from langchain.agents import tool
from typing import List, Callable, Any
import os

load_dotenv()


# TODO: 왜. 여기는 self를 쓰지 않는건가. 그런데 왜 또 실행은 되는 것인가.
class ExaSearchToolset:
    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return ExaSearchToolset._exa().search(
            f"{query}", use_autoprompt=True, num_results=3
        )

    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return ExaSearchToolset._exa().find_similar(url, num_results=3)

    @tool
    def get_contents(ids: str):
        """Get the contents of a webpage.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """
        # ids = eval(ids)
        contents = str(ExaSearchToolset._exa().get_contents(ids))
        print(contents)
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)

    def tools():
        return [
            ExaSearchToolset.search,
            ExaSearchToolset.find_similar,
            ExaSearchToolset.get_contents,
        ]

    def _exa():
        return Exa(api_key=os.environ["EXA_API_KEY"])
