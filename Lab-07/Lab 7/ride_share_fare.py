import math


def parse_trip(text):
    """Parse 'cab:km' -> (Cab, km). Returns None on invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    cab = parts[0].strip().title()
    if not cab:
        return None
    try:
        km = float(parts[1])
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(km) or km < 0:
        return None
    return cab, km


def fare_average(fares_csv):
    """Average of comma-separated integer fares. Returns None on invalid input."""
    if not isinstance(fares_csv, str) or not fares_csv.strip():
        return None
    try:
        values = [int(r) for r in fares_csv.split(',')]
    except (ValueError, OverflowError):
        return None
    if any(v < 0 for v in values):
        return None
    return sum(values) // len(values)


def payable_fare(text):
    """Parse 'fare|promo' -> fare*1.18 - promo (min 0). Returns None on invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        fare = float(parts[0])
        promo = float(parts[1])
    except (ValueError, OverflowError):
        return None
    if not (math.isfinite(fare) and math.isfinite(promo)) or fare < 0 or promo < 0:
        return None
    total = fare * 1.18 - promo
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    result = parse_trip(user_input)
    print("Cab and Distance:", result if result is not None else "Invalid input")

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    result = fare_average(user_input)
    print("Average Fare:", result if result is not None else "Invalid input")

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    result = payable_fare(user_input)
    print("Payable Fare:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()