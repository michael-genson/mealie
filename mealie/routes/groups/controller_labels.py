from functools import cached_property

from fastapi import APIRouter, Depends
from pydantic import UUID4

from mealie.routes._base.base_controllers import BaseUserController
from mealie.routes._base.controller import controller
from mealie.routes._base.mixins import HttpRepo
from mealie.routes._base.routers import MealieCrudRoute
from mealie.schema.group.group_shopping_list import ShoppingListMultiPurposeLabelCreate
from mealie.schema.labels import (
    MultiPurposeLabelCreate,
    MultiPurposeLabelOut,
    MultiPurposeLabelSave,
    MultiPurposeLabelSummary,
    MultiPurposeLabelUpdate,
)
from mealie.schema.labels.multi_purpose_label import MultiPurposeLabelPagination
from mealie.schema.mapper import cast
from mealie.schema.response.pagination import PaginationQuery

router = APIRouter(prefix="/groups/labels", tags=["Group: Multi Purpose Labels"], route_class=MealieCrudRoute)


@controller(router)
class MultiPurposeLabelsController(BaseUserController):
    @cached_property
    def repo(self):
        if not self.user:
            raise Exception("No user is logged in.")

        return self.repos.group_multi_purpose_labels.by_group(self.user.group_id)

    # =======================================================================
    # CRUD Operations

    @property
    def mixins(self) -> HttpRepo:
        return HttpRepo(self.repo, self.logger, self.registered_exceptions, self.t("generic.server-error"))

    @router.get("", response_model=MultiPurposeLabelPagination)
    def get_all(self, q: PaginationQuery = Depends(PaginationQuery)):
        response = self.repo.page_all(
            pagination=q,
            override=MultiPurposeLabelSummary,
        )

        response.set_pagination_guides(router.url_path_for("get_all"), q.dict())
        return response

    @router.post("", response_model=MultiPurposeLabelOut)
    def create_one(self, data: MultiPurposeLabelCreate):
        create_data = cast(data, MultiPurposeLabelSave, group_id=self.user.group_id)
        label: MultiPurposeLabelOut | None = self.mixins.create_one(create_data)  # type: ignore

        if not label:
            return

        # add label ref to shopping lists
        shopping_lists_repo = self.repos.group_shopping_lists.by_group(self.group_id)
        shopping_lists = shopping_lists_repo.page_all(PaginationQuery(page=1, per_page=-1))
        new_shopping_list_labels = [
            ShoppingListMultiPurposeLabelCreate(
                shopping_list_id=shopping_list.id, label_id=label.id, position=len(shopping_list.label_settings)
            )
            for shopping_list in shopping_lists.items
        ]

        self.repos.shopping_list_multi_purpose_labels.create_many(new_shopping_list_labels)
        return label

    @router.get("/{item_id}", response_model=MultiPurposeLabelOut)
    def get_one(self, item_id: UUID4):
        return self.repo.get_one(item_id)

    @router.put("/{item_id}", response_model=MultiPurposeLabelOut)
    def update_one(self, item_id: UUID4, data: MultiPurposeLabelUpdate):
        return self.mixins.update_one(data, item_id)

    @router.delete("/{item_id}", response_model=MultiPurposeLabelOut)
    def delete_one(self, item_id: UUID4):
        return self.mixins.delete_one(item_id)  # type: ignore
