import pytest
from tmforum import (
    AttachmentRefOrValue,
    CalendarPeriod,
    Characteristic,
    Context,
    GeographicAddress,
    GeographicAddressRelationship,
    GeographicAddressValidation,
    GeographicLocation,
    GeographicLocationRef,
    GeographicLocationRefOrValue,
    GeographicSiteFeature,
    GeographicSiteRelationship,
    GeographicSubAddress,
    GeographicSubAddressUnit,
    HourPeriod,
    Note,
    PartyRoleRef,
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
