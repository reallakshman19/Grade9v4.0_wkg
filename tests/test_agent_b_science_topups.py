"""Independent synthetic calculations for proposed Agent B top-ups; not exam keys."""
from math import isclose, pi, sqrt


def test_inverse_lens_displacement_fresh_transfer():
    screen_distance_cm, separation_cm = 96.0, 48.0
    focal_cm = (screen_distance_cm ** 2 - separation_cm ** 2) / (4 * screen_distance_cm)
    near = (screen_distance_cm - separation_cm) / 2
    far = (screen_distance_cm + separation_cm) / 2
    assert isclose(focal_cm, 18.0)
    assert (near, far) == (24.0, 72.0)
    assert isclose((screen_distance_cm - near) / near, 3.0)
    assert isclose((screen_distance_cm - far) / far, 1 / 3)
    assert 70.0 < 4 * focal_cm  # Discriminant < 0; no real screen image.


def test_unequal_droplet_topup_volume_area_and_free_energy():
    r = 1e-3
    tension = 0.072
    actual_volume_cubes = 8 * (r ** 3) + (2 * r) ** 3
    final_radius = actual_volume_cubes ** (1 / 3)
    area_before = 4 * pi * (8 * r ** 2 + (2 * r) ** 2)
    area_after = 4 * pi * final_radius ** 2
    eliminated = area_before - area_after
    energy = tension * eliminated
    assert isclose(final_radius ** 3, 16 * r ** 3, rel_tol=1e-10)
    assert isclose(eliminated, 7.1004967641686e-5, rel_tol=1e-10)
    assert isclose(energy, 5.112357670201392e-6, rel_tol=1e-10)
    assert isclose(eliminated / area_before, 0.47086631601060025, rel_tol=1e-10)
    # Negative control: treating 8 small + 1 large as 9 identical violates mass conservation.
    wrong_radius = 9 ** (1 / 3) * r
    assert not isclose(wrong_radius ** 3, actual_volume_cubes, rel_tol=1e-4)


def test_scandium_ionization_order_not_aufbau_reverse():
    # Isolated ions in their standard low-energy configurations.
    neutral = {"3d": 1, "4s": 2}
    doubly_ionized = {"3d": 1, "4s": 0}
    triply_ionized = {"3d": 0, "4s": 0}
    assert [x["3d"] for x in (neutral, doubly_ionized, triply_ionized)] == [1, 1, 0]
    assert neutral["4s"] - doubly_ionized["4s"] == 2
    assert doubly_ionized["3d"] - triply_ionized["3d"] == 1
