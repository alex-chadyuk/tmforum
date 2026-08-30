from __future__ import annotations
from dataclasses import dataclass, fields, field
from datetime import datetime, timezone
from typing import Any, Optional, List, get_type_hints, get_origin, get_args, Union
import sys, json, requests, enum
import dataclasses
import logging
from ._helpers import parse_response

__version__ = "0.9.0"


@dataclass
class Context:
    """Encapsulates details such as authorization and token-related URLs,
    client credentials, and the base URL for API calls.

    It also carries a logger
    instance for consistent logging across the application, defaulting to a stream
    handler if none is provided. The headers are used
    to manage request parameters in an API environment.

    Attributes:
        authorization_base_url (Optional[str]): The base URL for initiating OAuth
            authorization flows, if applicable.
        token_url (Optional[str]): The endpoint URL for exchanging authorization
            codes or credentials for an access token.
        token_name (Optional[str]): The name or key under which the token is stored.
        redirect_uri (Optional[str]): The URI to which the authorization server
            redirects after a successful authentication.
        client_id (Optional[str]): The client identifier used in OAuth flows.
        scope (Optional[str]): The scopes requested for authorization.
        access_token (Optional[str]): The bearer access token used for authenticated
            API requests.
        api_base_url (Optional[str]): The base URL for TM Forum API calls.
        logger (Optional[logging.Logger]): A logger instance for capturing logs.
            If not provided, a default logger named "tmforum" is instantiated
            with a stream handler.
        operator_name (Optional[str]): Optional tenant identifier header used by multi-tenant deployments.
        headers (Optional[dict]): A dictionary of default HTTP headers to include
            in API requests, if any.
        currency_code (str): Default currency code used for monetary values
            (default "USD").
    """

    authorization_base_url: Optional[str] = None
    token_url: Optional[str] = None
    token_name: Optional[str] = None
    redirect_uri: Optional[str] = None
    client_id: Optional[str] = None
    scope: Optional[str] = None
    access_token: Optional[str] = None
    api_base_url: Optional[str] = None
    logger: Optional[logging.Logger] = None
    operator_name: Optional[str] = None
    headers: Optional[dict] = None
    currency_code: str = "USD"

    def __post_init__(self):
        if self.logger is None:
            self.logger = logging.getLogger("tmforum")
            self.logger.setLevel(logging.DEBUG)

            if not self.logger.handlers:
                handler = logging.StreamHandler()
                handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)


class BaseCRUDMixin:
    """A mixin that provides basic Create, Read, Update, and Delete (CRUD) operations
    on TM Forum-compliant APIs.

    This mixin assumes that the subclass:
    - Implements a `get_resource_path(context: Context) -> str` class method that returns
      the API endpoint for the resource.
    - Inherits from an `Entity` class that provides `from_dict()` and `to_json()` methods.

    Usage:
        class MyEntity(Entity, BaseCRUDMixin):
            @classmethod
            def get_resource_path(cls, context: Context) -> str:
                return f"{context.api_base_url}/myEntity"

        entity = MyEntity(...)
        entity = entity.create(context)      # Create
        entity = entity.read(context)        # Read
        entity = entity.update({...}, context)  # Update
        entity.delete(context)               # Delete
    """

    @classmethod
    def from_id(cls, id: str, context: Context):
        """Retrieve an entity by its id, returning an instance of the class if found,
        otherwise None.
        """
        url = f"{cls.get_resource_path(context)}/{id}"
        response = requests.request("GET", url, headers=context.headers, data={})
        item = parse_response(response, context)
        if item.get("id"):
            return cls.from_dict(item)
        return None

    @classmethod
    def get_raw(cls, id: str, context: Context):
        """Retrieve raw dictionary data of an entity by its id without converting it
        into an object.
        """
        url = f"{cls.get_resource_path(context)}/{id}"
        response = requests.request("GET", url, headers=context.headers, data={})
        return parse_response(response, context)

    @classmethod
    def query_get(cls, path: str, context: Context):
        if path:
            url = f"{cls.get_resource_path(context)}?{path}"
        else:
            url = f"{cls.get_resource_path(context)}"
        response = requests.request("GET", url, headers=context.headers, data={})
        items = parse_response(response, context)
        entities = []
        try:
            for item in items:
                entities.append(cls.from_dict(item))
            return entities
        except Exception:
            return items

    @classmethod
    def make_get_all_curl(cls, context: Context):
        url = f"{cls.get_resource_path(context)}"
        return f"curl -X GET '{url}' -H 'Authorization: Bearer {context.access_token}' -H 'operator-name: {context.operator_name}'"

    def create(self, context: Context):
        """Create the current Entity (as defined by its fields) in the backend, returning
        a new instance with updated fields (e.g., assigned id).
        """
        url = f"{self.get_resource_path(context)}"
        payload = self.to_json()
        context.logger.debug(f"POST {url} - {payload}")
        response = requests.request("POST", url, headers=context.headers, data=payload)
        item = parse_response(response, context)
        return self.__class__.from_dict(item)

    def read(self, context: Context):
        """Refresh the current Entity instance by re-fetching its data from the backend using the
        entity's id.

        If the entity does not have an id, logs an error and returns the entity unchanged.
        """
        if not self.id:
            context.logger.error(
                f"{self.__class__.__name__}.id is undefined. Please check the {self.__class__.__name__} has been created."
            )
            return self
        url = f"{self.get_resource_path(context)}/{self.id}"
        response = requests.request("GET", url, headers=context.headers, data={})
        item = parse_response(response, context)
        if item.get("id"):
            return self.__class__.from_dict(item)
        return self

    def make_get_curl(self, context: Context):
        url = f"{self.get_resource_path(context)}/{self.id}"
        return f"curl -X GET '{url}' -H 'Authorization: Bearer {context.access_token}' -H 'operator-name: {context.operator_name}'"

    def update(
        self,
        payload: Union[dict, list],
        context: Context,
        custom_headers: dict = {},
    ):
        """Partially update the entity with the given payload.

        Sends a PATCH request to the backend and returns the updated entity.
        Pass additional headers in the custom_headers argument.
        """
        if not self.id:
            context.logger.error(
                f"{self.__class__.__name__}.id is undefined. Please check the {self.__class__.__name__} has been created."
            )
            return self
        url = f"{self.get_resource_path(context)}/{self.id}"
        context.logger.debug(f"PATCH {url} - {json.dumps(payload)}")
        response = requests.request(
            "PATCH",
            url,
            headers={**context.headers, **custom_headers},
            data=json.dumps(payload),
        )
        item = parse_response(response, context)
        if item.get("id"):
            return self.__class__.from_dict(item)
        return self

    def query_update(self, payload: Union[dict, list], context: Context):
        base_content_type = context.headers["Content-Type"]
        context.headers["Content-Type"] = "application/json-patch-query+json"
        entity = self.update(payload, context)
        context.headers["Content-Type"] = base_content_type
        return entity

    def delete(self, context: Context):
        """Delete the entity from the backend using its id.

        Logs an error if the entity lacks an id. Returns the backend's response.
        """
        if not self.id:
            context.logger.error(
                f"Cannot delete. {self.__class__.__name__}.id is undefined."
            )
            return self
        url = f"{self.get_resource_path(context)}/{self.id}"
        context.logger.info(f"Deleting {self.__class__.__name__} with id {self.id}")
        response = requests.request("DELETE", url, headers=context.headers, data={})
        item = parse_response(response, context)
        if response.status_code == 400:
            url = f"{self.get_resource_path(context)}/{self.id}?version={self.version}"
            response = requests.request("DELETE", url, headers=context.headers, data={})
            item = parse_response(response, context)
        return item


class Entity:
    """A base class representing a TM Forum-compliant entity with serialization and deserialization capabilities.

    This class expects subclasses to:
    - Define their fields using Python dataclasses.
    - Optionally handle post-initialization logic in `__post_init__`.
    - Leverage `from_dict()` and `to_dict()` for consistent serialization and deserialization.

    Usage:
        @dataclass(repr=False)
        class Product(Entity):
            name: str
             ... other fields ...

    Deserialize from dictionary
        product = Product.from_dict(product_data)

    Serialize to JSON
        json_str = product.to_json()
    """

    @classmethod
    def from_dict(cls, data):
        """Converts a dictionary of data, including nested dictionaries and lists,
        into an instance of the entity class.

        The method uses Python type hints to determine which classes
        to instantiate for nested data and can also utilize '@type' fields to pick the correct class.
        """

        module_dict = sys.modules[__name__].__dict__
        if isinstance(data, dict) and (type_name := data.get("@type")):
            cls_candidate = module_dict.get(type_name)
            if (
                cls_candidate
                and isinstance(cls_candidate, type)
                and issubclass(cls_candidate, Entity)
                and issubclass(cls_candidate, cls)
            ):
                cls = cls_candidate

        field_values = {}
        cls_fields = fields(cls)
        type_hints = get_type_hints(cls)

        for field in cls_fields:
            field_name = field.name
            field_type = type_hints[field_name]

            if field_name in data:
                value = data[field_name]

                if getattr(field_type, "__origin__", None) is Union:
                    union_of_types = field_type.__args__
                else:
                    union_of_types = ()

                if field_type is Any:
                    pass
                elif isinstance(value, dict):
                    if type_name := value.get("@type"):
                        cls_candidate = module_dict.get(type_name)
                        if (
                            cls_candidate
                            and isinstance(cls_candidate, type)
                            and issubclass(cls_candidate, Entity)
                        ):
                            value = cls_candidate.from_dict(value)
                    elif (
                        field_type
                        and isinstance(field_type, type)
                        and issubclass(field_type, Entity)
                    ):
                        try:
                            value = field_type.from_dict(value)
                        except ValueError:
                            pass
                    else:
                        for fallback_type in union_of_types:
                            if isinstance(fallback_type, type) and issubclass(
                                fallback_type, Entity
                            ):
                                try:
                                    value = fallback_type.from_dict(value)
                                except ValueError:
                                    pass

                elif isinstance(value, list):
                    if union_of_types:
                        item_type = field_type.__args__[0].__args__[0]
                    else:
                        item_type = field_type.__args__[0]

                    if getattr(item_type, "__origin__", None) is Union:
                        item_types = item_type.__args__
                        for member in item_types:
                            if isinstance(member, type) and issubclass(member, Entity):
                                item_type = member
                                break
                    else:
                        item_types = ()

                    if isinstance(item_type, type) and issubclass(item_type, Entity):
                        new_list = []
                        for item in value:
                            if isinstance(item, dict):
                                if type_name := item.get("@type"):
                                    cls_candidate = module_dict.get(type_name)
                                    if (
                                        cls_candidate
                                        and isinstance(cls_candidate, type)
                                        and issubclass(cls_candidate, Entity)
                                    ):
                                        instantiated_item = cls_candidate.from_dict(
                                            item
                                        )
                                elif item_types:
                                    for fallback_type in item_types:
                                        if isinstance(
                                            fallback_type, type
                                        ) and issubclass(fallback_type, Entity):
                                            try:
                                                instantiated_item = (
                                                    fallback_type.from_dict(item)
                                                )
                                            except Exception:
                                                pass
                                else:
                                    instantiated_item = item_type.from_dict(item)
                                try:
                                    new_list.append(instantiated_item)
                                except UnboundLocalError as e:
                                    print(f"WARNING!  Unknown entity type {type_name}")

                            else:
                                new_list.append(item)
                        value = new_list

                elif value:
                    if isinstance(field_type, type) and issubclass(
                        field_type, enum.Enum
                    ):
                        try:
                            value = field_type(value)
                        except ValueError:
                            pass

                    for fallback_type in union_of_types:
                        if isinstance(fallback_type, type) and issubclass(
                            fallback_type, enum.Enum
                        ):
                            try:
                                value = fallback_type(value)
                            except ValueError:
                                pass

                field_values[field_name] = value
            else:
                if field_name == "_referred_type":
                    if ref_type := data.get("@referredType"):
                        field_values[field_name] = ref_type
                elif field.default is not dataclasses.MISSING:
                    field_values[field_name] = field.default
                elif field.default_factory is not dataclasses.MISSING:
                    field_values[field_name] = field.default_factory()
                else:
                    field_values[field_name] = None

        return cls(**field_values)

    def to_dict(self):
        """Converts the entity (and any nested entities) back into a dictionary suitable for
        serialization.
        """
        representation = {}
        if hasattr(self, "_type"):
            representation["@type"] = self._type
        else:
            representation["@type"] = self.__class__.__name__
        if self.__class__.__base__.__name__ not in [
            "Entity",
            "EntityRef",
            "PolicyManagedEntity",
        ]:
            representation["@baseType"] = self.__class__.__base__.__name__

        for field in fields(self):
            field_name = field.name
            value = getattr(self, field_name)

            if value is None or (isinstance(value, list) and not value):
                continue

            if field_name == "_referred_type":
                representation["@referredType"] = value
                continue

            if field_name == "_schema_location":
                representation["@schemaLocation"] = value
                continue

            if field_name == "_target_product_order_item_schema":
                representation["@targetProductOrderItemSchema"] = value
                continue

            if field_name == "_type":
                continue

            if isinstance(value, Entity):
                representation[field_name] = value.to_dict()
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, Entity):
                        new_list.append(item.to_dict())
                    else:
                        new_list.append(item)
                representation[field_name] = new_list
            elif isinstance(value, enum.Enum):
                representation[field_name] = value.value
            else:
                representation[field_name] = value

        return representation

    def to_json(self):
        """Converts the entity into a JSON-formatted string."""
        return json.dumps(self.to_dict())

    def __repr__(self):
        """Returns the JSON representation of the entity, making debugging easier."""
        return self.to_json()

    def __post_init__(self):
        hints = get_type_hints(self.__class__)
        for field_info in dataclasses.fields(self):
            field_name = field_info.name
            field_value = getattr(self, field_name)
            declared_type = hints[field_name]

            if not field_value:
                continue

            origin = get_origin(declared_type)
            args = get_args(declared_type)

            is_list_type = False
            if origin is list:
                # e.g., List[ProductTerm]
                is_list_type = True
            elif origin is Union:
                # e.g., Union[List[ProductTerm], NoneType]
                for a in args:
                    if get_origin(a) is list:
                        is_list_type = True
                        break

            if is_list_type and not isinstance(field_value, list):
                raise ValueError(
                    f"Field '{field_name}' is declared as a list but got type '{type(field_value).__name__}' instead."
                )


@dataclass(repr=False)
class EntityRef(Entity):
    id: Optional[str] = None
    name: Optional[str] = None
    href: Optional[str] = None
    # version: Optional[str] = None
    _referred_type: Optional[str] = None

    @classmethod
    def from_entity(
        cls, entity: Entity, alt_ref_type: Optional[str] = None
    ) -> EntityRef:
        entity_class_name = entity.__class__.__name__
        ref_kwargs = {
            "id": entity.id,
            "name": getattr(entity, "name", None),
            "href": getattr(entity, "href", None),
            "_referred_type": (alt_ref_type or entity_class_name),
        }
        if (
            hasattr(entity, "version")
            and "version" in getattr(cls, "__dataclass_fields__", {})
            and (version := getattr(entity, "version", None))
        ):
            ref_kwargs["version"] = version
        ref = cls(**ref_kwargs)
        return ref


#########
#
# ENUMS
#
#########


@enum.unique
class AccountRelationshipType(enum.Enum):
    PARENT_ACCOUNT = "parentAccount"
    CHILD_ACCOUNT = "childAccount"
    FINANCIAL_ACCOUNT = "financialAccount"
    BILLING_ACCOUNT = "billingAccount"


@enum.unique
class AccountState(enum.Enum):
    CREATED = "created"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


@enum.unique
class AccountType(enum.Enum):
    BUSINESS = "business"
    INDIVIDUAL = "individual"
    TAX_EXEMPTED = "taxExempted"
    GOVERNMENT = "government"


@enum.unique
class AppliedCustomerBillingRateType(enum.Enum):
    PRODUCT_RECURRING_CHARGE = "appliedBillingChargeProductRecurringCharge"
    ONE_TIME_CHARGE = "appliedBillingChargeProductOneTimeCharge"
    BILLING_DISCOUNT = "appliedBillingCreditBillingDiscount"
    CREDIT_ADJUSTMENT = "appliedBillingChargeCreditAdjustment"
    DEBIT_ADJUSTMENT = "appliedBillingChargeDebitAdjustment"
    PENALTY_FEE = "appliedBillingChargePenaltyFee"


@enum.unique
class BalanceType(enum.Enum):
    DEPOSIT_BALANCE = "depositBalance"
    RECEIVABLE_BALANCE = "receivableBalance"
    PAYABLE_BALANCE = "payableBalance"
    LOYALTY_BALANCE = "loyaltyBalance"


@enum.unique
class BillingCycleSpecification_BillingPeriod(enum.Enum):
    BI_WEEKLY = "biWeekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semiAnnually"
    ANNUALLY = "annually"


@enum.unique
class BillingCycleSpecification_Frequency(enum.Enum):
    BI_WEEKLY = "biWeekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semiAnnually"
    ANNUALLY = "annually"


@enum.unique
class BillFormatBasePresentationType(enum.Enum):
    PRINT = "print"
    RENDERED = "rendered"
    PLAIN = "plain"


@enum.unique
class BundledProductOfferingPriceRelationshipTypeEnum(enum.Enum):
    NULLIFY = "nullify"
    COMPOSED_OF = "composedOf"


@enum.unique
class CatalogSubType(enum.Enum):
    TECHNICAL = "Technical"
    COMMERCIAL = "Commercial"


@enum.unique
class CategoryLifecycleStatusType(enum.Enum):
    IN_DRAFT = "inDraft"
    ACTIVE = "active"
    RETIRED = "retired"


@enum.unique
class CategoryType(enum.Enum):
    TECHNICAL = "Technical"
    COMMERCIAL = "Commercial"


@enum.unique
class CapacityStatus(enum.Enum):
    PLANNED = "planned"
    ACTUAL = "actual"


@enum.unique
class CharacteristicValueSpecificationRelationshipType(enum.Enum):
    MAPS = "maps"


@enum.unique
class ContactType(enum.Enum):
    BILLING_ADDRESS = "billingAddress"
    PROFESSIONAL = "professional"
    PERSONAL = "personal"
    OTHER = "other"


@enum.unique
class ChargeType(enum.Enum):
    IN_ARREAR = "inArrear"
    IN_ADVANCE = "inAdvance"
    PREPAID = "prepaid"


@enum.unique
class CheckProductConfigurationItemState(enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"


@enum.unique
class CommercialRelationshipTypeEnum(enum.Enum):
    UPGRADE_TO = "upgradeTo"
    DOWNGRADE_TO = "downgradeTo"
    ADD_ON_BY = "addOnBy"
    ADD_ON_OF = "addOnOf"
    CROSS_SELL_BY = "crossSellBy"


@enum.unique
class ConnectionAssociationType(enum.Enum):
    POINT_TO_POINT = "pointtoPoint"
    POINT_TO_MULTIPOINT = "pointtoMultipoint"


@enum.unique
class EntryType(enum.Enum):
    POST_CLOSURE = "postClosure"
    FULFILMENT = "fulfilment"
    POST_ACTIVATION = "postActivation"
    POST_COMMIT = "postCommit"


@enum.unique
class ExecutedAtEnum(enum.Enum):
    BEFORE_ALL = "beforeAll"
    BEFORE_POLICY = "beforePolicy"
    ON_PERMIT = "onPermit"
    ON_DENY = "onDeny"
    ON_INDETERMINATE = "onIndeterminate"
    ON_RESOLVED = "onResolved"
    ALWAYS = "always"
    AFTER_ALL = "afterAll"


@enum.unique
class IndividualStateType(enum.Enum):
    INITIALIZED = "initialized"
    VALIDATED = "validated"
    DECEASED = "deceased"


@enum.unique
class InitialProductOrderStateType(enum.Enum):
    ACKNOWLEDGED = "acknowledged"
    DRAFT = "draft"


@enum.unique
class JobStateType(enum.Enum):
    NOT_STARTED = "Not Started"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"


@enum.unique
class ItemActionType(enum.Enum):
    ADD = "add"
    MODIFY = "modify"
    NO_CHANGE = "noChange"
    DELETE = "delete"


@enum.unique
class LifecycleStatus(enum.Enum):
    IN_DRAFT = "inDraft"
    ACTIVE = "active"
    RETIRED = "retired"
    LAUNCHED = "launched"
    IN_TEST = "inTest"
    OBSOLETE = "obsolete"


@enum.unique
class NameType(enum.Enum):
    SHORT_NAME = "shortName"


@enum.unique
class NoteTypeEnum(enum.Enum):
    EMAIL = "Email"
    CALL = "Call"
    MEETING = "Meeting"
    OFFLINE_ACTIVITY = "Offline Activity"
    SOCIAL_MEDIA = "Social Media"
    OTHERS = "Others"


@enum.unique
class OneTimeFeeAppliesOnEnum(enum.Enum):
    ITEM = "item"
    QUANTITY = "quantity"


@enum.unique
class OrderFailurePolicy(enum.Enum):
    HALT_AND_ROLLBACK = "HaltAndRollback"
    HALT = "Halt"
    CONTINUE = "Continue"


@enum.unique
class OrderItemActionType(enum.Enum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"
    NO_CHANGE = "noChange"


@enum.unique
class OrderSequencingPolicy(enum.Enum):
    PARALLEL = "Parallel"
    SEQUENTIAL = "Sequential"
    ANY = "Any"


@enum.unique
class OrganizationStateType(enum.Enum):
    VALIDATED = "validated"
    INITIALIZED = "initialized"
    CLOSED = "closed"


@enum.unique
class OrganizationType(enum.Enum):
    COMPANY = "company"
    DEPARTMENT = "department"
    FOR_PROFIT_ORGANIZATION = "forProfitOrganisation"


@enum.unique
class PaymentStatus(enum.Enum):
    DUE = "due"
    PAID = "paid"
    OVERDUE = "overdue"


@enum.unique
class ProductCatalogLifecycleStatusType(enum.Enum):
    IN_DRAFT = "inDraft"
    ACTIVE = "active"
    RETIRED = "retired"


@enum.unique
class PolicyActionType(enum.Enum):
    RETURN_STATIC = "returnStatic"


@enum.unique
class PolicyCombiningAlgorithm(enum.Enum):
    DENY_OVERRIDES = "denyOverrides"
    PERMIT_OVERRIDES = "permitOverrides"
    FIRST_APPLICABLE = "firstApplicable"
    ONLY_ONE_APPLICABLE = "onlyOneApplicable"
    DENY_UNLESS_PERMIT = "denyUnlessPermit"
    PERMIT_UNLESS_DENY = "permitUnlessDeny"


@enum.unique
class PolicyConditionCombinationType(enum.Enum):
    ANY_OF = "anyOf"
    ALL_OF = "allOf"
    ONE_OF = "oneOf"
    NONE = "none"


@enum.unique
class PolicyConditionType(enum.Enum):
    SEGMENT_WHITELIST = "segmentWhitelist"
    SEGMENT_BLACKLIST = "segmentBlacklist"
    TENURE = "tenure"
    COUNT_ACTIVE = "countActive"
    COUNT_PURCHASE = "countPurchase"
    RELATIONSHIP_WHITELIST_ACTIVE = "relationshipWhitelistActive"
    RELATIONSHIP_WHITELIST_PURCHASE = "relationshipWhitelistPurchase"
    RELATIONSHIP_BLACKLIST_ACTIVE = "relationshipBlacklistActive"
    CUSTOM_ATTRIBUTE = "customAttribute"
    INPUT_EVALUATION = "inputEvaluation"


@enum.unique
class PolicyEntityLifecycleState(enum.Enum):
    IN_DESIGN = "inDesign"
    DESIGNED = "designed"
    ACTIVE = "active"
    RETIRED = "retired"
    REJECTED = "rejected"


@enum.unique
class PolicyExecutionStrategy(enum.Enum):
    DO_UNTIL_SUCCESS = "doUntilSuccess"
    DO_ALL = "doAll"
    DO_UNTIL_FAILURE = "doUntilFailure"
    DO_ALL_WITHOUT_FAILURE_OR_NOTHING = "doAllWithoutFailureOrDoNothing"


@enum.unique
class PolicyEffect(enum.Enum):
    PERMIT = "permit"
    DENY = "deny"


@enum.unique
class PolicySequenceType(enum.Enum):
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    BEST_EFFORT = "bestEffort"


@enum.unique
class PolicyVariableValueType(enum.Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"


@enum.unique
class PopRelationshipTypeEnum(enum.Enum):
    DISCOUNTS = "discounts"
    OVERRIDES = "overrides"
    MARKUP = "markup"
    DISCOUNT = "discount"
    APPLIES_TO = "appliesTo"


@enum.unique
class PriceBreakdownDetail(enum.Enum):
    SUMMARIZED_SINGLE_PRICE = "summarizedSinglePrice"
    DISCOUNT_SEPARATE_PRICE = "discountSeparatePrice"


@enum.unique
class PriceIntervalType(enum.Enum):
    CLOSED = "closed"
    CLOSED_BOTTOM = "closedBottom"
    CLOSED_TOP = "closedTop"


@enum.unique
class PriceType(enum.Enum):
    RECURRING_CHARGE = "recurringCharge"
    ONE_TIME_CHARGE = "oneTimeCharge"
    PRICE_ALTERATION = "priceAlteration"
    MARKUP = "markup"
    DISCOUNT = "discount"


@enum.unique
class PriorityType(enum.Enum):
    LOW = "low"
    LOWEST = "lowest"
    MEDIUM = "medium"
    HIGH = "high"
    TOP = "top"


@enum.unique
class ProductActionType(enum.Enum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"
    NO_CHANGE = "noChange"


@enum.unique
class ProductOfferingPriceAlterationTypeEnum(enum.Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    PERCENTAGE_RANGE = "percentageRange"
    AMOUNT_RANGE = "amountRange"
    MANUAL_OVERRIDE = "manualOverride"


@enum.unique
class ProductOrderItemRelationshipType(enum.Enum):
    MIGRATES_TO = "migratesTo"
    BUNDLES = "bundles"
    BUNDLED_BY = "bundledBy"
    RELIES_ON = "reliesOn"
    ENABLES = "enables"
    REQUIRES = "requires"
    DEPENDS_ON = "dependsOn"
    BRINGS = "brings"
    SUBSTITUTED_BY = "substitutedBy"
    ADD_ON_BY = "addOnBy"
    CROSS_SELL_BY = "crossSellBy"
    UPGRADE_TO = "upgradeTo"
    DOWNGRADE_TO = "downgradeTo"
    IS_BUNDLE_OF = "isBundleOf"
    IS_BUNDLED_BY = "isBundledBy"


@enum.unique
class ProductOrderItemStateType(enum.Enum):
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "inProgress"
    REJECTED = "rejected"
    HELD = "held"
    ASSESSING_CANCELLATION = "assessingCancellation"
    PENDING_CANCELLATION = "pendingCancellation"
    PENDING = "pending"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
    SUBMITTED = "submitted"
    DRAFT = "draft"
    WAITING_FOR_RESPONSE = "waitingForResponse"
    QUEUED = "queued"


@enum.unique
class ProductOrderStateType(enum.Enum):
    ACKNOWLEDGED = "acknowledged"
    REJECTED = "rejected"
    PENDING = "pending"
    HELD = "held"
    IN_PROGRESS = "inProgress"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
    ASSESSING_CANCELLATION = "assessingCancellation"
    PENDING_CANCELLATION = "pendingCancellation"
    DRAFT = "draft"
    IN_PROGRESS_ACCEPTED = "inProgressAccepted"
    QUEUED = "queued"


@enum.unique
class ProductRelationshipType(enum.Enum):
    MIGRATES_TO = "migratesTo"
    BUNDLES = "bundles"
    BUNDLED_BY = "bundledBy"
    RELIES_ON = "reliesOn"
    ENABLES = "enables"
    REQUIRES = "requires"
    DEPENDS_ON = "dependsOn"
    BRINGS = "brings"
    SUBSTITUTED_BY = "substitutedBy"
    ADD_ON_BY = "addOnBy"
    CROSS_SELL_BY = "crossSellBy"
    UPGRADE_TO = "upgradeTo"
    DOWNGRADE_TO = "downgradeTo"
    IS_BUNDLE_OF = "isBundleOf"
    IS_BUNDLED_BY = "isBundledBy"
    TARGETS = "targets"
    ADD_ON_OF = "addOnOf"


@enum.unique
class ProductSpecificationLifecycleStatusType(enum.Enum):
    IN_DRAFT = "inDraft"
    ACTIVE = "active"
    RETIRED = "retired"
    IN_STUDY = "inStudy"
    IN_DESIGN = "inDesign"
    IN_TEST = "inTest"
    LAUNCHED = "launched"
    OBSOLETE = "obsolete"
    REJECTED = "rejected"


@enum.unique
class ProductStatusType(enum.Enum):
    CREATED = "created"
    PENDING_ACTIVE = "pendingActive"
    CANCELLED = "cancelled"
    ACTIVE = "active"
    PENDING_TERMINATE = "pendingTerminate"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"
    ABORTED = "aborted"


@enum.unique
class ProviderType(enum.Enum):
    EXTERNAL = "External"
    INTERNAL = "Internal"


@enum.unique
class QualificationItemResultEnumType(enum.Enum):
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"


@enum.unique
class QuoteStateTypeEnum(enum.Enum):
    IN_PROGRESS = "inProgress"
    SUBMITTED_FOR_INTERNAL_APPROVAL = "submittedForInternalApproval"
    SENT_TO_CUSTOMER = "sentToCustomer"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "canceled"
    ACCEPTED = "accepted"
    INTERNAL_REVISION_REQUESTED = "internalRevisionRequested"
    EXTERNAL_REVISION_REQUESTED = "externalRevisionRequested"


@enum.unique
class RatingType(enum.Enum):
    PREPAID = "prepaid"
    POSTPAID = "postpaid"
    HYBRID = "hybrid"


@enum.unique
class RecurringChargePeriod(enum.Enum):
    DAILY = "daily"
    BI_WEEKLY = "biWeekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semiAnnually"
    YEARLY = "yearly"

    def to_quantity(self) -> Quantity:
        """
        Converts this RecurringChargePeriod into a Quantity with
        appropriate units and amount. For example, MONTHLY -> (units="month", amount=1).
        """
        if self == RecurringChargePeriod.DAILY:
            return Quantity(units="day", amount=1)
        elif self == RecurringChargePeriod.MONTHLY:
            return Quantity(units="month", amount=1)
        elif self == RecurringChargePeriod.QUARTERLY:
            return Quantity(units="month", amount=3)
        elif self == RecurringChargePeriod.SEMI_ANNUALLY:
            return Quantity(units="month", amount=6)
        elif self == RecurringChargePeriod.YEARLY:
            return Quantity(units="year", amount=1)
        return Quantity(units="unknown", amount=0)

    def to_duration(self) -> Duration:
        """
        Converts this RecurringChargePeriod into a Duration with
        appropriate units and amount. For example, MONTHLY -> (units="month", amount=1).
        """
        if self == RecurringChargePeriod.DAILY:
            return Duration(units="day", amount=1)
        elif self == RecurringChargePeriod.MONTHLY:
            return Duration(units="month", amount=1)
        elif self == RecurringChargePeriod.QUARTERLY:
            return Duration(units="month", amount=3)
        elif self == RecurringChargePeriod.SEMI_ANNUALLY:
            return Duration(units="month", amount=6)
        elif self == RecurringChargePeriod.YEARLY:
            return Duration(units="year", amount=1)
        return Duration(units="unknown", amount=0)


@enum.unique
class RelationshipTypeEnum(enum.Enum):
    HIERARCHICAL = "hierarchical"
    GEOGRAPHICAL = "geographical"


@enum.unique
class RenewalAction(enum.Enum):
    AUTO_RENEW = "autoRenew"
    MANUAL_REPURCHASE = "manualRepurchase"
    EXPIRE_AND_NO_ACTION = "expireAndNoAction"


@enum.unique
class RoleEnum(enum.Enum):
    ORDER_MANAGER = "orderManager"
    QUOTE_OR_ORDER_APPROVER = "quoteOrOrderApprover"
    CUSTOMER = "customer"
    DEALER = "dealer"
    CUSTOMER_CONTACT_PERSON = "customerContactPerson"
    BACKOFFICE_AGENT = "backofficeAgent"
    BILLING_AGENT = "billingAgent"
    PAYMENT_AGENT = "paymentAgent"
    PRODUCT_MANAGER = "productManager"
    ACCOUNT_MANAGER = "accountManager"
    APPLICATION_OWNER = "applicationOwner"
    SUPPLIER = "supplier"
    SUBSIDIARY = "subsidiary"
    APPROVER = "approver"
    OWNER = "owner"
    PROCUREMENT_RESPONSIBLE = "procurementResponsible"
    PAYMENT_RESPONSIBLE = "paymentResponsible"
    BILLING_RESPONSIBLE = "billingResponsible"
    CUSTOMER_SIGNATORY = "customerSignatory"
    FAMILY_MEMBER = "familyMember"
    AUTHORIZED_ADMIN = "authorizedAdmin"
    LEGAL_GUARDIAN = "legalGuardian"
    PARENT_OF = "parentOf"
    SPOUSE_OF = "spouseOf"
    VENDOR = "vendor"
    VENDOR_CONTACT_PERSON = "vendorContactPerson"
    BILLING_MANAGER = "billingManager"
    BILLING_QA_TEAM_MEMBER = "billingQaTeamMember"
    QUOTE_APPROVER = "quoteApprover"
    PAYMENT_MANAGEMENT_TEAM_MEMBER = "paymentManagementTeamMember"
    PRODUCT_ORDER_MANAGEMENT_TEAM_MEMBER = "productOrderManagementTeamMember"
    CUSTOMER_CARE_L1_TEAM_MEMBER = "customerCareL1TeamMember"
    CUSTOMER_CARE_L2_TEAM_MEMBER = "customerCareL2TeamMember"
    CUSTOMER_CARE_L3_TEAM_MEMBER = "customerCareL3TeamMember"
    BILLING_SUPPORT_BACK_OFFICE_TEAM_MEMBER = "billingSupportBackOfficeTeamMember"
    SALES_AGENT = "salesAgent"
    MARKETING_TEAM_MEMBER = "marketingTeamMember"
    CAMPAIGN_TEAM_MEMBER = "campaignTeamMember"
    PRIMARY_CONTACT_PERSON = "primaryContactPerson"
    SECONDARY_CONTACT_PERSON = "secondaryContactPerson"
    CHANNEL_PARTNER = "ChannelPartner"
    COMMUNICATION_SERVICE_PROVIDER = "communicationServiceProvider"
    OPERATE_API_ADMIN = "operateApiAdmin"
    OPERATE_API_EDITOR = "operateApiEditor"
    OPERATE_API_VIEWER = "operateApiViewer"
    PROSPECT = "prospect"


@enum.unique
class ResourceAdministrativeStateType(enum.Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    SHUTDOWN = "shutdown"


@enum.unique
class ResourceGraphSpecificationRelationshipType(enum.Enum):
    ADJACENCY = "adjacency"
    CONNECTIVITY = "connectivity"


@enum.unique
class ResourceOperationalStateType(enum.Enum):
    ENABLE = "enable"
    DISABLE = "disable"


@enum.unique
class ResourceStatusType(enum.Enum):
    ALARM = "alarm"
    AVAILABLE = "available"
    INSTALLED = "installed"
    NOT_EXISTS = "notExists"
    PENDING_REMOVAL = "pendingRemoval"
    PLANNED = "planned"
    RESERVED = "reserved"
    STANDBY = "standby"
    SUSPENDED = "suspended"
    UNKNOWN = "unknown"


@enum.unique
class ResourceUsageStateType(enum.Enum):
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"


@enum.unique
class SalesLeadPriorityType(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@enum.unique
class SalesLeadStatusType(enum.Enum):
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "inProgress"
    ACCEPTED = "accepted"
    PENDING = "pending"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


@enum.unique
class SalesOpportunityItemStateType(enum.Enum):
    ACCEPTED = "accepted"
    ACKNOWLEDGED = "acknowledged"
    CANCELLED = "cancelled"
    IN_PROGRESS = "inProgress"
    PENDING = "pending"
    REJECTED = "rejected"


@enum.unique
class SalesOpportunityStateType(enum.Enum):
    ACCEPTED = "accepted"
    ACKNOWLEDGED = "acknowledged"
    CANCELLED = "cancelled"
    IN_PROGRESS = "inProgress"
    PENDING = "pending"
    REJECTED = "rejected"


@enum.unique
class ServiceOperatingStatusType(enum.Enum):
    CONFIGURED = "configured"
    RUNNING = "running"
    STOPPED = "stopped"
    LIMITED = "limited"
    STOPPING = "stopping"
    PENDING = "pending"
    FAILED = "failed"
    STARTING = "starting"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@enum.unique
class ServiceOrderItemActionType(enum.Enum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"
    NO_CHANGE = "noChange"
    OTHER = "other"


@enum.unique
class ServiceOrderItemStateType(enum.Enum):
    ACKNOWLEDGED = "acknowledged"
    REJECTED = "rejected"
    PENDING = "pending"
    HELD = "held"
    IN_PROGRESS = "inProgress"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    ASSESSING_CANCELLATION = "assessingCancellation"
    PENDING_CANCELLATION = "pendingCancellation"
    PARTIAL = "partial"


@enum.unique
class ServiceOrderStateType(enum.Enum):
    ACKNOWLEDGED = "acknowledged"
    REJECTED = "rejected"
    PENDING = "pending"
    HELD = "held"
    IN_PROGRESS = "inProgress"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
    ASSESSING_CANCELLATION = "assessingCancellation"
    PENDING_CANCELLATION = "pendingCancellation"


@enum.unique
class ServiceStateType(enum.Enum):
    INACTIVE = "inactive"
    RESERVED = "reserved"
    ACTIVE = "active"
    FEASIBILITY_CHECKED = "feasibilityChecked"
    TERMINATED = "terminated"
    SUSPENDED = "suspended"
    DESIGNED = "designed"


@enum.unique
class SourceEnum(enum.Enum):
    EVENT = "event"
    ENVIRONMENT = "environment"
    SUBJECT = "subject"
    RESULT = "result"
    INPUT = "input"


@enum.unique
class StabilityIssueTypeEnum(enum.Enum):
    DEPRECATED = "deprecated"
    OUTDATED = "outdated"
    VALIDITY_WINDOW_ISSUE = "validityWindowIssue"


@enum.unique
class TaskStateType(enum.Enum):
    ACKNOWLEDGED = "acknowledged"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "inProgress"
    CANCELLED = "cancelled"
    DONE = "done"
    TERMINATED_WITH_ERROR = "terminatedWithError"


@enum.unique
class TaxCategory(enum.Enum):
    SALES_TAX = "salesTax"
    VAT = "VAT"


@enum.unique
class TechnicalRelationshipTypeEnum(enum.Enum):
    SUBSTITUTED_BY = "substitutedBy"
    DEPENDS_ON = "dependsOn"
    EXCLUDED_BY = "excludedBy"
    REQUIRES = "requires"
    USES = "uses"


@enum.unique
class TermDurationExtensionStrategyEnum(enum.Enum):
    INCLUSIVE = "inclusive"
    ADDITIVE = "additive"


@enum.unique
class WorkflowImpactTypeEnum(enum.Enum):
    PRICE_IMPACTING = "priceImpacting"
    PRODUCT_ORDER_IMPACTING = "productOrderImpacting"
    FULFILLMENT_IMPACTING = "fulfillmentImpacting"


#######
#      #
# REFS
#     #
#      #


@dataclass(repr=False)
class ItemRef(EntityRef):
    _referred_type: str = "Item"
    entityHref: Optional[str] = None
    itemId: Optional[str] = None


@dataclass(repr=False)
class AccountRef(EntityRef):
    _referred_type: str = "Account"


@dataclass(repr=False)
class AgreementItemRef(ItemRef):
    def __post_init__(self):
        raise NotImplementedError(f"{self.__class__.__name__} is not implemented yet.")


@dataclass(repr=False)
class AgreementRef(EntityRef):
    _referred_type: str = "Agreement"


@dataclass(repr=False)
class AppointmentRef(EntityRef):
    _referred_type: str = "Appointment"
    description: Optional[str] = None


@dataclass(repr=False)
class AssociationSpecificationRef(EntityRef):
    _referred_type: str = "AssociationSpecification"


@dataclass(repr=False)
class AttachmentRef(EntityRef):
    _referred_type: str = "Attachment"
    url: Optional[str] = None
    description: Optional[str] = None


@dataclass(repr=False)
class BillingAccountRef(EntityRef):
    _referred_type: str = "BillingAccount"
    ratingType: Optional[RatingType] = None


@dataclass(repr=False)
class BillingCycleSpecificationRef(EntityRef):
    _referred_type: str = "BillingCycleSpecification"


@dataclass(repr=False)
class BillFormatRef(EntityRef):
    _referred_type: str = "BillFormat"


@dataclass(repr=False)
class BillPresentationMediaRef(EntityRef):
    _referred_type: str = "BillPresentationMedia"


@dataclass(repr=False)
class CategoryRef(EntityRef):
    _referred_type: str = "Category"
    version: Optional[str] = None


@dataclass(repr=False)
class ChannelRef(EntityRef):
    _referred_type: str = "Channel"


@dataclass(repr=False)
class CharacteristicSpecificationRef(EntityRef):
    _referred_type: str = "CharacteristicSpecification"


@dataclass(repr=False)
class CharacteristicValueSpecificationRef(EntityRef):
    _referred_type: str = "CharacteristicValueSpecification"


@dataclass(repr=False)
class CapacitySpecificationRef(EntityRef):
    _referred_type: str = "CapacitySpecification"


@dataclass(repr=False)
class ConnectionPointSpecificationRef(EntityRef):
    _referred_type: str = "ConnectionPointSpecification"
    version: Optional[str] = None


@dataclass(repr=False)
class ConstraintRef(EntityRef):
    _referred_type: str = "Constraint"
    version: Optional[str] = None


@dataclass(repr=False)
class CustomerBillRef(EntityRef):
    _referred_type: str = "CustomerBill"


@dataclass(repr=False)
class EndpointSpecificationRef(EntityRef):
    _referred_type: str = "EndpointSpecification"
    role: Optional[str] = None
    isRoot: Optional[bool] = None
    connectionPointSpecification: Optional[ConnectionPointSpecificationRef] = None


@dataclass(repr=False)
class EntitySpecificationRef(EntityRef):
    _referred_type: str = "EntitySpecification"
    version: Optional[str] = None


@dataclass(repr=False)
class IntentRef(EntityRef):
    _referred_type: str = "Intent"


@dataclass(repr=False)
class IntentSpecificationRef(EntityRef):
    _referred_type: str = "IntentSpecification"


@dataclass(repr=False)
class FinancialAccountRef(EntityRef):
    _referred_type: str = "FinancialAccount"


@dataclass(repr=False)
class GeographicAddressRef(EntityRef):
    _referred_type: str = "GeographicAddress"


@dataclass(repr=False)
class MarketingCampaignRef(EntityRef):
    _referred_type: str = "MarketingCampaign"


@dataclass(repr=False)
class MarketSegmentRef(EntityRef):
    _referred_type: str = "MarketSegment"


@dataclass(repr=False)
class PaymentPlanRef(EntityRef):
    _referred_type: str = "PaymentPlan"


@dataclass(repr=False)
class PartyRef(EntityRef):
    _referred_type: str = "Party"


@dataclass(repr=False)
class OrganizationRef(PartyRef):
    _referred_type: str = "Organization"


@dataclass(repr=False)
class IndividualRef(PartyRef):
    _referred_type: str = "Individual"


@dataclass(repr=False)
class PartyRoleRef(EntityRef):
    _referred_type: str = "PartyRole"
    partyId: Optional[str] = None
    partyName: Optional[str] = None


@dataclass(repr=False)
class PartyRoleSpecificationRef(EntityRef):
    _referred_type: str = "PartyRoleSpecification"


@dataclass(repr=False)
class PaymentRef(EntityRef):
    _referred_type: str = "Payment"


@dataclass(repr=False)
class PaymentMethodRef(EntityRef):
    _referred_type: str = "PaymentMethod"


@dataclass(repr=False)
class PlaceRef(EntityRef):
    _referred_type: str = "Place"


@dataclass(repr=False)
class PolicyActionRef(EntityRef):
    _referred_type: str = "PolicyAction"


@dataclass(repr=False)
class PolicyConditionRef(EntityRef):
    _referred_type: str = "PolicyCondition"


@dataclass(repr=False)
class PolicyConstraintRef(EntityRef):
    _referred_type: str = "PolicyConstraint"


@dataclass(repr=False)
class PolicyDomainRef(EntityRef):
    _referred_type: str = "PolicyDomain"


@dataclass(repr=False)
class PolicyEventRef(EntityRef):
    _referred_type: str = "PolicyEvent"


@dataclass(repr=False)
class PolicyExpressionRef(EntityRef):
    _referred_type: str = "PolicyExpression"


@dataclass(repr=False)
class PolicyOperatorRef(EntityRef):
    _referred_type: str = "PolicyOperator"


@dataclass(repr=False)
class PolicyRef(EntityRef):
    _referred_type: str = "Policy"
    version: Optional[str] = None


@dataclass(repr=False)
class PolicyVariableRef(EntityRef):
    _referred_type: str = "PolicyVariable"


@dataclass(repr=False)
class ProcessFlowSpecificationRef(EntityRef):
    _referred_type: str = "ProcessFlowSpecification"


@dataclass(repr=False)
class ProductOfferingPriceRef(EntityRef):
    _referred_type: str = "ProductOfferingPrice"
    version: Optional[str] = None


@dataclass(repr=False)
class ProductOfferingQualificationItemRef(ItemRef):
    _referred_type: str = "ProductOfferingQualificationItem"
    productOfferingQualificationHref: Optional[str] = None
    productOfferingQualificationId: Optional[str] = None
    productOfferingQualificationName: Optional[str] = None


@dataclass(repr=False)
class ProductOfferingQualificationRef(EntityRef):
    _referred_type: str = "ProductOfferingQualification"


@dataclass(repr=False)
class ProductOfferingRef(EntityRef):
    _referred_type: str = "ProductOffering"
    version: Optional[str] = None


@dataclass(repr=False)
class ProductOfferingTermRef(EntityRef):
    _referred_type: str = "ProductOfferingTerm"


@dataclass(repr=False)
class ProductOrderItemRef(ItemRef):
    _referred_type: str = "ProductOrderItem"
    productOrderHref: Optional[str] = None
    productOrderId: Optional[str] = None
    productOrderItemId: Optional[str] = None


@dataclass(repr=False)
class ProductOrderRef(ItemRef):
    _referred_type: str = "ProductOrder"


@dataclass(repr=False)
class ProductRef(EntityRef):
    _referred_type: str = "Product"


@dataclass(repr=False)
class ProductSpecificationRef(EntityRef):
    _referred_type: Optional[str] = "ProductSpecification"
    targetProductSchema: Optional[TargetProductSchema] = None
    version: Optional[str] = None


@dataclass(repr=False)
class PromotionRef(EntityRef):
    _referred_type: Optional[str] = "Promotion"


@dataclass(repr=False)
class QuoteItemRef(EntityRef):
    _referred_type: Optional[str] = "QuoteItem"
    quoteHref: Optional[str] = None
    quoteId: Optional[str] = None
    quoteItemId: Optional[str] = None


@dataclass(repr=False)
class QuoteRef(EntityRef):
    _referred_type: Optional[str] = "Quote"


@dataclass(repr=False)
class RelatedOrderItem(EntityRef):
    _referred_type: Optional[str] = "ProductOrder"
    id: Optional[str] = None
    orderHref: Optional[str] = None
    orderId: Optional[str] = None
    orderItemAction: Optional[ItemActionType] = None
    orderItemId: Optional[str] = None
    role: Optional[str] = None


@dataclass(repr=False)
class ResourceCandidateRef(EntityRef):
    _referred_type: Optional[str] = "ResourceCandidate"
    version: Optional[str] = None


@dataclass(repr=False)
class ResourceCategoryRef(EntityRef):
    _referred_type: Optional[str] = "ResourceCategory"
    version: Optional[str] = None


@dataclass(repr=False)
class ResourceGraphSpecificationRef(EntityRef):
    _referred_type: Optional[str] = "ResourceGraphSpecification"


@dataclass(repr=False)
class ResourceOrderItemRef(EntityRef):
    _referred_type: Optional[str] = "ResourceOrderItem"
    itemId: Optional[str] = None
    resourceOrderHref: Optional[str] = None
    resourceOrderId: Optional[str] = None


@dataclass(repr=False)
class ResourceOrderRef(EntityRef):
    _referred_type: Optional[str] = "ResourceOrder"


@dataclass(repr=False)
class ResourceRef(EntityRef):
    _referred_type: Optional[str] = "Resource"


@dataclass(repr=False)
class ResourceSpecificationRef(EntityRef):
    _referred_type: Optional[str] = "ResourceSpecification"
    version: Optional[str] = None


@dataclass(repr=False)
class SalesActivityRef(EntityRef):
    _referred_type: Optional[str] = "SalesActivity"


@dataclass(repr=False)
class SalesLeadRef(EntityRef):
    _referred_type: Optional[str] = "SalesLead"


@dataclass(repr=False)
class SalesOpportunityRef(EntityRef):
    _referred_type: Optional[str] = "SalesOpportunity"


@dataclass(repr=False)
class SalesProjectRef(EntityRef):
    _referred_type: Optional[str] = "SalesProject"


@dataclass(repr=False)
class ServiceCandidateRef(EntityRef):
    _referred_type: Optional[str] = "ServiceCandidate"
    version: Optional[str] = None


@dataclass(repr=False)
class ServiceCategoryRef(EntityRef):
    _referred_type: Optional[str] = "ServiceCategory"
    version: Optional[str] = None


@dataclass(repr=False)
class ServiceLevelSpecificationRef(EntityRef):
    _referred_type: Optional[str] = "ServiceLevelSpecification"


@dataclass(repr=False)
class ServiceOrderItemRef(EntityRef):
    _referred_type: Optional[str] = "ServiceOrderItem"
    itemId: Optional[str] = None
    serviceOrderHref: Optional[str] = None
    serviceOrderId: Optional[str] = None


@dataclass(repr=False)
class ServiceOrderRef(EntityRef):
    _referred_type: Optional[str] = "ServiceOrder"


@dataclass(repr=False)
class ServiceRef(EntityRef):
    _referred_type: Optional[str] = "Service"


@dataclass(repr=False)
class ServiceSpecificationRef(EntityRef):
    _referred_type: Optional[str] = "ServiceSpecification"
    version: Optional[str] = None


@dataclass(repr=False)
class SLARef(EntityRef):
    _referred_type: Optional[str] = "SLA"


################
#
#
#
# CHARACTERISTICS


@dataclass(repr=False)
class CharacteristicRelationship(Entity):
    relationshipType: Optional[str] = None
    id: Optional[str] = None


@dataclass(repr=False)
class Characteristic(Entity):
    id: Optional[str] = None
    name: Optional[str] = None
    valueType: Optional[str] = None
    characteristicRelationship: Optional[List[CharacteristicRelationship]] = field(
        default_factory=list
    )
    characteristicSpecificationRef: Optional[CharacteristicSpecificationRef] = None
    characteristicValueSpecificationRef: Optional[
        CharacteristicValueSpecificationRef
    ] = None


@dataclass(repr=False)
class BooleanCharacteristic(Characteristic):
    value: Optional[bool] = None
    valueType: str = "Boolean"


@dataclass(repr=False)
class IntegerCharacteristic(Characteristic):
    value: Optional[int] = None
    valueType: str = "Integer"


@dataclass(repr=False)
class FloatCharacteristic(Characteristic):
    value: Optional[float] = None
    valueType: str = "Float"


@dataclass(repr=False)
class NumberCharacteristic(Characteristic):
    value: Optional[float] = None
    valueType: str = "Number"


@dataclass(repr=False)
class StringCharacteristic(Characteristic):
    value: Optional[str] = None
    valueType: str = "String"


@dataclass(repr=False)
class ObjectCharacteristic(Characteristic):
    value: Optional[dict] = None
    valueType: str = "Object"


@dataclass(repr=False)
class BooleanArrayCharacteristic(Characteristic):
    value: Optional[List[bool]] = field(default_factory=list)
    valueType: str = "BooleanArray"


@dataclass(repr=False)
class IntegerArrayCharacteristic(Characteristic):
    value: Optional[List[int]] = field(default_factory=list)
    valueType: str = "IntegerArray"


@dataclass(repr=False)
class NumberArrayCharacteristic(Characteristic):
    value: Optional[List[float]] = field(default_factory=list)
    valueType: str = "NumberArray"


@dataclass(repr=False)
class ObjectArrayCharacteristic(Characteristic):
    value: Optional[List[dict]] = field(default_factory=list)
    valueType: str = "ObjectArray"


@dataclass(repr=False)
class StringArrayCharacteristic(Characteristic):
    value: Optional[List[str]] = field(default_factory=list)
    valueType: str = "StringArray"


############
#
# ENTITIES
#
#############


@dataclass(repr=False)
class Money(Entity):
    unit: str
    value: float


@dataclass(repr=False)
class Duration(Entity):
    units: str
    amount: int


@dataclass(repr=False)
class TimePeriod(Entity):
    startDateTime: Optional[str] = None
    endDateTime: Optional[str] = None

    def _length_ms(self):
        start_dt = datetime.fromisoformat(self.startDateTime.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(self.endDateTime.replace("Z", "+00:00"))
        delta = end_dt - start_dt
        return int(delta.total_seconds() * 1000)


@dataclass(repr=False)
class TargetResourceSchema(Entity):
    """Reference to the schema and type of target resource described by resource specification."""

    _schema_location: Optional[str] = None


@dataclass(repr=False)
class TargetEntitySchema(Entity):
    """Reference to the schema and type of target entity described by a specification."""

    _schema_location: Optional[str] = None


@dataclass(repr=False)
class ApplicableTimePeriod(Entity):
    dayOfWeek: Optional[str] = None
    fromToDateTime: Optional[TimePeriod] = None
    rangeInterval: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class Quantity(Entity):
    units: str
    amount: int


@dataclass(repr=False)
class AllowedProductAction(Entity):
    action: Optional[ProductActionType] = None
    channel: Optional[List[ChannelRef]] = field(default_factory=list)
    id: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class Capacity(Entity):
    name: Optional[str] = None
    capacityStatus: Optional[CapacityStatus] = None
    capacityAmount: Optional[Quantity] = None
    capacityAmountFrom: Optional[Quantity] = None
    capacityAmountTo: Optional[Quantity] = None
    rangeInterval: Optional[str] = None
    relatedPlace: Optional[List[RelatedPlaceRef]] = field(default_factory=list)
    applicableTimePeriod: Optional[List[ApplicableTimePeriod]] = field(
        default_factory=list
    )
    capacityCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    relatedCapacity: Optional[List["Capacity"]] = field(default_factory=list)
    capacitySpecification: Optional[CapacitySpecificationRef] = None


@dataclass(repr=False)
class CapacitySpecification(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    href: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    capacityCharacteristicSpecification: Optional[List[CharacteristicSpecification]] = (
        field(default_factory=list)
    )
    relatedCapacitySpecification: Optional[List[CapacitySpecification]] = field(
        default_factory=list
    )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourcePool/v5/capacitySpecification"


@dataclass(repr=False)
class BundledProductSpecification(Entity):
    id: Optional[str] = None
    href: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None


@dataclass(repr=False)
class FulfilmentData(Entity):
    entryType: Optional[EntryType] = None
    fulfilmentPlan: Optional[str] = None
    id: Optional[str] = None
    triggeringAction: Optional[ItemActionType] = None


@dataclass(repr=False)
class Intent(Entity):
    def __post_init__(self):
        raise NotImplementedError(f"{self.__class__.__name__} is not implemented yet.")


@dataclass(repr=False)
class TargetProductSchema(Entity):
    id: Optional[str] = None
    _schema_location: Optional[str] = None


@dataclass(repr=False)
class StabilityOffendingEntity(Entity):
    id: Optional[str] = None
    _referred_type: Optional[str] = None
    version: Optional[str] = None


@dataclass(repr=False)
class StabilityResolution(Entity):
    entityId: Optional[str] = None
    version: Optional[str] = None


@dataclass(repr=False)
class StabilityIssue(Entity):
    offendingEntity: Optional[List[StabilityOffendingEntity]] = field(
        default_factory=list
    )
    type: Optional[StabilityIssueTypeEnum] = None


@dataclass(repr=False)
class ProductSpecificationRelationship(Entity):
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    relationshipType: Optional[TechnicalRelationshipTypeEnum] = None
    _referred_type: Optional[str] = None
    characteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )
    version: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class ProductSpecification(Entity, BaseCRUDMixin):
    attachment: Optional[List[Union[Attachment, AttachmentRef]]] = field(
        default_factory=list
    )
    brand: Optional[str] = None
    bundledProductSpecification: Optional[List[BundledProductSpecification]] = field(
        default_factory=list
    )
    category: Optional[List[CategoryRef]] = field(default_factory=list)
    description: Optional[str] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    fulfilmentData: Optional[List[FulfilmentData]] = field(default_factory=list)
    href: Optional[str] = None
    id: Optional[str] = None
    intentSpecification: Optional[IntentSpecificationRef] = None
    isBundle: bool = False
    lastUpdate: Optional[str] = None
    lifecycleStatus: Optional[ProductSpecificationLifecycleStatusType] = None
    name: Optional[str] = None
    policy: Optional[List[PolicyRef]] = field(default_factory=list)
    productNumber: Optional[str] = None
    productSpecCharacteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )
    productSpecificationRelationship: Optional[
        List[ProductSpecificationRelationship]
    ] = field(default_factory=list)
    provider: Optional[ProviderType] = None
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    resourceSpecification: Optional[List[ResourceSpecificationRef]] = field(
        default_factory=list
    )
    serviceSpecification: Optional[List[ServiceSpecificationRef]] = field(
        default_factory=list
    )
    targetProductSchema: Optional[TargetProductSchema] = None
    validFor: Optional[TimePeriod] = None
    vendor: Optional[str] = None
    version: Optional[str] = None
    isUnStable: Optional[bool] = None
    issues: Optional[List[StabilityIssue]] = field(default_factory=list)
    resolution: Optional[StabilityResolution] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return (
            f"{context.api_base_url}/productCatalogManagement/v5/productSpecification"
        )


@dataclass(repr=False)
class ApiProductSpecification(ProductSpecification):
    pass


@dataclass(repr=False)
class TaxItem(Entity):
    taxAmount: Optional[Money] = None
    taxCategory: Optional[str] = None
    taxRate: Optional[float] = None


@dataclass(repr=False)
class BundledProductOfferingPriceRelationship(Entity):
    version: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    relationshipType: Optional[BundledProductOfferingPriceRelationshipTypeEnum] = None
    bundledProductOfferingPriceId: Optional[str] = None


@dataclass(repr=False)
class ProductOfferingPriceRelationship(Entity):
    href: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    relationshipType: Optional[PopRelationshipTypeEnum] = None
    role: Optional[str] = None
    version: Optional[str] = None


@dataclass(repr=False)
class PricingLogicAlgorithm(Entity):
    description: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    plaSpecId: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class ProductOfferingPrice(Entity):
    description: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    isBundle: bool = False
    lifecycleStatus: Optional[LifecycleStatus] = None
    percentage: Optional[float] = None
    price: Optional[Money] = None
    priceType: Optional[PriceType] = None
    chargeType: Optional[ChargeType] = None
    recurringChargePeriodLength: Optional[int] = None
    recurringChargePeriodType: Optional[RecurringChargePeriod] = None
    unitOfMeasure: Optional[Quantity] = None
    validFor: Optional[TimePeriod] = None
    version: Optional[str] = None
    allowedAction: Optional[List[AllowedProductAction]] = field(default_factory=list)
    isPaymentPlanAllowed: bool = False
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    delayStartTime: Optional[Duration] = None
    isPercentage: bool = False
    isRange: bool = False
    lastUpdate: Optional[str] = None
    tax: Optional[List[TaxItem]] = field(default_factory=list)
    appliesOn: Optional[OneTimeFeeAppliesOnEnum] = None
    bundledPopRelationship: Optional[List[BundledProductOfferingPriceRelationship]] = (
        field(default_factory=list)
    )
    lowerOrderQuantity: Optional[float] = None
    lowerPercentageLimit: Optional[float] = None
    lowerPriceLimit: Optional[Money] = None
    lowerValueLimit: Optional[float] = None
    place: Optional[PlaceRef] = None
    policy: Optional[PolicyRef] = None
    popRelationship: Optional[List[ProductOfferingPriceRelationship]] = field(
        default_factory=list
    )
    priceAlterationType: Optional[List[ProductOfferingPriceAlterationTypeEnum]] = field(
        default_factory=list
    )
    pricingLogicAlgorithm: Optional[List[PricingLogicAlgorithm]] = field(
        default_factory=list
    )
    prodSpecCharValueUse: Optional[List[ProductSpecificationCharacteristicValueUse]] = (
        field(default_factory=list)
    )
    productOfferingTerm: Optional[List[ProductOfferingTerm]] = field(
        default_factory=list
    )
    rangeIntervalType: Optional[PriceIntervalType] = None
    upperOrderQuantity: Optional[float] = None
    upperPercentageLimit: Optional[float] = None
    upperPriceLimit: Optional[Money] = None
    upperValueLimit: Optional[float] = None


@dataclass(repr=False)
class ProductOfferingPriceTable(Entity):
    tableConfig: Optional[Any] = None
    tableData: Optional[List[Any]] = field(default_factory=list)
    isPopGenerated: Optional[bool] = None


@dataclass(repr=False)
class SimpleProductOfferingBasePriceTable(ProductOfferingPriceTable):
    pass


@dataclass(repr=False)
class SimpleProductOfferingComplexPriceTable(ProductOfferingPriceTable):
    pass


@dataclass(repr=False)
class BundleProductOfferingBasePriceTable(ProductOfferingPriceTable):
    pass


@dataclass(repr=False)
class BundleProductOfferingComplexPriceTable(SimpleProductOfferingComplexPriceTable):
    pass


@dataclass(repr=False)
class ProductOfferingTerm(Entity):
    id: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[Duration] = None
    name: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    delayStartTime: Optional[Duration] = None
    expiryNotificationPeriod: Optional[Duration] = (
        None  # deprecated; use multipleExpiryNotificationPeriod
    )
    multipleExpiryNotificationPeriod: Optional[List[Duration]] = field(
        default_factory=list
    )
    renewalAction: Optional[RenewalAction] = None
    termDurationExtensionStrategy: Optional[TermDurationExtensionStrategyEnum] = None
    autoRenewLimit: Optional[int] = None


@dataclass(repr=False)
class ProductOfferingRelationship(Entity):
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    relationshipType: Optional[CommercialRelationshipTypeEnum] = None
    role: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    version: Optional[str] = None
    _referred_type: Optional[str] = "ProductOffering"


@dataclass(repr=False)
class CharacteristicSpecificationRelationship(Entity):
    name: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    characteristicSpecificationId: Optional[str] = None
    id: Optional[str] = None
    parentSpecificationHref: Optional[str] = None
    parentSpecificationId: Optional[str] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class CharacteristicValueSpecificationRelationship(Entity):
    characteristicValueSpecificationId: Optional[str] = None
    id: Optional[str] = None
    parentProdSpecCharValueUseHref: Optional[str] = None
    parentProdSpecCharValueUseId: Optional[str] = None
    parentSpecificationId: Optional[str] = None
    relationshipType: Optional[CharacteristicValueSpecificationRelationshipType] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class CharacteristicValueSpecification(Entity):
    characteristicValueSpecificationRef: Optional[
        CharacteristicValueSpecificationRef
    ] = None
    charValueSpecRelationship: Optional[
        List[CharacteristicValueSpecificationRelationship]
    ] = field(default_factory=list)
    id: Optional[str] = None
    isDefault: bool = False
    rangeInterval: Optional[str] = None
    rangeType: Optional[str] = None
    regex: Optional[str] = None
    unitOfMeasure: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    valueFrom: Optional[float] = None
    valueTo: Optional[float] = None
    valueType: Optional[str] = None


@dataclass(repr=False)
class MapArrayCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[List[dict]] = None


@dataclass(repr=False)
class ObjectArrayCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[List[dict]] = None


@dataclass(repr=False)
class NumberArrayCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[List[float]] = None


@dataclass(repr=False)
class IntegerArrayCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[List[int]] = None


@dataclass(repr=False)
class StringArrayCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[List[str]] = None


@dataclass(repr=False)
class FloatArrayCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[List[float]] = None


@dataclass(repr=False)
class IntegerCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[int] = None


@dataclass(repr=False)
class NumberCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[float] = None


@dataclass(repr=False)
class FloatCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[float] = None


@dataclass(repr=False)
class MapCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[dict] = None


@dataclass(repr=False)
class ObjectCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[dict] = None


@dataclass(repr=False)
class StringCharacteristicValueSpecification(CharacteristicValueSpecification):
    value: Optional[str] = None


@dataclass(repr=False)
class CharacteristicSpecification(Entity):
    charSpecRelationship: Optional[List[CharacteristicSpecificationRelationship]] = (
        field(default_factory=list)
    )
    characteristicValueSpecification: Optional[
        List[CharacteristicValueSpecification]
    ] = field(default_factory=list)
    configurable: bool = True
    description: Optional[str] = None
    extensible: bool = True
    href: Optional[str] = None
    id: Optional[str] = None
    isUnique: bool = True
    maxCardinality: Optional[int] = None
    minCardinality: Optional[int] = None
    name: Optional[str] = None
    regex: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    valueType: Optional[str] = None
    workflowImpact: Optional[List[WorkflowImpactTypeEnum]] = None


@dataclass(repr=False)
class ProductSpecificationCharacteristicValueUse(Entity):
    characteristicSpecificationRef: Optional[CharacteristicSpecificationRef] = None
    description: Optional[str] = None
    id: Optional[str] = None
    maxCardinality: Optional[int] = None
    minCardinality: Optional[int] = None
    name: Optional[str] = None
    productSpecCharacteristicValue: Optional[List[CharacteristicValueSpecification]] = (
        field(default_factory=list)
    )
    productSpecification: Optional[ProductSpecificationRef] = None
    validFor: Optional[TimePeriod] = None
    valueType: Optional[str] = None


@dataclass(repr=False)
class SKU(Entity):
    id: Optional[str] = None
    href: Optional[str] = None
    skuId: Optional[str] = None
    refEntityId: Optional[str] = None
    refEntityVersion: Optional[str] = None
    characteristic: Optional[
        List[
            Union[
                ProductSpecificationCharacteristicValueUse,
                CharacteristicSpecification,
            ]
        ]
    ] = field(default_factory=list)
    productOfferingTerm: Optional[ProductOfferingTerm] = None
    createOn: Optional[str] = None
    lastUpdate: Optional[str] = None


@dataclass(repr=False)
class ProductOffering(Entity, BaseCRUDMixin):
    description: Optional[str] = None
    href: Optional[str] = None
    id: Optional[str] = None
    isBundle: bool = False
    isSellable: bool = True
    lifecycleStatus: Optional[LifecycleStatus] = None
    name: Optional[str] = None
    statusReason: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    version: Optional[str] = None
    createOn: Optional[str] = None
    lastUpdate: Optional[str] = None
    humanReadableId: Optional[str] = None
    isUnStable: Optional[bool] = None
    maximumCardinality: Optional[int] = None
    minimumCardinality: Optional[int] = None
    productSpecification: Optional[ProductSpecificationRef] = None
    prodSpecCharValueUse: Optional[List[ProductSpecificationCharacteristicValueUse]] = (
        field(default_factory=list)
    )
    productOfferingCharacteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )
    productOfferingPrice: Optional[
        List[
            Union[
                ProductOfferingPrice,
                ProductOfferingPriceRef,
            ]
        ]
    ] = field(default_factory=list)
    productOfferingTerm: Optional[List[ProductOfferingTerm]] = field(
        default_factory=list
    )
    productOfferingRelationship: Optional[List[ProductOfferingRelationship]] = field(
        default_factory=list
    )
    channel: Optional[List[ChannelRef]] = field(default_factory=list)
    allowedAction: Optional[List[AllowedProductAction]] = field(default_factory=list)
    bundledProductOffering: Optional[List[BundledProductOffering]] = field(
        default_factory=list
    )
    bundledGroupProductOffering: Optional[List[BundledGroupProductOffering]] = field(
        default_factory=list
    )
    policy: Optional[List[PolicyRef]] = field(default_factory=list)
    agreement: Optional[List[AgreementRef]] = field(default_factory=list)
    category: Optional[List[CategoryRef]] = field(default_factory=list)
    place: Optional[List[PlaceRef]] = field(default_factory=list)
    marketSegment: Optional[List[MarketSegmentRef]] = field(default_factory=list)
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    attachment: Optional[
        List[
            Union[
                Attachment,
                AttachmentRef,
            ]
        ]
    ] = field(default_factory=list)
    serviceCandidate: Optional[ServiceCandidateRef] = None
    resourceCandidate: Optional[ResourceCandidateRef] = None
    serviceLevelAgreement: Optional[SLARef] = None
    sku: Optional[List[SKU]] = field(default_factory=list)
    issues: Optional[List[StabilityIssue]] = field(default_factory=list)
    resolution: Optional[StabilityResolution] = None
    productOfferingPriceTable: Optional[
        List[
            Union[
                SimpleProductOfferingBasePriceTable,
                SimpleProductOfferingComplexPriceTable,
                BundleProductOfferingBasePriceTable,
                BundleProductOfferingComplexPriceTable,
            ]
        ]
    ] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/productCatalogManagement/v5/productOffering"

    def activate(self, context: Context) -> ProductOffering:
        payload = {"state": LifecycleStatus.ACTIVE.value}
        return self.update(payload, context)


@dataclass(repr=False)
class Price(Entity):
    dutyFreeAmount: Optional[Money] = None
    percentage: Optional[float] = None
    taxIncludedAmount: Optional[Money] = None
    taxRate: Optional[float] = None


@dataclass(repr=False)
class PriceAlteration(Entity):
    price: Optional[Price] = None
    id: Optional[str] = None
    applicationDuration: Optional[int] = None
    description: Optional[str] = None
    name: Optional[str] = None
    priceType: Optional[PriceType] = None
    priority: Optional[int] = None
    productOfferingPrice: Optional[ProductOfferingPriceRef] = None
    productOfferingTerm: Optional[ProductOfferingTermRef] = None
    recurringChargePeriod: Optional[RecurringChargePeriod] = None
    unitOfMeasure: Optional[str] = None
    isRange: Optional[bool] = None
    isPercentage: Optional[bool] = None
    lowerPercentageLimit: Optional[float] = None
    upperPercentageLimit: Optional[float] = None
    upperValueLimit: Optional[float] = None
    lowerValueLimit: Optional[float] = None
    lowerAmountLimit: Optional[Money] = None
    upperAmountLimit: Optional[Money] = None
    rangeIntervalType: Optional[PriceIntervalType] = None


@dataclass(repr=False)
class PaymentPlanItem(Entity):
    name: Optional[str] = None
    id: Optional[str] = None
    isInitial: bool = False
    isLocked: bool = False
    paymentAmountPercentage: Optional[float] = None
    paymentDateTime: Optional[str] = None
    sequence: Optional[int] = None
    totalAmount: Optional[Money] = None
    relatedEntity: Optional[List[EntityRef]] = field(default_factory=list)


@dataclass(repr=False)
class PaymentPlan(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    isPercentageBased: bool = False
    numberOfPayments: Optional[int] = None
    href: Optional[str] = None
    relatedParty: Optional[RelatedPartyRefOrPartyRoleRef] = None
    status: Optional[str] = None
    totalAmount: Optional[Money] = None
    paymentPlanItem: Optional[List[PaymentPlanItem]] = field(default_factory=list)
    paymentFrequency: Optional[str] = None
    planType: Optional[str] = None
    priority: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    paymentMethod: Optional[PaymentMethodRef] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/payment/v4/paymentPlan"


@dataclass(repr=False)
class ProductPrice(Entity):
    """Represents the price details associated with a product in the TM Forum TMF637 Product Inventory API.

    A ProductPrice object describes how a product is charged, including one-time charges,
    recurring charges, discounts, and related price alterations. It also can indicate
    payment plans, units of measure, and whether the price is a percentage or falls within
    a range.

    Attributes:
        price (Optional[Price]): A nested Price object holding the actual monetary value and currency of the product price.
        name (Optional[str]): A human-readable name or label for the product price component.
        description (Optional[str]): A textual description of this product price.
        id (Optional[str]): The unique identifier of this product price record.
        priceAlteration (Optional[List[PriceAlteration]]): A list of price alterations or adjustments (e.g., discounts, markups) that modify the base product price.
        recurringChargePeriod (Optional[RecurringChargePeriod]): Defines the frequency (e.g., daily, monthly) for recurring charges, if applicable.
        unitOfMeasure (Optional[str]): The unit of measure related to the price (e.g., GB, month), if relevant to how the price is calculated.
        priceType (Optional[PriceType]): The category of price (e.g., one-time charge, recurring charge, discount).
        chargeType (Optional[ChargeType]): More specific classification of the charge (e.g., in-advance, in-arrear for recurring charges).
        productOfferingPrice (Optional[ProductOfferingPriceRef]): Reference to the ProductOfferingPrice from which this product price was derived.
        isPercentage (Optional[bool]): Indicates whether the price is expressed as a percentage rather than a fixed amount.
        isPaymentPlanAllowed (Optional[bool]): Whether a payment plan can be applied to this price.
        paymentPlan (Optional[PaymentPlanRef]): A reference to a payment plan applicable to this product price, if any.
        isRange (Optional[bool]): Whether the price falls within a range rather than being a fixed amount.
        rangeIntervalType (Optional[str]): The type of interval used when the price is expressed as a range (e.g., interval-based pricing tiers).

    Example:
        product_price = ProductPrice(
            price=Price(dutyFreeAmount=Money(unit="USD", value=99.99)),
            name="Monthly Subscription",
            description="Standard internet subscription fee",
            priceType=PriceType.RECURRING_CHARGE,
            chargeType=ChargeType.IN_ADVANCE,
            recurringChargePeriod=RecurringChargePeriod.MONTHLY
        )
    """

    price: Optional[Price] = None
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    priceAlteration: Optional[List[PriceAlteration]] = field(default_factory=list)
    recurringChargePeriod: Optional[RecurringChargePeriod] = None
    recurringChargeOffset: Optional[Duration] = None
    unitOfMeasure: Optional[str] = None
    priceType: Optional[PriceType] = None
    chargeType: Optional[ChargeType] = None
    productOfferingPrice: Optional[ProductOfferingPriceRef] = None
    productOfferingTerm: Optional[ProductOfferingTermRef] = None
    isPercentage: Optional[bool] = None
    isPaymentPlanAllowed: Optional[bool] = None
    paymentPlan: Optional[PaymentPlanRef] = None
    isRange: Optional[bool] = None
    rangeIntervalType: Optional[str] = None
    lowerValueLimit: Optional[float] = None
    upperValueLimit: Optional[float] = None
    ratingType: Optional[RatingType] = None

    def __post_init__(self):
        super().__post_init__()
        if self.priceType == PriceType.RECURRING_CHARGE and (
            self.chargeType is None or self.recurringChargePeriod is None
        ):
            raise ValueError(
                "Both chargeType and recurringChargePeriod are required for recurring charges"
            )


@dataclass(repr=False)
class ProductRelationship(Entity):
    id: str
    href: Optional[str] = None
    name: Optional[str] = None
    relationshipType: Optional[ProductRelationshipType] = None
    _referred_type: Optional[str] = "Product"


@dataclass(repr=False)
class RelatedPartyRefOrPartyRoleRef(Entity):
    id: Optional[str] = None
    name: Optional[str] = None
    partyOrPartyRole: Optional[
        Union[
            PartyRef,
            PartyRoleRef,
        ]
    ] = None
    role: Optional[str] = None


@dataclass(repr=False)
class ProductTerm(Entity):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    productOfferingTerm: Optional[ProductOfferingTermRef] = None
    validFor: Optional[TimePeriod] = None
    duration: Optional[Duration] = None
    renewalAction: Optional[RenewalAction] = None
    delayStartTime: Optional[Duration] = None
    expiryNotificationPeriod: Optional[Duration] = (
        None  # deprecated; use multipleExpiryNotificationPeriod
    )
    multipleExpiryNotificationPeriod: Optional[List[Duration]] = field(
        default_factory=list
    )
    termDurationExtensionStrategy: Optional[TermDurationExtensionStrategyEnum] = None
    autoRenewLimit: Optional[int] = None


@dataclass(repr=False)
class ExternalIdentifier(Entity):
    externalIdentifierType: Optional[str] = None
    href: Optional[str] = None
    id: Optional[str] = None
    owner: Optional[str] = None
    value: Optional[str] = None


@dataclass(repr=False)
class CreditProfile(Entity):
    creditProfileDate: Optional[str] = None
    creditRiskRating: Optional[int] = None
    creditScore: Optional[int] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class PartyRole(Entity, BaseCRUDMixin):
    description: Optional[str] = None
    href: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    role: Optional[RoleEnum] = None
    status: Optional[str] = None
    statusReason: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    engagedParty: Optional[PartyRef] = None
    contactMedium: Optional[List[ContactMedium]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyOrPartyRole]] = field(default_factory=list)
    account: Optional[List[AccountRef]] = field(default_factory=list)
    paymentMethod: Optional[List[PaymentMethodRef]] = field(default_factory=list)
    characteristic: Optional[List[Characteristic]] = field(default_factory=list)
    agreement: Optional[List[AgreementRef]] = field(default_factory=list)
    creditProfile: Optional[List[CreditProfile]] = field(default_factory=list)
    partyRoleSpecification: Optional[PartyRoleSpecificationRef] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/partyRoleManagement/v5/partyRole"


@dataclass(repr=False)
class PartyCreditProfile(Entity):
    creditAgencyName: Optional[str] = None
    creditAgencyType: Optional[str] = None
    href: Optional[str] = None
    id: Optional[str] = None
    ratingReference: Optional[str] = None
    ratingScore: Optional[int] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class Party(Entity):
    href: Optional[str] = None
    id: Optional[str] = None
    createOn: Optional[str] = None
    lastUpdate: Optional[str] = None
    version: Optional[str] = None
    contactMedium: Optional[List[ContactMedium]] = field(default_factory=list)
    taxExemptionCertificate: Optional[List[TaxExemptionCertificate]] = field(
        default_factory=list
    )
    relatedParty: Optional[List[RelatedPartyOrPartyRole]] = field(default_factory=list)
    creditRating: Optional[List[PartyCreditProfile]] = field(default_factory=list)
    externalReference: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    partyCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)


@dataclass(repr=False)
class OrganizationIdentification(Entity):
    identificationId: Optional[str] = None
    identificationType: Optional[str] = None
    issuingAuthority: Optional[str] = None
    issuingDate: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    attachment: Optional[Attachment] = None


@dataclass(repr=False)
class OrganizationChildRelationship(Entity):
    relationshipType: Optional[str] = None
    organization: Optional[OrganizationRef] = None


@dataclass(repr=False)
class OrganizationParentRelationship(Entity):
    relationshipType: Optional[RelationshipTypeEnum] = None
    organization: Optional[OrganizationRef] = None


@dataclass(repr=False)
class OtherNameOrganization(Entity):
    name: Optional[str] = None
    nameType: Optional[NameType] = None
    tradingName: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class Organization(Party, BaseCRUDMixin):
    """Represents an Organization entity in the TM Forum Party Management API.

    This class encapsulates information about an organization, including its
    operational and legal attributes, hierarchical relationships, and various
    identifiers. An Organization may represent a legal entity, a department,
    or a business unit within a broader enterprise context.

    Attributes:
        existsDuring (Optional[TimePeriod]): The time period during which the organization is in effect.
        isHeadOffice (bool): Indicates if the organization is a head office.
        isLegalEntity (bool): Indicates if the organization is recognized as a legal entity.
        name (Optional[str]): The primary name of the organization.
        nameType (Optional[str]): The type of the name (e.g., legal, trading).
        organizationType (Optional[str]): A category defining the organization's structure (e.g., department, subsidiary).
        status (Optional[OrganizationStateType]): Current lifecycle state of the organization (e.g., initialized, validated).
        tradingName (Optional[str]): A name under which the organization commonly trades, if different from its legal name.
        organizationIdentification (Optional[List[OrganizationIdentification]]): A list of identifiers (e.g., registration numbers, tax IDs) associated with the organization.
        organizationChildRelationship (Optional[List[OrganizationChildRelationship]]): References to child organizations in a hierarchy.
        organizationParentRelationship (Optional[OrganizationParentRelationship]): A reference to the organization's parent in a hierarchy, if any.
        otherName (Optional[List[OtherNameOrganization]]): Additional names the organization may be known by.
        place (Optional[List[PlaceRef]]): One or more places where the organization is located or registered.
        marketSegment (Optional[List[MarketSegmentRef]]): Market segments the organization belongs to.

    Methods:
        get_resource_path(context: Context) -> str:
            Returns the endpoint path for organization operations (creation, retrieval, updates, deletions).

    Usage Example:
        org = Organization(
            name="Acme Corporation",
            status=OrganizationStateType.INITIALIZED,
            isHeadOffice=True,
            organizationIdentification=[...]
        )
        org = org.create(context)
        org = org.read(context)
    """

    existsDuring: Optional[TimePeriod] = None
    isHeadOffice: bool = True
    isLegalEntity: bool = True
    name: Optional[str] = None
    nameType: Optional[str] = None
    organizationType: Optional[OrganizationType] = None
    status: Optional[OrganizationStateType] = None
    tradingName: Optional[str] = None
    organizationIdentification: Optional[List[OrganizationIdentification]] = field(
        default_factory=list
    )
    organizationChildRelationship: Optional[List[OrganizationChildRelationship]] = (
        field(default_factory=list)
    )
    organizationParentRelationship: Optional[OrganizationParentRelationship] = None
    otherName: Optional[List[OtherNameOrganization]] = field(default_factory=list)
    place: Optional[List[PlaceRef]] = field(default_factory=list)
    marketSegment: Optional[List[MarketSegmentRef]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        """Returns the endpoint path for organization operations (creation, retrieval, updates, deletions)."""
        return f"{context.api_base_url}/partyManagement/v5/organization"


@dataclass(repr=False)
class Consumer(PartyRole):
    pass


@dataclass(repr=False)
class Producer(PartyRole):
    pass


@dataclass(repr=False)
class Disability(Entity):
    disabilityCode: Optional[str] = None
    disabilityName: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class LanguageAbility(Entity):
    languageCode: Optional[str] = None
    languageName: Optional[str] = None
    isFavouriteLanguage: Optional[bool] = None
    writingProficiency: Optional[str] = None
    readingProficiency: Optional[str] = None
    speakingProficiency: Optional[str] = None
    listeningProficiency: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class Skill(Entity):
    skillCode: Optional[str] = None
    skillName: Optional[str] = None
    evaluatedLevel: Optional[str] = None
    comment: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class OtherNameIndividual(Entity):
    title: Optional[str] = None
    aristocraticTitle: Optional[str] = None
    generation: Optional[str] = None
    givenName: Optional[str] = None
    preferredGivenName: Optional[str] = None
    familyNamePrefix: Optional[str] = None
    familyName: Optional[str] = None
    legalName: Optional[str] = None
    middleName: Optional[str] = None
    fullName: Optional[str] = None
    formattedName: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class IndividualIdentification(Entity):
    identificationId: Optional[str] = None
    identificationType: Optional[str] = None
    issuingAuthority: Optional[str] = None
    issuingDate: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    attachment: Optional[Union[Attachment, AttachmentRef]] = None


@dataclass(repr=False)
class Individual(Party, BaseCRUDMixin):
    """Represents an Individual entity in the TM Forum Party Management API.

    This class models a person (as opposed to an organization), capturing details
    about personal attributes, legal names, birth information, and other
    identifying characteristics. An Individual may also reference one or more
    products or roles associated with them in the enterprise.

    Attributes:
        familyName (Optional[str]): The individual's family or last name.
        status (Optional[IndividualStateType]): Current lifecycle state of the individual (e.g., initialized, validated).
        aristocraticTitle (Optional[str]): A title indicating nobility or aristocratic standing, if applicable.
        birthDate (Optional[str]): The date of birth of the individual.
        countryOfBirth (Optional[str]): The country where the individual was born.
        deathDate (Optional[str]): The date of death of the individual, if applicable.
        familyNamePrefix (Optional[str]): A prefix for the family name (e.g., "van", "de").
        formattedName (Optional[str]): The individual's name in a fully formatted representation.
        gender (Optional[str]): The gender of the individual.
        generation (Optional[str]): A generational indicator (e.g., "Jr.", "Sr.").
        givenName (Optional[str]): The individual's given or first name.
        legalName (Optional[str]): The individual's officially recognized legal name.
        location (Optional[str]): A location descriptor (e.g., city, region) associated with the individual.
        maritalStatus (Optional[str]): Marital status (e.g., single, married).
        middleName (Optional[str]): Any middle name(s).
        name (Optional[str]): A general name field, if needed.
        nationality (Optional[str]): The individual's nationality or citizenship.
        placeOfBirth (Optional[str]): A location representing where the individual was born.
        preferredGivenName (Optional[str]): The individual's preferred first name if different from their official name.
        title (Optional[str]): A prefix title (e.g., "Mr.", "Ms.", "Dr.").
        disability (Optional[List[Disability]]): A list describing any disability classifications.
        skill (Optional[List[Skill]]): A list of skills the individual holds.
        languageAbility (Optional[List[LanguageAbility]]): A list describing language proficiencies.
        individualIdentification (Optional[List[IndividualIdentification]]): Various forms of identification (e.g., passport, driver’s license).
        otherName (Optional[List[OtherNameIndividual]]): Any additional or alternative names the individual may go by.

    Methods:
        get_resource_path(context: Context) -> str:
            Returns the endpoint path for individual operations
            (creation, retrieval, updates, deletions).

    Usage Example:
        person = Individual(
            familyName="Doe",
            givenName="John",
            status=IndividualStateType.ACTIVE,
            nationality="USA"
        )
        person = person.create(context)
        person = person.read(context)
    """

    familyName: Optional[str] = None
    status: Optional[IndividualStateType] = None
    aristocraticTitle: Optional[str] = None
    birthDate: Optional[str] = None
    countryOfBirth: Optional[str] = None
    deathDate: Optional[str] = None
    familyNamePrefix: Optional[str] = None
    formattedName: Optional[str] = None
    gender: Optional[str] = None
    generation: Optional[str] = None
    givenName: Optional[str] = None
    legalName: Optional[str] = None
    location: Optional[str] = None
    maritalStatus: Optional[str] = None
    middleName: Optional[str] = None
    name: Optional[str] = None
    nationality: Optional[str] = None
    placeOfBirth: Optional[str] = None
    preferredGivenName: Optional[str] = None
    title: Optional[str] = None
    disability: Optional[List[Disability]] = field(default_factory=list)
    skill: Optional[List[Skill]] = field(default_factory=list)
    languageAbility: Optional[List[LanguageAbility]] = field(default_factory=list)
    individualIdentification: Optional[List[IndividualIdentification]] = field(
        default_factory=list
    )
    otherName: Optional[List[OtherNameIndividual]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/partyManagement/v5/individual"


@dataclass(repr=False)
class BusinessPartner(PartyRole):
    pass


@dataclass(repr=False)
class Supplier(PartyRole):
    pass


@dataclass(repr=False)
class SalesNote(Entity):
    id: Optional[str] = None
    noteType: Optional[NoteTypeEnum] = None
    author: Optional[str] = None
    owner: Optional[str] = None
    date: Optional[str] = None
    text: Optional[str] = None
    title: Optional[str] = None
    attachment: Optional[List[Union[Attachment, AttachmentRef]]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class RevenueEstimate(Entity):
    amount: Optional[Money] = None
    description: Optional[str] = None
    revenueType: Optional[str] = None


@dataclass(repr=False)
class SalesLead(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    createOn: Optional[str] = None
    creationDate: Optional[str] = None
    estimatedRevenue: Optional[Money] = None
    lastUpdate: Optional[str] = None
    href: Optional[str] = None
    note: Optional[List[SalesNote]] = field(default_factory=list)
    attachment: Optional[List[Union[Attachment, AttachmentRef]]] = field(
        default_factory=list
    )
    priority: Optional[SalesLeadPriorityType] = None
    prospectContact: Optional[List[ContactMedium]] = field(default_factory=list)
    rating: Optional[str] = None
    referredDate: Optional[str] = None
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    salesOpportunity: Optional[List[SalesOpportunityRef]] = field(default_factory=list)
    channel: Optional[ChannelRef] = None
    characteristic: Optional[List[Characteristic]] = field(default_factory=list)
    status: Optional[SalesLeadStatusType] = None
    statusChangeDate: Optional[str] = None
    statusChangeReason: Optional[str] = None
    type: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    salesLeadType: Optional[str] = None
    revenueEstimate: Optional[List[RevenueEstimate]] = field(default_factory=list)
    marketingCampaign: Optional[MarketingCampaignRef] = None
    marketSegment: Optional[MarketSegmentRef] = None
    productOffering: Optional[List[ProductOfferingRef]] = field(default_factory=list)
    agreement: Optional[List[AgreementRef]] = field(default_factory=list)
    prospectContactMedium: Optional[List[ContactMedium]] = field(default_factory=list)
    productSpecification: Optional[List[ProductSpecificationRef]] = field(
        default_factory=list
    )
    category: Optional[CategoryRef] = None
    product: Optional[List[ProductRef]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/salesManagement/v5/salesLead"


@dataclass(repr=False)
class SalesOpportunityItem(Entity):
    id: Optional[str] = None
    action: Optional[str] = None
    rating: Optional[str] = None
    priority: Optional[SalesLeadPriorityType] = None
    salesOpportunityItemStatus: Optional[SalesOpportunityItemStateType] = None
    validFor: Optional[TimePeriod] = None
    product: Optional[ProductRef] = None
    productOffering: Optional[ProductOfferingRef] = None
    revenueEstimate: Optional[List[RevenueEstimate]] = field(default_factory=list)
    salesActivity: Optional[List[SalesActivityRef]] = field(default_factory=list)
    quoteItem: Optional[List[QuoteItemRef]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class SalesOpportunity(Entity, BaseCRUDMixin):
    """
    Represents a SalesOpportunity entity in the TM Forum TMF699 Sales Management API.

    A SalesOpportunity is a qualified potential for a sale, created when a prospect
    demonstrates a concrete and actionable interest. As a formal entry in the sales
    pipeline it is tracked with an estimated value, a timeline and a probability of
    success, and its lifecycle is managed through defined sales stages until it is
    won or lost.
    """

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creationDate: Optional[str] = None
    referredDate: Optional[str] = None
    rating: Optional[str] = None
    salesOpportunityType: Optional[str] = None
    status: Optional[SalesOpportunityStateType] = None
    statusChangeDate: Optional[str] = None
    statusChangeReason: Optional[str] = None
    priority: Optional[SalesLeadPriorityType] = None
    validFor: Optional[TimePeriod] = None
    category: Optional[CategoryRef] = None
    channel: Optional[ChannelRef] = None
    marketSegment: Optional[MarketSegmentRef] = None
    marketingCampaign: Optional[MarketingCampaignRef] = None
    salesLead: Optional[List[SalesLeadRef]] = field(default_factory=list)
    revenueEstimate: Optional[List[RevenueEstimate]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    agreement: Optional[List[AgreementRef]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    quote: Optional[List[QuoteRef]] = field(default_factory=list)
    salesProject: Optional[List[SalesProjectRef]] = field(default_factory=list)
    salesOpportunityItem: Optional[List[SalesOpportunityItem]] = field(
        default_factory=list
    )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/salesManagement/v5/salesOpportunity"


@dataclass(repr=False)
class Place(Entity):
    id: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    createOn: Optional[str] = None
    lastUpdate: Optional[str] = None
    href: Optional[str] = None


@dataclass(repr=False)
class GeographicAddress(Place):
    def __post_init__(self):
        raise NotImplementedError(f"{self.__class__.__name__} is not implemented yet.")


@dataclass(repr=False)
class GeographicLocation(Place):
    def __post_init__(self):
        raise NotImplementedError(f"{self.__class__.__name__} is not implemented yet.")


@dataclass(repr=False)
class GeographicSite(Place):
    def __post_init__(self):
        raise NotImplementedError(f"{self.__class__.__name__} is not implemented yet.")


@dataclass(repr=False)
class RelatedPlaceRefOrValue(Entity):
    role: Optional[str] = None
    place: Optional[
        Union[
            GeographicAddress,
            GeographicLocation,
            GeographicSite,
            PlaceRef,
        ]
    ] = None
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    _referred_type: Optional[str] = None


@dataclass(repr=False)
class RelatedPlaceRef(Entity):
    role: Optional[str] = None
    place: Optional[PlaceRef] = None


@dataclass(repr=False)
class RelatedPartyOrPartyRole(Entity):
    id: Optional[str] = None
    role: Optional[RoleEnum] = None
    partyOrPartyRole: Optional[
        Union[
            PartyRef,
            PartyRole,
            Organization,
            Consumer,
            Producer,
            Individual,
            BusinessPartner,
            Supplier,
            PartyRoleRef,
        ]
    ] = None


@dataclass(repr=False)
class Product(Entity, BaseCRUDMixin):
    """
    Represents a Product entity in the TM Forum TMF637 Product Inventory API.

    A Product is a representation of a tangible or intangible good or service that
    has been sold to or is otherwise in use by a customer. This class provides methods for creating, reading,
    updating, and deleting product records in the backend system, as well as specific
    actions like termination.

    Attributes:
        name (Optional[str]): The name of the product.
        billingAccount (Optional[BillingAccountRef]): A reference to a billing account associated with the product.
        status (Optional[ProductStatusType]): The current lifecycle status of the product (e.g., active, suspended).
        isBundle (bool): Indicates whether this product is a bundle of multiple products/services.
        quantity (Optional[int]): The number of items ordered for the product.
        productPrice (Optional[List[ProductPrice]]): A list of product prices applicable to this product.
        id (Optional[str]): The globally unique identifier of the product record.
        href (Optional[str]): A hyperlink reference to the product record.
        description (Optional[str]): A textual description of the product.
        creationDate (Optional[str]): The date when the product record was created.
        startDate (Optional[str]): The date when the product became active.
        terminationDate (Optional[str]): The date when the product will be (or was) terminated.
        productTerm (Optional[List[ProductTerm]]): Terms and conditions associated with the product.
        productOffering (Optional[ProductOfferingRef]): A reference to the product offering from which this product instance was derived.
        productRelationship (Optional[List[ProductRelationship]]): Relationships that define how this product interacts with others.
        productOrderItem (Optional[List[RelatedOrderItem]]): References to order items related to this product.
        isCustomerVisible (Optional[bool]): Indicates if the product should be visible to the customer.
        orderDate (Optional[str]): The date on which the product was ordered.
        realizingResource (Optional[List[ResourceRef]]): References to resources realized by this product.
        relatedParty (Optional[List[RelatedPartyOrPartyRole]]): Parties related to this product (e.g., customers, partners).
        realizingService (Optional[List[ServiceRef]]): Services realized by this product.
        productSerialNumber (Optional[str]): A serial number associated with the product instance.
        place (Optional[List[RelatedPlaceRefOrValue]]): References or values of places related to this product.
        agreementItem (Optional[List[AgreementItemRef]]): Agreement items that may affect the product.

    Raises:
        ValueError: If any required fields (name, billingAccount, status, quantity, productPrice) are missing
                    at instantiation or if a recurring charge product price is missing required fields.

    Methods:
        get_resource_path(context: Context) -> str:
            Returns the API endpoint path for product operations.

        terminate(context: Context) -> Product:
            Terminates the product by updating its status to 'terminated' in the backend system.

    Example:
        product = Product(
            name="Internet Service",
            billingAccount=BillingAccountRef(id="billing-account-123"),
            status=ProductStatusType.ACTIVE,
            isBundle=False,
            quantity=1,
            productPrice=[...]
        )
        product = product.create(context)
        product = product.terminate(context)
    """

    name: Optional[str] = None
    billingAccount: Optional[BillingAccountRef] = None
    status: Optional[ProductStatusType] = None
    isBundle: bool = False
    quantity: Optional[int] = None
    productPrice: Optional[List[ProductPrice]] = field(default_factory=list)
    id: Optional[str] = None
    href: Optional[str] = None
    description: Optional[str] = None
    createOn: Optional[str] = None
    startDate: Optional[str] = None
    terminationDate: Optional[str] = None
    lastUpdate: Optional[str] = None
    productTerm: Optional[List[ProductTerm]] = field(default_factory=list)
    productOffering: Optional[ProductOfferingRef] = None
    productRelationship: Optional[List[ProductRelationship]] = field(
        default_factory=list
    )
    productOrderItem: Optional[List[RelatedOrderItem]] = field(default_factory=list)
    isCustomerVisible: Optional[bool] = None
    orderDate: Optional[str] = None
    productCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    realizingResource: Optional[List[ResourceRef]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyOrPartyRole]] = field(default_factory=list)
    realizingService: Optional[List[ServiceRef]] = field(default_factory=list)
    productSerialNumber: Optional[str] = None
    place: Optional[List[RelatedPlaceRefOrValue]] = field(default_factory=list)
    externalId: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    agreementItem: Optional[List[AgreementItemRef]] = field(default_factory=list)
    product: Optional[List[Union[Product, ProductRef]]] = field(default_factory=list)
    intent: Optional[Union[Intent, IntentRef]] = None
    productSpecification: Optional[ProductSpecificationRef] = None
    creationDate: Optional[str] = None
    quantityInBundle: Optional[int] = None

    def __post_init__(self):
        super().__post_init__()
        if not self.name:
            raise ValueError("Product requires name to be defined at instantiation")
        #     if not self.status:
        #         raise ValueError("Product requires status to be defined at instantiation")
        # if not self.productPrice:
        #     raise ValueError(
        #         "Product requires productPrice to be defined at instantiation"
        #     )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/productInventory/v5/product"

    def terminate(self, context: Context) -> Product:
        if not self.id:
            context.logger.error(
                f"{self.__class__.__name__}.id is undefined. Please check the {self.__class__.__name__} has been created."
            )
            return self
        payload = {"status": ProductStatusType.TERMINATED.value}
        return self.update(payload, context)

    def suspend(self, context: Context, skip_proration: bool = False) -> Product:
        if not self.id:
            context.logger.error(
                f"{self.__class__.__name__}.id is undefined. Please check the {self.__class__.__name__} has been created."
            )
            return self
        payload = {"status": ProductStatusType.SUSPENDED.value}
        if skip_proration:
            payload["skipProration"] = True
        return self.update(payload, context)

    def resume(self, context: Context) -> Product:
        if not self.id:
            context.logger.error(
                f"{self.__class__.__name__}.id is undefined. Please check the {self.__class__.__name__} has been created."
            )
            return self
        payload = {"status": ProductStatusType.ACTIVE.value}
        return self.update(payload, context)

    def get_acbrs(self, context: Context) -> List[Optional[AppliedCustomerBillingRate]]:
        return AppliedCustomerBillingRate.query_get(
            path=f"product.id={self.id}", context=context
        )


@dataclass(repr=False)
class UsageVolumeProduct(Product):
    pass


@dataclass(repr=False)
class RatePlanProduct(Product):
    pass


@dataclass(repr=False)
class ProductValue(Product):
    pass


@dataclass(repr=False)
class BillingCycleSpecification(Entity, BaseCRUDMixin):
    billingCycleStartDay: Optional[int] = None
    frequency: Optional[BillingCycleSpecification_Frequency] = None
    name: Optional[str] = None
    description: Optional[str] = None
    billingDateShift: Optional[int] = None
    chargeDateOffset: Optional[int] = None
    creditDateOffset: Optional[int] = None
    mailingDateOffset: Optional[int] = None
    paymentDueDateOffset: Optional[int] = None
    billingPeriod: Optional[BillingCycleSpecification_BillingPeriod] = None
    validFor: Optional[TimePeriod] = None
    id: Optional[str] = None
    href: Optional[str] = None
    isDynamic: Optional[bool] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/accountManagement/v5/billingCycleSpecification"


@dataclass(repr=False)
class BillFormat(Entity):
    name: Optional[str] = None
    templateEngine: Optional[str] = None
    templateHref: Optional[str] = None
    basePresentationType: Optional[str] = None


@dataclass(repr=False)
class BillPresentationMedia(Entity):
    name: Optional[str] = None
    basePresentationType: Optional[str] = None


@dataclass(repr=False)
class BillStructure(Entity):
    format: Optional[
        Union[
            BillFormat,
            BillFormatRef,
        ]
    ] = None
    cycleSpecification: Optional[
        Union[
            BillingCycleSpecification,
            BillingCycleSpecificationRef,
        ]
    ] = None
    presentationMedia: Optional[
        List[
            Union[
                BillPresentationMedia,
                BillPresentationMediaRef,
            ]
        ]
    ] = field(default_factory=list)


@dataclass(repr=False)
class AccountBalance(Entity):
    amount: Optional[Money] = None
    balanceType: Optional[BalanceType] = None
    id: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class AccountRelationship(Entity):
    href: Optional[str] = None
    id: Optional[str] = None
    relationshipType: Optional[AccountRelationshipType] = None
    validFor: Optional[TimePeriod] = None
    account: Optional[AccountRef] = None


@dataclass(repr=False)
class Attachment(Entity):
    href: Optional[str] = None
    id: Optional[str] = None
    attachmentType: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    url: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    mimeType: Optional[str] = None
    size: Optional[Quantity] = None


@dataclass(repr=False)
class AttachmentRefOrValue(Attachment):
    """An attachment carried either by reference or by value (TMF652)."""

    isRef: Optional[bool] = None
    _referred_type: Optional[str] = None


@dataclass(repr=False)
class OpenGatewayURLAttachment(Attachment):
    pass


@dataclass(repr=False)
class OpenGatewayAllowedProductAction(AllowedProductAction):
    _target_product_order_item_schema: Optional[str] = None


@dataclass(repr=False)
class ContactMedium(Entity):
    contactType: Optional[ContactType] = None
    id: Optional[str] = None
    preferred: bool = True
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class EmailContactMedium(ContactMedium):
    emailAddress: Optional[str] = None


@dataclass(repr=False)
class PhoneContactMedium(ContactMedium):
    phoneNumber: Optional[str] = None


@dataclass(repr=False)
class FaxContactMedium(ContactMedium):
    faxNumber: Optional[str] = None


@dataclass(repr=False)
class SocialContactMedium(ContactMedium):
    socialNetworkId: Optional[str] = None


@dataclass(repr=False)
class GeographicAddressContactMedium(ContactMedium):
    city: Optional[str] = None
    country: Optional[str] = None
    postCode: Optional[str] = None
    stateOrProvince: Optional[str] = None
    street1: Optional[str] = None
    street2: Optional[str] = None
    geographicAddress: Optional[GeographicAddressRef] = None


@dataclass(repr=False)
class Contact(Entity):
    contactName: Optional[str] = None
    contactType: Optional[ContactType] = None
    id: Optional[str] = None
    partyRoleType: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    relatedParty: Optional[RelatedPartyRefOrPartyRoleRef] = None
    contactMedium: Optional[List[ContactMedium]] = field(default_factory=list)


@dataclass(repr=False)
class TaxDefinition(Entity):
    id: Optional[str] = None
    jurisdictionLevel: Optional[str] = None
    jurisdictionName: Optional[str] = None
    name: Optional[str] = None
    taxType: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class TaxExemptionCertificate(Entity):
    certificateNumber: Optional[str] = None
    id: Optional[str] = None
    issuingJurisdiction: Optional[str] = None
    reason: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    taxDefinition: Optional[List[TaxDefinition]] = field(default_factory=list)
    attachment: Optional[Union[Attachment, AttachmentRef]] = None


@dataclass(repr=False)
class Account(Entity):
    accountType: Optional[AccountType] = None
    creditLimit: Optional[Money] = None
    description: Optional[str] = None
    href: Optional[str] = None
    id: Optional[str] = None
    lastUpdate: Optional[str] = None
    name: Optional[str] = None
    state: Optional[AccountState] = None
    accountBalance: Optional[List[AccountBalance]] = field(default_factory=list)
    contact: Optional[List[Contact]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    taxExemption: Optional[List[TaxExemptionCertificate]] = field(default_factory=list)
    accountRelationship: Optional[List[AccountRelationship]] = field(
        default_factory=list
    )
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)


@dataclass(repr=False)
class PartyAccount(Account):
    paymentStatus: Optional[PaymentStatus] = None
    financialAccount: Optional[FinancialAccountRef] = None
    billStructure: Optional[BillStructure] = None
    paymentPlan: Optional[List[PaymentPlan]] = field(default_factory=list)
    defaultPaymentMethod: Optional[PaymentMethodRef] = None


@dataclass(repr=False)
class BillingAccount(PartyAccount, BaseCRUDMixin):
    ratingType: Optional[RatingType] = None
    generateEmptyBill: bool = False
    nextBillNo: Optional[str] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/accountManagement/v5/billingAccount"


@dataclass(repr=False)
class FinancialAccount(Account, BaseCRUDMixin):

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/accountManagement/v5/financialAccount"

    def activate(self, context: Context) -> FinancialAccount:
        payload = {"state": AccountState.ACTIVE.value}
        return self.update(payload, context)


@dataclass(repr=False)
class AppliedBillingTaxRate(Entity):
    taxAmount: Money
    taxCategory: TaxCategory
    taxRate: float
    id: Optional[str] = None


@dataclass(repr=False)
class AppliedCustomerBillingRate(Entity, BaseCRUDMixin):
    appliedBillingRateType: Optional[AppliedCustomerBillingRateType] = None
    date: Optional[str] = None
    name: Optional[str] = None
    periodCoverage: Optional[TimePeriod] = None
    taxExcludedAmount: Optional[Money] = None
    taxIncludedAmount: Optional[Money] = None
    billingAccount: Optional[BillingAccountRef] = None
    description: Optional[str] = None
    id: Optional[str] = None
    href: Optional[str] = None
    product: Optional[ProductRef] = None
    bill: Optional[CustomerBillRef] = None
    appliedTax: Optional[List[AppliedBillingTaxRate]] = field(default_factory=list)
    isBilled: bool = False

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/customerBill/v5/appliedCustomerBillingRate"


@dataclass(repr=False)
class ConfigurationPrice(Entity):
    description: Optional[str] = None
    name: Optional[str] = None
    priceType: Optional[PriceType] = None
    id: Optional[str] = None
    price: Optional[Price] = None
    priceAlteration: Optional[List[PriceAlteration]] = field(default_factory=list)
    productOfferingPrice: Optional[ProductOfferingPriceRef] = None
    unitOfMeasure: Optional[str] = None
    recurringChargePeriod: Optional[Quantity] = None


@dataclass(repr=False)
class ConfigurationTerm(Entity):
    description: Optional[str] = None
    duration: Optional[Duration] = None
    isSelectable: bool = True
    isSelected: bool = True
    name: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    id: Optional[str] = None
    productOfferingTerm: Optional[ProductOfferingTermRef] = None
    renewalAction: Optional[RenewalAction] = None
    delayStartTime: Optional[Duration] = None
    multipleExpiryNotificationPeriod: Optional[List[Duration]] = field(
        default_factory=list
    )
    termDurationExtensionStrategy: Optional[TermDurationExtensionStrategyEnum] = None
    autoRenewLimit: Optional[int] = None


@dataclass(repr=False)
class BundledProductOfferingOption(Entity):
    numberRelOfferDefault: Optional[int] = None
    numberRelOfferLowerLimit: Optional[int] = None
    numberRelOfferUpperLimit: Optional[int] = None


@dataclass(repr=False)
class BundledGroupProductOfferingOption(Entity):
    numberRelOfferLowerLimit: Optional[int] = None
    numberRelOfferUpperLimit: Optional[int] = None


@dataclass(repr=False)
class BundledProductOffering(ProductOfferingRef):
    bundledProductOfferingOption: Optional[BundledProductOfferingOption] = None


@dataclass(repr=False)
class BundledGroupProductOffering(Entity):
    id: Optional[str] = None
    name: Optional[str] = None
    bundledProductOffering: Optional[
        List[Union[BundledProductOffering, ProductOfferingRef]]
    ] = field(default_factory=list)
    bundledGroupProductOfferingOption: Optional[BundledGroupProductOfferingOption] = (
        None
    )
    bundledGroupProductOffering: Optional[List[BundledGroupProductOffering]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class Category(Entity, BaseCRUDMixin):
    description: Optional[str] = None
    categoryType: Optional[CategoryType] = None
    href: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    isRoot: bool = False
    lastUpdate: Optional[str] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    lifecycleStatus: Optional[CategoryLifecycleStatusType] = None
    parent: Optional[CategoryRef] = None
    productOffering: Optional[
        List[Union[ProductOfferingRef, BundledProductOffering]]
    ] = field(default_factory=list)
    productSpecification: Optional[List[ProductSpecificationRef]] = field(
        default_factory=list
    )
    subCategory: Optional[List[CategoryRef]] = field(default_factory=list)
    validFor: Optional[TimePeriod] = None
    version: Optional[str] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/productCatalogManagement/v5/category"


@dataclass(repr=False)
class ProductCatalog(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    catalogSubType: Optional[CatalogSubType] = None
    catalogType: Optional[str] = None
    category: Optional[List[CategoryRef]] = field(default_factory=list)
    createOn: Optional[str] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    lastUpdate: Optional[str] = None
    lifecycleStatus: Optional[ProductCatalogLifecycleStatusType] = None
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    validFor: Optional[TimePeriod] = None
    version: Optional[str] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/productCatalogManagement/v5/productCatalog"


@dataclass(repr=False)
class ConfigurationAction(Entity):
    action: Optional[ProductActionType] = None
    description: Optional[str] = None
    isSelected: bool = True


@dataclass(repr=False)
class ConfigurationCharacteristicRelationship(Entity):
    id: Optional[str] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class ConfigurationCharacteristicValue(Entity):
    id: Optional[str] = None
    characteristicValue: Optional[Characteristic] = None
    isSelectable: Optional[bool] = None
    isSelected: Optional[bool] = None
    rangeInterval: Optional[str] = None
    regex: Optional[str] = None
    unitOfMeasure: Optional[str] = None
    valueFrom: Optional[float] = None
    valueTo: Optional[float] = None


@dataclass(repr=False)
class ConfigurationCharacteristic(Entity):
    configurationCharacteristicRelationship: Optional[
        List[ConfigurationCharacteristicRelationship]
    ] = field(default_factory=list)
    configurationCharacteristicValue: Optional[
        List[ConfigurationCharacteristicValue]
    ] = field(default_factory=list)
    description: Optional[str] = None
    id: Optional[str] = None
    isConfigurable: Optional[bool] = None
    maxCardinality: Optional[int] = None
    minCardinality: Optional[int] = None
    name: Optional[str] = None
    regex: Optional[str] = None
    valueType: Optional[str] = None


@dataclass(repr=False)
class ProductConfiguration(Entity):
    id: Optional[str] = None
    isSelectable: bool = True
    isSelected: bool = True
    isVisible: bool = True
    quantity: Optional[int] = None
    quantityInBundle: Optional[int] = None
    version: Optional[str] = None
    configurationAction: Optional[List[ConfigurationAction]] = field(
        default_factory=list
    )
    product: Optional[Union[Product, ProductRef]] = None
    productOffering: Optional[
        Union[
            ProductOfferingRef,
            BundledProductOffering,
        ]
    ] = None
    bundledProductOfferingOption: Optional[BundledProductOfferingOption] = None
    bundledGroupProductOffering: Optional[BundledGroupProductOffering] = None
    productSpecification: Optional[ProductSpecificationRef] = None
    configurationPrice: Optional[List[ConfigurationPrice]] = field(default_factory=list)
    configurationTerm: Optional[List[ConfigurationTerm]] = field(default_factory=list)
    configurationCharacteristic: Optional[List[ConfigurationCharacteristic]] = field(
        default_factory=list
    )
    policy: Optional[List[PolicyRef]] = field(default_factory=list)
    productConfiguration: Optional[List[ProductConfiguration]] = field(
        default_factory=list
    )

    def __post_init__(self):
        super().__post_init__()
        if not self.configurationAction:
            raise ValueError(
                "ProductConfiguration requires a configurationAction to be defined at instantiation."
            )


@dataclass(repr=False)
class StateReason(Entity):
    code: Optional[str] = None
    label: Optional[str] = None


@dataclass(repr=False)
class ProductConfigurationItemRelationship(Entity):
    id: Optional[str] = None
    relationshipType: Optional[ProductRelationshipType] = None


@dataclass(repr=False)
class CheckProductConfigurationItem(Entity):
    id: Optional[str] = None
    state: Optional[CheckProductConfigurationItemState] = None
    stateReason: Optional[List[StateReason]] = field(default_factory=list)
    productConfiguration: Optional[ProductConfiguration] = None
    alternateProductConfigurationProposal: Optional[List[ProductConfiguration]] = field(
        default_factory=list
    )
    productConfigurationItemRelationship: Optional[
        List[ProductConfigurationItemRelationship]
    ] = field(default_factory=list)
    productConfigurationItem: Optional[List[CheckProductConfigurationItem]] = field(
        default_factory=list
    )
    contextItem: Optional[ItemRef] = None

    def __post_init__(self):
        super().__post_init__()
        if not self.id:
            raise ValueError(
                "CheckProductConfigurationItem requires an id to be defined at instantiation"
            )


@dataclass(repr=False)
class CheckProductConfiguration(Entity):
    href: Optional[str] = None
    id: Optional[str] = None
    instantSync: bool = True
    provideAlternatives: bool = False
    state: Optional[TaskStateType] = None
    contextCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    channel: Optional[ChannelRef] = None
    checkProductConfigurationItem: Optional[List[CheckProductConfigurationItem]] = (
        field(default_factory=list)
    )
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    contextEntity: Optional[EntityRef] = None

    @classmethod
    def from_order(cls, product_order: ProductOrder) -> CheckProductConfiguration:
        order_ref = ProductOrderRef.from_entity(entity=product_order)

        channel = None
        if product_order.channel:
            channel = product_order.channel[0].channel

        cpc_items = []
        for order_item in product_order.productOrderItem:
            item_relationships = []
            for item_relationship in order_item.productOrderItemRelationship:
                item_relationships.append(
                    ProductConfigurationItemRelationship(
                        id=item_relationship.id,
                        relationshipType=ProductRelationshipType(
                            item_relationship.relationshipType.value
                        ),
                    ),
                )
            item_terms = []
            for item_term in order_item.orderTerm:
                item_terms.append(
                    ConfigurationTerm(
                        description=item_term.description,
                        duration=item_term.duration,
                        name=item_term.name,
                    ),
                )
            item_prices = []
            for order_price in order_item.itemPrice:
                item_prices.append(
                    ConfigurationPrice(
                        description=order_price.description,
                        name=order_price.name,
                        priceType=order_price.priceType,
                        productOfferingPrice=order_price.productOfferingPrice,
                        price=order_price.price,
                        priceAlteration=order_price.priceAlteration,
                        unitOfMeasure=order_price.unitOfMeasure,
                        recurringChargePeriod=order_price.recurringChargePeriod.to_quantity(),
                    )
                )
            product_value = None
            if order_item.product:
                product_value = Product.from_dict(order_item.product.to_dict())
                product_value.billingAccount = product_order.billingAccount
            cpc_item = CheckProductConfigurationItem(
                id=order_item.id,
                contextItem=ProductOrderItemRef.from_entity(order_item),
                productConfigurationItemRelationship=item_relationships,
                productConfiguration=ProductConfiguration(
                    quantity=order_item.quantity,
                    quantityInBundle=order_item.quantityInBundle,
                    configurationAction=[
                        ConfigurationAction(
                            action=ProductActionType(order_item.action.value),
                        )
                    ],
                    configurationTerm=item_terms,
                    configurationPrice=item_prices,
                    productOffering=order_item.productOffering,
                    product=product_value,
                ),
            )
            cpc_items.append(cpc_item)

        cpc = CheckProductConfiguration(
            channel=channel,
            contextEntity=order_ref,
            relatedParty=product_order.relatedParty,
            checkProductConfigurationItem=cpc_items,
        )
        return cpc


@dataclass(repr=False)
class OrderTerm(Entity):
    description: Optional[str] = None
    duration: Optional[Duration] = None
    id: Optional[str] = None
    name: Optional[str] = None


@dataclass(repr=False)
class OrderPrice(Entity):
    description: Optional[str] = None
    name: Optional[str] = None
    priceType: Optional[PriceType] = None
    recurringChargePeriod: Optional[RecurringChargePeriod] = None
    chargeType: Optional[ChargeType] = None
    unitOfMeasure: Optional[str] = None
    productOfferingPrice: Optional[ProductOfferingPriceRef] = None
    price: Optional[Price] = None
    priceAlteration: Optional[List[PriceAlteration]] = field(default_factory=list)


@dataclass(repr=False)
class OrderItemRelationship(Entity):
    id: Optional[str] = None
    relationshipType: Optional[ProductOrderItemRelationshipType] = None


@dataclass(repr=False)
class ProductOrderItem(Entity):
    action: Optional[ItemActionType] = None
    id: Optional[str] = None
    quantity: Optional[int] = None
    quantityInBundle: Optional[int] = None
    state: Optional[ProductOrderItemStateType] = None
    orderTerm: Optional[List[OrderTerm]] = field(default_factory=list)
    quoteItem: Optional[QuoteItemRef] = None
    productOffering: Optional[ProductOfferingRef] = None
    productOfferingQualificationItem: Optional[ProductOfferingQualificationItemRef] = (
        None
    )
    note: Optional[List[Note]] = field(default_factory=list)
    payment: Optional[List[PaymentRef]] = field(default_factory=list)
    billingAccount: Optional[BillingAccountRef] = None
    itemPrice: Optional[List[OrderPrice]] = field(default_factory=list)
    itemTotalPrice: Optional[List[OrderPrice]] = field(default_factory=list)
    product: Optional[Union[Product, ProductRef]] = None
    qualification: Optional[List[ProductOfferingQualificationRef]] = field(
        default_factory=list
    )
    appointment: Optional[AppointmentRef] = None
    productOrderItemRelationship: Optional[List[OrderItemRelationship]] = field(
        default_factory=list
    )
    productOrderItem: Optional[List[ProductOrderItem]] = field(default_factory=list)


@dataclass(repr=False)
class RelatedChannel(Entity):
    role: Optional[str] = None
    channel: Optional[ChannelRef] = None


@dataclass(repr=False)
class Milestone(Entity):
    description: Optional[str] = None
    id: Optional[str] = None
    message: Optional[str] = None
    milestoneDate: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None


@dataclass(repr=False)
class ProductOrderMilestone(Milestone):
    productOrderItem: Optional[List[ProductOrderItemRef]] = field(default_factory=list)


@dataclass(repr=False)
class OrderRelationship(Entity):
    href: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class ErrorMessage(Entity):
    code: Optional[str] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    referenceError: Optional[str] = None
    status: Optional[str] = None


@dataclass(repr=False)
class ProductOrderErrorMessage(ErrorMessage):
    productOrderItem: Optional[List[ProductOrderItemRef]] = field(default_factory=list)


@dataclass(repr=False)
class JeopardyAlert(Entity):
    alertDate: Optional[str] = None
    exception: Optional[str] = None
    id: Optional[str] = None
    jeopardyType: Optional[str] = None
    message: Optional[str] = None
    name: Optional[str] = None


@dataclass(repr=False)
class ProductOrderJeopardyAlert(JeopardyAlert):
    productOrderItem: Optional[List[ProductOrderItemRef]] = field(default_factory=list)


@dataclass(repr=False)
class ProductOrder(Entity, BaseCRUDMixin):
    cancellationDate: Optional[str] = None
    cancellationReason: Optional[str] = None
    category: Optional[str] = None
    completionDate: Optional[str] = None
    creationDate: Optional[str] = None
    createOn: Optional[str] = None
    lastUpdate: Optional[str] = None
    description: Optional[str] = None
    expectedCompletionDate: Optional[str] = None
    href: Optional[str] = None
    id: Optional[str] = None
    notificationContact: Optional[str] = None
    priority: Optional[PriorityType] = None
    requestedCompletionDate: Optional[str] = None
    requestedInitialState: Optional[InitialProductOrderStateType] = None
    requestedStartDate: Optional[str] = None
    state: Optional[ProductOrderStateType] = None
    orderTotalPrice: Optional[List[OrderPrice]] = field(default_factory=list)
    billingAccount: Optional[BillingAccountRef] = None
    productOrderMilestone: Optional[List[ProductOrderMilestone]] = field(
        default_factory=list
    )
    productOfferingQualification: Optional[List[ProductOfferingQualificationRef]] = (
        field(default_factory=list)
    )
    orderRelationship: Optional[List[OrderRelationship]] = field(default_factory=list)
    productOrderErrorMessage: Optional[List[ProductOrderErrorMessage]] = field(
        default_factory=list
    )
    productOrderJeopardyAlert: Optional[List[ProductOrderJeopardyAlert]] = field(
        default_factory=list
    )
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    channel: Optional[List[RelatedChannel]] = field(default_factory=list)
    productOrderItem: Optional[List[ProductOrderItem]] = field(default_factory=list)
    quote: Optional[List[QuoteRef]] = field(default_factory=list)
    agreement: Optional[List[AgreementRef]] = field(default_factory=list)
    payment: Optional[List[PaymentRef]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/productOrdering/v5/productOrder"

    def product_to_terminate(self, product: Product, context: Context):
        if not self.id:
            context.logger.error(
                f"{self.__class__.__name__}.id is undefined. Please check the {self.__class__.__name__} has been created."
            )
            return self
        if not product.id:
            context.logger.error(
                f"Cannot update order {self.id}: product id is undefined."
            )
            return self
        for order_item in self.productOrderItem:
            if order_item.product.id == product.id:
                payload = [
                    {
                        "op": "replace",
                        "value": ProductStatusType.TERMINATED.value,
                        "path": f"productOrderItem[?(@.id=='{order_item.id}')].product.status",
                    },
                    {
                        "op": "replace",
                        "value": ItemActionType.DELETE.value,
                        "path": f"productOrderItem[?(@.id=='{order_item.id}')].action",
                    },
                ]
                context.logger.info(f"Setting product {product.id} to terminate.")
                return self.query_update(payload=payload, context=context)
        context.logger.warning(
            f"Product with id {product.id} not found in order {self.id}"
        )
        return self


@dataclass(repr=False)
class RelatedParty(Entity):
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    partyOrPartyRole: Optional[Union[PartyRef, PartyRoleRef]] = None


@dataclass(repr=False)
class Authorization(Entity):
    id: Optional[str] = None
    approver: Optional[List[RelatedParty]] = None
    givenDate: Optional[str] = None
    name: Optional[str] = None
    requestedDate: Optional[str] = None
    signatureRepresentation: Optional[str] = None
    status: Optional[str] = None


@dataclass(repr=False)
class Quote(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    agreement: Optional[List[AgreementRef]] = field(default_factory=list)
    approvalWorkflowId: Optional[str] = None
    attachment: Optional[List[Union[Attachment, AttachmentRef]]] = field(
        default_factory=list
    )
    authorization: Optional[List[Authorization]] = field(default_factory=list)
    billingAccount: Optional[List[BillingAccountRef]] = field(default_factory=list)
    category: Optional[str] = None
    contactMedium: Optional[List[ContactMedium]] = field(default_factory=list)
    creationDate: Optional[str] = None
    currency: Optional[str] = None
    effectiveQuoteCompletionDate: Optional[str] = None
    expectedFulfillmentStartDate: Optional[str] = None
    expectedQuoteCompletionDate: Optional[str] = None
    externalId: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    instantSyncQuote: Optional[bool] = None
    note: Optional[List[Note]] = field(default_factory=list)
    place: Optional[List[PlaceRef]] = field(default_factory=list)
    productOfferingQualification: Optional[List[ProductOfferingQualificationRef]] = (
        field(default_factory=list)
    )
    quoteItem: Optional[List[QuoteItem]] = field(default_factory=list)
    quoteTotalPrice: Optional[List[QuotePrice]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    requestedQuoteCompletionDate: Optional[str] = None
    state: Optional[QuoteStateTypeEnum] = None
    validFor: Optional[TimePeriod] = None
    version: Optional[str] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/quoteManagement/v5/quote"


@dataclass(repr=False)
class QuoteItem(Entity):
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    action: Optional[ItemActionType] = None
    appointment: Optional[List[AppointmentRef]] = field(default_factory=list)
    attachment: Optional[List[Union[Attachment, AttachmentRef]]] = field(
        default_factory=list
    )
    note: Optional[List[Note]] = field(default_factory=list)
    product: Optional[Union[ProductValue, ProductRef]] = None
    productOffering: Optional[ProductOfferingRef] = None
    productOfferingQualificationItem: Optional[ProductOfferingQualificationItemRef] = (
        None
    )
    quantity: Optional[int] = None
    quantityInBundle: Optional[int] = None
    quoteItem: Optional[List[QuoteItem]] = field(default_factory=list)
    quoteItemAuthorization: Optional[List[Authorization]] = field(default_factory=list)
    quoteItemPrice: Optional[List[QuotePrice]] = field(default_factory=list)
    quoteItemRelationship: Optional[List[QuoteItemRelationship]] = field(
        default_factory=list
    )
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)
    state: Optional[str] = None


@dataclass(repr=False)
class QuotePrice(Entity):
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Price] = None
    priceAlteration: Optional[List[PriceAlteration]] = field(default_factory=list)
    priceType: Optional[PriceType] = None
    productOfferingPrice: Optional[ProductOfferingPriceRef] = None
    recurringChargePeriod: Optional[RecurringChargePeriod] = None
    unitOfMeasure: Optional[str] = None


@dataclass(repr=False)
class QuoteItemRelationship(Entity):
    id: Optional[str] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class PolicyManagedEntity(Entity, BaseCRUDMixin):
    """Fields required for managed (reusable) Policy entities"""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    lifecycleState: Optional[PolicyEntityLifecycleState] = None
    validFor: Optional[TimePeriod] = None
    note: Optional[List[Note]] = field(default_factory=list)


@dataclass(repr=False)
class Note(Entity):
    id: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    text: Optional[str] = None


@dataclass(repr=False)
class PolicyActionAtomic(Entity):
    constraint: Optional[
        Union[
            PolicyConditionAtomic,
            PolicyConditionComposite,
            PolicyConstraintRef,
            PolicyEventConstraint,
        ]
    ] = None
    executedAt: Optional[List[ExecutedAtEnum]] = field(default_factory=list)
    action: Optional[Union[PolicyExpression, PolicyExpressionRef]] = None
    actionType: Optional[PolicyActionType] = None


@dataclass(repr=False)
class PolicyActionComposite(Entity):
    constraint: Optional[
        Union[
            PolicyConditionAtomic,
            PolicyConditionComposite,
            PolicyConstraintRef,
            PolicyEventConstraint,
        ]
    ] = None
    executedAt: Optional[List[ExecutedAtEnum]] = field(default_factory=list)
    action: Optional[List[PolicyActionRelationship]] = field(default_factory=list)
    actionType: Optional[PolicyActionType] = None


@dataclass(repr=False)
class PolicyActionRelationship(Entity):
    priority: Optional[int] = None
    constraint: Optional[
        Union[
            PolicyConditionAtomic,
            PolicyConditionComposite,
            PolicyConstraintRef,
            PolicyEventConstraint,
        ]
    ] = None
    policyActionRefOrValue: Optional[
        Union[
            PolicyActionAtomic,
            PolicyActionComposite,
            PolicyActionRef,
        ]
    ] = None


@dataclass(repr=False)
class PolicyConditionAtomic(Entity):
    """PolicyCondition that executes only one statement"""

    isResultNegated: bool = False
    conditionType: Optional[PolicyConditionType] = None
    evaluationResult: Optional[bool] = None
    explanation: Optional[str] = None
    statement: Optional[
        Union[
            PolicyExpression,
            PolicyExpressionRef,
            PolicyOperator,
            PolicyOperatorRef,
        ]
    ] = None


@dataclass(repr=False)
class PolicyConditionComposite(Entity):
    """PolicyCondition that executes one or many PolicyConditions, applying condition combination
    logic
    """

    isResultNegated: bool = False
    conditionType: Optional[PolicyConditionType] = None
    evaluationResult: Optional[bool] = None
    explanation: Optional[str] = None
    conditionCombinationLogic: Optional[PolicyConditionCombinationType] = None
    condition: Optional[
        List[
            Union[
                PolicyConditionAtomic,
                PolicyConditionComposite,
                PolicyConditionRef,
            ]
        ]
    ] = field(default_factory=list)


@dataclass(repr=False)
class PolicyDomain(PolicyManagedEntity):
    scopedManagedEntity: Optional[List[EntityRef]] = field(default_factory=list)
    subDomainRef: Optional[List[EntityRef]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/policyManagement/v5/policyDomain"


@dataclass(repr=False)
class PolicyEventAtomicBase(Entity):
    """A PolicyEventAtomic is an occurrence of a single atomic event. It must be used as a abstract
    class overloaded by a particular event in TMF API domain for which Policy is defined
    """


@dataclass(repr=False)
class PolicyEventComposite(Entity):
    """A PolicyEventComposite is an event made of multiple PolicyEvents"""

    policyEventRelationship: Optional[List[PolicyEventRelationship]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class PolicyEventConstraint(Entity):
    """Constraint based on provided list of PolicyEvent references. If PolicyEvent type is found in
    the list then constraint is evaluated TRUE
    """

    policyEventType: Optional[List[str]] = field(default_factory=list)


@dataclass(repr=False)
class PolicyEventRelationship(Entity):
    priority: Optional[int] = None
    constraint: Optional[
        Union[
            PolicyConditionAtomic,
            PolicyConditionComposite,
            PolicyConstraintRef,
            PolicyEventConstraint,
        ]
    ] = None
    policyEventRefOrValue: Optional[
        Union[
            PolicyEventAtomicBase,
            PolicyEventComposite,
            PolicyEventRef,
        ]
    ] = None


@dataclass(repr=False)
class PolicyExpression(Entity):
    """PolicyExpression is a constraint based on text expression and parsed by an Expression
    Language (SpEL, JS, Groovy, FEEL, ...)
    """

    name: Optional[str] = None
    expression: Optional[str] = None
    expressionLanguage: Optional[str] = None
    lifecycleState: Optional[PolicyEntityLifecycleState] = None


@dataclass(repr=False)
class PolicyRelationship(Entity):
    priority: Optional[int] = None
    constraint: Optional[
        Union[
            PolicyConditionAtomic,
            PolicyConditionComposite,
            PolicyConstraint,
            PolicyConstraintRef,
            PolicyEventConstraint,
        ]
    ] = None
    policyRefOrValue: Optional[
        Union[
            PolicyRef,
            PolicyRule,
            PolicySet,
        ]
    ] = None


@dataclass(repr=False)
class PolicyOperator(Entity):
    name: Optional[str] = None
    variable: Optional[
        Union[
            PolicyVariableStatic,
            PolicyVariableDynamic,
        ]
    ] = None


@dataclass(repr=False)
class PolicyRule(Entity):
    """A PolicyRule is an intelligent data container. It contains data that define how the
    PolicyRule is used in a managed environment as well as a specification of behavior that
    dictates how the managed entities that it applies to will interact. The contained data
    is of four types:
     * data and metadata that define the semantics and behavior of the policy rule and the behavior that it imposes on the rest of the system,
     * a group of events that can be used to trigger the evaluation of the condition clause of a policy rule,
     * a group of conditions aggregated by the PolicyRule,
     * group of actions aggregated by the PolicyRule.
    """

    actionExecutionStrategy: Optional[PolicyExecutionStrategy] = None
    sequencedActions: Optional[PolicySequenceType] = None
    priority: Optional[int] = None
    policyDomainRef: Optional[List[PolicyDomainRef]] = field(default_factory=list)
    policyEventRelationship: Optional[List[PolicyEventRelationship]] = field(
        default_factory=list
    )
    policyActionRelationship: Optional[List[PolicyActionRelationship]] = field(
        default_factory=list
    )
    targetPolicyEffect: Optional[PolicyEffect] = None
    policyConditionRefOrValue: Optional[
        Union[
            PolicyConditionAtomic,
            PolicyConditionComposite,
            PolicyConditionRef,
            PolicyEventConstraint,
        ]
    ] = None


@dataclass(repr=False)
class PolicySet(Entity, BaseCRUDMixin):
    """A PolicySet is an aggregation of PolicyRules or PolicySets combined according to
    provided algorithm
    """

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    actionExecutionStrategy: Optional[PolicyExecutionStrategy] = None
    sequencedActions: Optional[PolicySequenceType] = None
    priority: Optional[int] = None
    lifecycleState: Optional[PolicyEntityLifecycleState] = None
    policyDomainRef: Optional[List[PolicyDomainRef]] = field(default_factory=list)
    policyEventRelationship: Optional[List[PolicyEventRelationship]] = field(
        default_factory=list
    )
    policyActionRelationship: Optional[List[PolicyActionRelationship]] = field(
        default_factory=list
    )
    combiningAlgorithm: Optional[PolicyCombiningAlgorithm] = None
    policyRelationship: Optional[List[PolicyRelationship]] = field(default_factory=list)


@dataclass(repr=False)
class ManagedPolicy(PolicySet):

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/policyManagement/v5/managedPolicy"


@dataclass(repr=False)
class PolicyVariableDynamic(Entity):
    """A variable that is resolved from event, environment or subject"""

    valueType: Optional[PolicyVariableValueType] = None
    format: Optional[str] = None
    resolver: Optional[List[PolicyVariableResolver]] = field(default_factory=list)


@dataclass(repr=False)
class PolicyVariableResolver(Entity):
    """A PolicyVariableResolver is a definition that describes from where is DynamicVariable
    fetched
    """

    source: Optional[SourceEnum] = None
    path: Optional[str] = None
    priority: Optional[int] = None
    constraint: Optional[
        Union[
            PolicyConditionAtomic,
            PolicyConditionComposite,
            PolicyConstraintRef,
            PolicyEventConstraint,
        ]
    ] = None


@dataclass(repr=False)
class PolicyVariableStatic(Entity):
    name: Optional[str] = None
    valueType: Optional[str] = None
    value: Any = None

    def __post_init__(self):
        if self.value is not None and self.valueType is not None:
            actual_class_name = self.value.__class__.__name__
            if actual_class_name == "list" and self.valueType == "array":
                return
            if actual_class_name == "int" and self.valueType == "integer":
                return
            if actual_class_name == "str" and self.valueType == "string":
                return
            if actual_class_name != self.valueType:
                raise ValueError(
                    f"Value type mismatch: expected '{self.valueType}' but got '{actual_class_name}' "
                    f"for value of type {type(self.value)}"
                )


@dataclass(repr=False)
class PolicyConstraint(Entity):
    isResultNegated: bool = False
    statement: Optional[
        Union[
            PolicyExpression,
            PolicyExpressionRef,
            PolicyOperator,
            PolicyOperatorRef,
        ]
    ] = None


@dataclass(repr=False)
class ManagedPolicyVariable(PolicyVariableStatic, PolicyManagedEntity):
    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/policyManagement/v5/managedPolicyVariable"


@dataclass(repr=False)
class PolicyCatalog(PolicyManagedEntity):
    policyDomainFilter: Optional[List[PolicyDomainRef]] = field(default_factory=list)
    policy: Optional[List[PolicyRef]] = field(default_factory=list)
    policyEvent: Optional[List[PolicyEventRef]] = field(default_factory=list)
    policyCondition: Optional[List[PolicyConditionRef]] = field(default_factory=list)
    policyExpression: Optional[List[PolicyExpressionRef]] = field(default_factory=list)
    policyOperator: Optional[List[PolicyOperatorRef]] = field(default_factory=list)
    policyVariable: Optional[List[PolicyVariableRef]] = field(default_factory=list)
    policyAction: Optional[List[PolicyActionRef]] = field(default_factory=list)
    policyConstraint: Optional[List[PolicyConstraintRef]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/policyManagement/v5/policyCatalog"

    def append_policy_variable(
        self, policy_variable: ManagedPolicyVariable, context: Context
    ) -> PolicyCatalog:
        self.policyVariable.append(PolicyVariableRef.from_entity(policy_variable))
        catalog = self.update(
            payload={"policyVariable": [var.to_dict() for var in self.policyVariable]},
            context=context,
        )
        return catalog


@dataclass(repr=False)
class Feature(Entity):
    id: Optional[str] = None
    name: Optional[str] = None
    isBundle: Optional[bool] = None
    isEnabled: Optional[bool] = None
    name: Optional[str] = None
    constraint: Optional[List[ConstraintRef]] = field(default_factory=list)
    featureCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    featureRelationship: Optional[List[FeatureRelationship]] = field(
        default_factory=list
    )
    policyConstraint: Optional[List[PolicyRef]] = field(default_factory=list)


@dataclass(repr=False)
class FeatureRelationship(Entity):
    id: Optional[str] = None
    name: Optional[str] = None
    href: Optional[str] = None
    relationshipType: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class FeatureSpecificationRelationship(Entity):
    """Relationship between feature specifications (dependency, exclusivity, aggregation)."""

    relationshipType: Optional[str] = None
    featureId: Optional[str] = None
    parentSpecificationId: Optional[str] = None
    parentSpecificationHref: Optional[str] = None
    name: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class FeatureSpecificationCharacteristicRelationship(Entity):
    """Relationship between characteristics of feature specifications."""

    characteristicId: Optional[str] = None
    featureId: Optional[str] = None
    name: Optional[str] = None
    relationshipType: Optional[str] = None
    resourceSpecificationHref: Optional[str] = None
    resourceSpecificationId: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class FeatureSpecificationCharacteristic(CharacteristicSpecification):
    """Characteristic of a feature specification."""

    featureSpecCharRelationship: Optional[
        List[FeatureSpecificationCharacteristicRelationship]
    ] = field(default_factory=list)
    featureSpecCharacteristicValue: Optional[List[CharacteristicValueSpecification]] = (
        field(default_factory=list)
    )


@dataclass(repr=False)
class FeatureSpecification(Entity):
    """Specification for an entity feature."""

    version: Optional[str] = None
    id: Optional[str] = None
    isBundle: Optional[bool] = None
    validFor: Optional[TimePeriod] = None
    featureSpecRelationship: Optional[List[FeatureSpecificationRelationship]] = field(
        default_factory=list
    )
    policyConstraint: Optional[List[PolicyRef]] = field(default_factory=list)
    isEnabled: Optional[bool] = None
    featureSpecCharacteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )
    constraint: Optional[List[ConstraintRef]] = field(default_factory=list)
    name: Optional[str] = None


@dataclass(repr=False)
class RelatedResourceOrderItem(Entity):
    _referred_type: Optional[str] = None
    resourceOrderHref: Optional[str] = None
    resourceOrderId: Optional[str] = None
    itemAction: Optional[OrderItemActionType] = None
    itemId: Optional[str] = None
    role: Optional[str] = None


@dataclass(repr=False)
class ResourceRelationship(EntityRef):
    _referred_type: Optional[str] = "Resource"
    resourceRelationshipCharacteristic: Optional[List[Characteristic]] = field(
        default_factory=list
    )
    resource: Optional[Union[Resource, ResourceRef]] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class Resource(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    href: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    endOperatingDate: Optional[str] = None
    startOperatingDate: Optional[str] = None
    resourceVersion: Optional[str] = None
    administrativeState: Optional[ResourceAdministrativeStateType] = None
    operationalState: Optional[ResourceOperationalStateType] = None
    resourceStatus: Optional[ResourceStatusType] = None
    usageState: Optional[ResourceUsageStateType] = None
    validFor: Optional[TimePeriod] = None
    note: Optional[List[Note]] = field(default_factory=list)
    place: Optional[List[RelatedPlaceRef]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    resourceRelationship: Optional[List[ResourceRelationship]] = field(
        default_factory=list
    )
    resourceCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    attachment: Optional[List[AttachmentRef]] = field(default_factory=list)
    resourceSpecification: Optional[ResourceSpecificationRef] = None
    activationFeature: Optional[List[Feature]] = field(default_factory=list)
    intent: Optional[IntentRef] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    supportingResource: Optional[List[Union["Resource", ResourceRef]]] = field(
        default_factory=list
    )
    resourceOrderItem: Optional[List[RelatedResourceOrderItem]] = field(
        default_factory=list
    )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceInventory/v5/resource"


@dataclass(repr=False)
class LogicalResource(Resource):
    value: Optional[str] = None


@dataclass(repr=False)
class PhysicalResource(Resource):
    manufactureDate: Optional[str] = None
    powerState: Optional[str] = None
    serialNumber: Optional[str] = None
    versionNumber: Optional[str] = None


@dataclass(repr=False)
class ResourceCollection(Resource):
    containedResource: Optional[List[Union[Resource, ResourceRef]]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class TaskResource(Entity):
    """Base class for task resources (e.g. AvailabilityCheck, Extract, Push)."""

    id: Optional[str] = None
    href: Optional[str] = None
    state: Optional[TaskStateType] = None
    errorMessage: Optional[List[ErrorMessage]] = field(default_factory=list)


@dataclass(repr=False)
class AvailabilityCheck(TaskResource):
    """Availability check task for a resource pool (TMF685)."""

    capacityDemand: Optional[Capacity] = None
    capacityOption: Optional[List[Capacity]] = field(default_factory=list)


@dataclass(repr=False)
class Push(TaskResource):
    """Push task for a resource pool (TMF685)."""

    pushedResource: Optional[List[ResourceRef]] = field(default_factory=list)


@dataclass(repr=False)
class Extract(TaskResource):
    """Extract task for a resource pool (TMF685)."""

    capacityDemand: Optional[Capacity] = None
    extractedResource: Optional[List[ResourceRef]] = field(default_factory=list)


@dataclass(repr=False)
class ResourcePool(LogicalResource, BaseCRUDMixin):
    capacity: Optional[List[Capacity]] = field(default_factory=list)
    pooledResourceSpecification: Optional[ResourceSpecificationRef] = None
    pooledResource: Optional[List[ResourceRef]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourcePool/v5/resourcePool"

    def check_availability(self, context: Context) -> List[AvailabilityCheck]:
        url = f"{self.get_resource_path(context)}/{self.id}/availabilityCheck"
        response = requests.request("GET", url, headers=context.headers, data={})
        items = parse_response(response, context)
        availability_checks = []
        for item in items:
            availability_checks.append(AvailabilityCheck.from_dict(item))
        return availability_checks


@dataclass(repr=False)
class ExternalId(Entity):
    """Identifier of an entity within an external system (TMF652)."""

    id: Optional[str] = None
    entityType: Optional[str] = None
    owner: Optional[str] = None


@dataclass(repr=False)
class ResourceRefOrValue(Entity):
    """A resource carried either by reference or by value (TMF652)."""

    id: Optional[str] = None
    href: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    endOperatingDate: Optional[str] = None
    startOperatingDate: Optional[str] = None
    resourceVersion: Optional[str] = None
    administrativeState: Optional[ResourceAdministrativeStateType] = None
    operationalState: Optional[ResourceOperationalStateType] = None
    resourceStatus: Optional[ResourceStatusType] = None
    usageState: Optional[ResourceUsageStateType] = None
    place: Optional[RelatedPlaceRefOrValue] = None
    note: Optional[List[Note]] = field(default_factory=list)
    attachment: Optional[List[AttachmentRefOrValue]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)
    resourceCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    resourceRelationship: Optional[List[ResourceRelationship]] = field(
        default_factory=list
    )
    resourceSpecification: Optional[ResourceSpecificationRef] = None
    _referred_type: Optional[str] = None


@dataclass(repr=False)
class ResourceOrderItemRelationship(Entity):
    """Link between resource order items (TMF652)."""

    relationshipType: Optional[str] = None
    orderItem: Optional[ResourceOrderItemRef] = None


@dataclass(repr=False)
class ResourceOrderItem(Entity):
    """A single actionable item of a resource order (TMF652)."""

    id: Optional[str] = None
    action: Optional[OrderItemActionType] = None
    quantity: Optional[int] = None
    state: Optional[str] = None
    appointment: Optional[AppointmentRef] = None
    orderItemRelationship: Optional[List[ResourceOrderItemRelationship]] = field(
        default_factory=list
    )
    resource: Optional[ResourceRefOrValue] = None
    resourceSpecification: Optional[ResourceSpecificationRef] = None


@dataclass(repr=False)
class ResourceOrder(Entity, BaseCRUDMixin):
    """A request to provision a set of logical and physical resources (TMF652).

    A Resource Order is triggered by a service order fulfilment or raised
    directly against the resource ordering API.

    Usage:
        order = ResourceOrder.from_dict(payload)
        order.get(context, resource_id="1234")
    """

    id: Optional[str] = None
    href: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    externalId: Optional[str] = None
    orderType: Optional[str] = None
    priority: Optional[int] = None
    state: Optional[str] = None
    orderDate: Optional[str] = None
    completionDate: Optional[str] = None
    expectedCompletionDate: Optional[str] = None
    requestedCompletionDate: Optional[str] = None
    requestedStartDate: Optional[str] = None
    startDate: Optional[str] = None
    externalReference: Optional[List[ExternalId]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    orderItem: Optional[List[ResourceOrderItem]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceOrderingManagement/v4/resourceOrder"


@dataclass(repr=False)
class CancelResourceOrder(Entity, BaseCRUDMixin):
    """A task requesting cancellation of an existing resource order (TMF652)."""

    id: Optional[str] = None
    href: Optional[str] = None
    cancellationReason: Optional[str] = None
    effectiveCancellationDate: Optional[str] = None
    requestedCancellationDate: Optional[str] = None
    state: Optional[TaskStateType] = None
    resourceOrder: Optional[ResourceOrderRef] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return (
            f"{context.api_base_url}/resourceOrderingManagement/v4/cancelResourceOrder"
        )


@dataclass(repr=False)
class ConnectionSpecification(Entity):
    """Resource graph edge specification connecting endpoint specifications."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    associationType: Optional[ConnectionAssociationType] = None
    endpointSpecification: Optional[List[EndpointSpecificationRef]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class ResourceGraphSpecificationRelationship(Entity):
    """Link between resource graph specifications."""

    relationshipType: Optional[ResourceGraphSpecificationRelationshipType] = None
    resourceGraph: Optional[ResourceGraphSpecificationRef] = None


@dataclass(repr=False)
class ResourceGraphSpecification(Entity):
    """Resource graph specification."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    graphSpecificationRelationship: Optional[
        List[ResourceGraphSpecificationRelationship]
    ] = field(default_factory=list)
    connectionSpecification: Optional[List[ConnectionSpecification]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class ResourceSpecificationRelationship(Entity):
    """Migration, substitution, dependency or exclusivity relationship between resource specifications."""

    relationshipType: Optional[str] = None
    role: Optional[str] = None
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    defaultQuantity: Optional[int] = None
    maximumQuantity: Optional[int] = None
    minimumQuantity: Optional[int] = None
    characteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class ResourceSpecification(Entity, BaseCRUDMixin):
    """Base class for a generic means of implementing a particular type of Resource."""

    description: Optional[str] = None
    version: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    isBundle: Optional[bool] = None
    lastUpdate: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    targetResourceSchema: Optional[TargetResourceSchema] = None
    featureSpecification: Optional[List[FeatureSpecification]] = field(
        default_factory=list
    )
    attachment: Optional[List[Union[Attachment, AttachmentRef]]] = field(
        default_factory=list
    )
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    resourceSpecCharacteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )
    resourceSpecRelationship: Optional[List[ResourceSpecificationRelationship]] = field(
        default_factory=list
    )
    intentSpecification: Optional[IntentSpecificationRef] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceCatalog/v5/resourceSpecification"


@dataclass(repr=False)
class PhysicalResourceSpecification(ResourceSpecification):
    """Specification for a physical resource (hardware item)."""

    model: Optional[str] = None
    part: Optional[str] = None
    sku: Optional[str] = None
    vendor: Optional[str] = None


@dataclass(repr=False)
class LogicalResourceSpecification(ResourceSpecification):
    """Specification for a logical resource; base type for ResourcePoolSpecification."""


@dataclass(repr=False)
class ResourceFunctionSpecification(LogicalResourceSpecification):
    """Specification of a function transforming inputs into outputs, e.g. a firewall."""

    connectionPointSpecification: Optional[List[ConnectionPointSpecificationRef]] = (
        field(default_factory=list)
    )
    connectivitySpecification: Optional[List[ResourceGraphSpecification]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class ResourcePoolSpecification(LogicalResourceSpecification):
    """Specification for a resource pool (LogicalResourceSpecification subtype)."""

    capacitySpecification: Optional[List[CapacitySpecificationRef]] = field(
        default_factory=list
    )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourcePool/v5/resourcePoolSpecification"


@dataclass(repr=False)
class ResourceCategory(Entity, BaseCRUDMixin):
    """Logical container grouping resource candidates; categories can nest."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    lastUpdate: Optional[str] = None
    parentId: Optional[str] = None
    isRoot: Optional[bool] = None
    validFor: Optional[TimePeriod] = None
    category: Optional[List[ResourceCategoryRef]] = field(default_factory=list)
    resourceSpecification: Optional[List[ResourceSpecificationRef]] = field(
        default_factory=list
    )
    resourceCandidate: Optional[List[ResourceCandidateRef]] = field(
        default_factory=list
    )
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceCatalog/v5/resourceCategory"


@dataclass(repr=False)
class ResourceCandidate(Entity, BaseCRUDMixin):
    """Makes a resource specification available through one or more resource catalogs."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    lastUpdate: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    category: Optional[List[ResourceCategoryRef]] = field(default_factory=list)
    resourceSpecification: Optional[ResourceSpecificationRef] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceCatalog/v5/resourceCandidate"


@dataclass(repr=False)
class ResourceCatalog(Entity, BaseCRUDMixin):
    """Root entity for resource catalog management.

    A resource catalog groups resource specifications, made available through
    resource candidates, that an organization offers to its consumers.

    Attributes:
        name (Optional[str]): Name of the catalog.
        catalogType (Optional[str]): Type of catalog, e.g. "Resource".
        lifecycleStatus (Optional[str]): Current lifecycle status, e.g. "Active".
        category (Optional[List[ResourceCategoryRef]]): Root categories in this catalog.
        relatedParty (Optional[List[RelatedPartyRefOrPartyRoleRef]]): Parties involved
            in this catalog.
        validFor (Optional[TimePeriod]): Period the catalog is valid for.

    Example:
        >>> catalog = ResourceCatalog.from_id("5574", context)
        >>> [c.name for c in catalog.category]
        ['Secure Home']
    """

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    catalogType: Optional[str] = None
    version: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    lastUpdate: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    category: Optional[List[ResourceCategoryRef]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceCatalog/v5/resourceCatalog"


@dataclass(repr=False)
class ImportJob(Entity, BaseCRUDMixin):
    """Batch task importing resources from a file into the catalog."""

    id: Optional[str] = None
    href: Optional[str] = None
    contentType: Optional[str] = None
    creationDate: Optional[str] = None
    completionDate: Optional[str] = None
    errorLog: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    status: Optional[JobStateType] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceCatalog/v5/importJob"


@dataclass(repr=False)
class ExportJob(Entity, BaseCRUDMixin):
    """Batch task exporting catalog resources to a file."""

    id: Optional[str] = None
    href: Optional[str] = None
    contentType: Optional[str] = None
    creationDate: Optional[str] = None
    completionDate: Optional[str] = None
    errorLog: Optional[str] = None
    path: Optional[str] = None
    query: Optional[str] = None
    url: Optional[str] = None
    status: Optional[JobStateType] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/resourceCatalog/v5/exportJob"


@dataclass(repr=False)
class ServiceRelationship(Entity):
    relationshipType: Optional[str] = None
    service: Optional[Union[Service, ServiceRef]] = None
    serviceRelationshipCharacteristic: Optional[List[Characteristic]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class Service(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    name: Optional[str] = None
    href: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    endDate: Optional[str] = None
    hasStarted: Optional[bool] = None
    isBundle: Optional[bool] = None
    isServiceEnabled: Optional[bool] = None
    isStateful: Optional[bool] = None
    operatingStatus: Optional[ServiceOperatingStatusType] = None
    operatingStatusContextUpdate: Optional[ContextUpdate] = None
    serviceDate: Optional[str] = None
    serviceType: Optional[str] = None
    startDate: Optional[str] = None
    startMode: Optional[str] = None
    state: Optional[ServiceStateType] = None
    serviceSpecification: Optional[ServiceSpecificationRef] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    serviceCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    serviceRelationship: Optional[List[ServiceRelationship]] = field(
        default_factory=list
    )
    supportingService: Optional[List[Union[Service, ServiceRef]]] = field(
        default_factory=list
    )
    note: Optional[List[Note]] = field(default_factory=list)
    supportingResource: Optional[List[ResourceRef]] = field(default_factory=list)
    feature: Optional[List[Feature]] = field(default_factory=list)
    serviceOrderItem: Optional[List[RelatedServiceOrderItem]] = field(
        default_factory=list
    )
    intent: Optional[List[Union[Intent, IntentRef]]] = field(default_factory=list)
    place: Optional[List[RelatedPlaceRefOrValue]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedPartyRefOrPartyRoleRef]] = field(
        default_factory=list
    )
    relatedEntity: Optional[List[RelatedEntityRefOrValue]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/serviceInventory/v5/service"


@dataclass(repr=False)
class RelatedServiceOrderItem(Entity):
    itemAction: Optional[OrderItemActionType] = None
    itemId: Optional[str] = None
    role: Optional[str] = None
    serviceOrderHref: Optional[str] = None
    serviceOrderId: Optional[str] = None


@dataclass(repr=False)
class RelatedEntityRefOrValue(Entity):
    role: Optional[str] = None
    entity: Optional[Union[Entity, EntityRef]] = None


@dataclass(repr=False)
class ServiceSpecRelationship(Entity):
    """A service specification related to another service specification."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    relationshipType: Optional[str] = None
    role: Optional[str] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class EntitySpecificationRelationship(Entity):
    """A relationship from a specification to another entity specification."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    relationshipType: Optional[str] = None
    role: Optional[str] = None
    associationSpec: Optional[AssociationSpecificationRef] = None
    validFor: Optional[TimePeriod] = None


@dataclass(repr=False)
class ServiceSpecification(Entity, BaseCRUDMixin):
    """Blueprint describing a type of service, its characteristics and features.

    A service specification defines what a service looks like before it is
    instantiated: the characteristics it carries, the resource specifications
    it relies on, and its relationships to other specifications.

    Attributes:
        name (Optional[str]): Name given to the specification.
        isBundle (Optional[bool]): True when the specification bundles others.
        lifecycleStatus (Optional[str]): Current lifecycle status, e.g. "Active".
        specCharacteristic (Optional[List[CharacteristicSpecification]]):
            Characteristics the service can take.
        serviceSpecRelationship (Optional[List[ServiceSpecRelationship]]):
            Related service specifications, e.g. migration or dependency.
        targetEntitySchema (Optional[TargetEntitySchema]): Pointer to the schema
            defining the target entity.

    Example:
        >>> spec = ServiceSpecification.from_id("42", context)
        >>> [c.name for c in spec.specCharacteristic]
        ['Bandwidth']
    """

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    isBundle: Optional[bool] = None
    lifecycleStatus: Optional[str] = None
    lastUpdate: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    targetEntitySchema: Optional[TargetEntitySchema] = None
    attachment: Optional[List[Union[Attachment, AttachmentRef]]] = field(
        default_factory=list
    )
    constraint: Optional[List[ConstraintRef]] = field(default_factory=list)
    entitySpecRelationship: Optional[List[EntitySpecificationRelationship]] = field(
        default_factory=list
    )
    featureSpecification: Optional[List[FeatureSpecification]] = field(
        default_factory=list
    )
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)
    resourceSpecification: Optional[List[ResourceSpecificationRef]] = field(
        default_factory=list
    )
    serviceLevelSpecification: Optional[List[ServiceLevelSpecificationRef]] = field(
        default_factory=list
    )
    serviceSpecRelationship: Optional[List[ServiceSpecRelationship]] = field(
        default_factory=list
    )
    specCharacteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return (
            f"{context.api_base_url}/serviceCatalogManagement/v4/serviceSpecification"
        )


@dataclass(repr=False)
class ServiceCandidate(Entity, BaseCRUDMixin):
    """Makes a service specification available through one or more service catalogs."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    lastUpdate: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    category: Optional[List[ServiceCategoryRef]] = field(default_factory=list)
    serviceSpecification: Optional[ServiceSpecificationRef] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/serviceCatalogManagement/v4/serviceCandidate"


@dataclass(repr=False)
class ServiceCategory(Entity, BaseCRUDMixin):
    """Logical container grouping service candidates; categories can nest."""

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    lastUpdate: Optional[str] = None
    parentId: Optional[str] = None
    isRoot: Optional[bool] = None
    validFor: Optional[TimePeriod] = None
    category: Optional[List[ServiceCategoryRef]] = field(default_factory=list)
    serviceCandidate: Optional[List[ServiceCandidateRef]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/serviceCatalogManagement/v4/serviceCategory"


@dataclass(repr=False)
class ServiceCatalog(Entity, BaseCRUDMixin):
    """Root entity for service catalog management.

    A service catalog groups service specifications, made available through
    service candidates, that an organization offers to its consumers.

    Attributes:
        name (Optional[str]): Name of the service catalog.
        lifecycleStatus (Optional[str]): Current lifecycle status, e.g. "Active".
        category (Optional[List[ServiceCategoryRef]]): Root categories in this catalog.
        relatedParty (Optional[List[RelatedParty]]): Parties involved in this catalog.
        validFor (Optional[TimePeriod]): Period the catalog is valid for.

    Example:
        >>> catalog = ServiceCatalog.from_id("3830", context)
        >>> [c.name for c in catalog.category]
        ['Connectivity']
    """

    id: Optional[str] = None
    href: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    lastUpdate: Optional[str] = None
    validFor: Optional[TimePeriod] = None
    category: Optional[List[ServiceCategoryRef]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/serviceCatalogManagement/v4/serviceCatalog"


@dataclass(repr=False)
class ContextUpdate(Entity):
    """Date and reason context behind the current value of a status or state (TMF641)."""

    id: Optional[str] = None
    lastUpdate: Optional[str] = None
    reason: Optional[str] = None
    relatedEntity: Optional[List[EntityRef]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)


@dataclass(repr=False)
class ExternalReference(Entity):
    """Reference to an entity held in an external system (TMF641)."""

    id: Optional[str] = None
    href: Optional[str] = None
    externalReferenceType: Optional[str] = None
    name: Optional[str] = None


@dataclass(repr=False)
class JsonPatch(Entity):
    """A single JSON Patch (RFC 6902) operation, used by ``ServiceOrderItem.modifyPath``.

    The RFC's ``from`` member is not modelled: it is a Python keyword, and the
    serializer maps field names to wire names verbatim. It applies only to the
    ``move`` and ``copy`` operations, which TMF641 order payloads do not use.
    """

    op: Optional[str] = None
    path: Optional[str] = None
    value: Any = None


@dataclass(repr=False)
class ServiceOrderRelationship(Entity):
    """Link between a service order and another service order (TMF641)."""

    id: Optional[str] = None
    href: Optional[str] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class ServiceOrderItemRelationship(Entity):
    """Link between service order items (TMF641)."""

    relationshipType: Optional[str] = None
    orderItem: Optional[ServiceOrderItemRef] = None


@dataclass(repr=False)
class OrderItemSpecRelationship(Entity):
    """Link between order item specifications (TMF641)."""

    orderItemSpecificationId: Optional[str] = None
    parentOrderSpecificationHref: Optional[str] = None
    parentOrderSpecificationId: Optional[str] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class ServiceOrderMilestone(Milestone):
    """A significant change or stage in the processing of a service order (TMF641)."""

    serviceOrderItem: Optional[List[ServiceOrderItemRef]] = field(default_factory=list)


@dataclass(repr=False)
class ServiceOrderJeopardyAlert(JeopardyAlert):
    """A predicted exception putting completion of a service order at risk (TMF641)."""

    serviceOrderItem: Optional[List[ServiceOrderItemRef]] = field(default_factory=list)


@dataclass(repr=False)
class ServiceOrderErrorMessage(ErrorMessage):
    """An error that causes a status change in a service order (TMF641)."""

    timestamp: Optional[str] = None
    serviceOrderItem: Optional[List[ServiceOrderItemRef]] = field(default_factory=list)


@dataclass(repr=False)
class ServiceOrderItemErrorMessage(ErrorMessage):
    """An error that causes a status change in a service order item (TMF641)."""

    timestamp: Optional[str] = None


@dataclass(repr=False)
class ServiceRefOrValue(Entity):
    """A service carried either by reference or by value (TMF641)."""

    id: Optional[str] = None
    href: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    endDate: Optional[str] = None
    serviceDate: Optional[str] = None
    startDate: Optional[str] = None
    startMode: Optional[str] = None
    serviceType: Optional[str] = None
    hasStarted: Optional[bool] = None
    isBundle: Optional[bool] = None
    isServiceEnabled: Optional[bool] = None
    isStateful: Optional[bool] = None
    operatingStatus: Optional[ServiceOperatingStatusType] = None
    operatingStatusContextUpdate: Optional[ContextUpdate] = None
    state: Optional[ServiceStateType] = None
    serviceSpecification: Optional[ServiceSpecificationRef] = None
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    feature: Optional[List[Feature]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    place: Optional[List[RelatedPlaceRefOrValue]] = field(default_factory=list)
    relatedEntity: Optional[List[RelatedEntityRefOrValue]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)
    serviceCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    serviceOrderItem: Optional[List[RelatedServiceOrderItem]] = field(
        default_factory=list
    )
    serviceRelationship: Optional[List[ServiceRelationship]] = field(
        default_factory=list
    )
    supportingResource: Optional[List[ResourceRef]] = field(default_factory=list)
    supportingService: Optional[List[ServiceRefOrValue]] = field(default_factory=list)
    _referred_type: Optional[str] = None


@dataclass(repr=False)
class OrderItemSpecification(Entity):
    """Template describing an order item, shared by orders built from it (TMF641)."""

    id: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    attachment: Optional[List[AttachmentRefOrValue]] = field(default_factory=list)
    constraint: Optional[List[ConstraintRef]] = field(default_factory=list)
    orderItemSpecRelationship: Optional[List[OrderItemSpecRelationship]] = field(
        default_factory=list
    )
    specCharacteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class ServiceOrderItemSpecification(OrderItemSpecification):
    """Template describing a service order item (TMF641)."""

    actionType: Optional[ServiceOrderItemActionType] = None
    otherAction: Optional[str] = None
    serviceCategory: Optional[ServiceCategoryRef] = None
    serviceSpecification: Optional[ServiceSpecificationRef] = None


@dataclass(repr=False)
class OrderSpecification(Entity):
    """Template describing an order, shared by orders built from it (TMF641)."""

    id: Optional[str] = None
    href: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    lastUpdate: Optional[str] = None
    lifecycleStatus: Optional[str] = None
    version: Optional[str] = None
    isAutoResumeAllowed: Optional[bool] = None
    isAutoUnlockAllowed: Optional[bool] = None
    isBundle: Optional[bool] = None
    isSyncModeEnabled: Optional[bool] = None
    failurePolicy: Optional[OrderFailurePolicy] = None
    sequencingPolicy: Optional[OrderSequencingPolicy] = None
    targetEntitySchema: Optional[TargetEntitySchema] = None
    validFor: Optional[TimePeriod] = None
    workflow: Optional[ProcessFlowSpecificationRef] = None
    attachment: Optional[List[AttachmentRefOrValue]] = field(default_factory=list)
    constraint: Optional[List[ConstraintRef]] = field(default_factory=list)
    entitySpecRelationship: Optional[List[EntitySpecificationRelationship]] = field(
        default_factory=list
    )
    externalIdentifier: Optional[List[ExternalIdentifier]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)
    specCharacteristic: Optional[List[CharacteristicSpecification]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class ServiceOrderSpecification(OrderSpecification, BaseCRUDMixin):
    """Template by which service orders are instantiated and described (TMF641).

    Service orders sharing a specification share the same set of behaviour.

    Usage:
        spec = ServiceOrderSpecification.from_dict(payload)
        spec.get(context, resource_id="1234")
    """

    serviceOrderItemSpecification: Optional[List[ServiceOrderItemSpecification]] = (
        field(default_factory=list)
    )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/serviceOrdering/v4/serviceOrderSpecification"


@dataclass(repr=False)
class ServiceOrderItem(Entity):
    """A single actionable item of a service order (TMF641)."""

    id: Optional[str] = None
    name: Optional[str] = None
    otherAction: Optional[str] = None
    quantity: Optional[int] = None
    action: Optional[ServiceOrderItemActionType] = None
    state: Optional[ServiceOrderItemStateType] = None
    appointment: Optional[AppointmentRef] = None
    service: Optional[ServiceRefOrValue] = None
    errorMessage: Optional[List[ServiceOrderItemErrorMessage]] = field(
        default_factory=list
    )
    modifyPath: Optional[List[JsonPatch]] = field(default_factory=list)
    orderItemCharacteristic: Optional[List[Characteristic]] = field(
        default_factory=list
    )
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)
    serviceOrderItem: Optional[List[ServiceOrderItem]] = field(default_factory=list)
    serviceOrderItemRelationship: Optional[List[ServiceOrderItemRelationship]] = field(
        default_factory=list
    )


@dataclass(repr=False)
class ServiceOrder(Entity, BaseCRUDMixin):
    """A request to provision a set of services (TMF641).

    A service order is raised by a product order fulfilment process or directly
    against the service ordering API.

    Usage:
        order = ServiceOrder.from_dict(payload)
        order.get(context, resource_id="1234")
    """

    id: Optional[str] = None
    href: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    externalId: Optional[str] = None
    notificationContact: Optional[str] = None
    priority: Optional[str] = None
    cancellationDate: Optional[str] = None
    cancellationReason: Optional[str] = None
    completionDate: Optional[str] = None
    expectedCompletionDate: Optional[str] = None
    lastUpdate: Optional[str] = None
    orderDate: Optional[str] = None
    requestedCompletionDate: Optional[str] = None
    requestedStartDate: Optional[str] = None
    startDate: Optional[str] = None
    state: Optional[ServiceOrderStateType] = None
    orderSpecification: Optional[EntitySpecificationRef] = None
    errorMessage: Optional[List[ServiceOrderErrorMessage]] = field(default_factory=list)
    externalReference: Optional[List[ExternalReference]] = field(default_factory=list)
    jeopardyAlert: Optional[List[ServiceOrderJeopardyAlert]] = field(
        default_factory=list
    )
    milestone: Optional[List[ServiceOrderMilestone]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    orderCharacteristic: Optional[List[Characteristic]] = field(default_factory=list)
    orderRelationship: Optional[List[ServiceOrderRelationship]] = field(
        default_factory=list
    )
    relatedEntity: Optional[List[RelatedEntityRefOrValue]] = field(default_factory=list)
    relatedParty: Optional[List[RelatedParty]] = field(default_factory=list)
    serviceOrderItem: Optional[List[ServiceOrderItem]] = field(default_factory=list)

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/serviceOrdering/v4/serviceOrder"


@dataclass(repr=False)
class CancelServiceOrder(Entity, BaseCRUDMixin):
    """A task requesting cancellation of an existing service order (TMF641)."""

    id: Optional[str] = None
    href: Optional[str] = None
    cancellationReason: Optional[str] = None
    completionMessage: Optional[str] = None
    effectiveCancellationDate: Optional[str] = None
    requestedCancellationDate: Optional[str] = None
    state: Optional[TaskStateType] = None
    errorMessage: Optional[ErrorMessage] = None
    serviceOrder: Optional[ServiceOrderRef] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/serviceOrdering/v4/cancelServiceOrder"


@dataclass(repr=False)
class CheckProductOfferingQualification(Entity, BaseCRUDMixin):
    id: Optional[str] = None
    creationDate: Optional[str] = None
    description: Optional[str] = None
    effectiveQualificationDate: Optional[str] = None
    expectedQualificationCompletionDate: Optional[str] = None
    expirationDate: Optional[str] = None
    href: Optional[str] = None
    instantSyncQualification: Optional[bool] = None
    provideAlternative: Optional[bool] = None
    provideOnlyAvailable: Optional[bool] = None
    provideResultReason: Optional[bool] = None
    qualificationResult: Optional[str] = None
    requestedQualificationCompletionDate: Optional[str] = None
    state: Optional[TaskStateType] = None
    relatedParty: Optional[List[RelatedPartyOrPartyRole]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    channel: Optional[ChannelRef] = None
    checkProductOfferingQualificationItem: Optional[
        List[CheckProductOfferingQualificationItem]
    ] = field(default_factory=list)
    eligibilityCharacteristic: Optional[List[Characteristic]] = field(
        default_factory=list
    )

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/productOfferingQualification/v5/checkProductOfferingQualification"


@dataclass(repr=False)
class CheckProductOfferingQualificationItem(Entity):
    id: Optional[str] = None
    action: Optional[OrderItemActionType] = None
    expectedActivationDate: Optional[str] = None
    qualificationItemResult: Optional[QualificationItemResultEnumType] = None
    state: Optional[TaskStateType] = None
    terminationError: Optional[List[TerminationError]] = field(default_factory=list)
    qualificationItemRelationship: Optional[
        List[ProductOfferingQualificationItemRelationship]
    ] = field(default_factory=list)
    eligibilityResultReason: Optional[List[EligibilityResultReason]] = field(
        default_factory=list
    )
    checkProductOfferingQualificationItem: Optional[
        List[CheckProductOfferingQualificationItem]
    ] = field(default_factory=list)
    promotion: Optional[List[PromotionRef]] = field(default_factory=list)
    productOffering: Optional[ProductOfferingRef] = None
    alternateProductOfferingProposal: Optional[
        List[AlternateProductOfferingProposal]
    ] = field(default_factory=list)
    product: Optional[Union[Product, ProductRef]] = None
    category: Optional[CategoryRef] = None
    note: Optional[List[Note]] = field(default_factory=list)


@dataclass(repr=False)
class ProductOfferingQualificationItemRelationship(Entity):
    id: Optional[str] = None
    relationshipType: Optional[str] = None


@dataclass(repr=False)
class EligibilityResultReason(Entity):
    code: Optional[str] = None
    label: Optional[str] = None


@dataclass(repr=False)
class AlternateProductOfferingProposal(Entity):
    id: Optional[str] = None
    alternateActivationDate: Optional[str] = None
    alternateProductOffering: Optional[ProductOfferingRef] = None
    promotion: Optional[PromotionRef] = None
    alternateProduct: Optional[Union[Product, ProductRef]] = None


@dataclass(repr=False)
class TerminationError(Entity):
    id: Optional[str] = None
    value: Optional[str] = None


@dataclass(repr=False)
class QueryProductOfferingQualification(Entity, BaseCRUDMixin):
    creationDate: Optional[str] = None
    description: Optional[str] = None
    effectiveQualificationDate: Optional[str] = None
    expectedQualificationCompletionDate: Optional[str] = None
    expirationDate: Optional[str] = None
    href: Optional[str] = None
    id: Optional[str] = None
    instantSyncQualification: Optional[bool] = None
    requestedQualificationCompletionDate: Optional[str] = None
    state: Optional[TaskStateType] = None
    relatedParty: Optional[List[RelatedPartyOrPartyRole]] = field(default_factory=list)
    note: Optional[List[Note]] = field(default_factory=list)
    channel: Optional[ChannelRef] = None
    qualifiedProductOfferingItem: Optional[
        List[QueryProductOfferingQualificationItem]
    ] = field(default_factory=list)
    searchCriteria: Optional[QueryProductOfferingQualificationItem] = None

    @classmethod
    def get_resource_path(cls, context: Context) -> str:
        return f"{context.api_base_url}/productOfferingQualification/v5/queryProductOfferingQualification"


@dataclass(repr=False)
class QueryProductOfferingQualificationItem(Entity):
    id: Optional[str] = None
    productOffering: Optional[ProductOfferingRef] = None
    product: Optional[Union[Product, ProductRef]] = None
    category: Optional[CategoryRef] = None
    promotion: Optional[PromotionRef] = None
    qualificationItemRelationship: Optional[
        List[ProductOfferingQualificationItemRelationship]
    ] = field(default_factory=list)
