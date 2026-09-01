import pytest
from tmforum import (
    AttachmentRefOrValue,
    CalendarPeriod,
    Characteristic,
    Context,
    EmailContactMedium,
    EntityRef,
    ExternalIdentifier,
    GeographicAddress,
    GeographicAddressRef,
    GeographicAddressRelationship,
    GeographicAddressValidation,
    GeographicLocation,
    GeographicLocationRef,
    GeographicLocationRefOrValue,
    GeographicSite,
    GeographicSiteFeature,
    GeographicSiteRelationship,
    GeographicSubAddress,
    GeographicSubAddressUnit,
    HourPeriod,
    Note,
    PartyRoleRef,
    PhoneContactMedium,
    Quantity,
    RelatedGeographicAddressRef,
    RelatedGeographicLocationRef,
    RelatedPartyRefOrPartyRoleRef,
    TaskStateType,
    TimePeriod,
)


@pytest.fixture
def geographic_sub_address_dict():
    sub_address = {
        "@type": "GeographicSubAddress",
        "@baseType": "Entity",
        "id": "sub-4711",
        "href": "/geographicAddressManagement/v5/geographicSubAddress/sub-4711",
        "name": "Tower B, level 3",
        "buildingName": "Northgate Tower",
        "levelNumber": "3",
        "levelType": "FLOOR",
        "privateStreetName": "Campus Walk",
        "privateStreetNumber": "17",
        "subAddressType": "subUnit",
        "subUnit": [
            {
                "@type": "GeographicSubAddressUnit",
                "@baseType": "Entity",
                "subUnitNumber": "12A",
                "subUnitType": "FLAT",
            },
            {
                "@type": "GeographicSubAddressUnit",
                "@baseType": "Entity",
                "subUnitNumber": "3-7",
                "subUnitType": "RACK",
            },
        ],
    }
    return sub_address


@pytest.fixture
def geographic_sub_address_1(geographic_sub_address_dict):
    return GeographicSubAddress.from_dict(geographic_sub_address_dict)


def test_geographic_sub_address_instantiates_with_id(geographic_sub_address_dict):
    sub_address = GeographicSubAddress.from_dict(geographic_sub_address_dict)
    assert sub_address.id == "sub-4711"
    assert sub_address.buildingName == "Northgate Tower"
    assert sub_address.subAddressType == "subUnit"
    assert sub_address.subUnit[0].subUnitNumber == "12A"


def test_geographic_sub_address_instantiates_classes(geographic_sub_address_1):
    sub_units = geographic_sub_address_1.subUnit
    assert isinstance(sub_units[0], GeographicSubAddressUnit)
    assert isinstance(sub_units[1], GeographicSubAddressUnit)
    assert sub_units[1].subUnitType == "RACK"


def test_geographic_sub_address_to_dict_round_trip(geographic_sub_address_1):
    sub_address_dict = geographic_sub_address_1.to_dict()
    assert sub_address_dict["@type"] == "GeographicSubAddress"
    # direct Entity subclasses do not carry an "@baseType" discriminator
    assert "@baseType" not in sub_address_dict

    sub_unit = sub_address_dict["subUnit"][0]
    assert sub_unit["@type"] == "GeographicSubAddressUnit"
    assert "@baseType" not in sub_unit
    assert sub_unit["subUnitNumber"] == "12A"


def test_geographic_sub_address_raises_when_sub_unit_not_a_list():
    with pytest.raises(ValueError):
        GeographicSubAddress(
            name="Bad sub address",
            subUnit=GeographicSubAddressUnit(subUnitNumber="12A"),
        )


@pytest.fixture
def geographic_site_feature_dict():
    site_feature = {
        "@type": "GeographicSiteFeature",
        "@baseType": "Feature",
        "id": "feat-01",
        "name": "Site access instructions",
        "isBundle": False,
        "isEnabled": True,
        "featureCategory": ["Access Information", "Safety"],
        "featureCharacteristic": [
            {
                "@type": "Characteristic",
                "name": "gateCode",
                "value": "4471",
            }
        ],
        "validFor": [
            {
                "@type": "CalendarPeriod",
                "@baseType": "Entity",
                "day": "mon-to-fri",
                "timeZone": "GMT+1",
                "status": "available",
                "hourPeriod": [
                    {
                        "@type": "HourPeriod",
                        "@baseType": "Entity",
                        "startHour": "08:00",
                        "endHour": "12:00",
                    },
                    {
                        "@type": "HourPeriod",
                        "@baseType": "Entity",
                        "startHour": "13:00",
                        "endHour": "17:30",
                    },
                ],
            },
            {
                "@type": "CalendarPeriod",
                "@baseType": "Entity",
                "day": "weekend",
                "timeZone": "GMT+1",
                "status": "booked",
            },
        ],
        "attachment": [
            {
                "@type": "AttachmentRefOrValue",
                "id": "att-01",
                "name": "Site survey",
                "mimeType": "application/pdf",
                "url": "https://mycsp.com/attachments/att-01.pdf",
                "isRef": False,
            }
        ],
        "note": [
            {
                "@type": "Note",
                "@baseType": "Entity",
                "author": "Jane Doe",
                "date": "2025-07-18T00:00:00Z",
                "text": "Beware of the loose handrail on the east stairwell.",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "@baseType": "Entity",
                "role": "siteOwner",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "id": "role-99",
                    "name": "Facilities manager",
                    "@referredType": "PartyRole",
                },
            }
        ],
    }
    return site_feature


@pytest.fixture
def geographic_site_feature_1(geographic_site_feature_dict):
    return GeographicSiteFeature.from_dict(geographic_site_feature_dict)


def test_geographic_site_feature_instantiates_with_id(geographic_site_feature_dict):
    site_feature = GeographicSiteFeature.from_dict(geographic_site_feature_dict)
    assert site_feature.id == "feat-01"
    assert site_feature.isEnabled is True
    assert site_feature.featureCategory == ["Access Information", "Safety"]
    assert site_feature.validFor[0].hourPeriod[1].endHour == "17:30"


def test_geographic_site_feature_instantiates_classes(geographic_site_feature_1):
    calendar_period = geographic_site_feature_1.validFor[0]
    related_party = geographic_site_feature_1.relatedParty[0]
    assert isinstance(calendar_period, CalendarPeriod)
    assert isinstance(calendar_period.hourPeriod[0], HourPeriod)
    assert isinstance(geographic_site_feature_1.validFor[1], CalendarPeriod)
    assert isinstance(
        geographic_site_feature_1.featureCharacteristic[0], Characteristic
    )
    assert isinstance(geographic_site_feature_1.attachment[0], AttachmentRefOrValue)
    assert isinstance(geographic_site_feature_1.note[0], Note)
    assert isinstance(related_party, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(related_party.partyOrPartyRole, PartyRoleRef)


def test_geographic_site_feature_to_dict_round_trip(geographic_site_feature_1):
    site_feature_dict = geographic_site_feature_1.to_dict()
    assert site_feature_dict["@type"] == "GeographicSiteFeature"
    assert site_feature_dict["@baseType"] == "Feature"

    calendar_period = site_feature_dict["validFor"][0]
    assert calendar_period["@type"] == "CalendarPeriod"
    assert calendar_period["hourPeriod"][0]["@type"] == "HourPeriod"
    assert calendar_period["hourPeriod"][0]["startHour"] == "08:00"


def test_geographic_site_feature_raises_when_valid_for_not_a_list():
    with pytest.raises(ValueError):
        GeographicSiteFeature(
            name="Bad feature",
            validFor=CalendarPeriod(day="monday", status="available"),
        )


@pytest.fixture
def geographic_site_relationship_dict():
    site_relationship = {
        "@type": "GeographicSiteRelationship",
        "@baseType": "Entity",
        "id": "site-88",
        "href": "/geographicSiteManagement/v5/geographicSite/site-88",
        "role": "backupSite",
        "relationshipType": "isBackupOf",
        "validFor": {
            "startDateTime": "2025-07-18T00:00:00Z",
            "endDateTime": "2025-12-31T00:00:00Z",
        },
    }
    return site_relationship


def test_geographic_site_relationship(geographic_site_relationship_dict):
    site_relationship = GeographicSiteRelationship.from_dict(
        geographic_site_relationship_dict
    )
    assert site_relationship.id == "site-88"
    assert site_relationship.role == "backupSite"
    assert site_relationship.relationshipType == "isBackupOf"
    assert isinstance(site_relationship.validFor, TimePeriod)

    site_relationship_dict = site_relationship.to_dict()
    assert site_relationship_dict["@type"] == "GeographicSiteRelationship"
    assert "@baseType" not in site_relationship_dict
    assert site_relationship_dict["validFor"]["endDateTime"] == "2025-12-31T00:00:00Z"


@pytest.fixture
def geographic_address_relationship_dict():
    address_relationship = {
        "@type": "GeographicAddressRelationship",
        "id": "addr-12",
        "name": "Main depot address",
        "href": "/geographicAddressManagement/v5/geographicAddress/addr-12",
        "relationshipType": "isSubAddressOf",
        "@referredType": "GeographicAddress",
    }
    return address_relationship


def test_geographic_address_relationship(geographic_address_relationship_dict):
    address_relationship = GeographicAddressRelationship.from_dict(
        geographic_address_relationship_dict
    )
    assert address_relationship.id == "addr-12"
    assert address_relationship.name == "Main depot address"
    assert address_relationship.relationshipType == "isSubAddressOf"
    assert address_relationship._referred_type == "GeographicAddress"

    address_relationship_dict = address_relationship.to_dict()
    assert address_relationship_dict["@type"] == "GeographicAddressRelationship"
    assert address_relationship_dict["@referredType"] == "GeographicAddress"
    assert address_relationship_dict["relationshipType"] == "isSubAddressOf"


# TMF673 Geographic Address Management v4.0.0


@pytest.fixture
def geographic_address_dict():
    address = {
        "@type": "GeographicAddress",
        "@baseType": "Place",
        "id": "addr-9931",
        "href": "/geographicAddressManagement/v4/geographicAddress/addr-9931",
        "name": "Northgate Tower",
        "streetNr": "42",
        "streetNrSuffix": "B",
        "streetNrLast": "48",
        "streetNrLastSuffix": "D",
        "streetName": "Campus Walk",
        "streetType": "Avenue",
        "streetSuffix": "North",
        "locality": "Docklands",
        "city": "Dublin",
        "stateOrProvince": "Leinster",
        "postcode": "D01 X4F2",
        "country": "Ireland",
        "geographicLocation": {
            "@type": "GeographicLocationRefOrValue",
            "id": "loc-7",
            "href": "/geographicSiteManagement/v4/geographicLocation/loc-7",
            "name": "Northgate Tower footprint",
            "bbox": [-6.24, 53.34, -6.23, 53.35],
            "@referredType": "GeographicLocation",
        },
        "geographicSubAddress": [
            {
                "@type": "GeographicSubAddress",
                "id": "sub-9931-1",
                "name": "Tower B, level 3",
                "buildingName": "Northgate Tower",
                "levelNumber": "3",
                "levelType": "FLOOR",
                "subAddressType": "subUnit",
                "subUnitNumber": "12A",
                "subUnitType": "FLAT",
            }
        ],
    }
    return address


@pytest.fixture
def geographic_address_1(geographic_address_dict):
    return GeographicAddress.from_dict(geographic_address_dict)


def test_geographic_address_instantiates_with_id(geographic_address_dict):
    address = GeographicAddress.from_dict(geographic_address_dict)
    assert address.id == "addr-9931"
    assert address.city == "Dublin"
    assert address.country == "Ireland"
    assert address.postcode == "D01 X4F2"
    assert address.streetNr == "42"
    assert address.streetNrLastSuffix == "D"
    assert address.streetType == "Avenue"
    # inherited from Place
    assert address.name == "Northgate Tower"


def test_geographic_address_instantiates_classes(geographic_address_1):
    assert isinstance(
        geographic_address_1.geographicLocation, GeographicLocationRefOrValue
    )
    assert geographic_address_1.geographicLocation.bbox == [-6.24, 53.34, -6.23, 53.35]
    assert (
        geographic_address_1.geographicLocation._referred_type == "GeographicLocation"
    )

    sub_address = geographic_address_1.geographicSubAddress[0]
    assert isinstance(sub_address, GeographicSubAddress)
    assert sub_address.levelType == "FLOOR"


def test_geographic_sub_address_carries_flat_sub_unit_fields(geographic_address_1):
    """TMF673 v4 puts subUnitNumber/subUnitType flat on the sub-address, while
    the v5 shape nests them under subUnit; both must survive from_dict."""
    sub_address = geographic_address_1.geographicSubAddress[0]
    assert sub_address.subUnitNumber == "12A"
    assert sub_address.subUnitType == "FLAT"
    assert sub_address.subUnit == []


def test_geographic_address_to_dict_round_trip(geographic_address_1):
    address_dict = geographic_address_1.to_dict()
    assert address_dict["@type"] == "GeographicAddress"
    assert address_dict["@baseType"] == "Place"
    assert address_dict["city"] == "Dublin"

    location = address_dict["geographicLocation"]
    assert location["@type"] == "GeographicLocationRefOrValue"
    assert location["@referredType"] == "GeographicLocation"
    assert location["bbox"] == [-6.24, 53.34, -6.23, 53.35]

    sub_address = address_dict["geographicSubAddress"][0]
    assert sub_address["@type"] == "GeographicSubAddress"
    assert sub_address["subUnitNumber"] == "12A"


def test_geographic_address_raises_when_sub_address_not_a_list():
    with pytest.raises(ValueError):
        GeographicAddress(
            name="Bad address",
            geographicSubAddress=GeographicSubAddress(name="Tower B"),
        )


def test_geographic_address_resource_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert GeographicAddress.get_resource_path(context) == (
        "https://mycsp.com/tmf-api/geographicAddressManagement/v4/geographicAddress"
    )


@pytest.fixture
def geographic_location_dict():
    location = {
        "@type": "GeographicLocation",
        "@baseType": "Place",
        "id": "loc-7",
        "href": "/geographicSiteManagement/v4/geographicLocation/loc-7",
        "name": "Northgate Tower footprint",
        "bbox": [-6.24, 53.34, -6.23, 53.35],
    }
    return location


def test_geographic_location(geographic_location_dict):
    location = GeographicLocation.from_dict(geographic_location_dict)
    assert location.id == "loc-7"
    assert location.name == "Northgate Tower footprint"
    assert location.bbox == [-6.24, 53.34, -6.23, 53.35]

    location_dict = location.to_dict()
    assert location_dict["@type"] == "GeographicLocation"
    assert location_dict["@baseType"] == "Place"
    assert location_dict["bbox"] == [-6.24, 53.34, -6.23, 53.35]


def test_geographic_location_raises_when_bbox_not_a_list():
    with pytest.raises(ValueError):
        GeographicLocation(name="Bad location", bbox=-6.24)


def test_geographic_location_ref():
    location_ref = GeographicLocationRef.from_dict(
        {
            "@type": "GeographicLocationRef",
            "id": "loc-7",
            "href": "/geographicSiteManagement/v4/geographicLocation/loc-7",
            "name": "Northgate Tower footprint",
        }
    )
    assert location_ref.id == "loc-7"
    assert location_ref._referred_type == "GeographicLocation"

    location_ref_dict = location_ref.to_dict()
    assert location_ref_dict["@type"] == "GeographicLocationRef"
    assert location_ref_dict["@referredType"] == "GeographicLocation"


@pytest.fixture
def geographic_address_validation_dict(geographic_address_dict):
    validation = {
        "@type": "GeographicAddressValidation",
        "id": "val-556",
        "href": "/geographicAddressManagement/v4/geographicAddressValidation/val-556",
        "provideAlternative": True,
        "validationDate": "2026-09-01T09:15:00.000Z",
        "validationResult": "partial",
        "state": "done",
        "submittedGeographicAddress": {
            "@type": "GeographicAddress",
            "@baseType": "Place",
            "streetNr": "42",
            "streetName": "Campus Walk",
            "city": "Dublin",
            "country": "Ireland",
        },
        "validGeographicAddress": geographic_address_dict,
        "alternateGeographicAddress": [
            {
                "@type": "GeographicAddress",
                "@baseType": "Place",
                "id": "addr-9932",
                "streetNr": "44",
                "streetName": "Campus Walk",
                "city": "Dublin",
                "postcode": "D01 X4F3",
                "country": "Ireland",
            }
        ],
    }
    return validation


@pytest.fixture
def geographic_address_validation_1(geographic_address_validation_dict):
    return GeographicAddressValidation.from_dict(geographic_address_validation_dict)


def test_geographic_address_validation_instantiates_with_id(
    geographic_address_validation_dict,
):
    validation = GeographicAddressValidation.from_dict(
        geographic_address_validation_dict
    )
    assert validation.id == "val-556"
    assert validation.provideAlternative is True
    assert validation.validationResult == "partial"
    assert validation.validationDate == "2026-09-01T09:15:00.000Z"


def test_geographic_address_validation_instantiates_classes(
    geographic_address_validation_1,
):
    assert geographic_address_validation_1.state == TaskStateType.DONE
    assert isinstance(
        geographic_address_validation_1.submittedGeographicAddress, GeographicAddress
    )
    assert isinstance(
        geographic_address_validation_1.validGeographicAddress, GeographicAddress
    )
    assert geographic_address_validation_1.validGeographicAddress.postcode == "D01 X4F2"

    alternates = geographic_address_validation_1.alternateGeographicAddress
    assert isinstance(alternates[0], GeographicAddress)
    assert alternates[0].streetNr == "44"


def test_geographic_address_validation_to_dict_round_trip(
    geographic_address_validation_1,
):
    validation_dict = geographic_address_validation_1.to_dict()
    assert validation_dict["@type"] == "GeographicAddressValidation"
    # direct Entity subclasses do not carry an "@baseType" discriminator
    assert "@baseType" not in validation_dict
    assert validation_dict["state"] == "done"
    assert validation_dict["provideAlternative"] is True

    submitted = validation_dict["submittedGeographicAddress"]
    assert submitted["@type"] == "GeographicAddress"
    assert submitted["@baseType"] == "Place"
    assert submitted["streetName"] == "Campus Walk"

    assert validation_dict["alternateGeographicAddress"][0]["postcode"] == "D01 X4F3"


def test_geographic_address_validation_raises_when_alternates_not_a_list():
    with pytest.raises(ValueError):
        GeographicAddressValidation(
            validationResult="partial",
            alternateGeographicAddress=GeographicAddress(city="Dublin"),
        )


def test_geographic_address_validation_resource_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert GeographicAddressValidation.get_resource_path(context) == (
        "https://mycsp.com/tmf-api"
        "/geographicAddressManagement/v4/geographicAddressValidation"
    )


@pytest.fixture
def geographic_site_dict():
    site = {
        "@type": "GeographicSite",
        "@baseType": "Place",
        "id": "site-4711",
        "href": "/geographicSiteManagement/v5/geographicSite/site-4711",
        "name": "Northgate Distribution Centre",
        "description": "A three-storey warehouse with a retail counter",
        "code": "BTS",
        "status": "active",
        "siteCategory": "Warehouse",
        "creationDate": "2024-09-23T00:00:00Z",
        "lastUpdate": "2024-10-03T00:00:00Z",
        "externalIdentifier": [
            {
                "@type": "ExternalIdentifier",
                "externalIdentifierType": "assetRegister",
                "owner": "FacilitiesCo",
                "id": "ext-88",
                "value": "NDC-0001",
            }
        ],
        "capacity": [
            {"@type": "Quantity", "units": "racks", "amount": 240},
            {"@type": "Quantity", "units": "people", "amount": 85},
        ],
        "note": [
            {
                "@type": "Note",
                "id": "note-01",
                "author": "Site Manager",
                "date": "2025-01-14T08:00:00Z",
                "text": "Loading bay 3 is out of service until March",
            }
        ],
        "calendar": [
            {
                "@type": "CalendarPeriod",
                "@baseType": "Entity",
                "day": "weekdays",
                "timeZone": "+01:00",
                "status": "available",
                "hourPeriod": [
                    {
                        "@type": "HourPeriod",
                        "startHour": "06:00",
                        "endHour": "22:00",
                    }
                ],
            }
        ],
        "contactMedium": [
            {
                "@type": "EmailContactMedium",
                "@baseType": "ContactMedium",
                "id": "cm-01",
                "preferred": True,
                "emailAddress": "ndc.reception@example.com",
            },
            {
                "@type": "PhoneContactMedium",
                "@baseType": "ContactMedium",
                "id": "cm-02",
                "preferred": False,
                "phoneNumber": "+353-1-555-0199",
            },
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "siteManager",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "id": "role-19",
                    "name": "Ilse Vermeulen",
                    "@referredType": "PartyRole",
                },
            }
        ],
        "relatedAddress": [
            {
                "@type": "RelatedGeographicAddressRef",
                "role": "delivery-address",
                "address": {
                    "@type": "GeographicAddressRef",
                    "id": "addr-77",
                    "name": "Unit 4, Campus Walk",
                    "@referredType": "GeographicAddress",
                },
            }
        ],
        "relatedLocation": [
            {
                "@type": "RelatedGeographicLocationRef",
                "role": "service-access",
                "location": {
                    "@type": "GeographicLocationRef",
                    "id": "loc-31",
                    "name": "North gate manhole",
                    "@referredType": "GeographicLocation",
                },
            }
        ],
        "geographicSiteRelationship": [
            {
                "@type": "GeographicSiteRelationship",
                "id": "site-88",
                "role": "backupSite",
                "relationshipType": "isBackupOf",
                "name": "Southgate Depot",
                "@referredType": "GeographicSite",
                "associationSpec": {
                    "@type": "EntityRef",
                    "id": "assoc-2",
                    "name": "site-backup-spec",
                },
                "validFor": {
                    "startDateTime": "2025-07-18T00:00:00Z",
                    "endDateTime": "2025-12-31T00:00:00Z",
                },
            }
        ],
        "siteFeature": [
            {
                "@type": "GeographicSiteFeature",
                "@baseType": "Feature",
                "id": "feat-09",
                "name": "Hazard information",
                "isEnabled": True,
                "featureCategory": ["Safety"],
                "featureCharacteristic": [
                    {
                        "@type": "Characteristic",
                        "name": "hazmatClass",
                        "value": "3",
                    }
                ],
            }
        ],
    }
    return site


@pytest.fixture
def geographic_site_1(geographic_site_dict):
    return GeographicSite.from_dict(geographic_site_dict)


def test_geographic_site_instantiates_with_id(geographic_site_1):
    assert geographic_site_1.id == "site-4711"
    assert geographic_site_1.name == "Northgate Distribution Centre"
    assert geographic_site_1.code == "BTS"
    assert geographic_site_1.status == "active"
    assert geographic_site_1.siteCategory == "Warehouse"
    assert geographic_site_1.creationDate == "2024-09-23T00:00:00Z"
    assert geographic_site_1.lastUpdate == "2024-10-03T00:00:00Z"


def test_geographic_site_instantiates_classes(geographic_site_1):
    assert isinstance(geographic_site_1.externalIdentifier[0], ExternalIdentifier)
    assert isinstance(geographic_site_1.capacity[0], Quantity)
    assert isinstance(geographic_site_1.note[0], Note)
    assert isinstance(geographic_site_1.calendar[0], CalendarPeriod)
    assert isinstance(geographic_site_1.calendar[0].hourPeriod[0], HourPeriod)
    assert isinstance(geographic_site_1.siteFeature[0], GeographicSiteFeature)
    assert isinstance(
        geographic_site_1.siteFeature[0].featureCharacteristic[0], Characteristic
    )

    contact_media = geographic_site_1.contactMedium
    assert isinstance(contact_media[0], EmailContactMedium)
    assert isinstance(contact_media[1], PhoneContactMedium)
    assert contact_media[0].emailAddress == "ndc.reception@example.com"
    assert contact_media[1].phoneNumber == "+353-1-555-0199"

    related_party = geographic_site_1.relatedParty[0]
    assert isinstance(related_party, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(related_party.partyOrPartyRole, PartyRoleRef)

    related_address = geographic_site_1.relatedAddress[0]
    assert isinstance(related_address, RelatedGeographicAddressRef)
    assert isinstance(related_address.address, GeographicAddressRef)
    assert related_address.role == "delivery-address"

    related_location = geographic_site_1.relatedLocation[0]
    assert isinstance(related_location, RelatedGeographicLocationRef)
    assert isinstance(related_location.location, GeographicLocationRef)
    assert related_location.role == "service-access"

    relationship = geographic_site_1.geographicSiteRelationship[0]
    assert isinstance(relationship, GeographicSiteRelationship)
    assert isinstance(relationship.associationSpec, EntityRef)
    assert isinstance(relationship.validFor, TimePeriod)
    assert relationship.name == "Southgate Depot"
    assert relationship._referred_type == "GeographicSite"


def test_geographic_site_capacity_values(geographic_site_1):
    capacities = {q.units: q.amount for q in geographic_site_1.capacity}
    assert capacities == {"racks": 240, "people": 85}


def test_geographic_site_to_dict_round_trip(geographic_site_1):
    site_dict = geographic_site_1.to_dict()
    assert site_dict["@type"] == "GeographicSite"
    assert site_dict["@baseType"] == "Place"
    assert site_dict["siteCategory"] == "Warehouse"

    assert site_dict["contactMedium"][0]["@type"] == "EmailContactMedium"
    assert site_dict["contactMedium"][0]["@baseType"] == "ContactMedium"

    related_address = site_dict["relatedAddress"][0]
    assert related_address["@type"] == "RelatedGeographicAddressRef"
    assert related_address["address"]["@referredType"] == "GeographicAddress"

    related_location = site_dict["relatedLocation"][0]
    assert related_location["location"]["@type"] == "GeographicLocationRef"

    relationship = site_dict["geographicSiteRelationship"][0]
    assert relationship["@referredType"] == "GeographicSite"
    assert relationship["associationSpec"]["id"] == "assoc-2"

    site_feature = site_dict["siteFeature"][0]
    assert site_feature["@type"] == "GeographicSiteFeature"
    assert site_feature["@baseType"] == "Feature"


def test_geographic_site_raises_when_calendar_not_a_list():
    with pytest.raises(ValueError):
        GeographicSite(
            name="Bad site",
            calendar=CalendarPeriod(day="mon", status="available"),
        )


def test_geographic_site_resource_path():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert GeographicSite.get_resource_path(context) == (
        "https://mycsp.com/tmf-api/geographicSiteManagement/v5/geographicSite"
    )
