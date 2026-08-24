"""Initial Schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-07-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True),
        sa.Column('domain', sa.String(255), nullable=True),
        sa.Column('settings_json', sa.JSON(), nullable=True),
    )

    # 2. Roles
    op.create_table(
        'roles',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('permissions_json', sa.JSON(), nullable=True),
    )

    # 3. Users
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('is_superuser', sa.Boolean(), default=False, nullable=False),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='SET NULL'), nullable=True),
        sa.Column('role_id', sa.String(36), sa.ForeignKey('roles.id', ondelete='SET NULL'), nullable=True),
    )

    # 4. Datasets
    op.create_table(
        'datasets',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(512), nullable=False),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=False),
        sa.Column('row_count', sa.Integer(), nullable=True),
        sa.Column('column_schema', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(50), default='PENDING', nullable=False),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('uploaded_by_id', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    # 5. MLModels
    op.create_table(
        'ml_models',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('algorithm', sa.String(50), nullable=False),
        sa.Column('hyperparameters', sa.JSON(), nullable=True),
        sa.Column('metrics', sa.JSON(), nullable=True),
        sa.Column('artifact_path', sa.String(512), nullable=True),
        sa.Column('status', sa.String(50), default='TRAINING', nullable=False),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('dataset_id', sa.String(36), sa.ForeignKey('datasets.id', ondelete='CASCADE'), nullable=False),
    )

    # 6. Forecasts
    op.create_table(
        'forecasts',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('horizon_days', sa.Integer(), nullable=False),
        sa.Column('confidence_interval', sa.Float(), default=0.95, nullable=False),
        sa.Column('forecast_data', sa.JSON(), nullable=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('model_id', sa.String(36), sa.ForeignKey('ml_models.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_by_id', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    # 7. Reports
    op.create_table(
        'reports',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('report_type', sa.String(50), nullable=False),
        sa.Column('file_path', sa.String(512), nullable=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('forecast_id', sa.String(36), sa.ForeignKey('forecasts.id', ondelete='CASCADE'), nullable=True),
    )

    # 8. Integrations
    op.create_table(
        'integrations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('provider', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), default='ACTIVE', nullable=False),
        sa.Column('config_json', sa.JSON(), nullable=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
    )

    # 9. Subscriptions
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('plan_name', sa.String(50), nullable=False),
        sa.Column('stripe_customer_id', sa.String(255), nullable=True),
        sa.Column('stripe_subscription_id', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), default='ACTIVE', nullable=False),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, unique=True),
    )

    # 10. Payments
    op.create_table(
        'payments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('amount_cents', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(10), default='USD', nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(255), nullable=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
    )

    # 11. AuditLogs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('payments')
    op.drop_table('subscriptions')
    op.drop_table('integrations')
    op.drop_table('reports')
    op.drop_table('forecasts')
    op.drop_table('ml_models')
    op.drop_table('datasets')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('organizations')
