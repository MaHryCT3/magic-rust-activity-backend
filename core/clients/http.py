from urllib.parse import urljoin

from httpx import AsyncClient, Response

from core.logger import logger


class HTTPClient:
    def __init__(self, base_url: str = '', headers: dict | None = None) -> None:
        self.client = AsyncClient(timeout=60 * 30, headers=headers)
        self.base_url = base_url

    async def request(
        self,
        url: str,
        http_method: str,
        query: dict | None = None,
        payload: dict | None = None,
        body: dict | None = None,
        **kwargs,
    ) -> Response:
        url = urljoin(self.base_url, url)
        logger.debug(f'Make request: {http_method}: {url} | Query: {query} | Payload: {payload} | Body: {body}')
        response = await self.client.request(http_method, url, params=query, data=payload, json=body, **kwargs)
        logger.debug(f'Receive response {response.request.method} {response.request.url}: {response.text}')
        response.raise_for_status()
        return response

    async def get(
        self,
        url: str,
        query: dict | None = None,
        headers: dict | None = None,
        **kwargs,
    ) -> Response:
        return await self.request(
            url,
            http_method='GET',
            query=query,
            headers=headers,
            **kwargs,
        )

    async def post(
        self,
        url: str,
        query: dict | None = None,
        payload: dict | None = None,
        body: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        return await self.request(
            url,
            http_method='POST',
            query=query,
            payload=payload,
            body=body,
            headers=headers,
        )

    async def patch(
        self,
        url: str,
        query: dict | None = None,
        payload: dict | None = None,
        body: dict | None = None,
        headers: dict | None = None,
    ):
        return await self.request(
            url,
            http_method='PATCH',
            query=query,
            payload=payload,
            body=body,
            headers=headers,
        )
