# Changelog

All notable changes to the [`tmforum`](https://pypi.org/project/tmforum/) package are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) (0.x — API may change between minor versions).

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
