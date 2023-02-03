"""added shopping list label settings

Revision ID: b04a08da2108
Revises: 167eb69066ad
Create Date: 2023-02-02 22:03:19.837244

"""
import sqlalchemy as sa

import mealie.db.migration_types
from alembic import op

# revision identifiers, used by Alembic.
revision = "b04a08da2108"
down_revision = "167eb69066ad"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "shopping_lists_multi_purpose_labels",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("update_at", sa.DateTime(), nullable=True),
        sa.Column("id", mealie.db.migration_types.GUID(), nullable=False),
        sa.Column("shopping_list_id", mealie.db.migration_types.GUID(), nullable=False),
        sa.Column("label_id", mealie.db.migration_types.GUID(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["label_id"],
            ["multi_purpose_labels.id"],
        ),
        sa.ForeignKeyConstraint(
            ["shopping_list_id"],
            ["shopping_lists.id"],
        ),
        sa.PrimaryKeyConstraint("id", "shopping_list_id", "label_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shopping_lists_multi_purpose_labels")
    # ### end Alembic commands ###
