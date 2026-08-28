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
    Note,
    PartyRoleRef,
    PhoneContactMedium,
    ProductOfferingRef,
    ProductRef,
    ProductSpecificationRef,
    QuoteItemRef,
    QuoteRef,
    RelatedPartyRefOrPartyRoleRef,
    RevenueEstimate,
    SalesActivityRef,
    SalesLead,
    SalesLeadPriorityType,
    SalesLeadRef,
    SalesLeadStatusType,
    SalesNote,
    SalesOpportunity,
    SalesOpportunityItem,
    SalesOpportunityItemStateType,
    SalesOpportunityRef,
    SalesOpportunityStateType,
    SalesProjectRef,
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


@pytest.fixture
def sales_opportunity_dict():
    sales_opportunity = {
        "@type": "SalesOpportunity",
        "@baseType": "Entity",
        "id": "opp-4711",
        "href": "/salesManagement/v5/salesOpportunity/opp-4711",
        "name": "Fiber upgrade for ACME",
        "description": "Qualified interest in upgrading 40 sites to fiber",
        "creationDate": "2025-08-01T09:00:00Z",
        "referredDate": "2025-07-17T00:00:00Z",
        "rating": "hot",
        "salesOpportunityType": "upsell",
        "status": "inProgress",
        "statusChangeDate": "2025-08-05T11:30:00Z",
        "statusChangeReason": "Technical validation completed",
        "priority": "high",
        "validFor": {
            "startDateTime": "2025-08-01T00:00:00Z",
            "endDateTime": "2026-01-31T00:00:00Z",
        },
        "category": {
            "@type": "CategoryRef",
            "id": "cat-01",
            "name": "Connectivity",
        },
        "channel": {
            "@type": "ChannelRef",
            "id": "chan-02",
            "name": "Direct Sales",
        },
        "marketSegment": {
            "@type": "MarketSegmentRef",
            "id": "seg-01",
            "name": "Small and Medium Companies",
        },
        "marketingCampaign": {
            "@type": "MarketingCampaignRef",
            "id": "camp-01",
            "name": "Fiber Spring Campaign",
        },
        "salesLead": [
            {
                "@type": "SalesLeadRef",
                "id": "5411-fe45",
                "name": "New services opportunity",
            }
        ],
        "revenueEstimate": [
            {
                "@type": "RevenueEstimate",
                "@baseType": "Entity",
                "description": "Consolidated annual recurring revenue",
                "revenueType": "recurring",
                "amount": {
                    "@type": "Money",
                    "unit": "USD",
                    "value": 58000.0,
                },
            }
        ],
        "note": [
            {
                "@type": "Note",
                "id": "note-01",
                "author": "Jane Salesperson",
                "date": "2025-08-05T11:30:00Z",
                "text": "Customer confirmed budget for Q4",
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
                "role": "customer",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "PartyRole",
                    "id": "pr-01",
                    "name": "ACME Corp",
                },
            }
        ],
        "quote": [
            {
                "@type": "QuoteRef",
                "id": "quote-01",
                "name": "Fiber upgrade quote",
            }
        ],
        "salesProject": [
            {
                "@type": "SalesProjectRef",
                "id": "proj-01",
                "name": "ACME nationwide fiber rollout",
            }
        ],
        "salesOpportunityItem": [
            {
                "@type": "SalesOpportunityItem",
                "id": "1",
                "action": "add",
                "rating": "hot",
                "priority": "medium",
                "salesOpportunityItemStatus": "pending",
                "validFor": {
                    "startDateTime": "2025-08-01T00:00:00Z",
                    "endDateTime": "2026-01-31T00:00:00Z",
                },
                "product": {
                    "@type": "ProductRef",
                    "id": "prod-01",
                    "name": "Existing Copper Line",
                },
                "productOffering": {
                    "@type": "ProductOfferingRef",
                    "id": "po-01",
                    "name": "Fiber 1G",
                    "version": "2.0",
                },
                "revenueEstimate": [
                    {
                        "@type": "RevenueEstimate",
                        "description": "Item level recurring revenue",
                        "revenueType": "recurring",
                        "amount": {
                            "@type": "Money",
                            "unit": "USD",
                            "value": 1450.0,
                        },
                    }
                ],
                "salesActivity": [
                    {
                        "@type": "SalesActivityRef",
                        "id": "act-01",
                        "name": "Site survey",
                    }
                ],
                "quoteItem": [
                    {
                        "@type": "QuoteItemRef",
                        "quoteId": "quote-01",
                        "quoteItemId": "1",
                        "quoteHref": "/quoteManagement/v5/quote/quote-01",
                    }
                ],
                "note": [
                    {
                        "@type": "Note",
                        "id": "note-02",
                        "author": "Jane Salesperson",
                        "text": "40 sites in scope",
                    }
                ],
                "relatedParty": [
                    {
                        "@type": "RelatedPartyRefOrPartyRoleRef",
                        "role": "salesAgent",
                        "partyOrPartyRole": {
                            "@type": "PartyRoleRef",
                            "id": "pr-02",
                            "name": "Jane Salesperson",
                        },
                    }
                ],
            }
        ],
    }
    return sales_opportunity


@pytest.fixture
def sales_opportunity_1(sales_opportunity_dict):
    return SalesOpportunity.from_dict(sales_opportunity_dict)


def test_sales_opportunity_instantiates_with_id(sales_opportunity_dict):
    sales_opportunity = SalesOpportunity.from_dict(sales_opportunity_dict)
    assert sales_opportunity.id == "opp-4711"
    assert sales_opportunity.name == "Fiber upgrade for ACME"
    assert sales_opportunity.salesOpportunityType == "upsell"
    assert sales_opportunity.statusChangeReason == "Technical validation completed"
    assert sales_opportunity.revenueEstimate[0].amount.value == 58000.0


def test_sales_opportunity_instantiates_classes(sales_opportunity_1):
    revenue_estimate = sales_opportunity_1.revenueEstimate[0]
    related_party = sales_opportunity_1.relatedParty[0]
    assert isinstance(sales_opportunity_1.status, SalesOpportunityStateType)
    assert isinstance(sales_opportunity_1.priority, SalesLeadPriorityType)
    assert isinstance(sales_opportunity_1.validFor, TimePeriod)
    assert isinstance(revenue_estimate, RevenueEstimate)
    assert isinstance(revenue_estimate.amount, Money)
    assert isinstance(sales_opportunity_1.category, CategoryRef)
    assert isinstance(sales_opportunity_1.channel, ChannelRef)
    assert isinstance(sales_opportunity_1.marketSegment, MarketSegmentRef)
    assert isinstance(sales_opportunity_1.marketingCampaign, MarketingCampaignRef)
    assert isinstance(sales_opportunity_1.salesLead[0], SalesLeadRef)
    assert isinstance(sales_opportunity_1.agreement[0], AgreementRef)
    assert isinstance(sales_opportunity_1.quote[0], QuoteRef)
    assert isinstance(sales_opportunity_1.salesProject[0], SalesProjectRef)
    assert isinstance(sales_opportunity_1.note[0], Note)
    assert isinstance(related_party, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(related_party.partyOrPartyRole, PartyRoleRef)


def test_sales_opportunity_item_instantiates_classes(sales_opportunity_1):
    item = sales_opportunity_1.salesOpportunityItem[0]
    assert isinstance(item, SalesOpportunityItem)
    assert item.id == "1"
    assert item.action == "add"
    assert isinstance(item.salesOpportunityItemStatus, SalesOpportunityItemStateType)
    assert isinstance(item.priority, SalesLeadPriorityType)
    assert isinstance(item.validFor, TimePeriod)
    assert isinstance(item.product, ProductRef)
    assert isinstance(item.productOffering, ProductOfferingRef)
    assert item.productOffering.version == "2.0"
    assert isinstance(item.revenueEstimate[0], RevenueEstimate)
    assert isinstance(item.revenueEstimate[0].amount, Money)
    assert isinstance(item.salesActivity[0], SalesActivityRef)
    assert isinstance(item.quoteItem[0], QuoteItemRef)
    assert item.quoteItem[0].quoteItemId == "1"
    assert isinstance(item.note[0], Note)
    assert isinstance(item.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(item.relatedParty[0].partyOrPartyRole, PartyRoleRef)


def test_sales_opportunity_to_dict_round_trip(sales_opportunity_1):
    sales_opportunity_dict = sales_opportunity_1.to_dict()
    assert sales_opportunity_dict["@type"] == "SalesOpportunity"
    # SalesOpportunity derives directly from Entity, so no @baseType is emitted.
    assert "@baseType" not in sales_opportunity_dict
    assert sales_opportunity_dict["salesLead"][0]["@type"] == "SalesLeadRef"
    assert sales_opportunity_dict["quote"][0]["@type"] == "QuoteRef"
    assert sales_opportunity_dict["salesProject"][0]["@type"] == "SalesProjectRef"
    assert sales_opportunity_dict["revenueEstimate"][0]["@type"] == "RevenueEstimate"
    assert sales_opportunity_dict["status"] == "inProgress"
    assert sales_opportunity_dict["priority"] == "high"
    item_dict = sales_opportunity_dict["salesOpportunityItem"][0]
    assert item_dict["@type"] == "SalesOpportunityItem"
    assert item_dict["salesOpportunityItemStatus"] == "pending"
    assert item_dict["salesActivity"][0]["@type"] == "SalesActivityRef"
    assert item_dict["quoteItem"][0]["@type"] == "QuoteItemRef"


def test_sales_opportunity_raises_when_item_not_a_list():
    with pytest.raises(ValueError):
        SalesOpportunity(
            name="Bad opportunity",
            salesOpportunityItem=SalesOpportunityItem(id="1"),
        )


def test_sales_opportunity_item_raises_when_note_not_a_list():
    with pytest.raises(ValueError):
        SalesOpportunityItem(id="1", note=Note(id="note-01"))


def test_sales_opportunity_resource_path_is_v5():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        SalesOpportunity.get_resource_path(context)
        == "https://mycsp.com/tmf-api/salesManagement/v5/salesOpportunity"
    )
