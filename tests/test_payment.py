import pytest
from tmforum import (
    AccountRef,
    ChannelRef,
    Context,
    EntityRef,
    Money,
    Payment,
    PaymentItem,
    PaymentMethod,
    PaymentMethodRefOrValue,
    PaymentRef,
    PaymentStatus,
    Refund,
    RelatedParty,
    TimePeriod,
)


@pytest.fixture
def payment_dict():
    return {
        "@type": "Payment",
        "id": "pay-8821",
        "href": "https://mycsp.com/tmf-api/payment/v4/payment/pay-8821",
        "name": "March invoice settlement",
        "description": "Settlement of invoice INV-2026-03 by stored card",
        "authorizationCode": "AUTH-77201",
        "correlatorId": "corr-5f3a",
        "paymentDate": "2026-03-14T09:12:00.000Z",
        "status": "captured",
        "statusDate": "2026-03-14T09:12:04.000Z",
        "account": {
            "@type": "AccountRef",
            "id": "acc-341",
            "href": "https://mycsp.com/tmf-api/accountManagement/v5/billingAccount/acc-341",
            "name": "Jane Doe billing account",
            "description": "Primary postpaid billing account",
            "@referredType": "BillingAccount",
        },
        "amount": {"@type": "Money", "unit": "EUR", "value": 118.5},
        "taxAmount": {"@type": "Money", "unit": "EUR", "value": 18.5},
        "totalAmount": {"@type": "Money", "unit": "EUR", "value": 118.5},
        "channel": {
            "@type": "ChannelRef",
            "id": "chan-web",
            "name": "Self-care portal",
            "@referredType": "Channel",
        },
        "payer": {
            "@type": "RelatedParty",
            "id": "party-99",
            "href": "https://mycsp.com/tmf-api/partyManagement/v5/individual/party-99",
            "name": "Jane Doe",
            "role": "payer",
        },
        "paymentItem": [
            {
                "@type": "PaymentItem",
                "id": "pi-1",
                "amount": {"@type": "Money", "unit": "EUR", "value": 100.0},
                "taxAmount": {"@type": "Money", "unit": "EUR", "value": 18.5},
                "totalAmount": {"@type": "Money", "unit": "EUR", "value": 118.5},
                "item": {
                    "@type": "EntityRef",
                    "id": "bill-2026-03",
                    "href": "https://mycsp.com/tmf-api/customerBill/v5/customerBill/bill-2026-03",
                    "name": "Invoice INV-2026-03",
                    "@referredType": "CustomerBill",
                },
            }
        ],
        "paymentMethod": {
            "@type": "PaymentMethodRefOrValue",
            "@baseType": "PaymentMethod",
            "id": "pm-55",
            "href": "https://mycsp.com/tmf-api/paymentMethod/v4/paymentMethod/pm-55",
            "name": "Visa ending 4242",
            "description": "Stored bank card",
            "status": "active",
            "statusDate": "2026-01-05T10:00:00.000Z",
            "isPreferred": True,
            "@referredType": "BankCard",
            "validFor": {
                "@type": "TimePeriod",
                "startDateTime": "2026-01-05T00:00:00.000Z",
                "endDateTime": "2029-01-31T23:59:59.000Z",
            },
            "relatedParty": {
                "@type": "RelatedParty",
                "id": "party-99",
                "name": "Jane Doe",
                "role": "owner",
            },
            "account": [
                {
                    "@type": "AccountRef",
                    "id": "acc-341",
                    "name": "Jane Doe billing account",
                    "@referredType": "BillingAccount",
                }
            ],
        },
    }


@pytest.fixture
def refund_dict():
    return {
        "@type": "Refund",
        "id": "ref-104",
        "href": "https://mycsp.com/tmf-api/payment/v4/refund/ref-104",
        "name": "Goodwill refund",
        "description": "Refund of duplicated March settlement",
        "authorizationCode": "AUTH-77455",
        "correlatorId": "corr-9b11",
        "refundDate": "2026-03-20T16:40:00.000Z",
        "status": "done",
        "statusDate": "2026-03-20T16:41:12.000Z",
        "account": {
            "@type": "AccountRef",
            "id": "acc-341",
            "name": "Jane Doe billing account",
            "@referredType": "BillingAccount",
        },
        "amount": {"@type": "Money", "unit": "EUR", "value": 118.5},
        "taxAmount": {"@type": "Money", "unit": "EUR", "value": 18.5},
        "totalAmount": {"@type": "Money", "unit": "EUR", "value": 118.5},
        "channel": {
            "@type": "ChannelRef",
            "id": "chan-callcenter",
            "name": "Call centre",
            "@referredType": "Channel",
        },
        "payment": {
            "@type": "PaymentRef",
            "id": "pay-8821",
            "href": "https://mycsp.com/tmf-api/payment/v4/payment/pay-8821",
            "name": "March invoice settlement",
            "@referredType": "Payment",
        },
        "requestor": {
            "@type": "RelatedParty",
            "id": "agent-12",
            "name": "Care agent 12",
            "role": "requestor",
        },
        "paymentMethod": {
            "@type": "PaymentMethodRefOrValue",
            "@baseType": "PaymentMethod",
            "id": "pm-55",
            "name": "Visa ending 4242",
            "@referredType": "BankCard",
        },
    }


def test_payment_from_dict_nested_types(payment_dict):
    payment = Payment.from_dict(payment_dict)

    assert isinstance(payment, Payment)
    assert payment.id == "pay-8821"
    assert payment.authorizationCode == "AUTH-77201"
    assert payment.correlatorId == "corr-5f3a"
    assert payment.paymentDate == "2026-03-14T09:12:00.000Z"
    assert payment.status == PaymentStatus.CAPTURED

    assert isinstance(payment.account, AccountRef)
    assert payment.account._referred_type == "BillingAccount"
    assert payment.account.description == "Primary postpaid billing account"

    assert isinstance(payment.amount, Money)
    assert payment.amount.value == 118.5
    assert isinstance(payment.taxAmount, Money)
    assert isinstance(payment.totalAmount, Money)
    assert isinstance(payment.channel, ChannelRef)
    assert isinstance(payment.payer, RelatedParty)
    assert payment.payer.role == "payer"

    assert len(payment.paymentItem) == 1
    item = payment.paymentItem[0]
    assert isinstance(item, PaymentItem)
    assert isinstance(item.item, EntityRef)
    assert item.item._referred_type == "CustomerBill"
    assert isinstance(item.amount, Money)
    assert isinstance(item.totalAmount, Money)

    method = payment.paymentMethod
    assert isinstance(method, PaymentMethodRefOrValue)
    assert isinstance(method, PaymentMethod)
    assert method._referred_type == "BankCard"
    assert method.isPreferred is True
    assert isinstance(method.validFor, TimePeriod)
    assert isinstance(method.relatedParty, RelatedParty)
    assert isinstance(method.account[0], AccountRef)


def test_refund_from_dict_nested_types(refund_dict):
    refund = Refund.from_dict(refund_dict)

    assert isinstance(refund, Refund)
    assert refund.refundDate == "2026-03-20T16:40:00.000Z"
    assert refund.status == PaymentStatus.DONE
    assert isinstance(refund.account, AccountRef)
    assert isinstance(refund.amount, Money)
    assert isinstance(refund.channel, ChannelRef)
    assert isinstance(refund.payment, PaymentRef)
    assert refund.payment._referred_type == "Payment"
    assert isinstance(refund.requestor, RelatedParty)
    assert refund.requestor.role == "requestor"
    assert isinstance(refund.paymentMethod, PaymentMethodRefOrValue)


def test_payment_status_covers_transaction_and_account_values():
    assert PaymentStatus("pendingAuthorization") is PaymentStatus.PENDING_AUTHORIZATION
    assert PaymentStatus("denied") is PaymentStatus.DENIED
    assert PaymentStatus("due") is PaymentStatus.DUE


def test_payment_unknown_status_passes_through(payment_dict):
    payment_dict = dict(payment_dict, status="settledOffline")
    payment = Payment.from_dict(payment_dict)

    assert payment.status == "settledOffline"
    assert payment.to_dict()["status"] == "settledOffline"


def test_payment_item_must_be_a_list(payment_dict):
    with pytest.raises(ValueError):
        Payment(
            name="Bad payment",
            paymentItem=PaymentItem(id="pi-1"),
        )


def test_payment_resource_path_is_v4():
    context = Context(api_base_url="https://mycsp.com/tmf-api")
    assert (
        Payment.get_resource_path(context)
        == "https://mycsp.com/tmf-api/payment/v4/payment"
    )


def test_refund_resource_path_is_v4():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")
    assert (
        Refund.get_resource_path(context)
        == "https://mycsp.com:8080/tmf-api/payment/v4/refund"
    )


def test_payment_to_dict_round_trip(payment_dict):
    result = Payment.from_dict(payment_dict).to_dict()

    assert result["@type"] == "Payment"
    assert "@baseType" not in result
    assert result["status"] == "captured"
    assert result["account"]["@referredType"] == "BillingAccount"
    assert result["payer"]["role"] == "payer"

    item_dict = result["paymentItem"][0]
    assert item_dict["@type"] == "PaymentItem"
    assert item_dict["item"]["@referredType"] == "CustomerBill"
    assert item_dict["totalAmount"]["value"] == 118.5

    method_dict = result["paymentMethod"]
    assert method_dict["@type"] == "PaymentMethodRefOrValue"
    assert method_dict["@baseType"] == "PaymentMethod"
    assert method_dict["@referredType"] == "BankCard"
    assert method_dict["isPreferred"] is True
    assert method_dict["account"][0]["@type"] == "AccountRef"

    assert Payment.from_dict(result).to_dict() == result


def test_refund_to_dict_round_trip(refund_dict):
    result = Refund.from_dict(refund_dict).to_dict()

    assert result["@type"] == "Refund"
    assert "@baseType" not in result
    assert result["status"] == "done"
    assert result["payment"]["@referredType"] == "Payment"
    assert result["paymentMethod"]["@baseType"] == "PaymentMethod"

    assert Refund.from_dict(result).to_dict() == result
