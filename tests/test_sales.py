import pytest
from tmforum import (
    AgreementRef,
    CategoryRef,
    ChannelRef,
    Context,
    EmailContactMedium,
    FaxContactMedium,
    GeographicAddressContactMedium,
    GeographicAddressRef,
    MarketingCampaignRef,
    MarketSegmentRef,
    Money,
    PartyRoleRef,
    PhoneContactMedium,
    ProductOfferingRef,
    ProductRef,
    ProductSpecificationRef,
    RelatedPartyRefOrPartyRoleRef,
    RevenueEstimate,
    SalesLead,
    SalesLeadPriorityType,
    SalesLeadStatusType,
    SalesNote,
    SalesOpportunityRef,
    SocialContactMedium,
    TimePeriod,
)


@pytest.fixture
def sales_lead_dict():
    sales_lead = {
        "@type": "SalesLead",
        "@baseType": "Entity",
        "id": "5411-fe45",
        "href": "/salesManagement/v5/salesLead/5411-fe45",
        "name": "New services opportunity",
        "description": "Prospect interested in a fiber upgrade bundle",
        "creationDate": "2025-07-18T00:00:00Z",
        "lastUpdate": "2025-07-19T12:00:00Z",
        "referredDate": "2025-07-17T00:00:00Z",
        "rating": "hot",
        "priority": "high",
        "status": "inProgress",
        "statusChangeDate": "2025-07-19T12:00:00Z",
        "statusChangeReason": "Qualified after first call",
        "salesLeadType": "newBusiness",
        "validFor": {
            "startDateTime": "2025-07-18T00:00:00Z",
            "endDateTime": "2025-12-31T00:00:00Z",
        },
        "revenueEstimate": [
            {
                "@type": "RevenueEstimate",
                "@baseType": "Entity",
                "description": "First year recurring revenue",
                "revenueType": "recurring",
                "amount": {
                    "@type": "Money",
                    "unit": "USD",
                    "value": 1499.99,
                },
            }
        ],
        "marketingCampaign": {
            "@type": "MarketingCampaignRef",
            "id": "camp-01",
            "name": "Fiber Spring Campaign",
        },
        "marketSegment": {
            "@type": "MarketSegmentRef",
            "id": "seg-01",
            "name": "Small and Medium Companies",
        },
        "channel": {
            "@type": "ChannelRef",
            "id": "chan-01",
            "name": "Web",
        },
        "category": {
            "@type": "CategoryRef",
            "id": "cat-01",
            "name": "Connectivity",
        },
        "productOffering": [
            {
                "@type": "ProductOfferingRef",
                "id": "po-01",
                "name": "Fiber 1G",
            }
        ],
        "productSpecification": [
            {
                "@type": "ProductSpecificationRef",
                "id": "ps-01",
                "name": "Fiber Access",
                "version": "1.0",
            }
        ],
        "product": [
            {
                "@type": "ProductRef",
                "id": "prod-01",
                "name": "Existing Copper Line",
            }
        ],
        "salesOpportunity": [
            {
                "@type": "SalesOpportunityRef",
                "id": "opp-01",
                "name": "Fiber upgrade opportunity",
            }
        ],
        "agreement": [
            {
                "@type": "AgreementRef",
                "id": "agr-01",
                "name": "Master Service Agreement",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "prospect",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "PartyRole",
                    "id": "pr-01",
                    "name": "ACME Corp",
                    "partyId": "party-01",
                    "partyName": "ACME Corporation",
                },
            }
        ],
        "prospectContactMedium": [
            {
                "@type": "EmailContactMedium",
                "@baseType": "ContactMedium",
                "id": "cm-01",
                "preferred": True,
                "contactType": "professional",
                "emailAddress": "buyer@example.com",
            },
            {
                "@type": "PhoneContactMedium",
                "@baseType": "ContactMedium",
                "id": "cm-02",
                "phoneNumber": "+1 555 0100",
            },
            {
                "@type": "FaxContactMedium",
                "@baseType": "ContactMedium",
                "id": "cm-03",
                "faxNumber": "+1 555 0101",
            },
            {
                "@type": "SocialContactMedium",
                "@baseType": "ContactMedium",
                "id": "cm-04",
                "socialNetworkId": "@acmecorp",
            },
            {
                "@type": "GeographicAddressContactMedium",
                "@baseType": "ContactMedium",
                "id": "cm-05",
                "city": "Ottawa",
                "country": "Canada",
                "postCode": "K1A 0A1",
                "stateOrProvince": "ON",
                "street1": "123 Fiber St",
                "street2": "Suite 500",
                "geographicAddress": {
                    "@type": "GeographicAddressRef",
                    "id": "ga-01",
                },
            },
        ],
        "note": [
            {
                "@type": "SalesNote",
                "id": "note-01",
                "author": "Jane Salesperson",
                "date": "2025-07-19T12:00:00Z",
                "text": "Prospect asked for a formal quote",
            }
        ],
    }
    return sales_lead


@pytest.fixture
def sales_lead_1(sales_lead_dict):
    return SalesLead.from_dict(sales_lead_dict)


def test_sales_lead_instantiates_with_id(sales_lead_dict):
    sales_lead = SalesLead.from_dict(sales_lead_dict)
    assert sales_lead.id == "5411-fe45"
    assert sales_lead.salesLeadType == "newBusiness"
    assert sales_lead.revenueEstimate[0].amount.value == 1499.99


def test_sales_lead_instantiates_classes(sales_lead_1):
    revenue_estimate = sales_lead_1.revenueEstimate[0]
    related_party = sales_lead_1.relatedParty[0]
    assert isinstance(sales_lead_1.status, SalesLeadStatusType)
    assert isinstance(sales_lead_1.priority, SalesLeadPriorityType)
    assert isinstance(sales_lead_1.validFor, TimePeriod)
    assert isinstance(revenue_estimate, RevenueEstimate)
    assert isinstance(revenue_estimate.amount, Money)
    assert isinstance(sales_lead_1.marketingCampaign, MarketingCampaignRef)
    assert isinstance(sales_lead_1.marketSegment, MarketSegmentRef)
    assert isinstance(sales_lead_1.channel, ChannelRef)
    assert isinstance(sales_lead_1.category, CategoryRef)
    assert isinstance(sales_lead_1.productOffering[0], ProductOfferingRef)
    assert isinstance(sales_lead_1.productSpecification[0], ProductSpecificationRef)
    assert isinstance(sales_lead_1.product[0], ProductRef)
    assert isinstance(sales_lead_1.salesOpportunity[0], SalesOpportunityRef)
    assert isinstance(sales_lead_1.agreement[0], AgreementRef)
    assert isinstance(related_party, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(related_party.partyOrPartyRole, PartyRoleRef)
    assert isinstance(sales_lead_1.note[0], SalesNote)


def test_sales_lead_contact_medium_subtypes(sales_lead_1):
    media = sales_lead_1.prospectContactMedium
    assert isinstance(media[0], EmailContactMedium)
    assert isinstance(media[1], PhoneContactMedium)
    assert isinstance(media[2], FaxContactMedium)
    assert media[2].faxNumber == "+1 555 0101"
    assert isinstance(media[3], SocialContactMedium)
    assert media[3].socialNetworkId == "@acmecorp"
    assert isinstance(media[4], GeographicAddressContactMedium)
    assert isinstance(media[4].geographicAddress, GeographicAddressRef)


def test_sales_lead_to_dict_round_trip(sales_lead_1):
    sales_lead_dict = sales_lead_1.to_dict()
    assert sales_lead_dict["@type"] == "SalesLead"
    assert sales_lead_dict["salesOpportunity"][0]["@type"] == "SalesOpportunityRef"
    assert sales_lead_dict["revenueEstimate"][0]["@type"] == "RevenueEstimate"
    contact_medium = sales_lead_dict["prospectContactMedium"][0]
    assert contact_medium["@type"] == "EmailContactMedium"
    assert contact_medium["@baseType"] == "ContactMedium"


def test_sales_lead_raises_when_sales_opportunity_not_a_list():
    with pytest.raises(ValueError):
        SalesLead(
            name="Bad lead",
            salesOpportunity=SalesOpportunityRef(id="opp-01"),
        )


def test_sales_lead_resource_path_is_v5():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        SalesLead.get_resource_path(context)
        == "https://mycsp.com/tmf-api/salesManagement/v5/salesLead"
    )


def test_revenue_estimate_to_dict():
    estimate = RevenueEstimate(
        amount=Money(unit="USD", value=100.0),
        revenueType="oneTime",
    )
    estimate_dict = estimate.to_dict()
    assert estimate_dict["@type"] == "RevenueEstimate"
    assert estimate_dict["amount"]["value"] == 100.0
