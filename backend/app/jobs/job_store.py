from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from uuid import UUID, uuid4

from scraper.models import Product


@dataclass
class Job:
    job_id: UUID = field(default_factory=uuid4)
    status: str = "pending"
    progress: int = 0
    products: list[Product] = field(default_factory=list)
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[UUID, Job] = {}
        self._lock = Lock()

    def create(self) -> Job:
        job = Job()
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def get(self, job_id: UUID) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def update(self, job_id: UUID, **changes: object) -> None:
        with self._lock:
            job = self._jobs[job_id]
            for key, value in changes.items():
                setattr(job, key, value)
