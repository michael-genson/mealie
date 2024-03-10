"""added user to shopping list

Revision ID: 2298bb460ffd
Revises: ba1e4a6cfe99
Create Date: 2024-02-23 16:15:07.115641

"""

from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import orm

import mealie.db.migration_types
from alembic import op

# revision identifiers, used by Alembic.
revision = "2298bb460ffd"
down_revision = "ba1e4a6cfe99"
branch_labels = None
depends_on = None


def is_postgres():
    return op.get_context().dialect.name == "postgresql"


def find_user_id_for_group(group_id: UUID):
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    if is_postgres():
        stmt = "SELECT id FROM users WHERE group_id=:group_id AND admin = TRUE LIMIT 1"
    else:
        stmt = "SELECT id FROM users WHERE group_id=:group_id AND admin = 1 LIMIT 1"

    with session:
        try:
            # try to find an admin user
            user_id = session.execute(sa.text(stmt).bindparams(group_id=group_id)).scalar_one()
        except orm.exc.NoResultFound:
            # fallback to any user
            user_id = session.execute(
                sa.text("SELECT id FROM users WHERE group_id=:group_id LIMIT 1").bindparams(group_id=group_id)
            ).scalar_one()
        return user_id


def populate_shopping_list_users():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    with session:
        list_ids_and_group_ids = session.execute(sa.text("SELECT id, group_id FROM shopping_lists")).all()
        for list_id, group_id in list_ids_and_group_ids:
            user_id = find_user_id_for_group(group_id)
            session.execute(
                sa.text(f"UPDATE shopping_lists SET user_id=:user_id WHERE id=:id").bindparams(
                    user_id=user_id, id=list_id
                )
            )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("shopping_lists") as batch_op:
        # allow nulls during migration
        batch_op.add_column(sa.Column("user_id", mealie.db.migration_types.GUID(), nullable=True))
        batch_op.create_index(op.f("ix_shopping_lists_user_id"), ["user_id"], unique=False)
        batch_op.create_foreign_key("fk_user_shopping_lists", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###

    populate_shopping_list_users()

    # forbid nulls after migration
    with op.batch_alter_table("shopping_lists") as batch_op:
        batch_op.alter_column("user_id", nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "shopping_lists", type_="foreignkey")
    op.drop_index(op.f("ix_shopping_lists_user_id"), table_name="shopping_lists")
    op.drop_column("shopping_lists", "user_id")
    # ### end Alembic commands ###
