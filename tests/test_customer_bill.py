import pytest
from tmforum import (
    AppliedBillingTaxRate,
    AppliedCustomerBillingRate,
    AppliedCustomerBillingRateType,
    AppliedPayment,
    AttachmentRefOrValue,
    BillCycle,
    BillCycleRef,
    BillCycleSpecificationRef,
    BillingAccountRef,
    Characteristic,
    Context,
    CustomerBill,
    CustomerBillOnDemand,
    CustomerBillOnDemandStateType,
    CustomerBillRef,
    CustomerBillRunType,
    CustomerBillStateType,
    FinancialAccountRef,
    Money,
    PartyRef,
    PaymentMethodRef,
    PaymentRef,
    RelatedPartyRefOrPartyRoleRef,
    StringCharacteristic,
    TaxCategory,
    TaxItem,
    TimePeriod,
)


@pytest.fixture
def customer_bill_dict():
    return {
        "@type": "CustomerBill",
        "id": "bill-2026-03",
        "href": "https://mycsp.com/tmf-api/customerBill/v5/customerBill/bill-2026-03",
        "billNo": "INV-2026-03",
        "category": "normal",
        "billDate": "2026-03-01T00:00:00.000Z",
        "lastUpdate": "2026-03-02T08:15:00.000Z",
        "nextBillDate": "2026-04-01T00:00:00.000Z",
        "paymentDueDate": "2026-03-21T00:00:00.000Z",
        "runType": "onCycle",
        "state": "sent",
        "amountDue": {"@type": "Money", "unit": "EUR", "value": 118.5},
        "remainingAmount": {"@type": "Money", "unit": "EUR", "value": 18.5},
        "taxExcludedAmount": {"@type": "Money", "unit": "EUR", "value": 100.0},
        "taxIncludedAmount": {"@type": "Money", "unit": "EUR", "value": 118.5},
        "billingPeriod": {
            "@type": "TimePeriod",
            "startDateTime": "2026-02-01T00:00:00.000Z",
            "endDateTime": "2026-02-28T23:59:59.000Z",
        },
        "billingAccount": {
            "@type": "BillingAccountRef",
            "id": "acc-341",
            "name": "Jane Doe billing account",
            "ratingType": "Postpaid",
            "@referredType": "BillingAccount",
        },
        "financialAccount": {
            "@type": "FinancialAccountRef",
            "id": "fin-12",
            "name": "Receivables",
            "@referredType": "FinancialAccount",
        },
        "paymentMethod": {
            "@type": "PaymentMethodRef",
            "id": "pm-55",
            "name": "Visa ending 4242",
            "@referredType": "BankCard",
        },
        "billCycle": {
            "@type": "BillCycleRef",
            "id": "bc-2026-02",
            "name": "February 2026 cycle",
            "@referredType": "BillCycle",
        },
        "appliedPayment": [
            {
                "@type": "AppliedPayment",
                "appliedAmount": {"@type": "Money", "unit": "EUR", "value": 100.0},
                "payment": {
                    "@type": "PaymentRef",
                    "id": "pay-8821",
                    "name": "March invoice settlement",
                    "@referredType": "Payment",
                },
            }
        ],
        "billDocument": [
            {
                "@type": "AttachmentRefOrValue",
                "id": "att-1",
                "name": "INV-2026-03.pdf",
                "mimeType": "application/pdf",
                "url": "https://mycsp.com/documents/INV-2026-03.pdf",
            }
        ],
        "taxItem": [
            {
                "@type": "TaxItem",
                "taxCategory": "VAT",
                "taxRate": 18.5,
                "taxAmount": {"@type": "Money", "unit": "EUR", "value": 18.5},
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyRefOrPartyRoleRef",
                "role": "billReceiver",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "party-99",
                    "name": "Jane Doe",
                },
            }
        ],
    }


@pytest.fixture
def customer_bill_on_demand_dict():
    return {
        "@type": "CustomerBillOnDemand",
        "id": "cbod-77",
        "href": "https://mycsp.com/tmf-api/customerBill/v5/customerBillOnDemand/cbod-77",
        "name": "Interim bill request",
        "description": "Customer requested an interim bill before the cycle close",
        "lastUpdate": "2026-03-10T11:30:00.000Z",
        "state": "inProgress",
        "billingAccount": {
            "@type": "BillingAccountRef",
            "id": "acc-341",
            "name": "Jane Doe billing account",
            "@referredType": "BillingAccount",
        },
        "customerBill": {
            "@type": "CustomerBillRef",
            "id": "bill-2026-03",
            "name": "Invoice INV-2026-03",
            "@referredType": "CustomerBill",
        },
        "relatedParty": {
            "@type": "RelatedPartyRefOrPartyRoleRef",
            "role": "requestor",
            "partyOrPartyRole": {
                "@type": "PartyRef",
                "id": "party-99",
                "name": "Jane Doe",
            },
        },
    }


@pytest.fixture
def bill_cycle_dict():
    return {
        "@type": "BillCycle",
        "id": "bc-2026-02",
        "href": "https://mycsp.com/tmf-api/customerBill/v5/billCycle/bc-2026-02",
        "name": "February 2026 cycle",
        "description": "Monthly cycle for postpaid residential accounts",
        "billingDate": "2026-03-01T00:00:00.000Z",
        "billingPeriod": "monthly",
        "chargeDate": "2026-03-02T00:00:00.000Z",
        "creditDate": "2026-03-03T00:00:00.000Z",
        "mailingDate": "2026-03-04T00:00:00.000Z",
        "paymentDueDate": "2026-03-21T00:00:00.000Z",
        "validFor": {
            "@type": "TimePeriod",
            "startDateTime": "2026-02-01T00:00:00.000Z",
            "endDateTime": "2026-02-28T23:59:59.000Z",
        },
        "BillCycleSpecification": {
            "@type": "BillCycleSpecificationRef",
            "id": "bcs-monthly",
            "name": "Monthly residential",
            "description": "Bills on the first of every month",
            "@referredType": "BillCycleSpecification",
        },
    }


@pytest.fixture
def applied_customer_billing_rate_dict():
    return {
        "@type": "AppliedCustomerBillingRate",
        "id": "acbr-1",
        "href": "https://mycsp.com/tmf-api/customerBill/v5/appliedCustomerBillingRate/acbr-1",
        "name": "Monthly subscription",
        "description": "Recurring charge for the broadband plan",
        "date": "2026-02-01T00:00:00.000Z",
        "appliedBillingRateType": "appliedBillingChargeProductRecurringCharge",
        "isBilled": True,
        "taxExcludedAmount": {"@type": "Money", "unit": "EUR", "value": 100.0},
        "taxIncludedAmount": {"@type": "Money", "unit": "EUR", "value": 118.5},
        "periodCoverage": {
            "@type": "TimePeriod",
            "startDateTime": "2026-02-01T00:00:00.000Z",
            "endDateTime": "2026-02-28T23:59:59.000Z",
        },
        "bill": {
            "@type": "CustomerBillRef",
            "id": "bill-2026-03",
            "@referredType": "CustomerBill",
        },
        "appliedTax": [
            {
                "@type": "AppliedBillingTaxRate",
                "id": "abtr-1",
                "href": "https://mycsp.com/tmf-api/customerBill/v5/appliedBillingTaxRate/abtr-1",
                "taxCategory": "VAT",
                "taxRate": 18.5,
                "taxAmount": {"@type": "Money", "unit": "EUR", "value": 18.5},
            }
        ],
        "characteristic": [
            {
                "@type": "StringCharacteristic",
                "name": "invoiceSection",
                "valueType": "string",
                "value": "Subscriptions",
            }
        ],
    }


def test_customer_bill_from_dict_nested_types(customer_bill_dict):
    bill = CustomerBill.from_dict(customer_bill_dict)

    assert isinstance(bill, CustomerBill)
    assert bill.billNo == "INV-2026-03"
    assert bill.state is CustomerBillStateType.SENT
    assert bill.runType is CustomerBillRunType.ON_CYCLE

    assert isinstance(bill.amountDue, Money)
    assert bill.amountDue.value == 118.5
    assert isinstance(bill.remainingAmount, Money)
    assert isinstance(bill.taxExcludedAmount, Money)
    assert isinstance(bill.taxIncludedAmount, Money)
    assert isinstance(bill.billingPeriod, TimePeriod)

    assert isinstance(bill.billingAccount, BillingAccountRef)
    assert bill.billingAccount._referred_type == "BillingAccount"
    assert isinstance(bill.financialAccount, FinancialAccountRef)
    assert isinstance(bill.paymentMethod, PaymentMethodRef)
    assert isinstance(bill.billCycle, BillCycleRef)

    assert len(bill.appliedPayment) == 1
    applied = bill.appliedPayment[0]
    assert isinstance(applied, AppliedPayment)
    assert isinstance(applied.appliedAmount, Money)
    assert isinstance(applied.payment, PaymentRef)

    assert isinstance(bill.billDocument[0], AttachmentRefOrValue)
    assert bill.billDocument[0].mimeType == "application/pdf"

    assert isinstance(bill.taxItem[0], TaxItem)
    assert isinstance(bill.taxItem[0].taxAmount, Money)

    assert isinstance(bill.relatedParty[0], RelatedPartyRefOrPartyRoleRef)
    assert isinstance(bill.relatedParty[0].partyOrPartyRole, PartyRef)
    assert bill.relatedParty[0].role == "billReceiver"


def test_customer_bill_on_demand_from_dict_nested_types(customer_bill_on_demand_dict):
    request = CustomerBillOnDemand.from_dict(customer_bill_on_demand_dict)

    assert isinstance(request, CustomerBillOnDemand)
    assert request.name == "Interim bill request"
    assert request.state is CustomerBillOnDemandStateType.IN_PROGRESS
    assert isinstance(request.billingAccount, BillingAccountRef)
    assert isinstance(request.customerBill, CustomerBillRef)
    assert request.customerBill._referred_type == "CustomerBill"
    assert isinstance(request.relatedParty, RelatedPartyRefOrPartyRoleRef)
    assert isinstance(request.relatedParty.partyOrPartyRole, PartyRef)


def test_bill_cycle_from_dict_nested_types(bill_cycle_dict):
    cycle = BillCycle.from_dict(bill_cycle_dict)

    assert isinstance(cycle, BillCycle)
    assert cycle.billingPeriod == "monthly"
    assert cycle.chargeDate == "2026-03-02T00:00:00.000Z"
    assert cycle.creditDate == "2026-03-03T00:00:00.000Z"
    assert cycle.mailingDate == "2026-03-04T00:00:00.000Z"
    assert isinstance(cycle.validFor, TimePeriod)
    assert isinstance(cycle.BillCycleSpecification, BillCycleSpecificationRef)
    assert (
        cycle.BillCycleSpecification.description == "Bills on the first of every month"
    )
    assert cycle.BillCycleSpecification._referred_type == "BillCycleSpecification"


def test_applied_customer_billing_rate_characteristic_and_tax_href(
    applied_customer_billing_rate_dict,
):
    rate = AppliedCustomerBillingRate.from_dict(applied_customer_billing_rate_dict)

    assert isinstance(rate, AppliedCustomerBillingRate)
    assert (
        rate.appliedBillingRateType
        is AppliedCustomerBillingRateType.PRODUCT_RECURRING_CHARGE
    )
    assert rate.isBilled is True
    assert isinstance(rate.bill, CustomerBillRef)

    tax = rate.appliedTax[0]
    assert isinstance(tax, AppliedBillingTaxRate)
    assert tax.taxCategory is TaxCategory.VAT
    assert (
        tax.href
        == "https://mycsp.com/tmf-api/customerBill/v5/appliedBillingTaxRate/abtr-1"
    )

    characteristic = rate.characteristic[0]
    assert isinstance(characteristic, StringCharacteristic)
    assert isinstance(characteristic, Characteristic)
    assert characteristic.value == "Subscriptions"


def test_customer_bill_unknown_state_passes_through(customer_bill_dict):
    customer_bill_dict = dict(customer_bill_dict, state="disputed")
    bill = CustomerBill.from_dict(customer_bill_dict)

    assert bill.state == "disputed"
    assert bill.to_dict()["state"] == "disputed"


def test_customer_bill_tax_item_must_be_a_list():
    with pytest.raises(ValueError):
        CustomerBill(
            billNo="INV-2026-03",
            taxItem=TaxItem(taxCategory="VAT", taxRate=18.5),
        )


def test_customer_bill_resource_paths():
    context = Context(api_base_url="https://mycsp.com/tmf-api")

    assert (
        CustomerBill.get_resource_path(context)
        == "https://mycsp.com/tmf-api/customerBill/v5/customerBill"
    )
    assert (
        CustomerBillOnDemand.get_resource_path(context)
        == "https://mycsp.com/tmf-api/customerBill/v5/customerBillOnDemand"
    )
    assert (
        BillCycle.get_resource_path(context)
        == "https://mycsp.com/tmf-api/customerBill/v5/billCycle"
    )
    assert (
        AppliedCustomerBillingRate.get_resource_path(context)
        == "https://mycsp.com/tmf-api/customerBill/v5/appliedCustomerBillingRate"
    )


def test_customer_bill_to_dict_round_trip(customer_bill_dict):
    result = CustomerBill.from_dict(customer_bill_dict).to_dict()

    assert result["@type"] == "CustomerBill"
    assert "@baseType" not in result
    assert result["state"] == "sent"
    assert result["runType"] == "onCycle"
    assert result["billingAccount"]["@referredType"] == "BillingAccount"
    assert result["appliedPayment"][0]["payment"]["@referredType"] == "Payment"
    assert result["relatedParty"][0]["partyOrPartyRole"]["@type"] == "PartyRef"


def test_bill_cycle_to_dict_round_trip(bill_cycle_dict):
    result = BillCycle.from_dict(bill_cycle_dict).to_dict()

    assert result["@type"] == "BillCycle"
    assert result["BillCycleSpecification"]["@type"] == "BillCycleSpecificationRef"
    assert result["BillCycleSpecification"]["@referredType"] == "BillCycleSpecification"
