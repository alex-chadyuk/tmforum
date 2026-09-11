import pytest
from tmforum import (
    AccountBalance,
    AgreementSpecificationRef,
    AppointmentStateType,
    BillingAccountRef,
    CalendarEventRef,
    Context,
    Customer360,
    Customer360Account,
    Customer360Agreement,
    Customer360Appointment,
    Customer360CustomerBill,
    Customer360Customer,
    Customer360LoyaltyAccount,
    Customer360PartyInteraction,
    Customer360PaymentMethod,
    Customer360ProductOrder,
    Customer360Product,
    Customer360Promotion,
    Customer360Quote,
    Customer360ServiceProblem,
    Customer360TroubleTicket,
    CustomerBillStateType,
    Duration,
    ExternalIdentifier,
    GeographicAddressContactMedium,
    GeographicAddressRef,
    ItemActionType,
    Money,
    OrderPrice,
    OrderTerm,
    PartyRef,
    PartyRoleRef,
    PhoneContactMedium,
    ProductOfferingRef,
    ProductOrderItem,
    ProductOrderItemStateType,
    ProductOrderStateType,
    ProductStatusType,
    Quote,
    QuoteStateTypeEnum,
    RelatedPartyOrPartyRole,
    RelatedPartyRefOrPartyRoleRef,
    ServiceRef,
    TimePeriod,
    TroubleTicketStatusType,
)


@pytest.fixture
def customer360_dict():
    return {
        "@type": "Customer360",
        "href": "https://host:port/tmf-api/customer360/v5/customer360/1140",
        "id": "1140",
        "@schemaLocation": "/schema-registry/schema/Customer360",
        "validFor": {
            "startDateTime": "2018-06-13T00:00:00.000Z",
            "endDateTime": "2019-01-11T00:00:00.000Z",
        },
        "customer": {
            "@type": "Customer360Customer",
            "href": "https://host:port/tmf-api/customerManagement/v5/customer/1140",
            "id": "1140",
            "name": "Moon Football Club",
            "status": "Approved",
            "contactMedium": [
                {
                    "@type": "PhoneContactMedium",
                    "@baseType": "ContactMedium",
                    "id": "2256789876",
                    "preferred": True,
                    "contactType": "homePhone",
                    "phoneNumber": "01 09 75 83 51",
                },
                {
                    "@type": "GeographicAddressContactMedium",
                    "@baseType": "ContactMedium",
                    "id": "12345",
                    "preferred": False,
                    "contactType": "homeAddress",
                    "city": "Paris",
                    "country": "France",
                    "postCode": "75014",
                    "street1": "15 Rue des Canards",
                    "geographicAddress": {
                        "@type": "GeographicAddressRef",
                        "@referredType": "GeographicAddress",
                        "id": "12345",
                        "href": (
                            "https://host:port/tmf-api/geographicAddressManagement/v5"
                            "/geographicAddress/12345"
                        ),
                    },
                },
            ],
            "engagedParty": {
                "@type": "PartyRef",
                "@referredType": "Organization",
                "href": "https://host:port/tmf-api/partyManagement/v5/organization/500",
                "id": "500",
                "name": "Happy Travellers",
            },
            "relatedParty": [
                {
                    "@type": "RelatedPartyOrPartyRole",
                    "role": "bill receiver",
                    "partyOrPartyRole": {
                        "@type": "PartyRef",
                        "@referredType": "Organization",
                        "id": "2777",
                        "name": "John Doe (Accounting) Ltd",
                    },
                }
            ],
            "validFor": {
                "startDateTime": "2018-06-12T00:00:00.000Z",
                "endDateTime": "2019-01-11T00:00:00.000Z",
            },
        },
        "account": [
            {
                "@type": "Customer360Account",
                "href": "https://host:port/tmf-api/accountManagement/v5/account/5430",
                "id": "5430",
                "accountType": "Business",
                "description": "Main billing account of the club",
                "lastUpdate": "2018-06-14T10:30:00.000Z",
                "name": "Home Account",
                "state": "Inactive",
            }
        ],
        "agreement": [
            {
                "@type": "Customer360Agreement",
                "href": "https://host:port/tmf-api/agreementManagement/v4/agreement/28",
                "id": "28",
                "name": "Summer Contract Agreement",
                "agreementType": "commercial",
                "status": "inProgress",
                "agreementPeriod": {
                    "startDateTime": "2024-04-25T00:00:00.000Z",
                    "endDateTime": "2028-04-25T00:00:00.000Z",
                },
                "agreementSpecification": {
                    "@type": "AgreementSpecificationRef",
                    "@referredType": "AgreementSpecification",
                    "id": "9834-11",
                    "name": "Bandwith extender",
                    "description": "Special agreement with higher bandwith.",
                    "version": "2.0",
                },
                "engagedParty": [
                    {
                        "@type": "PartyRef",
                        "@referredType": "Organization",
                        "id": "1140",
                        "name": "Moon Football Club",
                    },
                    {
                        "@type": "PartyRoleRef",
                        "@referredType": "Supplier",
                        "id": "pr-77",
                        "name": "Fibre Partner",
                        "partyId": "org-77",
                    },
                ],
            }
        ],
        "appointment": [
            {
                "@type": "Customer360Appointment",
                "href": "https://serverRoot/tmf-api/appointment/v4/appointment/21",
                "id": "21",
                "calendarEvent": {
                    "@type": "CalendarEventRef",
                    "@referredType": "CalendarEvent",
                    "id": "33",
                    "name": "Intervention calendar event",
                },
                "category": "intervention",
                "creationDate": "2018-02-01T14:40:43.000Z",
                "description": "Fix an internet connexion problem for a customer",
                "externalId": "432113",
                "lastUpdate": "2018-02-04T14:40:43.000Z",
                "status": "confirmed",
                "validFor": {
                    "startDateTime": "2018-02-15T14:00:00.000Z",
                    "endDateTime": "2018-02-15T16:00:00.000Z",
                },
            }
        ],
        "customerBill": [
            {
                "@type": "Customer360CustomerBill",
                "id": "CB-123",
                "billNo": "33-34198237",
                "category": "Monthly",
                "state": "sent",
            },
            {
                "@type": "Customer360CustomerBill",
                "id": "CB-124",
                "billNo": "780123456",
                "category": "normal",
                "state": "settled",
            },
        ],
        "loyaltyAccount": [
            {
                "@type": "Customer360LoyaltyAccount",
                "@baseType": "PartyAccount",
                "id": "12345",
                "description": "Loyalty account for loyalty program member",
                "lastUpdate": "2024-05-01T20:30:52.370Z",
                "name": "Loyalty Account",
                "state": "Active",
                "accountType": "Loyalty Account",
                "relatedParty": [
                    {
                        "@type": "RelatedPartyRefOrPartyRoleRef",
                        "role": "Loyalty Program Member",
                        "partyOrPartyRole": {
                            "@type": "PartyRoleRef",
                            "@referredType": "LoyaltyProgramMember",
                            "id": "1140",
                            "name": "Moon Football Club",
                        },
                    }
                ],
                "accountBalance": [
                    {
                        "@type": "AccountBalance",
                        "id": "AB123",
                        "amount": {"value": 50, "unit": "POINTS"},
                        "balanceType": "LoyaltyEarningsWallet",
                        "validFor": {
                            "startDateTime": "2021-03-17T00:00:00.000Z",
                            "endDateTime": "2022-03-17T00:00:00.000Z",
                        },
                    }
                ],
                "externalIdentifier": [
                    {
                        "@type": "ExternalIdentifier",
                        "owner": "LoyaltyHub",
                        "externalIdentifierType": "memberNumber",
                        "id": "LH-99812",
                    }
                ],
            }
        ],
        "partyInteraction": [
            {
                "@type": "Customer360PartyInteraction",
                "id": "123",
                "interactionDate": {
                    "startDateTime": "2019-10-02T11:36:18.758Z",
                    "endDateTime": "2019-10-02T11:53:21.789Z",
                },
                "description": "Visit to store",
                "reason": "The user wanted to buy TV and internet plan",
                "status": "ongoing",
            }
        ],
        "paymentMethod": [
            {
                "@type": "Customer360PaymentMethod",
                "id": "12345",
                "description": "My gold mastercard",
                "isPreferred": True,
                "validFor": {
                    "startDateTime": "2021-03-17T00:00:00.000Z",
                    "endDateTime": "2024-04-16T00:00:00.000Z",
                },
                "name": "Main credit card",
                "status": "active",
                "statusDate": "2021-03-17T00:00:00.000Z",
            }
        ],
        "productOrder": [
            {
                "@type": "Customer360ProductOrder",
                "id": "30001",
                "category": "B2C product order",
                "completionDate": "2019-05-02T08:13:59.506Z",
                "description": "Product Order illustration sample",
                "expectedCompletionDate": "2019-05-02T08:13:59.506Z",
                "externalId": "PO-456",
                "creationDate": "2019-04-30T08:13:59.506Z",
                "priority": "1",
                "state": "completed",
                "productOrderItem": [
                    {
                        "@type": "ProductOrderItem",
                        "id": "1",
                        "action": "add",
                        "quantity": 1,
                        "state": "completed",
                        "itemTerm": [
                            {
                                "@type": "OrderTerm",
                                "name": "12 month commitment",
                                "duration": {"amount": 12, "units": "month"},
                            }
                        ],
                        "itemPrice": [
                            {
                                "@type": "OrderPrice",
                                "name": "Monthly fee",
                                "billingAccount": {
                                    "@type": "BillingAccountRef",
                                    "@referredType": "BillingAccount",
                                    "id": "ba-5430",
                                },
                            }
                        ],
                    }
                ],
            }
        ],
        "product": [
            {
                "@type": "Customer360Product",
                "id": "g265-tf85",
                "description": "product description",
                "name": "Voice Over IP Basic instance for Jean",
                "productOffering": {
                    "@type": "ProductOfferingRef",
                    "@referredType": "ProductOffering",
                    "id": "PO-101-1",
                    "name": "Voice Over IP Basic",
                },
                "status": "active",
            }
        ],
        "promotion": [
            {
                "@type": "Customer360Promotion",
                "id": "promo-7",
                "name": "Summer double data",
                "description": "Double data allowance for three months",
                "type": "discount",
                "lifecycleStatus": "active",
                "lastUpdate": "2024-06-01T09:00:00.000Z",
                "validFor": {
                    "startDateTime": "2024-06-01T00:00:00.000Z",
                    "endDateTime": "2024-09-01T00:00:00.000Z",
                },
            }
        ],
        "quote": [
            {
                "@type": "Customer360Quote",
                "id": "12dd-78hg",
                "category": "BSBS Quote",
                "creationDate": "2021-05-05T12:45:12.028Z",
                "description": "Quote illustration",
                "effectiveQuoteCompletionDate": "2021-05-21T12:45:12.028Z",
                "expectedFulfillmentStartDate": "2021-05-21T12:45:12.028Z",
                "expectedQuoteCompletionDate": "2021-05-14T12:45:12.028Z",
                "state": "approved",
                "validFor": {
                    "startDateTime": "2021-05-06T12:45:12.033Z",
                    "endDateTime": "2021-06-06T12:45:12.033Z",
                },
                "version": "1",
            }
        ],
        "serviceProblem": [
            {
                "@type": "Customer360ServiceProblem",
                "id": "problemxxxx0000",
                "affectedService": [
                    {
                        "@type": "ServiceRef",
                        "@referredType": "Service",
                        "id": "NW1_Tokyo_Osaka",
                    },
                    {
                        "@type": "ServiceRef",
                        "@referredType": "Service",
                        "id": "NW1_Tokyo_xxxx",
                    },
                ],
                "category": "supplier.originated",
                "description": "connection failure between Tokyo and Osaka",
                "originatingSystem": "System_001",
                "priority": 1,
                "reason": "Network infrastructure failure",
                "status": "resolved",
            }
        ],
        "troubleTicket": [
            {
                "@type": "Customer360TroubleTicket",
                "id": "3180",
                "creationDate": "2019-05-31T07:34:45.968Z",
                "description": "I do not accept the last VOD charge",
                "expectedResolutionDate": "2019-06-10T07:34:45.968Z",
                "externalIdentifier": "213-9909",
                "lastUpdate": "2019-06-01T10:15:30.500Z",
                "name": "Compliant over last bill",
                "priority": "High",
                "requestedResolutionDate": "2019-05-31T07:34:45.968Z",
                "severity": "Urgent",
                "status": "pending",
                "statusChangeDate": "2019-06-01T10:15:30.500Z",
                "statusChangeReason": "Need more information from the customer",
                "ticketType": "Bill Dispute",
            }
        ],
    }


@pytest.fixture
def customer360_1(customer360_dict):
    return Customer360.from_dict(customer360_dict)


def test_customer360_instantiates_with_id(customer360_1):
    c360 = customer360_1

    assert isinstance(c360, Customer360)
    assert c360.id == "1140"
    assert c360.href.endswith("/customer360/v5/customer360/1140")
    assert isinstance(c360.validFor, TimePeriod)
    assert c360.validFor.startDateTime == "2018-06-13T00:00:00.000Z"


def test_customer360_instantiates_customer(customer360_1):
    customer = customer360_1.customer

    assert isinstance(customer, Customer360Customer)
    assert customer.name == "Moon Football Club"
    assert customer.status == "Approved"
    assert isinstance(customer.validFor, TimePeriod)

    assert isinstance(customer.contactMedium[0], PhoneContactMedium)
    assert customer.contactMedium[0].phoneNumber == "01 09 75 83 51"
    assert isinstance(customer.contactMedium[1], GeographicAddressContactMedium)
    assert isinstance(customer.contactMedium[1].geographicAddress, GeographicAddressRef)

    assert isinstance(customer.engagedParty, PartyRef)
    assert customer.engagedParty._referred_type == "Organization"

    assert isinstance(customer.relatedParty[0], RelatedPartyOrPartyRole)
    assert isinstance(customer.relatedParty[0].partyOrPartyRole, PartyRef)
    assert customer.relatedParty[0].partyOrPartyRole.id == "2777"


def test_customer360_instantiates_accounts(customer360_1):
    account = customer360_1.account[0]

    assert isinstance(account, Customer360Account)
    assert account.accountType == "Business"
    assert account.state == "Inactive"

    loyalty = customer360_1.loyaltyAccount[0]
    assert isinstance(loyalty, Customer360LoyaltyAccount)
    assert isinstance(loyalty, Customer360Account)
    assert loyalty.name == "Loyalty Account"
    assert loyalty.accountType == "Loyalty Account"

    assert isinstance(loyalty.accountBalance[0], AccountBalance)
    assert isinstance(loyalty.accountBalance[0].amount, Money)
    assert loyalty.accountBalance[0].amount.unit == "POINTS"
    assert isinstance(loyalty.accountBalance[0].validFor, TimePeriod)

    assert isinstance(loyalty.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(loyalty.relatedParty[0].partyOrPartyRole, PartyRoleRef)
    assert (
        loyalty.relatedParty[0].partyOrPartyRole._referred_type
        == "LoyaltyProgramMember"
    )

    assert isinstance(loyalty.externalIdentifier[0], ExternalIdentifier)
    assert loyalty.externalIdentifier[0].id == "LH-99812"


def test_customer360_instantiates_agreement(customer360_1):
    agreement = customer360_1.agreement[0]

    assert isinstance(agreement, Customer360Agreement)
    assert agreement.agreementType == "commercial"
    assert agreement.status == "inProgress"
    assert isinstance(agreement.agreementPeriod, TimePeriod)

    spec = agreement.agreementSpecification
    assert isinstance(spec, AgreementSpecificationRef)
    assert spec._referred_type == "AgreementSpecification"
    assert spec.description == "Special agreement with higher bandwith."
    assert spec.version == "2.0"

    assert isinstance(agreement.engagedParty[0], PartyRef)
    assert isinstance(agreement.engagedParty[1], PartyRoleRef)
    assert agreement.engagedParty[1].partyId == "org-77"


def test_customer360_instantiates_appointment(customer360_1):
    appointment = customer360_1.appointment[0]

    assert isinstance(appointment, Customer360Appointment)
    assert appointment.status is AppointmentStateType.CONFIRMED
    assert appointment.externalId == "432113"
    assert isinstance(appointment.validFor, TimePeriod)
    assert isinstance(appointment.calendarEvent, CalendarEventRef)
    assert appointment.calendarEvent._referred_type == "CalendarEvent"
    assert appointment.calendarEvent.id == "33"


def test_customer360_instantiates_bills_interactions_and_payment_methods(
    customer360_1,
):
    bills = customer360_1.customerBill

    assert all(isinstance(b, Customer360CustomerBill) for b in bills)
    assert bills[0].state is CustomerBillStateType.SENT
    assert bills[1].state is CustomerBillStateType.SETTLED
    assert bills[1].billNo == "780123456"

    interaction = customer360_1.partyInteraction[0]
    assert isinstance(interaction, Customer360PartyInteraction)
    assert isinstance(interaction.interactionDate, TimePeriod)
    assert interaction.status == "ongoing"

    payment_method = customer360_1.paymentMethod[0]
    assert isinstance(payment_method, Customer360PaymentMethod)
    assert payment_method.isPreferred is True
    assert payment_method.statusDate == "2021-03-17T00:00:00.000Z"


def test_customer360_instantiates_product_order(customer360_1):
    order = customer360_1.productOrder[0]

    assert isinstance(order, Customer360ProductOrder)
    assert order.state is ProductOrderStateType.COMPLETED
    assert order.priority == "1"

    item = order.productOrderItem[0]
    assert isinstance(item, ProductOrderItem)
    assert item.action is ItemActionType.ADD
    assert item.state is ProductOrderItemStateType.COMPLETED

    assert isinstance(item.itemTerm[0], OrderTerm)
    assert isinstance(item.itemTerm[0].duration, Duration)
    assert item.itemTerm[0].duration.amount == 12

    assert isinstance(item.itemPrice[0], OrderPrice)
    assert isinstance(item.itemPrice[0].billingAccount, BillingAccountRef)
    assert item.itemPrice[0].billingAccount.id == "ba-5430"


def test_customer360_instantiates_products_promotions_and_quotes(customer360_1):
    product = customer360_1.product[0]

    assert isinstance(product, Customer360Product)
    assert product.status is ProductStatusType.ACTIVE
    assert isinstance(product.productOffering, ProductOfferingRef)

    promotion = customer360_1.promotion[0]
    assert isinstance(promotion, Customer360Promotion)
    assert promotion.type == "discount"
    assert promotion.lifecycleStatus == "active"
    assert isinstance(promotion.validFor, TimePeriod)

    quote = customer360_1.quote[0]
    assert isinstance(quote, Customer360Quote)
    assert quote.state is QuoteStateTypeEnum.APPROVED
    assert quote.version == "1"
    assert isinstance(quote.validFor, TimePeriod)


def test_customer360_instantiates_problems_and_tickets(customer360_1):
    problem = customer360_1.serviceProblem[0]

    assert isinstance(problem, Customer360ServiceProblem)
    assert problem.priority == 1
    assert problem.status == "resolved"
    assert [s.id for s in problem.affectedService] == [
        "NW1_Tokyo_Osaka",
        "NW1_Tokyo_xxxx",
    ]
    assert all(isinstance(s, ServiceRef) for s in problem.affectedService)

    ticket = customer360_1.troubleTicket[0]
    assert isinstance(ticket, Customer360TroubleTicket)
    assert ticket.status is TroubleTicketStatusType.PENDING
    assert ticket.externalIdentifier == "213-9909"
    assert ticket.ticketType == "Bill Dispute"


def test_customer360_defaults_to_empty_lists():
    c360 = Customer360.from_dict({"@type": "Customer360", "id": "1140"})

    assert c360.customer is None
    assert c360.validFor is None
    assert c360.account == []
    assert c360.agreement == []
    assert c360.appointment == []
    assert c360.customerBill == []
    assert c360.partyInteraction == []
    assert c360.loyaltyAccount == []
    assert c360.paymentMethod == []
    assert c360.productOrder == []
    assert c360.product == []
    assert c360.promotion == []
    assert c360.quote == []
    assert c360.serviceProblem == []
    assert c360.troubleTicket == []


def test_value_objects_default_to_empty_lists():
    assert Customer360Customer().contactMedium == []
    assert Customer360Customer().relatedParty == []
    assert Customer360LoyaltyAccount().accountBalance == []
    assert Customer360LoyaltyAccount().externalIdentifier == []
    assert Customer360Agreement().engagedParty == []
    assert Customer360ProductOrder().productOrderItem == []
    assert Customer360ServiceProblem().affectedService == []
    assert ProductOrderItem().itemTerm == []


def test_customer360_rejects_non_list_account():
    with pytest.raises(ValueError):
        Customer360(account=Customer360Account(id="5430"))


def test_loyalty_account_rejects_non_list_balance():
    with pytest.raises(ValueError):
        Customer360LoyaltyAccount(accountBalance=AccountBalance(id="AB123"))


def test_customer360_unknown_status_passes_through():
    ticket = Customer360TroubleTicket.from_dict(
        {"@type": "Customer360TroubleTicket", "id": "1", "status": "submitted"}
    )

    assert ticket.status == "submitted"


def test_appointment_state_type_values():
    assert {s.value for s in AppointmentStateType} == {
        "confirmed",
        "cancelled",
        "pending",
        "rescheduled",
        "inProgress",
        "completed",
        "expired",
        "failed",
    }


def test_trouble_ticket_status_type_values():
    assert {s.value for s in TroubleTicketStatusType} == {
        "acknowledged",
        "rejected",
        "pending",
        "held",
        "inProgress",
        "cancelled",
        "closed",
        "resolved",
    }


@pytest.mark.parametrize(
    "value, member",
    [
        ("acknowledged", QuoteStateTypeEnum.ACKNOWLEDGED),
        ("pending", QuoteStateTypeEnum.PENDING),
        ("declined", QuoteStateTypeEnum.DECLINED),
        ("cancelled", QuoteStateTypeEnum.CANCELLED),
    ],
)
def test_quote_state_type_covers_customer360_values(value, member):
    quote_ = Customer360Quote.from_dict(
        {"@type": "Customer360Quote", "id": "q-1", "state": value}
    )
    quote = Quote.from_dict({"@type": "Quote", "id": "q-1", "state": value})

    assert quote_.state is member
    assert quote.state is member


def test_quote_state_type_no_longer_accepts_canceled():
    quote = Quote.from_dict({"@type": "Quote", "id": "q-1", "state": "canceled"})

    assert QuoteStateTypeEnum.CANCELLED.value == "cancelled"
    assert quote.state == "canceled"


def test_customer360_resource_path():
    context = Context(api_base_url="https://host:port/tmf-api")

    assert (
        Customer360.get_resource_path(context)
        == "https://host:port/tmf-api/customer360/v5/customer360"
    )


def test_customer360_to_dict_round_trip(customer360_dict):
    result = Customer360.from_dict(customer360_dict).to_dict()

    assert result["@type"] == "Customer360"
    assert "@baseType" not in result
    assert result["id"] == "1140"
    assert result["validFor"]["startDateTime"] == "2018-06-13T00:00:00.000Z"

    customer = result["customer"]
    assert customer["@type"] == "Customer360Customer"
    assert "@baseType" not in customer
    assert customer["contactMedium"][0]["@type"] == "PhoneContactMedium"
    assert customer["contactMedium"][0]["@baseType"] == "ContactMedium"
    assert customer["engagedParty"]["@referredType"] == "Organization"
    assert customer["relatedParty"][0]["partyOrPartyRole"]["@type"] == "PartyRef"

    assert result["account"][0]["@type"] == "Customer360Account"

    loyalty = result["loyaltyAccount"][0]
    assert loyalty["@type"] == "Customer360LoyaltyAccount"
    assert loyalty["@baseType"] == "Customer360Account"
    assert loyalty["accountBalance"][0]["amount"]["unit"] == "POINTS"
    assert loyalty["externalIdentifier"][0]["id"] == "LH-99812"

    agreement = result["agreement"][0]
    assert agreement["@type"] == "Customer360Agreement"
    assert agreement["agreementSpecification"]["@type"] == "AgreementSpecificationRef"
    assert (
        agreement["agreementSpecification"]["@referredType"] == "AgreementSpecification"
    )
    assert agreement["agreementSpecification"]["version"] == "2.0"
    assert agreement["engagedParty"][0]["@type"] == "PartyRef"
    assert agreement["engagedParty"][1]["@type"] == "PartyRoleRef"

    appointment = result["appointment"][0]
    assert appointment["status"] == "confirmed"
    assert appointment["calendarEvent"]["@type"] == "CalendarEventRef"
    assert appointment["calendarEvent"]["@referredType"] == "CalendarEvent"

    assert result["customerBill"][1]["state"] == "settled"
    assert result["partyInteraction"][0]["@type"] == "Customer360PartyInteraction"
    assert result["paymentMethod"][0]["isPreferred"] is True

    order = result["productOrder"][0]
    assert order["state"] == "completed"
    item = order["productOrderItem"][0]
    assert item["@type"] == "ProductOrderItem"
    assert item["action"] == "add"
    assert item["itemTerm"][0]["@type"] == "OrderTerm"
    assert item["itemTerm"][0]["duration"]["amount"] == 12
    assert item["itemPrice"][0]["billingAccount"]["@referredType"] == "BillingAccount"

    assert result["product"][0]["status"] == "active"
    assert result["promotion"][0]["type"] == "discount"
    assert result["quote"][0]["state"] == "approved"
    assert result["serviceProblem"][0]["affectedService"][1]["id"] == "NW1_Tokyo_xxxx"
    assert result["troubleTicket"][0]["status"] == "pending"
    assert result["troubleTicket"][0]["externalIdentifier"] == "213-9909"
