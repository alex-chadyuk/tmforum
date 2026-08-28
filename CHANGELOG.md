# Changelog

All notable changes to the [`tmforum`](https://pypi.org/project/tmforum/) package are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) (0.x — API may change between minor versions).

## 0.7.0 — 2026-08-28

Source spec: TMF633 Service Catalog Management v4.0.0.

All four REST resources of TMF633 were missing from the SDK; this release adds them
together with the sub-entities and references they depend on. Paths follow the spec's
`basePath` (`serviceCatalogManagement/v4`) rather than the v5 used elsewhere, because
no v5 TMF633 spec is vendored.

### Added

- `ServiceCatalog` — CRUD resource at `serviceCatalogManagement/v4/serviceCatalog`:
  `id`, `href`, `name`, `description`, `version`, `lifecycleStatus`, `lastUpdate`,
  `validFor`, `category`, `relatedParty`.
- `ServiceCategory` — CRUD resource at `serviceCatalogManagement/v4/serviceCategory`:
  as above plus `parentId`, `isRoot`, `serviceCandidate`, and nested `category`.
- `ServiceCandidate` — CRUD resource at `serviceCatalogManagement/v4/serviceCandidate`:
  as above plus `serviceSpecification`.
- `ServiceSpecification` — CRUD resource at
  `serviceCatalogManagement/v4/serviceSpecification`: `isBundle`, `targetEntitySchema`,
  `attachment` (typed as the spec's `AttachmentRefOrValue` union,
  `Union[Attachment, AttachmentRef]`), `constraint`, `entitySpecRelationship`,
  `featureSpecification`, `relatedParty`, `resourceSpecification`,
  `serviceLevelSpecification`, `serviceSpecRelationship`, `specCharacteristic`.
- `ServiceSpecRelationship` — `id`, `href`, `name`, `relationshipType`, `role`,
  `validFor`.
- `EntitySpecificationRelationship` — as above plus
  `associationSpec: AssociationSpecificationRef`.
- `TargetEntitySchema` — `_schema_location`, the entity counterpart to the existing
  `TargetResourceSchema`.
- `FeatureSpecificationCharacteristic` — subclass of `CharacteristicSpecification`
  adding `featureSpecCharRelationship` and `featureSpecCharacteristicValue`.
  Subclassing keeps `FeatureSpecification.featureSpecCharacteristic` typed as
  `List[CharacteristicSpecification]` while letting the `@type` discriminator resolve
  payloads to the richer class.
- `FeatureSpecificationCharacteristicRelationship` — `characteristicId`, `featureId`,
  `name`, `relationshipType`, `resourceSpecificationHref`, `resourceSpecificationId`,
  `validFor`.
- New references: `AssociationSpecificationRef`, `ConstraintRef` (with `version`),
  `ServiceCategoryRef` (with `version`), `ServiceLevelSpecificationRef`.
- `version` on the existing `ServiceCandidateRef`, per the spec.
- `constraint: List[ConstraintRef]` on the existing `FeatureSpecification`. The
  pre-existing `policyConstraint: List[PolicyRef]` is unchanged.
- `tests/test_service_catalog.py` covering all four resources.

### Notes

- `ImportJob` and `ExportJob` already match the TMF633 field set, but their
  `get_resource_path` remains bound to `resourceCatalog/v5`, so TMF633's
  `serviceCatalogManagement/v4` job endpoints are not addressable.
- `Quantity.amount` stays `int`; TMF633 types it as `number`.

## 0.6.0 — 2026-08-28

Source spec: TMF632 Party Management v5.0.0.

Both REST resources of TMF632 (`Individual`, `Organization`) were already present and
complete; this release fills in the sub-entities beneath them and replaces the
`NotImplementedError` stubs for the party-role subtypes.

### Added

- `Disability` — `disabilityCode`, `disabilityName`, `validFor`.
- `LanguageAbility` — `languageCode`, `languageName`, `isFavouriteLanguage`, and the
  `writingProficiency` / `readingProficiency` / `speakingProficiency` /
  `listeningProficiency` scores, plus `validFor`.
- `Skill` — `skillCode`, `skillName`, `evaluatedLevel`, `comment`, `validFor`.
- `OtherNameIndividual` — the individual counterpart to the existing
  `OtherNameOrganization`: `title`, `aristocraticTitle`, `generation`, `givenName`,
  `preferredGivenName`, `familyNamePrefix`, `familyName`, `legalName`, `middleName`,
  `fullName`, `formattedName`, `validFor`.
- `IndividualIdentification` — `identificationId`, `identificationType`,
  `issuingAuthority`, `issuingDate`, `validFor`, and `attachment` typed as the spec's
  `AttachmentRefOrValue` union (`Union[Attachment, AttachmentRef]`).
- `CreditProfile` — `creditProfileDate`, `creditRiskRating`, `creditScore`, `validFor`.
  Distinct from the pre-existing `PartyCreditProfile`, which the spec keeps separate.
- `PartyRoleSpecificationRef` — reference to a party role specification.
- Characteristic subtypes: `ObjectCharacteristic` plus the array-valued
  `BooleanArrayCharacteristic`, `IntegerArrayCharacteristic`, `NumberArrayCharacteristic`,
  `ObjectArrayCharacteristic`, and `StringArrayCharacteristic`.
- `tests/test_party.py` covering `Individual`, `Organization`, and the party-role
  subtypes: nested-type sweeps, `@type` round-trips, list validation, and resource paths.

### Changed

- `Consumer`, `Producer`, `BusinessPartner`, and `Supplier` are now real subclasses of
  `PartyRole` instead of stubs raising `NotImplementedError`. This matches the spec, where
  all four derive from `PartyRole` and add no fields of their own. **Breaking for anyone
  relying on their previous bases** — `Consumer` and `Producer` derived from `Party`, and
  `BusinessPartner` and `Supplier` from `Entity`. All four now inherit `PartyRole`'s fields
  and its `partyRoleManagement/v5/partyRole` resource path.
- `Individual`: `disability`, `skill`, `languageAbility`, `individualIdentification`, and
  `otherName` were typed `List[dict]` and are now typed to their proper entity classes, so
  `from_dict` deserializes them instead of leaving raw dicts.
- `PartyRole`: added `agreement` (`List[AgreementRef]`), `creditProfile`
  (`List[CreditProfile]`), and `partyRoleSpecification` (`PartyRoleSpecificationRef`).
- `Characteristic`: added `valueType` on the base class, where the spec declares it. The
  scalar subtypes continue to pin it to their own constant.

## 0.5.0 — 2026-08-28

Source spec: TMF634 Resource Catalog Management v5.0.0.

### Added

- `ResourceCatalog` — the root catalog entity, CRUD-enabled at
  `resourceCatalog/v5/resourceCatalog`. Fields merged from the spec's `Catalog` parent and
  `ResourceCatalog` itself: `id`, `href`, `name`, `description`, `catalogType`, `version`,
  `lifecycleStatus`, `lastUpdate`, `validFor`, `category`, `relatedParty`,
  `externalIdentifier`.
- `ResourceCategory` — CRUD-enabled at `resourceCatalog/v5/resourceCategory`; groups
  candidates and nests via `category` (`parentId`, `isRoot`, `resourceSpecification`,
  `resourceCandidate`, `relatedParty`, `externalIdentifier`, `validFor`).
- `ResourceCandidate` — CRUD-enabled at `resourceCatalog/v5/resourceCandidate`; publishes a
  `ResourceSpecificationRef` into one or more catalogs (`category`, `validFor`,
  `lifecycleStatus`, `externalIdentifier`).
- `ImportJob` and `ExportJob` — batch catalog load/extract tasks, CRUD-enabled at
  `resourceCatalog/v5/importJob` and `resourceCatalog/v5/exportJob` (`contentType`,
  `creationDate`, `completionDate`, `errorLog`, `path`, `url`, `status`; `ExportJob` also
  carries `query`).
- New reference class: `ResourceCategoryRef` (`version`).
- New enum: `JobStateType` (`Not Started`, `Running`, `Succeeded`, `Failed` — the spec
  defines these values in Title Case rather than camelCase).
- Test coverage for all five new resources in `tests/test_resource_catalog.py`.

### Changed

- `ResourceCandidateRef` gains `version`, which the spec defines but the SDK was missing.

### Notes

- `ResourceCandidate.name` is included even though the spec's base schema omits it from
  `properties`: `ResourceCandidate_FVO` lists it under `required` and every example payload
  carries it.
- `lifecycleStatus` is typed `Optional[str]` on all three catalog entities — TMF634 declares
  it as a plain string, unlike TMF620's enumerated equivalent.
- The spec's abstract `Catalog` parent is not implemented as its own class; its fields are
  merged into `ResourceCatalog`, matching how `ProductCatalog` extends `Entity` directly.

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
