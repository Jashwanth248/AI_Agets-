from geo_toolkit import compare_claimed_distance, haversine_distance_km, validate_coordinates


def test_coordinate_validation():
    assert validate_coordinates(45, -123)["is_valid"] is True
    assert validate_coordinates(120, 0)["is_valid"] is False


def test_haversine_paris_london():
    result = haversine_distance_km(48.8566, 2.3522, 51.5074, -0.1278)
    assert 340 <= result["distance_km"] <= 350


def test_compare_distance_claim():
    result = compare_claimed_distance(48.8566, 2.3522, 51.5074, -0.1278, 900)
    assert result["verdict"] == "Inaccurate"
