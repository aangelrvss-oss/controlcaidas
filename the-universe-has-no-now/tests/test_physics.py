"""Physics validation of the simulations used in the film."""
import os, sys, math, numpy as np, pytest
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "source", "render"))
os.environ.setdefault("LD_LIBRARY_PATH", "/root/lib")

def test_lorentz_simultaneity_values_on_screen():
    # S16: v = 0.55c, events at x = ±3 light-seconds, simultaneous in the rest frame
    v = 0.55; g = 1 / math.sqrt(1 - v * v)
    tA = g * (0 - v * (-3.0)); tB = g * (0 - v * 3.0)
    assert abs(tA - 1.976) < 0.01 and abs(tB + 1.976) < 0.01 and tB < tA

def test_light_clock_gamma():
    assert abs(1 / math.sqrt(1 - 0.36) - 1.25) < 1e-9

def test_gps_numbers():
    # Ashby 2003: velocity term ≈ -7.2 µs/day, gravitational term ≈ +45.7 µs/day
    c = 299792458.0; G = 6.674e-11; M = 5.972e24; R = 6.371e6; r = 2.6561e7
    v2 = G * M / r
    sr = -0.5 * v2 / c ** 2 * 86400e6
    gr = (G * M / c ** 2) * (1 / R - 1 / r) * 86400e6
    assert -7.6 < sr < -6.8 and 44 < gr < 47 and 37 < sr + gr < 40

def test_gravitational_time_dilation_33cm():
    g, c = 9.80, 299792458.0
    assert abs(g * 0.33 / c ** 2 - 3.6e-17) < 0.2e-17

def test_light_travel_times():
    c = 299792458.0
    assert abs(3.844e8 / c - 1.28) < 0.02
    assert abs(1.496e11 / c / 60 - 8.3) < 0.1
    assert abs(40075e3 / c * 7.48 - 1.0) < 0.01     # 7.48 laps per second
    assert 1e-19 < 1e-10 / c < 1e-18

@pytest.fixture(scope="module")
def table():
    from nonow import bh
    return bh.table()

def test_critical_impact_parameter(table):
    from nonow.bh import B_CRIT
    b = table.b; cap = table.captured
    i = np.argmax(~cap[b > 1.0]); bc = b[b > 1.0][i]
    assert abs(bc - B_CRIT) < 2e-3

def test_weak_field_deflection(table):
    # deflection for b = 40 M should be ≈ 4M/b (+ 15πM²/(4b²)) once the finite start radius is accounted for
    b = 40.0; j = np.argmin(abs(table.b - b))
    straight_sweep = math.pi - 2 * math.asin(b / table.R_far)
    deflection = table.phi_end[j] - straight_sweep
    expected = 4 / b + 15 * math.pi / (4 * b * b)
    assert abs(deflection - expected) < 0.01

def test_horizon_capture_and_escape(table):
    assert table.captured[np.argmin(abs(table.b - 2.0))]
    assert not table.captured[np.argmin(abs(table.b - 8.0))]

def test_shadow_diameter_matches_eht_scale():
    # 2 * 3*sqrt(3) GM/c^2 in units of r_s = 2GM/c^2
    assert abs(2 * 3 * math.sqrt(3) / 2 - 5.196) < 0.01

def test_redshift_factor_physical_range():
    # Keplerian disk at r = 8M: g between ~0.6 and ~1.6 across azimuth for an edge-on view
    r = 8.0; Om = r ** -1.5; Lz = np.linspace(-6, 6, 100) * 0.9
    g = math.sqrt(1 - 3 / r) / (1 - Om * Lz)
    assert g.min() > 0.5 and g.max() < 2.0

def test_hydrogen_orbital_sampling_normalisation():
    from nonow.scenes.orbital import sample_orbital
    pts = sample_orbital(1, 0, 0, 20000, np.random.default_rng(1))
    r = np.linalg.norm(pts, axis=1)
    # mean radius of the 1s state is 1.5 a0
    assert abs(r.mean() - 1.5) < 0.08

def test_point_mass_lens_einstein_ring():
    thetaE = 150.0
    th = np.array([thetaE, 2 * thetaE, 0.5 * thetaE])
    beta = th - thetaE ** 2 / th
    assert abs(beta[0]) < 1e-9 and beta[1] > 0 and beta[2] < 0
