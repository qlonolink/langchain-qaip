from typing import (
    Any,
    Dict,
    List,
)

import requests
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.utils import get_from_dict_or_env
from pydantic import model_validator

QAIP_SEARCH_API_URL = "https://developer.qaip.com/api/v1/search"
USER_AGENT = "qaip-langchain-retriever/1.0"


class QAIPRetriever(BaseRetriever):
    api_key: str = ""

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "QAIP_API_KEY")
        return values

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

    def _search(self, query: str, **keywords: Any) -> List[dict]:
        body = {
            "query": query,
        }
        for key in ["tag_ids", "source_types", "file_types", "date_from", "date_to", "domains", "limit", "offset"]:
            if key in keywords and keywords[key]:
                body[key] = keywords[key]

        response = requests.post(url=QAIP_SEARCH_API_URL, headers=self._headers, json=body, timeout=60)
        if response.status_code != 200:
            raise Exception(f"Error in search request: {response}")

        return response.json()

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
        **keywords: Any,
    ) -> List[Document]:
        search_results = self._search(query, **keywords)

        return [Document(page_content=result.pop("text"), metadata=result) for result in search_results["results"]]
