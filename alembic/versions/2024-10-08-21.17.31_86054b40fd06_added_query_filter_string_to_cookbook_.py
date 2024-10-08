"""added query_filter_string to cookbook and mealplan

Revision ID: 86054b40fd06
Revises: 1fe4bd37ccc8
Create Date: 2024-10-08 21:17:31.601903

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "86054b40fd06"
down_revision: str | None = "1fe4bd37ccc8"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def migrate_cookbooks():
    pass  # TODO: convert old cookbook filters to query_filter_string


def migrate_mealplan_rules():
    pass  # TODO: convert old mealplan rule filters to query_filter_string


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("cookbooks", schema=None) as batch_op:
        batch_op.add_column(sa.Column("query_filter_string", sa.String(), nullable=False))

    with op.batch_alter_table("group_meal_plan_rules", schema=None) as batch_op:
        batch_op.add_column(sa.Column("query_filter_string", sa.String(), nullable=False))

    # ### end Alembic commands ###

    migrate_cookbooks()
    migrate_mealplan_rules()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("group_meal_plan_rules", schema=None) as batch_op:
        batch_op.drop_column("query_filter_string")

    with op.batch_alter_table("cookbooks", schema=None) as batch_op:
        batch_op.drop_column("query_filter_string")

    # ### end Alembic commands ###
