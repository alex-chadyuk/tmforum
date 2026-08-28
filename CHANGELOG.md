# Changelog

All notable changes to the [`tmforum`](https://pypi.org/project/tmforum/) package are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) (0.x — API may change between minor versions).

## 0.4.0 — 2026-08-28

Source spec: TMF634 Resource Catalog Management v5.0.0.

### Added

- New `ResourceSpecification` subtypes, resolved polymorphically by `@type` and sharing the
  existing `resourceCatalog/v5/resourceSpecification` path:
  - `PhysicalResourceSpecification` (`model`, `part`, `sku`, `vendor`).
  - `ResourceFunctionSpecification`, a `LogicalResourceSpecification` subtype
    (`connectionPointSpecification`, `connectivitySpecification`).
- New entities: `ResourceGraphSpecification` (`id`, `href`, `name`, `description`,
  `graphSpecificationRelationship`, `connectionSpecification`),
  `ResourceGraphSpecificationRelationship` (`relationshipType`, `resourceGraph`) and
  `ConnectionSpecification` (`id`, `href`, `name`, `associationType`, `endpointSpecification`).
- New reference classes: `ConnectionPointSpecificationRef` (`version`),
  `EndpointSpecificationRef` (`role`, `isRoot`, `connectionPointSpecification`),
  `ResourceGraphSpecificationRef`.
- New enums: `ConnectionAssociationType`, `ResourceGraphSpecificationRelationshipType`.
- Resource catalog test coverage in `tests/test_resource_catalog.py`.

### Notes

- No existing classes were modified. `ResourceSpecification` and its whole dependency tree
  (`TargetResourceSchema`, `FeatureSpecification`, `FeatureSpecificationRelationship`,
  `CharacteristicSpecification`, `CharacteristicSpecificationRelationship`,
  `CharacteristicValueSpecification`, `ResourceSpecificationRelationship`, `Attachment`,
  `AttachmentRef`, `RelatedPartyRefOrPartyRoleRef`, `ExternalIdentifier`, `PolicyRef`,
  `IntentSpecificationRef`, `TimePeriod`, `Quantity`) was already field-complete against the
  base, `_FVO` and `_MVO` variants.
- The spec's `CharacteristicSpecification.@valueSchemaLocation` is not implemented: `Entity`
  only maps the reserved `@schemaLocation`, `@referredType`, `@type` and
  `@targetProductOrderItemSchema` keys, and supporting a new one would require changing the
  base class's serialization.

## 0.3.0 — 2026-08-28

Source spec: TMF699 Sales Management v5.0.0.

### Added

- New CRUD resource `SalesOpportunity` (`salesManagement/v5/salesOpportunity`), covering
  `name`, `description`, `creationDate`, `referredDate`, `rating`, `salesOpportunityType`,
  `status`, `statusChangeDate`, `statusChangeReason`, `priority`, `validFor`, `category`,
  `channel`, `marketSegment`, `marketingCampaign`, `salesLead`, `revenueEstimate`, `note`,
  `agreement`, `relatedParty`, `quote`, `salesProject` and `salesOpportunityItem`.
- New entity: `SalesOpportunityItem` (`id`, `action`, `rating`, `priority`,
  `salesOpportunityItemStatus`, `validFor`, `product`, `productOffering`, `revenueEstimate`,
  `salesActivity`, `quoteItem`, `note`, `relatedParty`).
- New reference classes: `SalesActivityRef`, `SalesProjectRef`.
- New enums: `SalesOpportunityStateType`, `SalesOpportunityItemStateType`.
- `SalesOpportunity` test coverage in `tests/test_sales.py`.

### Notes

- The spec's `SalesPriorityType` maps to the existing `SalesLeadPriorityType` enum
  (identical members `low`/`medium`/`high`); no duplicate enum was introduced.
- No existing classes were modified — every entity in `SalesOpportunity`'s dependency tree
  (`RevenueEstimate`, `Note`, `QuoteRef`, `QuoteItemRef`, `RelatedPartyRefOrPartyRoleRef`,
  `CategoryRef`, `ChannelRef`, `MarketSegmentRef`, `MarketingCampaignRef`, `AgreementRef`,
  `ProductRef`, `ProductOfferingRef`, `SalesLeadRef`) was already field-complete.

## 0.2.0 — 2026-08-27

Source spec: TMF699 Sales Management v5.0.0.

### Added

- New reference classes: `MarketingCampaignRef`, `GeographicAddressRef`.
- New entity: `RevenueEstimate` (`amount`, `description`, `revenueType`).
- New `ContactMedium` subtypes: `FaxContactMedium` (`faxNumber`), `SocialContactMedium` (`socialNetworkId`).
- `SalesLead`: new v5 fields `salesLeadType`, `revenueEstimate`, `marketingCampaign`, `marketSegment`, `productOffering`, `agreement`, `prospectContactMedium`, `productSpecification`, `category`, `product` (v4 fields `type`, `estimatedRevenue`, `prospectContact` are kept alongside).
- `GeographicAddressContactMedium`: new `geographicAddress` field.
- Test suite for TMF699 Sales (`tests/test_sales.py`).

### Changed

- `SalesLead.salesOpportunity` is now a list (`Optional[List[SalesOpportunityRef]]`), matching the v5 spec.
- `SalesLead.get_resource_path` now targets `salesManagement/v5/salesLead` (was `v4`).
- `AgreementRef` is now implemented (was a `NotImplementedError` placeholder).

## 0.1.0 — 2026-08-06

### Added

- Initial release: dataclass entity models with `@type` / `@referredType`-aware `from_dict` / `to_dict` serialization, plus a thin `BaseCRUDMixin` REST layer driven by a `Context` object.
- Entity coverage for TMF620 Product Catalog, TMF622 Product Ordering, TMF637 Product Inventory, TMF632 Party Management, TMF669 Party Role, TMF666 Account Management, TMF678 Customer Bill, TMF648 Quote, TMF679 Product Offering Qualification, TMF699 Sales Management (`SalesLead`), TMF723 Policy Management, TMF638 Service Inventory, TMF639 Resource Inventory, TMF634 Resource Catalog, TMF685 Resource Pool, TMF676 Payment, and TMF760 Product Configuration (entity models only) — see the "Supported TM Forum APIs" table in the README.
- Pure-offline test suite exercising serialization, polymorphism, and `__post_init__` validation.
