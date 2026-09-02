import pytest
from tmforum import (
    AccountBalance,
    AccountRelationship,
    AccountRef,
    AccountState,
    AccountType,
    BalanceType,
    BillFormat,
    BillFormatRef,
    BillPresentationMedia,
    BillStructure,
    BillingAccount,
    BillingCycleSpecification,
    Contact,
    Context,
    EmailContactMedium,
    FinancialAccount,
    FinancialAccountRef,
    Money,
    PartyAccount,
    PartyRef,
    PaymentMethodRef,
    PaymentPlan,
    PaymentStatus,
    RelatedPartyRefOrPartyRoleRef,
    SettlementAccount,
    TaxDefinition,
    TaxExemptionCertificate,
    TimePeriod,
)


@pytest.fixture
def settlement_account_dict():
    return {
        "@type": "SettlementAccount",
        "@baseType": "PartyAccount",
        "id": "sa-4711",
        "href": "https://mycsp.com/tmf-api/accountManagement/v5/settlementAccount/sa-4711",
        "name": "Wholesale settlement account",
        "description": "Settlement account for interconnect partner",
        "accountType": "business",
        "state": "active",
        "paymentStatus": "due",
        "lastUpdate": "2026-01-14T00:00:00.000Z",
        "creditLimit": {
            "@type": "Money",
            "unit": "EUR",
            "value": 25000.0,
        },
        "accountBalance": [
            {
                "@type": "AccountBalance",
                "id": "bal-1",
                "balanceType": "receivableBalance",
                "amount": {"@type": "Money", "unit": "EUR", "value": 1200.0},
                "validFor": {
                    "@type": "TimePeriod",
                    "startDateTime": "2026-01-01T00:00:00.000Z",
                    "endDateTime": "2026-12-31T00:00:00.000Z",
                },
            }
        ],
        "accountRelationship": [
            {
                "@type": "AccountRelationship",
                "id": "rel-1",
                "relationshipType": "parent",
                "account": {
                    "@type": "AccountRef",
                    "id": "acc-99",
                    "name": "Parent account",
                },
            }
        ],
        "contact": [
            {
                "@type": "Contact",
                "id": "contact-1",
                "contactName": "Jane Roe",
                "contactType": "billingAddress",
                "contactMedium": [
                    {
                        "@type": "EmailContactMedium",
                        "id": "cm-1",
                        "emailAddress": "jane.roe@example.com",
                    }
                ],
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "settlementPartner",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "party-77",
                    "name": "Interconnect Partner Ltd",
                },
            }
        ],
        "taxExemption": [
            {
                "@type": "TaxExemptionCertificate",
                "id": "tec-1",
                "certificateNumber": "EX-2026-001",
                "taxDefinition": [
                    {
                        "@type": "TaxDefinition",
                        "id": "tax-1",
                        "name": "VAT",
                        "taxType": "VAT",
                    }
                ],
            }
        ],
        "financialAccount": {
            "@type": "FinancialAccountRef",
            "id": "fa-1",
            "name": "AR account",
        },
        "defaultPaymentMethod": {
            "@type": "PaymentMethodRef",
            "id": "pm-1",
            "name": "SEPA transfer",
        },
        "paymentPlan": [
            {
                "@type": "PaymentPlan",
                "planType": "installment",
                "numberOfPayments": 3,
                "totalAmount": {"@type": "Money", "unit": "EUR", "value": 900.0},
            }
        ],
        "billStructure": {
            "@type": "BillStructure",
            "format": {
                "@type": "BillFormat",
                "id": "bf-1",
                "name": "Detailed PDF",
                "description": "Itemised PDF bill",
            },
            "cycleSpecification": {
                "@type": "BillingCycleSpecification",
                "id": "bcs-1",
                "name": "Monthly",
                "frequency": "monthly",
            },
            "presentationMedia": [
                {
                    "@type": "BillPresentationMedia",
                    "id": "bpm-1",
                    "name": "Email",
                    "description": "Bill delivered by email",
                }
            ],
        },
    }


def test_settlement_account_from_dict(settlement_account_dict):
    account = PartyAccount.from_dict(settlement_account_dict)

    assert isinstance(account, SettlementAccount)
    assert isinstance(account, PartyAccount)
    assert account.name == "Wholesale settlement account"
    assert account.state == AccountState.ACTIVE
    assert account.accountType == AccountType.BUSINESS
    assert account.paymentStatus == PaymentStatus.DUE

    assert isinstance(account.creditLimit, Money)
    assert isinstance(account.accountBalance[0], AccountBalance)
    assert account.accountBalance[0].balanceType == BalanceType.RECEIVABLE_BALANCE
    assert isinstance(account.accountBalance[0].amount, Money)
    assert isinstance(account.accountBalance[0].validFor, TimePeriod)

    assert isinstance(account.accountRelationship[0], AccountRelationship)
    assert isinstance(account.accountRelationship[0].account, AccountRef)

    assert isinstance(account.contact[0], Contact)
    assert isinstance(account.contact[0].contactMedium[0], EmailContactMedium)

    assert isinstance(account.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(account.relatedParty[0].partyOrPartyRole, PartyRef)

    assert isinstance(account.taxExemption[0], TaxExemptionCertificate)
    assert isinstance(account.taxExemption[0].taxDefinition[0], TaxDefinition)

    assert isinstance(account.financialAccount, FinancialAccountRef)
    assert isinstance(account.defaultPaymentMethod, PaymentMethodRef)
    assert isinstance(account.paymentPlan[0], PaymentPlan)


def test_settlement_account_bill_structure(settlement_account_dict):
    account = PartyAccount.from_dict(settlement_account_dict)

    bill_structure = account.billStructure
    assert isinstance(bill_structure, BillStructure)
    assert isinstance(bill_structure.format, BillFormat)
    assert bill_structure.format.description == "Itemised PDF bill"
    assert isinstance(bill_structure.cycleSpecification, BillingCycleSpecification)
    assert isinstance(bill_structure.presentationMedia[0], BillPresentationMedia)
    assert bill_structure.presentationMedia[0].description == "Bill delivered by email"


def test_settlement_account_round_trip(settlement_account_dict):
    account = SettlementAccount.from_dict(settlement_account_dict)

    payload = account.to_dict()
    assert payload["@type"] == "SettlementAccount"
    assert payload["@baseType"] == "PartyAccount"
    assert payload["id"] == "sa-4711"
    assert payload["billStructure"]["format"]["@type"] == "BillFormat"


def test_bill_structure_accepts_refs():
    bill_structure = BillStructure.from_dict(
        {
            "@type": "BillStructure",
            "format": {"@type": "BillFormatRef", "id": "bf-1", "name": "Detailed PDF"},
        }
    )
    assert isinstance(bill_structure.format, BillFormatRef)


def test_account_resource_paths():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    base = "https://mycsp.com/tmf-api/accountManagement/v5"

    assert SettlementAccount.get_resource_path(context) == f"{base}/settlementAccount"
    assert PartyAccount.get_resource_path(context) == f"{base}/partyAccount"
    assert BillFormat.get_resource_path(context) == f"{base}/billFormat"
    assert (
        BillPresentationMedia.get_resource_path(context)
        == f"{base}/billPresentationMedia"
    )
    assert BillingAccount.get_resource_path(context) == f"{base}/billingAccount"
    assert FinancialAccount.get_resource_path(context) == f"{base}/financialAccount"
    assert (
        BillingCycleSpecification.get_resource_path(context)
        == f"{base}/billingCycleSpecification"
    )
