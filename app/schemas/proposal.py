from pydantic import BaseModel, Field
from typing import List


class ProposalRequest(BaseModel):
    document_ids: List[int]
    request: str


class ProposalSection(BaseModel):
    title: str
    content: List[str]


class ProposalSource(BaseModel):
    document_id: int
    document_title: str
    chunk_id: int
    relevant_content: str


class ProposalChartData(BaseModel):
    label: str
    value: float


class ProposalChart(BaseModel):
    title: str
    chart_type: str
    description: str
    data: List[ProposalChartData]
    source_chunk_ids: List[int]


class GeneratedChart(BaseModel):
    title: str
    chart_type: str
    url: str


class ProposalResponse(BaseModel):
    request: str
    document_ids: List[int]

    sections: List[ProposalSection]

    charts: List[ProposalChart] = Field(
        default_factory=list
    )

    generated_charts: List[GeneratedChart] = Field(
        default_factory=list
    )

    sources: List[ProposalSource]

    report_url: str