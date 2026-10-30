from dc_fixture import format_price
from dc_fixture.price import format_price as direct_format_price

print(format_price(12.5, "EUR"))
print(direct_format_price(3, "USD"))
