import pytest
from tmforum import (
    AccountRef,
    AgreementRef,
    Attachment,
    BooleanArrayCharacteristic,
    BusinessPartner,
    Characteristic,
    Consumer,
    Context,
    CreditProfile,
    Disability,
    EmailContactMedium,
    ExternalIdentifier,
    GeographicAddressContactMedium,
    Individual,
    IndividualIdentification,
    IndividualStateType,
    IntegerArrayCharacteristic,
    LanguageAbility,
    MarketSegmentRef,
    NumberArrayCharacteristic,
    ObjectArrayCharacteristic,
    ObjectCharacteristic,
    Organization,
    OrganizationChildRelationship,
    OrganizationIdentification,
    OrganizationParentRelationship,
    OrganizationRef,
    OrganizationStateType,
    OtherNameIndividual,
    OtherNameOrganization,
    PartyCreditProfile,
    PartyRef,
    PartyRole,
    PartyRoleRef,
    PartyRoleSpecificationRef,
    PaymentMethodRef,
    PhoneContactMedium,
    PlaceRef,
    Producer,
    RelatedPartyOrPartyRole,
    Skill,
    StringArrayCharacteristic,
    Supplier,
    TaxExemptionCertificate,
    TimePeriod,
)


@pytest.fixture
def individual_dict():
    return {
        "@type": "Individual",
        "@baseType": "Party",
        "id": "3644-4dfd",
        "href": "/partyManagement/v5/individual/3644-4dfd",
        "givenName": "Jean",
        "familyName": "Pontus",
        "middleName": "Marie",
        "legalName": "Jean Marie Pontus",
        "formattedName": "Mr Jean Marie Pontus",
        "preferredGivenName": "Johnny",
        "familyNamePrefix": "de",
        "aristocraticTitle": "Baron",
        "generation": "Jr",
        "title": "Mr",
        "gender": "male",
        "birthDate": "1967-11-11T00:00:00Z",
        "countryOfBirth": "France",
        "placeOfBirth": "Bordeaux",
        "nationality": "French",
        "maritalStatus": "married",
        "location": "Paris",
        "status": "validated",
        "otherName": [
            {
                "@type": "OtherNameIndividual",
                "givenName": "Jeanne",
                "familyName": "Dupont",
                "fullName": "Jeanne Dupont",
                "validFor": {
                    "startDateTime": "1990-01-01T00:00:00Z",
                    "endDateTime": "2000-01-01T00:00:00Z",
                },
            }
        ],
        "individualIdentification": [
            {
                "@type": "IndividualIdentification",
                "identificationId": "1122334455",
                "identificationType": "passport",
                "issuingAuthority": "French Republic",
                "issuingDate": "2015-06-01T00:00:00Z",
                "attachment": {
                    "@type": "Attachment",
                    "id": "att-01",
                    "name": "passport scan",
                    "mimeType": "application/pdf",
                    "url": "https://mycsp.com/attachment/att-01",
                },
            }
        ],
        "disability": [
            {
                "@type": "Disability",
                "disabilityCode": "VIS",
                "disabilityName": "Visual impairment",
                "validFor": {"startDateTime": "2010-01-01T00:00:00Z"},
            }
        ],
        "languageAbility": [
            {
                "@type": "LanguageAbility",
                "languageCode": "fr",
                "languageName": "French",
                "isFavouriteLanguage": True,
                "writingProficiency": "native",
                "readingProficiency": "native",
                "speakingProficiency": "native",
                "listeningProficiency": "native",
            }
        ],
        "skill": [
            {
                "@type": "Skill",
                "skillCode": "JAVA",
                "skillName": "Java language",
                "evaluatedLevel": "expert",
                "comment": "Certified 2024",
            }
        ],
        "contactMedium": [
            {
                "@type": "EmailContactMedium",
                "contactType": "email",
                "emailAddress": "jean.pontus@example.com",
            },
            {
                "@type": "PhoneContactMedium",
                "contactType": "phone",
                "phoneNumber": "+33 6 12 34 56 78",
            },
        ],
        "partyCharacteristic": [
            {
                "@type": "StringArrayCharacteristic",
                "name": "hobbies",
                "value": ["sailing", "chess"],
            },
            {
                "@type": "ObjectCharacteristic",
                "name": "preferences",
                "value": {"channel": "email"},
            },
        ],
        "externalReference": [
            {
                "@type": "ExternalIdentifier",
                "externalIdentifierType": "CRM",
                "owner": "Salesforce",
                "value": "0031t00000abcde",
            }
        ],
        "creditRating": [
            {
                "@type": "PartyCreditProfile",
                "creditAgencyName": "Experian",
                "ratingScore": 720,
            }
        ],
        "taxExemptionCertificate": [
            {"@type": "TaxExemptionCertificate", "id": "tax-01"}
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyOrPartyRole",
                "role": "employer",
                "partyOrPartyRole": {"@type": "OrganizationRef", "id": "org-99"},
            }
        ],
    }


@pytest.fixture
def organization_dict():
    return {
        "@type": "Organization",
        "@baseType": "Party",
        "id": "500",
        "href": "/partyManagement/v5/organization/500",
        "name": "Acme Telecom",
        "tradingName": "Acme",
        "nameType": "legal",
        "organizationType": "company",
        "isHeadOffice": True,
        "isLegalEntity": True,
        "status": "validated",
        "existsDuring": {"startDateTime": "1998-01-01T00:00:00Z"},
        "organizationIdentification": [
            {
                "@type": "OrganizationIdentification",
                "identificationId": "FR123456789",
                "identificationType": "VAT",
                "issuingAuthority": "French Republic",
            }
        ],
        "organizationChildRelationship": [
            {
                "@type": "OrganizationChildRelationship",
                "relationshipType": "subsidiary",
                "organization": {"@type": "OrganizationRef", "id": "501"},
            }
        ],
        "organizationParentRelationship": {
            "@type": "OrganizationParentRelationship",
            "relationshipType": "parent",
            "organization": {"@type": "OrganizationRef", "id": "499"},
        },
        "otherName": [{"@type": "OtherNameOrganization", "name": "Acme Corp"}],
        "contactMedium": [
            {
                "@type": "GeographicAddressContactMedium",
                "contactType": "postal",
                "city": "Paris",
                "country": "France",
            }
        ],
        "place": [{"@type": "PlaceRef", "id": "place-01"}],
        "marketSegment": [{"@type": "MarketSegmentRef", "id": "seg-01"}],
    }


@pytest.fixture
def party_role_dict():
    return {
        "@type": "Supplier",
        "@baseType": "PartyRole",
        "id": "role-01",
        "href": "/partyRoleManagement/v5/partyRole/role-01",
        "name": "Fiber equipment supplier",
        "description": "Supplies fiber termination units",
        "status": "active",
        "statusReason": "Contract signed",
        "validFor": {"startDateTime": "2024-01-01T00:00:00Z"},
        "engagedParty": {"@type": "OrganizationRef", "id": "org-77"},
        "partyRoleSpecification": {
            "@type": "PartyRoleSpecificationRef",
            "id": "spec-01",
            "name": "Supplier role spec",
        },
        "agreement": [{"@type": "AgreementRef", "id": "agr-01"}],
        "account": [{"@type": "AccountRef", "id": "acc-01"}],
        "paymentMethod": [{"@type": "PaymentMethodRef", "id": "pm-01"}],
        "creditProfile": [
            {
                "@type": "CreditProfile",
                "creditProfileDate": "2025-01-01T00:00:00Z",
                "creditRiskRating": 3,
                "creditScore": 810,
                "validFor": {"startDateTime": "2025-01-01T00:00:00Z"},
            }
        ],
        "characteristic": [
            {
                "@type": "IntegerArrayCharacteristic",
                "name": "leadTimes",
                "value": [5, 10, 15],
            }
        ],
        "contactMedium": [
            {"@type": "EmailContactMedium", "emailAddress": "sales@supplier.com"}
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyOrPartyRole",
                "role": "buyer",
                "partyOrPartyRole": {"@type": "PartyRoleRef", "id": "role-02"},
            }
        ],
    }


@pytest.fixture
def individual_1(individual_dict):
    return Individual.from_dict(individual_dict)


@pytest.fixture
def organization_1(organization_dict):
    return Organization.from_dict(organization_dict)


@pytest.fixture
def supplier_1(party_role_dict):
    return PartyRole.from_dict(party_role_dict)


def test_individual_from_dict(individual_1):
    assert isinstance(individual_1, Individual)
    assert individual_1.id == "3644-4dfd"
    assert individual_1.givenName == "Jean"
    assert individual_1.status == IndividualStateType.VALIDATED

    assert isinstance(individual_1.otherName[0], OtherNameIndividual)
    assert individual_1.otherName[0].fullName == "Jeanne Dupont"
    assert isinstance(individual_1.otherName[0].validFor, TimePeriod)

    assert isinstance(
        individual_1.individualIdentification[0], IndividualIdentification
    )
    assert individual_1.individualIdentification[0].identificationType == "passport"
    assert isinstance(individual_1.individualIdentification[0].attachment, Attachment)

    assert isinstance(individual_1.disability[0], Disability)
    assert individual_1.disability[0].disabilityCode == "VIS"

    assert isinstance(individual_1.languageAbility[0], LanguageAbility)
    assert individual_1.languageAbility[0].isFavouriteLanguage is True

    assert isinstance(individual_1.skill[0], Skill)
    assert individual_1.skill[0].skillName == "Java language"

    assert isinstance(individual_1.contactMedium[0], EmailContactMedium)
    assert isinstance(individual_1.contactMedium[1], PhoneContactMedium)
    assert isinstance(individual_1.externalReference[0], ExternalIdentifier)
    assert isinstance(individual_1.creditRating[0], PartyCreditProfile)
    assert isinstance(individual_1.taxExemptionCertificate[0], TaxExemptionCertificate)
    assert isinstance(individual_1.relatedParty[0], RelatedPartyOrPartyRole)
    assert isinstance(individual_1.relatedParty[0].partyOrPartyRole, OrganizationRef)


def test_individual_array_characteristics(individual_1):
    string_array, obj = individual_1.partyCharacteristic
    assert isinstance(string_array, StringArrayCharacteristic)
    assert string_array.value == ["sailing", "chess"]
    assert string_array.valueType == "StringArray"
    assert isinstance(obj, ObjectCharacteristic)
    assert obj.value == {"channel": "email"}
    assert obj.valueType == "Object"


def test_organization_from_dict(organization_1):
    assert isinstance(organization_1, Organization)
    assert organization_1.name == "Acme Telecom"
    assert organization_1.status == OrganizationStateType.VALIDATED
    assert isinstance(
        organization_1.organizationIdentification[0], OrganizationIdentification
    )
    assert isinstance(
        organization_1.organizationChildRelationship[0], OrganizationChildRelationship
    )
    assert isinstance(
        organization_1.organizationChildRelationship[0].organization, OrganizationRef
    )
    assert isinstance(
        organization_1.organizationParentRelationship, OrganizationParentRelationship
    )
    assert isinstance(organization_1.otherName[0], OtherNameOrganization)
    assert isinstance(organization_1.contactMedium[0], GeographicAddressContactMedium)
    assert isinstance(organization_1.place[0], PlaceRef)
    assert isinstance(organization_1.marketSegment[0], MarketSegmentRef)
    assert isinstance(organization_1.existsDuring, TimePeriod)


def test_supplier_resolves_via_type_discriminator(supplier_1):
    assert isinstance(supplier_1, Supplier)
    assert isinstance(supplier_1, PartyRole)
    assert supplier_1.name == "Fiber equipment supplier"
    assert isinstance(supplier_1.engagedParty, OrganizationRef)
    assert isinstance(supplier_1.partyRoleSpecification, PartyRoleSpecificationRef)
    assert isinstance(supplier_1.agreement[0], AgreementRef)
    assert isinstance(supplier_1.account[0], AccountRef)
    assert isinstance(supplier_1.paymentMethod[0], PaymentMethodRef)
    assert isinstance(supplier_1.creditProfile[0], CreditProfile)
    assert supplier_1.creditProfile[0].creditScore == 810
    assert isinstance(supplier_1.creditProfile[0].validFor, TimePeriod)
    assert isinstance(supplier_1.characteristic[0], IntegerArrayCharacteristic)
    assert supplier_1.characteristic[0].value == [5, 10, 15]
    assert isinstance(supplier_1.contactMedium[0], EmailContactMedium)
    assert isinstance(supplier_1.relatedParty[0].partyOrPartyRole, PartyRoleRef)


@pytest.mark.parametrize("cls", [Consumer, Producer, BusinessPartner, Supplier])
def test_party_role_subtypes_extend_party_role(cls):
    instance = cls(id="x", name="n")
    assert isinstance(instance, PartyRole)
    assert cls.get_resource_path(Context(api_base_url="https://mycsp.com/tmf-api")) == (
        "https://mycsp.com/tmf-api/partyRoleManagement/v5/partyRole"
    )


@pytest.mark.parametrize(
    "cls,value,expected_value_type",
    [
        (BooleanArrayCharacteristic, [True, False], "BooleanArray"),
        (IntegerArrayCharacteristic, [1, 2], "IntegerArray"),
        (NumberArrayCharacteristic, [1.5, 2.5], "NumberArray"),
        (ObjectArrayCharacteristic, [{"a": 1}], "ObjectArray"),
        (StringArrayCharacteristic, ["a"], "StringArray"),
    ],
)
def test_array_characteristics(cls, value, expected_value_type):
    instance = cls(name="c", value=value)
    assert isinstance(instance, Characteristic)
    assert instance.valueType == expected_value_type
    assert instance.to_dict()["value"] == value


def test_individual_to_dict_round_trip(individual_1):
    d = individual_1.to_dict()
    assert d["@type"] == "Individual"
    assert d["@baseType"] == "Party"
    assert d["status"] == "validated"
    assert d["otherName"][0]["@type"] == "OtherNameIndividual"
    assert d["individualIdentification"][0]["@type"] == "IndividualIdentification"
    assert d["individualIdentification"][0]["attachment"]["@type"] == "Attachment"
    assert d["disability"][0]["@type"] == "Disability"
    assert d["languageAbility"][0]["@type"] == "LanguageAbility"
    assert d["skill"][0]["@type"] == "Skill"
    assert d["partyCharacteristic"][0]["@type"] == "StringArrayCharacteristic"

    round_tripped = Individual.from_dict(d)
    assert isinstance(round_tripped.skill[0], Skill)
    assert round_tripped.skill[0].skillCode == "JAVA"


def test_organization_to_dict_round_trip(organization_1):
    d = organization_1.to_dict()
    assert d["@type"] == "Organization"
    assert d["@baseType"] == "Party"
    assert d["organizationIdentification"][0]["@type"] == "OrganizationIdentification"
    assert (
        d["organizationParentRelationship"]["@type"] == "OrganizationParentRelationship"
    )
    assert d["status"] == "validated"


def test_supplier_to_dict_round_trip(supplier_1):
    d = supplier_1.to_dict()
    assert d["@type"] == "Supplier"
    assert d["@baseType"] == "PartyRole"
    assert d["creditProfile"][0]["@type"] == "CreditProfile"
    assert d["partyRoleSpecification"]["@type"] == "PartyRoleSpecificationRef"
    assert d["agreement"][0]["@type"] == "AgreementRef"


def test_individual_raises_when_skill_not_a_list():
    with pytest.raises(ValueError):
        Individual(givenName="Jean", skill=Skill(skillCode="JAVA"))


def test_party_role_raises_when_credit_profile_not_a_list():
    with pytest.raises(ValueError):
        PartyRole(name="role", creditProfile=CreditProfile(creditScore=1))


def test_party_resource_paths_are_v5():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        Individual.get_resource_path(context)
        == "https://mycsp.com/tmf-api/partyManagement/v5/individual"
    )
    assert (
        Organization.get_resource_path(context)
        == "https://mycsp.com/tmf-api/partyManagement/v5/organization"
    )
