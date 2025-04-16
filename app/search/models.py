from __future__ import annotations

from app.records.models import APIResponse, Record
from django.utils.functional import cached_property


class APISearchResponse(APIResponse):

    @cached_property
    def records(self) -> list[Record]:
        records = []
        if "data" in self._raw:
            records = [
                Record(record["@template"]["details"])
                for record in self._raw["data"]
                if "@template" in record and "details" in record["@template"]
            ]
        return records

    @cached_property
    def stats_total(self) -> int:
        return int(self.get("stats.total", "0"))

    @cached_property
    def stats_results(self) -> int:
        return int(self.get("stats.results", "0"))
