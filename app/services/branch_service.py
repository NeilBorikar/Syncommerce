from app.repositories.branch_repository import BranchRepository
from app.utils.logger import logger

class BranchService:
    def __init__(self, db):
        self.repo = BranchRepository(db)

    def create_branch(self, data: dict):
        branch = self.repo.create(data)
        logger.info(f"Branch created: {branch['id']}")
        return branch

    def get_by_business(self, business_id: str):
        return self.repo.get_by_business(business_id)

    def update_branch(self, branch_id: str, data: dict):
        return self.repo.update(branch_id, data)
