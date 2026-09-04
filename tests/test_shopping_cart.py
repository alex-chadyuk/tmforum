import pytest
from tmforum import (
    CartItem,
    CartItemActionType,
    CartItemRelationship,
    CartItemStatusType,
    CartPrice,
    CartTerm,
    ContactMedium,
    Context,
    Duration,
    EmailContactMedium,
    Money,
    Note,
    Price,
    PriceAlteration,
    PriceType,
    ProductOfferingPriceRef,
    ProductOfferingRef,
    ProductRef,
    RecurringChargePeriod,
    RelatedPartyOrPartyRole,
    ShoppingCart,
    TimePeriod,
)


@pytest.fixture
def shopping_cart_dict():
    return {
        "@type": "ShoppingCart",
        "@baseType": "Entity",
        "id": "cart-4417",
        "href": "https://mycsp.com/tmf-api/shoppingCart/v5/shoppingCart/cart-4417",
        "creationDate": "2026-06-02T09:15:00.000Z",
        "lastUpdate": "2026-06-02T09:42:11.000Z",
        "validFor": {
            "startDateTime": "2026-06-02T09:15:00.000Z",
            "endDateTime": "2026-06-03T09:15:00.000Z",
        },
        "contactMedium": [
            {
                "@type": "EmailContactMedium",
                "id": "cm-1",
                "contactType": "email",
                "preferred": True,
                "emailAddress": "jan.novak@example.com",
            }
        ],
        "relatedParty": [
            {
                "@type": "RelatedPartyOrPartyRole",
                "id": "rp-1",
                "role": "customer",
                "partyOrPartyRole": {
                    "@type": "PartyRef",
                    "id": "party-77",
                    "name": "Jan Novak",
                    "@referredType": "Individual",
                },
            }
        ],
        "cartItem": [
            {
                "@type": "CartItem",
                "id": "01",
                "action": "add",
                "status": "active",
                "quantity": 2,
                "productOffering": {
                    "@type": "ProductOfferingRef",
                    "id": "po-500",
                    "name": "Mobile broadband 50GB",
                    "@referredType": "ProductOffering",
                },
                "product": {
                    "@type": "ProductRef",
                    "id": "prod-900",
                    "name": "Existing broadband line",
                    "@referredType": "Product",
                },
                "itemTerm": [
                    {
                        "@type": "CartTerm",
                        "name": "24 month contract",
                        "description": "Minimum contract duration",
                        "duration": {"units": "month", "amount": 24},
                    }
                ],
                "note": [
                    {
                        "@type": "Note",
                        "id": "note-1",
                        "author": "agent-12",
                        "date": "2026-06-02T09:20:00.000Z",
                        "text": "Customer asked for delivery to the office",
                    }
                ],
                "itemPrice": [
                    {
                        "@type": "CartPrice",
                        "name": "Monthly subscription",
                        "description": "Recurring charge for the mobile plan",
                        "priceType": "recurringCharge",
                        "recurringChargePeriod": "monthly",
                        "unitOfMeasure": "GB",
                        "productOfferingPrice": {
                            "@type": "ProductOfferingPriceRef",
                            "id": "pop-31",
                            "name": "Mobile broadband monthly",
                            "@referredType": "ProductOfferingPrice",
                        },
                        "price": {
                            "@type": "Price",
                            "taxRate": 21.0,
                            "dutyFreeAmount": {"unit": "EUR", "value": 20.0},
                            "taxIncludedAmount": {"unit": "EUR", "value": 24.2},
                        },
                        "priceAlteration": [
                            {
                                "@type": "PriceAlteration",
                                "id": "alt-1",
                                "name": "Welcome discount",
                                "priceType": "discount",
                                "applicationDuration": 3,
                                "priority": 1,
                                "price": {
                                    "@type": "Price",
                                    "percentage": 25.0,
                                },
                            }
                        ],
                    }
                ],
                "itemTotalPrice": [
                    {
                        "@type": "CartPrice",
                        "name": "Cart item total",
                        "priceType": "recurringCharge",
                        "price": {
                            "@type": "Price",
                            "taxIncludedAmount": {"unit": "EUR", "value": 48.4},
                        },
                    }
                ],
                "cartItemRelationship": [
                    {
                        "@type": "CartItemRelationship",
                        "id": "02",
                        "relationshipType": "shipping",
                    }
                ],
                "cartItem": [
                    {
                        "@type": "CartItem",
                        "id": "01.1",
                        "action": "add",
                        "quantity": 1,
                        "productOffering": {
                            "@type": "ProductOfferingRef",
                            "id": "po-501",
                            "name": "SIM card",
                            "@referredType": "ProductOffering",
                        },
                    }
                ],
            },
            {
                "@type": "CartItem",
                "id": "02",
                "action": "noChange",
                "status": "saveForLater",
                "quantity": 1,
                "productOffering": {
                    "@type": "ProductOfferingRef",
                    "id": "po-620",
                    "name": "Handset insurance",
                    "@referredType": "ProductOffering",
                },
            },
        ],
        "cartTotalPrice": [
            {
                "@type": "CartPrice",
                "name": "Cart total",
                "priceType": "recurringCharge",
                "recurringChargePeriod": "monthly",
                "price": {
                    "@type": "Price",
                    "taxIncludedAmount": {"unit": "EUR", "value": 48.4},
                },
            }
        ],
    }


@pytest.fixture
def shopping_cart_1(shopping_cart_dict):
    return ShoppingCart.from_dict(shopping_cart_dict)


def test_shopping_cart_instantiates_with_id(shopping_cart_dict):
    cart = ShoppingCart.from_dict(shopping_cart_dict)

    assert cart.id == "cart-4417"
    assert cart.creationDate == "2026-06-02T09:15:00.000Z"
    assert cart.lastUpdate == "2026-06-02T09:42:11.000Z"
    assert cart.href.endswith("/shoppingCart/cart-4417")


def test_shopping_cart_instantiates_classes(shopping_cart_1):
    cart = shopping_cart_1

    assert isinstance(cart, ShoppingCart)
    assert isinstance(cart.validFor, TimePeriod)
    assert cart.validFor.startDateTime == "2026-06-02T09:15:00.000Z"

    assert isinstance(cart.contactMedium[0], ContactMedium)
    assert isinstance(cart.contactMedium[0], EmailContactMedium)
    assert cart.contactMedium[0].emailAddress == "jan.novak@example.com"

    assert isinstance(cart.relatedParty[0], RelatedPartyOrPartyRole)
    assert cart.relatedParty[0].partyOrPartyRole.id == "party-77"
    assert cart.relatedParty[0].partyOrPartyRole._referred_type == "Individual"

    assert isinstance(cart.cartTotalPrice[0], CartPrice)
    assert cart.cartTotalPrice[0].priceType is PriceType.RECURRING_CHARGE
    assert cart.cartTotalPrice[0].recurringChargePeriod is RecurringChargePeriod.MONTHLY
    assert isinstance(cart.cartTotalPrice[0].price, Price)
    assert isinstance(cart.cartTotalPrice[0].price.taxIncludedAmount, Money)
    assert cart.cartTotalPrice[0].price.taxIncludedAmount.value == 48.4


def test_shopping_cart_instantiates_cart_items(shopping_cart_1):
    item = shopping_cart_1.cartItem[0]

    assert isinstance(item, CartItem)
    assert item.id == "01"
    assert item.quantity == 2
    assert item.action is CartItemActionType.ADD
    assert item.status is CartItemStatusType.ACTIVE

    assert isinstance(item.productOffering, ProductOfferingRef)
    assert item.productOffering._referred_type == "ProductOffering"
    assert isinstance(item.product, ProductRef)
    assert item.product.id == "prod-900"

    assert isinstance(item.itemTerm[0], CartTerm)
    assert isinstance(item.itemTerm[0].duration, Duration)
    assert item.itemTerm[0].duration.amount == 24
    assert item.itemTerm[0].duration.units == "month"

    assert isinstance(item.note[0], Note)
    assert item.note[0].author == "agent-12"

    assert isinstance(item.itemPrice[0], CartPrice)
    assert item.itemPrice[0].unitOfMeasure == "GB"
    assert isinstance(item.itemPrice[0].productOfferingPrice, ProductOfferingPriceRef)
    assert isinstance(item.itemPrice[0].priceAlteration[0], PriceAlteration)
    assert item.itemPrice[0].priceAlteration[0].priceType is PriceType.DISCOUNT
    assert item.itemPrice[0].priceAlteration[0].applicationDuration == 3

    assert isinstance(item.itemTotalPrice[0], CartPrice)
    assert item.itemTotalPrice[0].price.taxIncludedAmount.value == 48.4

    assert isinstance(item.cartItemRelationship[0], CartItemRelationship)
    assert item.cartItemRelationship[0].id == "02"
    assert item.cartItemRelationship[0].relationshipType == "shipping"

    assert isinstance(item.cartItem[0], CartItem)
    assert item.cartItem[0].id == "01.1"
    assert item.cartItem[0].productOffering.id == "po-501"

    save_for_later = shopping_cart_1.cartItem[1]
    assert save_for_later.action is CartItemActionType.NO_CHANGE
    assert save_for_later.status is CartItemStatusType.SAVE_FOR_LATER


def test_shopping_cart_defaults_to_empty_lists():
    cart = ShoppingCart.from_dict({"@type": "ShoppingCart", "id": "cart-1"})

    assert cart.cartItem == []
    assert cart.cartTotalPrice == []
    assert cart.contactMedium == []
    assert cart.relatedParty == []
    assert cart.validFor is None


def test_cart_item_defaults_to_empty_lists():
    item = CartItem.from_dict({"@type": "CartItem", "id": "01"})

    assert item.itemTerm == []
    assert item.cartItem == []
    assert item.note == []
    assert item.itemPrice == []
    assert item.itemTotalPrice == []
    assert item.cartItemRelationship == []
    assert item.action is None
    assert item.status is None


def test_cart_price_non_enum_price_type_passes_through():
    """TMF663 types priceType/recurringChargePeriod as free strings.

    The SDK annotates them with its shared enums for consistency with every other
    price class; values outside those enums must survive a round trip untouched.
    """
    price = CartPrice.from_dict(
        {
            "@type": "CartPrice",
            "priceType": "allowance",
            "recurringChargePeriod": "week",
        }
    )

    assert price.priceType == "allowance"
    assert price.recurringChargePeriod == "week"
    assert price.to_dict()["priceType"] == "allowance"
    assert price.to_dict()["recurringChargePeriod"] == "week"


def test_cart_item_unknown_action_passes_through():
    item = CartItem.from_dict({"@type": "CartItem", "id": "01", "action": "replace"})

    assert item.action == "replace"
    assert item.to_dict()["action"] == "replace"


def test_shopping_cart_resource_path():
    context = Context(api_base_url="https://mycsp.com:8080/tmf-api")

    assert ShoppingCart.get_resource_path(context) == (
        "https://mycsp.com:8080/tmf-api/shoppingCart/v5/shoppingCart"
    )


def test_shopping_cart_to_dict_round_trip(shopping_cart_dict):
    result = ShoppingCart.from_dict(shopping_cart_dict).to_dict()

    assert result["@type"] == "ShoppingCart"
    assert "@baseType" not in result
    assert result["cartItem"][0]["@type"] == "CartItem"
    assert result["cartItem"][0]["action"] == "add"
    assert result["cartItem"][0]["itemPrice"][0]["@type"] == "CartPrice"
    assert result["cartTotalPrice"][0]["recurringChargePeriod"] == "monthly"
