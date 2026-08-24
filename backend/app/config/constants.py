from enum import Enum

class RoleName(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    SALES_ANALYST = "SALES_ANALYST"

class DatasetStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"

class ModelAlgorithm(str, Enum):
    PROPHET = "PROPHET"
    XGBOOST = "XGBOOST"
    ARIMA = "ARIMA"
    LSTM = "LSTM"
    ENSEMBLE = "ENSEMBLE"

class ModelStatus(str, Enum):
    TRAINING = "TRAINING"
    READY = "READY"
    FAILED = "FAILED"

class SubscriptionPlan(str, Enum):
    STARTER = "STARTER"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"

class IntegrationProvider(str, Enum):
    SALESFORCE = "SALESFORCE"
    HUBSPOT = "HUBSPOT"
    STRIPE = "STRIPE"
    WEBHOOK = "WEBHOOK"
