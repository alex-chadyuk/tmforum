# tmforum

Unofficial Python SDK for [TM Forum Open APIs](https://www.tmforum.org/oda/open-apis/) — plain-dataclass entity models, `@type`-aware (de)serialization, and thin REST CRUD helpers.

- **No heavy dependencies** — just `requests`. Entities are standard-library `dataclasses`, not pydantic models.
- **Polymorphism-aware serialization** — `from_dict` resolves `@type` / `@referredType` discriminators to the right Python class; `to_dict` emits them back, so round-tripping TMF payloads preserves their type structure.
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
| TMF622 Product Ordering | `productOrdering/v5` | `ProductOrder` |
| TMF637 Product Inventory | `productInventory/v5` | `Product` |
| TMF632 Party Management | `partyManagement/v5` | `Individual`, `Organization` |
| TMF669 Party Role | `partyRoleManagement/v5` | `PartyRole` |
| TMF666 Account Management | `accountManagement/v5` | `BillingAccount`, `FinancialAccount`, `BillingCycleSpecification` |
| TMF678 Customer Bill | `customerBill/v5` | `AppliedCustomerBillingRate` |
| TMF648 Quote | `quoteManagement/v5` | `Quote` |
| TMF679 Product Offering Qualification | `productOfferingQualification/v5` | `CheckProductOfferingQualification`, `QueryProductOfferingQualification` |
| TMF699 Sales Management | `salesManagement/v5` | `SalesLead` |
| TMF723 Policy Management | `policyManagement/v5` | `PolicyDomain`, `ManagedPolicy`, `ManagedPolicyVariable`, `PolicyCatalog` |
| TMF638 Service Inventory | `serviceInventory/v5` | `Service` |
| TMF639 Resource Inventory | `resourceInventory/v5` | `Resource` |
| TMF634 Resource Catalog | `resourceCatalog/v5` | `ResourceSpecification` |
| TMF685 Resource Pool | `resourcePool/v5` | `ResourcePool`, `ResourcePoolSpecification`, `CapacitySpecification` |
| TMF676 Payment | `payment/v4` | `PaymentPlan` |
| TMF760 Product Configuration | *(entity models only)* | `CheckProductConfiguration.from_order()` |

## How it works

Every entity is a `@dataclass` inheriting from `Entity`, which provides recursive `from_dict` / `to_dict` / `to_json`. Type resolution uses each field's type hints plus the payload's `@type` discriminator, so nested and polymorphic structures (e.g. `RelatedPartyRefOrPartyRoleRef`, price alterations, characteristic subtypes) deserialize into the correct classes.

Entities that map to REST resources also inherit `BaseCRUDMixin`, which implements `from_id`, `create`, `read`, `update` (JSON PATCH semantics), `query_get`, and `delete` against `{context.api_base_url}/{resource_path}`. A `Context` dataclass carries `api_base_url`, `access_token`, `headers`, an optional logger, and OAuth-related fields — pass it to every call; there is no global state.

## Status

Alpha. The entity models and serialization are exercised by a pure-offline test suite; the CRUD layer follows the TMF REST conventions, but server implementations vary in the extensions and versions they accept. Issues and PRs welcome.

## License & trademark notice

MIT — see [LICENSE](LICENSE).

This is an **unofficial, community project**. TM Forum® and the TMF API names are trademarks of TM Forum. This project is not affiliated with, endorsed, or sponsored by TM Forum. The Open API specifications referenced are © TM Forum.
