# Changelog

All notable changes to the [`tmforum`](https://pypi.org/project/tmforum/) package are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) (0.x — API may change between minor versions).

## 0.13.0 — 2026-09-01

Source spec: TMF760 Product Configuration v5.0.0.

Completes the API's second REST resource, `QueryProductConfiguration` — the task
that returns the constraints within which a product may be configured (for a new
offering) or the actions that may be applied to it (for a product from
inventory). Its whole sub-entity graph (`ProductConfiguration` and below) was
already present from the `CheckProductConfiguration` side and is reused
unchanged; `ProductConfiguration` needed no fields added, matching the spec 17
for 17.

The spec's `oneOf` pseudo-schemas (`ProductRefOrValue`, `PartyRefOrPartyRoleRef`,
`PartyOrPartyRole`, `PlaceRefOrValue`, `IntentRefOrValue`,
`GeographicLocationRefOrValue`) get no classes of their own — the SDK inlines
them as `Union[...]` at the field, as it already does elsewhere. `Hub`, the eight
`*Event` listeners and the `_EVO`/`_RES` variants are not modelled.

`QueryProductConfigurationItem.state` is typed `Optional[str]`: the spec declares
a plain string with no enumeration (the description offers "accepted, rejected"
only as an example), so unlike the `Check` sibling it gets no enum.

### Added

- `QueryProductConfiguration` (CRUD,
  `productConfiguration/v5/queryProductConfiguration`) — `id`, `href`,
  `instantSync`, `state`, `channel`, `contextEntity`, `contextCharacteristic`,
  `relatedParty`, `requestProductConfigurationItem`,
  `computedProductConfigurationItem`.
- `QueryProductConfigurationItem` — `id`, `state`, `stateReason`, `contextItem`,
  `productConfiguration`, `productConfigurationItemRelationship` and the
  recursive `queryProductConfigurationItem`. Requires `id` at instantiation,
  mirroring `CheckProductConfigurationItem`.
- `CheckProductConfiguration` is now a CRUD resource: it gains `BaseCRUDMixin`
  and `get_resource_path` → `productConfiguration/v5/checkProductConfiguration`.
- `ItemRef.entityId` — present in the spec, previously missing alongside
  `entityHref` and `itemId`.
- `CreditProfile.id` and `CreditProfile.href` — the spec derives it from
  `Addressable`.

### Notes

`GeographicAddress`, `GeographicLocation`, `GeographicSite`, `Intent` and
`AgreementItemRef` remain `NotImplementedError` stubs. TMF760 references them
transitively through `Product`, and its spec carries their full field sets, but
they belong to other APIs and filling them in is left to those.

## 0.12.0 — 2026-09-01

Source spec: TMF936 Open Gateway Operate API — Product Catalog v5.0.0.

Adds the GSMA Open Gateway specializations of the product catalog: the two REST
resources the API exposes (`productOffering`, `productSpecification`) and the
sub-entities and enumerations they narrow. TMF936 layers its types over an
abstract DCS tier (`DcsProductOffering`, `DcsProductSpecification`, …), each
documented as "a subset of the standard schema"; rather than duplicate that
tier, the Open Gateway classes extend the SDK's existing `ProductOffering` /
`ProductSpecification` / `ProductOfferingPrice` / `Attachment` and override only
the fields TMF936 constrains. Consequence: `to_dict()` emits
`@baseType: "ProductOffering"` where a TMF936 server emits
`"DcsProductOffering"`. `Hub`, the four `*Event` schemas and their payloads, the
`_RES` variants and `Error` are not modelled.

This spec has no `_FVO`/`_MVO` variants.

### Added

- `OpenGatewayProductOffering` (CRUD,
  `openGatewayOperateAPIProductCatalog/v5/productOffering`, extends
  `ProductOffering`) — narrows `lifecycleStatus`, `productSpecification`,
  `productOfferingPrice`, `allowedAction` and `attachment`; adds
  `productOfferingTermOrConditionSpecification`.
- `OpenGatewayProductSpecification` (CRUD,
  `openGatewayOperateAPIProductCatalog/v5/productSpecification`, extends
  `ProductSpecification`) — narrows `lifecycleStatus`,
  `productSpecificationRelationship` and `attachment`; adds `allowedAction`,
  which the standard `ProductSpecification` does not carry.
- `UsageVolumeProductSpecification` — discriminator subtype, no added fields.
- `OpenGatewayProductOfferingPrice` (extends `ProductOfferingPrice`) — narrows
  `lifecycleStatus` and `priceType`.
- `OpenGatewayProductOfferingTermOrConditionSpecification` — `id`, `name`,
  `description`, `attachment`.
- `OpenGatewayProductSpecificationRelationship` (extends
  `ProductSpecificationRelationship`) — narrows `relationshipType`.
- `OpenGatewayAttachment` (extends `Attachment`) — narrows `attachmentType`;
  `OpenGatewayFileAttachment` for base64 `content`.
- `ApiVersionInformation` — `apiName`, `apiVersion`, `apiBasePath`,
  `apiGrantInformation`, `apiStatus`.
- `ApiGrantInformation` — `purpose`, `scope`, `grantType`, `legalBasis`.
- `TargetProductOrderItemSchema` — `@schemaLocation` of the target product
  order item schema.

### New refs

- `OpenGatewayProductSpecificationRef` (extends `ProductSpecificationRef`,
  referred type `OpenGatewayProductSpecification`).

### New enums

- `OpenGatewayProductOfferingLifecycleStatusType`,
  `OpenGatewayProductSpecificationLifecycleStatus`,
  `OpenGatewayProductOfferingPriceLifecycleStatus`,
  `OpenGatewayProductOfferingPriceType`,
  `OpenGatewayAllowedProductActionType`, `OpenGatewayAttachmentType`,
  `OpenGatewayProductSpecificationRelationshipType`.
- `ApiStandardNameType`, `ApiStatusType`.
- `DpvPurposeType` (95 values) and `DpvLegalBasisType` (25 values), from the
  W3C Data Privacy Vocabulary v2.

### Changed

- `ApiProductSpecification` now extends `OpenGatewayProductSpecification`
  instead of `ProductSpecification`, and gains `apiStandardName` and
  `apiVersionInformation`. It was previously an empty subclass. The rebase is
  required for `@type` resolution: `from_dict` only switches to a subtype that
  is a subclass of the calling class, so without it
  `OpenGatewayProductSpecification.query_get()` against `/productSpecification`
  would silently drop the API fields. Its resource path changes from
  `productCatalogManagement/v5` to
  `openGatewayOperateAPIProductCatalog/v5/productSpecification`.
- `OpenGatewayURLAttachment` now extends `OpenGatewayAttachment` instead of
  `Attachment`. No fields change — `url` and `mimeType` are still inherited.
- `OpenGatewayAllowedProductAction.action` is narrowed from `ProductActionType`
  to `OpenGatewayAllowedProductActionType` (`add`, `delete`).

## 0.11.0 — 2026-09-01

Source spec: TMF679 Product Offering Qualification v5.0.0.

Adds the geographic place sub-entities the TMF679 payloads reference but the
SDK did not yet model, together with the calendar value objects they use.
None of these are REST resources in the spec, so no `get_resource_path` is
added and the supported-API table is unchanged. Fields are the union across
each schema's base, `_FVO` and `_MVO` variants (identical in all seven cases —
only `required` markers and variant-suffixed types differ); `_EVO` and `_RES`
variants are not modelled.

### New entities

- `HourPeriod` — `startHour`, `endHour`
- `CalendarPeriod` — `day`, `timeZone`, `hourPeriod`, `status`
- `GeographicSubAddressUnit` — `subUnitNumber`, `subUnitType`
- `GeographicSubAddress` — `id`, `href`, `name`, `buildingName`, `levelNumber`,
  `levelType`, `privateStreetName`, `privateStreetNumber`, `subUnit`,
  `subAddressType`
- `GeographicSiteRelationship` — `id`, `href`, `role`, `relationshipType`,
  `validFor`
- `GeographicSiteFeature` (extends `Feature`) — `validFor`, `attachment`,
  `note`, `relatedParty`, `featureCategory`. Note that `validFor` here is a
  **list of `CalendarPeriod`**, not a `TimePeriod`, matching the spec.

### New refs

- `GeographicAddressRelationship` (extends `EntityRef`, referred type
  `GeographicAddress`) — adds `relationshipType`

### Changed

- No existing classes were modified; no fields were added to existing entities.

## 0.10.0 — 2026-08-30

Source spec: TMF676 Payment Management v4.0.0.

The SDK previously covered TMF676 only through `PaymentPlan`. This release adds
the API's two REST resources — `Payment` and `Refund` — plus the sub-entities
they depend on. Paths follow the spec's `basePath` (`payment/v4`), matching the
existing `PaymentPlan` path.

This is a Swagger 2.0 spec, so there are no `_FVO`/`_MVO` variants; the
`_Create` variants add no fields over their base schemas — they only omit
server-assigned ones — so each entity is modelled from the base schema alone.
`*Event` / `*EventPayload`, `EventSubscription` and `Error` schemas are not
modelled.

### Added

- `Payment` (CRUD, `payment/v4/payment`) — settlement of one or more items,
  with payer, channel, account, payment method and per-item amounts.
- `Refund` (CRUD, `payment/v4/refund`) — reimbursement of a previous payment,
  referencing it via `PaymentRef` and carrying the requesting party.
- `PaymentItem` — an individual item settled by a `Payment`.
- `PaymentMethod` — a means of payment; no path in this spec (owned by TMF670),
  so it is a plain entity without CRUD.
- `PaymentMethodRefOrValue` — payment method carried by reference or by value.
- `PaymentStatus` gained the TMF676 transaction states: `pendingAuthorization`,
  `authorized`, `captured`, `failed`, `canceled`, `denied`, `done` (the existing
  `due` / `paid` / `overdue` account values are unchanged). The same value set
  covers the spec's `PaymentStatusExampleType` and `RefundStatusExampleType`.
- `AccountRef` gained `description`, present in the spec's `AccountRef`.

`AccountRef`, `ChannelRef`, `PaymentRef`, `PaymentMethodRef`, `Money`,
`TimePeriod`, `RelatedParty` and `EntityRef` already existed and are reused
as-is. Note that the SDK's `RelatedParty` is v5-shaped (it also carries
`partyOrPartyRole`); all fields TMF676 v4 needs are present.

## 0.9.0 — 2026-08-30

Source spec: TMF641 Service Ordering v4.2.0.

The SDK had no TMF641 coverage at all. This release adds all three of the API's
REST resources plus the sub-entities, references and enums they depend on. Paths
follow the spec's `basePath` (`serviceOrdering/v4`).

This is a Swagger 2.0 spec, so there are no `_FVO`/`_MVO` variants; the
`_Create` / `_Update` variants add no fields over their base schemas — they only
omit server-assigned ones — so each entity is modelled from the base schema
alone, in line with the SDK's single-class-plus-`BaseCRUDMixin` pattern.
`*Event` / `*EventPayload` schemas are not modelled.

`ServiceOrderSpecification` and `ServiceOrderItemSpecification` are each a strict
superset of the spec's `OrderSpecification` / `OrderItemSpecification`, so the
generic bases are implemented as classes in their own right and the service
variants subclass them.

### Added

- `ServiceOrder` — CRUD resource at `serviceOrdering/v4/serviceOrder`: `id`,
  `href`, `category`, `description`, `externalId`, `notificationContact`,
  `priority`, `cancellationDate`, `cancellationReason`, `completionDate`,
  `expectedCompletionDate`, `lastUpdate`, `orderDate`, `requestedCompletionDate`,
  `requestedStartDate`, `startDate`, `state`, `orderSpecification`,
  `errorMessage`, `externalReference`, `jeopardyAlert`, `milestone`, `note`,
  `orderCharacteristic`, `orderRelationship`, `relatedEntity`, `relatedParty`,
  `serviceOrderItem`.
- `CancelServiceOrder` — CRUD resource at `serviceOrdering/v4/cancelServiceOrder`:
  `id`, `href`, `cancellationReason`, `completionMessage`,
  `effectiveCancellationDate`, `requestedCancellationDate`, `state`,
  `errorMessage`, `serviceOrder`.
- `ServiceOrderSpecification` — CRUD resource at
  `serviceOrdering/v4/serviceOrderSpecification`, subclassing `OrderSpecification`
  and adding `serviceOrderItemSpecification`.
- `OrderSpecification` — generic order template: `id`, `href`, `description`,
  `name`, `lastUpdate`, `lifecycleStatus`, `version`, `isAutoResumeAllowed`,
  `isAutoUnlockAllowed`, `isBundle`, `isSyncModeEnabled`, `failurePolicy`,
  `sequencingPolicy`, `targetEntitySchema`, `validFor`, `workflow`, `attachment`,
  `constraint`, `entitySpecRelationship`, `externalIdentifier`, `relatedParty`,
  `specCharacteristic`.
- `OrderItemSpecification` — generic order item template: `id`, `description`,
  `name`, `attachment`, `constraint`, `orderItemSpecRelationship`,
  `specCharacteristic`.
- `ServiceOrderItemSpecification` — subclasses `OrderItemSpecification`, adding
  `actionType`, `otherAction`, `serviceCategory`, `serviceSpecification`.
- `ServiceOrderItem` — `id`, `name`, `otherAction`, `quantity`, `action`, `state`,
  `appointment`, `service`, `errorMessage`, `modifyPath`, `orderItemCharacteristic`,
  `relatedParty`, `serviceOrderItem` (self-nesting), `serviceOrderItemRelationship`.
- `ServiceRefOrValue` — a service carried by reference or by value, mirroring
  `ResourceRefOrValue`.
- `ServiceOrderMilestone` (subclasses `Milestone`), `ServiceOrderJeopardyAlert`
  (subclasses `JeopardyAlert`), `ServiceOrderErrorMessage` and
  `ServiceOrderItemErrorMessage` (both subclass `ErrorMessage`, adding `timestamp`).
- `ServiceOrderRelationship`, `ServiceOrderItemRelationship`,
  `OrderItemSpecRelationship`, `ContextUpdate`, `ExternalReference`.
- `JsonPatch` — `op`, `path`, `value`. RFC 6902's `from` member is not modelled:
  it is a Python keyword and the serializer maps field names to wire names
  verbatim. It applies only to `move` / `copy`, which TMF641 payloads do not use.
- References: `ServiceOrderRef`, `ServiceOrderItemRef`, `EntitySpecificationRef`,
  `ProcessFlowSpecificationRef`.
- Enums: `ServiceOrderStateType`, `ServiceOrderItemStateType`,
  `ServiceOrderItemActionType`, `OrderFailurePolicy`, `OrderSequencingPolicy`.
  `ServiceOrderItemActionType` carries the `other` member that the existing
  `OrderItemActionType` / `ItemActionType` lack.
- `TaskStateType` gains the `accepted` member used by `CancelServiceOrder.state`.
- `Service` gains `operatingStatusContextUpdate`; `ExternalIdentifier` gains
  `href`; `Feature` gains `constraint` (distinct from the existing
  `policyConstraint`).

### Notes

Two spec/SDK divergences are left as they are: `Characteristic.value` and
`CharacteristicValueSpecification.value` stay on the typed subclasses
(`StringCharacteristic`, `IntegerCharacteristic`, …), and
`RelatedEntityRefOrValue` keeps the SDK's `role` + `entity` shape rather than the
spec's flat `id` / `href` / `name`.

## 0.8.0 — 2026-08-28

Source spec: TMF652 Resource Order Management v4.0.0.

The SDK had no TMF652 coverage at all. This release adds both of the API's REST
resources plus the sub-entities and references they depend on. Paths follow the
spec's `basePath` (`resourceOrderingManagement/v4`); no v5 TMF652 spec is vendored.

The `_Create` / `_Update` schema variants add no fields over their base schemas —
they only omit server-assigned ones — so each entity is modelled from the base
schema alone, in line with the SDK's single-class-plus-`BaseCRUDMixin` pattern.

### Added

- `ResourceOrder` — CRUD resource at `resourceOrderingManagement/v4/resourceOrder`:
  `id`, `href`, `category`, `description`, `name`, `externalId`, `orderType`,
  `priority`, `state`, `orderDate`, `completionDate`, `expectedCompletionDate`,
  `requestedCompletionDate`, `requestedStartDate`, `startDate`, `externalReference`,
  `note`, `orderItem`, `relatedParty`.
- `CancelResourceOrder` — CRUD resource at
  `resourceOrderingManagement/v4/cancelResourceOrder`: `id`, `href`,
  `cancellationReason`, `effectiveCancellationDate`, `requestedCancellationDate`,
  `state` (`TaskStateType`), `resourceOrder`.
- `ResourceOrderItem` — `id`, `action` (`OrderItemActionType`), `quantity`, `state`,
  `appointment`, `orderItemRelationship`, `resource`, `resourceSpecification`.
- `ResourceOrderItemRelationship` — `relationshipType`, `orderItem`.
- `ResourceRefOrValue` — a resource carried by reference or by value.
- `AttachmentRefOrValue` — subclasses `Attachment`, adding `isRef` and
  `@referredType`.
- `ExternalId` — `id`, `entityType`, `owner`. Kept distinct from the existing
  `ExternalIdentifier`, which has a different shape (`externalIdentifierType`,
  `value`) and a different `@type` on the wire.
- `ResourceOrderRef`, `ResourceOrderItemRef` — new `EntityRef` subclasses.
- `RelatedPlaceRefOrValue` gained `id`, `href`, `name` and `@referredType`, the flat
  shape TMF652 uses. Existing fields and defaults are unchanged.

### Notes

- `ResourceOrder.state` and `ResourceOrderItem.state` are typed `Optional[str]`:
  TMF652 v4 declares both as free-form strings with no enumeration.
- `CancelOrder` is defined in the spec but referenced nowhere; it is not modelled.
- Event, event-payload and hub schemas are out of scope, as in previous releases.

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
