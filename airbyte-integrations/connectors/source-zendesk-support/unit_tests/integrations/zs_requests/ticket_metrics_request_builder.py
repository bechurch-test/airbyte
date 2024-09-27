# Copyright (c) 2023 Airbyte, Inc., all rights reserved.

from typing import Optional

from .base_request_builder import ZendeskSupportBaseRequestBuilder
from .request_authenticators.authenticator import Authenticator


class TicketMetricsRequestBuilder(ZendeskSupportBaseRequestBuilder):
    @classmethod
    def stateful_ticket_metrics_endpoint(cls, authenticator: Authenticator, ticket_id: int) -> "TicketMetricsRequestBuilder":
        return cls("d3v-airbyte", f"tickets/{ticket_id}/metrics").with_authenticator(authenticator)

    @classmethod
    def stateless_ticket_metrics_endpoint(cls, authenticator: Authenticator) -> "TicketMetricsRequestBuilder":
        return cls("d3v-airbyte", "ticket_metrics").with_authenticator(authenticator)

    def __init__(self, subdomain: str, resource: str) -> None:
        super().__init__(subdomain, resource)
        self._page_size: Optional[int] = None

    @property
    def query_params(self):
        params = super().query_params or {}
        if self._page_size:
            params["page[size]"] = self._page_size
        return params

    def with_page_size(self, page_size: int = 100) -> "TicketMetricsRequestBuilder":
        self._page_size: int = page_size
        return self
