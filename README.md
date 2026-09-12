# tmforum

Unofficial Python SDK for [TM Forum Open APIs](https://www.tmforum.org/oda/open-apis/) — plain-dataclass entity models, `@type`-aware (de)serialization, and thin REST CRUD helpers.

- **No heavy dependencies** — just `requests`. Entities are standard-library `dataclasses`, not pydantic models.
- **Polymorphism-aware serialization** — `from_dict` resolves `@type` / `@referredType` discriminators to the right Python class; `to_dict` emits them back, so round-tripping TMF payloads preserves their type structure, unknown vendor attributes included.
- **Thin CRUD layer** — `create` / `read` / `update` / `delete` / `query_get` methods that map 1:1 onto the TMF REST conventions. No hidden state, no client object: a small `Context` carries the base URL, auth, and headers.

## Install

```bash
pip install tmforum
```

Python 3.9+.

## Quickstart

```python
from tmforum import Context, Individual, ProductOffering

context = Context(
    api_base_url="https://api.example.com/tmf-api",
    access_token="...",
    currency_code="USD",
)
context.headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {context.access_token}",
}

# Create, read, query, delete — TMF632 Party Management
person = Individual(givenName="Jane", familyName="Doe")
person = person.create(context)     # POST /partyManagement/v5/individual
person = person.read(context)       # GET  /partyManagement/v5/individual/{id}

# TMF620 Product Catalog
offers = ProductOffering.query_get("lifecycleStatus=Active", context)

person.delete(context)              # DELETE /partyManagement/v5/individual/{id}
```

Serialization works without a server:

```python
from tmforum import Product

product = Product.from_dict({
    "@type": "Product",
    "id": "42",
    "name": "Fibre 500",
    "status": "active",
    "billingAccount": {"@type": "BillingAccountRef", "id": "ba-1"},
    "isBundle": False,
    "quantity": 1,
    "productPrice": [],
})
assert product.billingAccount.id == "ba-1"
payload = product.to_dict()         # emits @type discriminators back
```

## Supported TM Forum APIs

The SDK targets the **v5** payload shapes of the Open APIs.

| TMF API | Resource path | Main SDK classes |
|---|---|---|
| TMF620 Product Catalog | `productCatalogManagement/v5` | `ProductCatalog`, `Category`, `ProductOffering`, `ProductSpecification` |
| TMF622 Product Ordering | `productOrdering/v5` | `ProductOrder`, `CancelProductOrder` |
| TMF637 Product Inventory | `productInventory/v5` | `Product` |
| TMF632 Party Management | `partyManagement/v5` | `Individual`, `Organization` |
| TMF669 Party Role | `partyRoleManagement/v5` | `PartyRole`, `Supplier`, `BusinessPartner`, `Consumer`, `Producer` |
| TMF629 Customer Management | `customerManagement/v5` | `Customer` |
| TMF666 Account Management | `accountManagement/v5` | `BillingAccount`, `SettlementAccount`, `PartyAccount`, `FinancialAccount`, `BillingCycleSpecification`, `BillFormat`, `BillPresentationMedia` |
| TMF678 Customer Bill | `customerBill/v5` | `CustomerBill`, `CustomerBillOnDemand`, `BillCycle`, `AppliedCustomerBillingRate` |
| TMF648 Quote | `quoteManagement/v5` | `Quote` |
| TMF679 Product Offering Qualification | `productOfferingQualification/v5` | `CheckProductOfferingQualification`, `QueryProductOfferingQualification` |
| TMF699 Sales Management | `salesManagement/v5` | `SalesLead`, `SalesOpportunity` |
| TMF723 Policy Management | `policyManagement/v5` | `PolicyDomain`, `ManagedPolicy`, `ManagedPolicyVariable`, `PolicyCatalog` |
| TMF633 Service Catalog | `serviceCatalogManagement/v4` | `ServiceCatalog`, `ServiceCategory`, `ServiceCandidate`, `ServiceSpecification` |
| TMF638 Service Inventory | `serviceInventory/v5` | `Service` |
| TMF641 Service Ordering | `serviceOrdering/v4` | `ServiceOrder`, `ServiceOrderItem`, `CancelServiceOrder`, `ServiceOrderSpecification` |
| TMF639 Resource Inventory | `resourceInventory/v5` | `Resource` |
| TMF634 Resource Catalog | `resourceCatalog/v5` | `ResourceCatalog`, `ResourceCategory`, `ResourceCandidate`, `ResourceSpecification`, `PhysicalResourceSpecification`, `LogicalResourceSpecification`, `ResourceFunctionSpecification`, `ImportJob`, `ExportJob` |
| TMF652 Resource Ordering | `resourceOrderingManagement/v4` | `ResourceOrder`, `ResourceOrderItem`, `CancelResourceOrder` |
| TMF685 Resource Pool | `resourcePool/v5` | `ResourcePool`, `ResourcePoolSpecification`, `CapacitySpecification` |
| TMF676 Payment | `payment/v4` | `Payment`, `Refund`, `PaymentMethod`, `PaymentPlan` |
| TMF936 Open Gateway Operate — Product Catalog | `openGatewayOperateAPIProductCatalog/v5` | `OpenGatewayProductOffering`, `OpenGatewayProductSpecification`, `ApiProductSpecification`, `UsageVolumeProductSpecification` |
| TMF760 Product Configuration | `productConfiguration/v5` | `CheckProductConfiguration`, `QueryProductConfiguration`, `ProductConfiguration` |
| TMF673 Geographic Address | `geographicAddressManagement/v4` | `GeographicAddress`, `GeographicAddressValidation`, `GeographicSubAddress`, `GeographicLocation` |
| TMF674 Geographic Site | `geographicSiteManagement/v5` | `GeographicSite`, `GeographicSiteFeature`, `GeographicSiteRelationship` |
| TMF767 Product Usage Catalog | `productUsageCatalogManagement/v5` | `ProductUsageSpecification` |
| TMF770 Fraud Management | `fraudManagement/v5` | `EvaluateFraudRisk` |
| TMF663 Shopping Cart | `shoppingCart/v5` | `ShoppingCart`, `CartItem`, `CartPrice`, `CartTerm` |
| TMF771 Resource Usage Management | `resourceUsageManagement/v5` | `ResourceUsage`, `ResourceUsageSpecification` |
| TMF683 Party Interaction | `partyInteraction/v5` | `PartyInteraction`, `InteractionItem` |
| TMF656 Service Problem | `serviceProblemManagement/v5` | `ServiceProblem`, `ServiceProblemEventRecord`, `ProblemAcknowledgement`, `ProblemUnacknowledgement`, `ProblemGroup`, `ProblemUngroup` |
| TMF677 Usage Consumption | `usageConsumption/v5` | `QueryUsageConsumption`, `UsageConsumptionReport`, `Bucket`, `BucketCounter`, `ConsumptionSummary` |
| TMF717 Customer 360 | `customer360/v5` | `Customer360` (read-only), with `Customer360Customer`, `Customer360Account`, `Customer360LoyaltyAccount` and the other `Customer360*` value objects |
| TMF921 Intent Management | `intentManagement/v5` | `Intent`, `ProbeIntent`, `IntentSpecification`, `IntentReport` (via `Intent.get_intent_reports`) |
| TMF701 Process Management | `processManagement/v5` | `Process`, `ProcessSpecification`, `Task`, `TaskSpecification` |

## How it works

Every entity is a `@dataclass` inheriting from `Entity`, which provides recursive `from_dict` / `to_dict` / `to_json`. Type resolution uses each field's type hints plus the payload's `@type` discriminator, so nested and polymorphic structures (e.g. `RelatedPartyRefOrPartyRoleRef`, price alterations, characteristic subtypes) deserialize into the correct classes.

Entities that map to REST resources also inherit `BaseCRUDMixin`, which implements `from_id`, `create`, `read`, `update` (JSON PATCH semantics), `query_get`, and `delete` against `{context.api_base_url}/{resource_path}`. A `Context` dataclass carries `api_base_url`, `access_token`, `headers`, an optional logger, and OAuth-related fields — pass it to every call; there is no global state.

Parsing is lenient, because real deployments extend and bend the specs. A value `from_dict` cannot map — an unknown `@type`, a list where a single value is declared, an object its class rejects — is kept exactly as it came and reported as a warning on the `tmforum` logger, so one odd field never costs the rest of the response:

```python
product = Product.from_dict(payload)                 # warns, keeps what it cannot map
product = Product.from_dict(payload, strict=True)    # raises FromDictError(path=...)

context.strict_parsing = True                        # same, for the CRUD helpers
```

Payload attributes the SDK does not model — vendor extensions, `@schemaLocation` on a class without the field — are kept in `entity.extra_attributes` and emitted again by `to_dict`, so a payload survives a round trip unchanged. A vendor `@type` the SDK does not know, but whose `@baseType` it does, parses as that base class and keeps its own `@type` on the way out.

## Status

Alpha. The entity models and serialization are exercised by a pure-offline test suite; the CRUD layer follows the TMF REST conventions, but server implementations vary in the extensions and versions they accept. Issues and PRs welcome.

## License & trademark notice

MIT — see [LICENSE](LICENSE).

This is an **unofficial, community project**. TM Forum® and the TMF API names are trademarks of TM Forum. This project is not affiliated with, endorsed, or sponsored by TM Forum. The Open API specifications referenced are © TM Forum.
