"""Optional FastAPI contract scaffold. Domain handlers are implemented in the engine."""

from typing import NoReturn

from fastapi import FastAPI, HTTPException
from pydantic import Field

from autodq.models import CheckConfig, DatasetProfile, FitConfig, Model, Report, RuleBook, Status
from autodq.table import Cell


class TableInput(Model):
    header: tuple[str, ...] = Field(min_length=1)
    rows: tuple[tuple[Cell, ...], ...]


class FitInput(Model):
    table: TableInput
    config: FitConfig = Field(default_factory=FitConfig)


class ReviewInput(Model):
    book: RuleBook
    decisions: dict[str, Status]


class CheckInput(Model):
    table: TableInput
    book: RuleBook
    config: CheckConfig = Field(default_factory=CheckConfig)


class Health(Model):
    status: str


app = FastAPI(title="AutoDQ API scaffold", version="0.1.0")
api = "/api/v1"


def pending() -> NoReturn:
    raise HTTPException(status_code=501, detail="Transport scaffold. Run the CLI for local analysis.")


@app.get(f"{api}/health", response_model=Health)
def health() -> Health:
    return Health(status="scaffold")


@app.post(f"{api}/profiles", response_model=DatasetProfile, responses={501: {"description": "Scaffold"}})
def profile_snapshot(payload: TableInput) -> DatasetProfile:
    # Build Table.from_rows(payload.header, payload.rows) and call autodq.profile.
    pending()


@app.post(f"{api}/rulebooks/fit", response_model=RuleBook, responses={501: {"description": "Scaffold"}})
def fit_rulebook(payload: FitInput) -> RuleBook:
    # Pass the validated reference table and config to autodq.fit.
    pending()


@app.post(f"{api}/rulebooks/review", response_model=RuleBook, responses={501: {"description": "Scaffold"}})
def review_rulebook(payload: ReviewInput) -> RuleBook:
    # Validate the user's review permissions and apply autodq.review to the selected version.
    pending()


@app.post(f"{api}/checks", response_model=Report, responses={501: {"description": "Scaffold"}})
def check_snapshot(payload: CheckInput) -> Report:
    # Pass the new table, approved book, and config to autodq.check.
    # For large snapshots move CPU-bound work to a worker and return a run ID.
    pending()
