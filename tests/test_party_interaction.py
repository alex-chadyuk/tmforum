import pytest
from tmforum import (
    AttachmentRefOrValue,
    ChannelRef,
    Context,
    ExternalIdentifier,
    InteractionItem,
    InteractionItemRelationship,
    InteractionRelationship,
    Note,
    PartyInteraction,
    PartyRoleRef,
    ProductOrderRef,
    RelatedChannel,
    RelatedEntityRefOrValue,
    RelatedPartyOrPartyRole,
    RelatedPartyRefOrPartyRoleRef,
    TimePeriod,
)


@pytest.fixture
def party_interaction_dict():
    return {
        "@type": "PartyInteraction",
        "@baseType": "Entity",
        "id": "pi-1034",
        "href": "https://mycsp.com/tmf-api/partyInteraction/v5/partyInteraction/pi-1034",
        "description": "Customer called about a late delivery",
        "direction": "inbound",
        "reason": "Complaint about order delivery",
        "status": "inProgress",
        "statusChangeDate": "2026-04-02T11:15:00.000Z",
        "creationDate": "2026-04-02T10:42:00.000Z",
        "lastUpdate": "2026-04-02T11:15:00.000Z",
        "interactionDate": {
            "startDateTime": "2026-04-02T10:42:00.000Z",
            "endDateTime": "2026-04-02T10:59:00.000Z",
        },
        "relatedChannel": [
            {
                "@type": "RelatedChannel",
                "role": "interactionChannel",
                "channel": {
                    "@type": "ChannelRef",
                    "@referredType": "Channel",
                    "id": "ch-call-centre",
                    "name": "Call Centre",
                },
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyOrPartyRole",
                "role": "initiator",
                "partyOrPartyRole": {
                    "@type": "PartyRoleRef",
                    "@referredType": "PartyRole",
                    "id": "pr-88",
                    "name": "Jane Doe",
                    "partyId": "party-88",
                    "partyName": "Jane Doe",
                },
            }
        ],
        "attachment": [
            {
                "@type": "AttachmentRefOrValue",
                "id": "att-12",
                "name": "Call recording",
                "mimeType": "audio/mpeg",
                "url": "https://mycsp.com/recordings/att-12.mp3",
                "isRef": False,
            }
        ],
        "note": [
            {
                "@type": "Note",
                "id": "note-1",
                "author": "Agent Smith",
                "date": "2026-04-02T10:58:00.000Z",
                "text": "Customer requested a callback once the order ships.",
            }
        ],
        "interactionItem": [
            {
                "@type": "InteractionItem",
                "id": "ii-1",
                "interactionItemType": "Complaint",
                "reason": "Order delivered late",
                "resolution": "Refund of delivery charge agreed",
                "creationDate": "2026-04-02T10:45:00.000Z",
                "lastUpdate": "2026-04-02T10:57:00.000Z",
                "itemDate": {
                    "startDateTime": "2026-04-02T10:45:00.000Z",
                    "endDateTime": "2026-04-02T10:57:00.000Z",
                },
                "item": {
                    "@type": "RelatedEntityRefOrValue",
                    "role": "subject",
                    "entity": {
                        "@type": "ProductOrderRef",
                        "@referredType": "ProductOrder",
                        "id": "po-501",
                        "name": "Broadband install order",
                    },
                },
                "relatedChannel": [
                    {
                        "@type": "RelatedChannel",
                        "role": "itemChannel",
                        "channel": {
                            "@type": "ChannelRef",
                            "@referredType": "Channel",
                            "id": "ch-call-centre",
                            "name": "Call Centre",
                        },
                    }
                ],
                "relatedParty": [
                    {
                        "@type": "RelatedPartyRefOrPartyRoleRef",
                        "role": "handlingAgent",
                        "partyOrPartyRole": {
                            "@type": "PartyRoleRef",
                            "@referredType": "PartyRole",
                            "id": "pr-12",
                            "name": "Agent Smith",
                        },
                    }
                ],
                "attachment": [
                    {
                        "@type": "AttachmentRefOrValue",
                        "id": "att-13",
                        "name": "Delivery proof",
                        "mimeType": "application/pdf",
                        "url": "https://mycsp.com/docs/att-13.pdf",
                        "isRef": False,
                    }
                ],
                "note": [
                    {
                        "@type": "Note",
                        "id": "note-2",
                        "author": "Agent Smith",
                        "date": "2026-04-02T10:56:00.000Z",
                        "text": "Delivery partner confirmed the two-day delay.",
                    }
                ],
                "interactionItemRelationship": [
                    {
                        "@type": "InteractionItemRelationship",
                        "id": "ii-2",
                        "relationshipType": "relatedTo",
                    }
                ],
            },
            {
                "@type": "InteractionItem",
                "id": "ii-2",
                "interactionItemType": "Ticket",
                "reason": "Delivery partner investigation",
            },
        ],
        "interactionRelationship": [
            {
                "@type": "InteractionRelationship",
                "@referredType": "PartyInteraction",
                "id": "pi-1030",
                "relationshipType": "parent",
            }
        ],
        "externalIdentifier": [
            {
                "@type": "ExternalIdentifier",
                "owner": "MagentoCommerce",
                "externalIdentifierType": "Case",
                "id": "case-77812",
            }
        ],
    }


@pytest.fixture
def party_interaction_1(party_interaction_dict):
    return PartyInteraction.from_dict(party_interaction_dict)


def test_party_interaction_instantiates_with_id(party_interaction_dict):
    pi = PartyInteraction.from_dict(party_interaction_dict)

    assert pi.id == "pi-1034"
    assert pi.direction == "inbound"
    assert pi.reason == "Complaint about order delivery"
    assert pi.status == "inProgress"
    assert pi.statusChangeDate == "2026-04-02T11:15:00.000Z"
    assert pi.creationDate == "2026-04-02T10:42:00.000Z"
    assert pi.lastUpdate == "2026-04-02T11:15:00.000Z"
    assert pi.href.endswith("/partyInteraction/pi-1034")


def test_party_interaction_instantiates_classes(party_interaction_1):
    pi = party_interaction_1

    assert isinstance(pi, PartyInteraction)

    assert isinstance(pi.interactionDate, TimePeriod)
    assert pi.interactionDate.endDateTime == "2026-04-02T10:59:00.000Z"

    assert isinstance(pi.relatedChannel[0], RelatedChannel)
    assert isinstance(pi.relatedChannel[0].channel, ChannelRef)
    assert pi.relatedChannel[0].channel._referred_type == "Channel"

    assert isinstance(pi.relatedParty[0], RelatedPartyOrPartyRole)
    assert isinstance(pi.relatedParty[0].partyOrPartyRole, PartyRoleRef)
    assert pi.relatedParty[0].partyOrPartyRole.partyId == "party-88"

    assert isinstance(pi.attachment[0], AttachmentRefOrValue)
    assert pi.attachment[0].isRef is False

    assert isinstance(pi.note[0], Note)
    assert pi.note[0].author == "Agent Smith"

    assert isinstance(pi.interactionRelationship[0], InteractionRelationship)
    assert pi.interactionRelationship[0].id == "pi-1030"
    assert pi.interactionRelationship[0].relationshipType == "parent"
    assert pi.interactionRelationship[0]._referred_type == "PartyInteraction"

    assert isinstance(pi.externalIdentifier[0], ExternalIdentifier)
    assert pi.externalIdentifier[0].owner == "MagentoCommerce"


def test_party_interaction_item_instantiates_classes(party_interaction_1):
    item = party_interaction_1.interactionItem[0]

    assert isinstance(item, InteractionItem)
    assert item.id == "ii-1"
    assert item.interactionItemType == "Complaint"
    assert item.resolution == "Refund of delivery charge agreed"
    assert item.creationDate == "2026-04-02T10:45:00.000Z"
    assert item.lastUpdate == "2026-04-02T10:57:00.000Z"

    assert isinstance(item.itemDate, TimePeriod)
    assert isinstance(item.item, RelatedEntityRefOrValue)
    assert isinstance(item.item.entity, ProductOrderRef)
    assert item.item.entity.id == "po-501"

    assert isinstance(item.relatedChannel[0], RelatedChannel)
    assert isinstance(item.relatedChannel[0].channel, ChannelRef)

    assert isinstance(item.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(item.relatedParty[0].partyOrPartyRole, PartyRoleRef)

    assert isinstance(item.attachment[0], AttachmentRefOrValue)
    assert isinstance(item.note[0], Note)

    assert isinstance(item.interactionItemRelationship[0], InteractionItemRelationship)
    assert item.interactionItemRelationship[0].id == "ii-2"
    assert item.interactionItemRelationship[0].relationshipType == "relatedTo"


def test_party_interaction_defaults_to_empty_lists():
    pi = PartyInteraction.from_dict(
        {"@type": "PartyInteraction", "id": "pi-1", "direction": "outbound"}
    )

    assert pi.relatedChannel == []
    assert pi.relatedParty == []
    assert pi.attachment == []
    assert pi.note == []
    assert pi.interactionItem == []
    assert pi.interactionRelationship == []
    assert pi.externalIdentifier == []
    assert pi.interactionDate is None
    assert pi.status is None


def test_interaction_item_defaults_to_empty_lists(party_interaction_1):
    item = party_interaction_1.interactionItem[1]

    assert item.relatedChannel == []
    assert item.relatedParty == []
    assert item.attachment == []
    assert item.note == []
    assert item.interactionItemRelationship == []
    assert item.item is None
    assert item.itemDate is None


def test_party_interaction_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")

    assert PartyInteraction.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/partyInteraction/v5/partyInteraction"
    )


def test_party_interaction_to_dict_round_trip(party_interaction_dict):
    result = PartyInteraction.from_dict(party_interaction_dict).to_dict()

    assert result["@type"] == "PartyInteraction"
    assert "@baseType" not in result
    assert result["direction"] == "inbound"
    assert result["relatedChannel"][0]["channel"]["@referredType"] == "Channel"
    assert result["relatedParty"][0]["partyOrPartyRole"]["@referredType"] == "PartyRole"
    assert result["interactionItem"][0]["@type"] == "InteractionItem"
    assert result["interactionItem"][0]["item"]["entity"]["@referredType"] == (
        "ProductOrder"
    )
    assert result["interactionItem"][0]["interactionItemRelationship"][0]["@type"] == (
        "InteractionItemRelationship"
    )
    assert result["interactionRelationship"][0]["@referredType"] == "PartyInteraction"
    assert result["externalIdentifier"][0]["owner"] == "MagentoCommerce"


def test_interaction_relationship_from_entity(party_interaction_1):
    ref = InteractionRelationship.from_entity(party_interaction_1)

    assert isinstance(ref, InteractionRelationship)
    assert ref.id == "pi-1034"
    assert ref._referred_type == "PartyInteraction"
