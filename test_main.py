import pytest
from fastapi.testclient import TestClient

from main import app, hitung_subnet

client = TestClient(app)


# ==========================================
# Unit Tests: hitung_subnet
# ==========================================


@pytest.mark.parametrize(
    "case_id,ip,prefix,expected",
    [
        (
            "TC-01",
            "172.16.5.130",
            25,
            {
                "mask": "255.255.255.128",
                "network": "172.16.5.128",
                "broadcast": "172.16.5.255",
                "first_host": "172.16.5.129",
                "last_host": "172.16.5.254",
                "usable_hosts": 126,
            },
        ),
        (
            "TC-02",
            "10.0.0.0",
            30,
            {
                "mask": "255.255.255.252",
                "network": "10.0.0.0",
                "broadcast": "10.0.0.3",
                "first_host": "10.0.0.1",
                "last_host": "10.0.0.2",
                "usable_hosts": 2,
            },
        ),
        (
            "TC-03",
            "192.168.1.0",
            31,
            {
                "mask": "255.255.255.254",
                "network": "192.168.1.0",
                "broadcast": None,
                "first_host": "192.168.1.0",
                "last_host": "192.168.1.1",
                "usable_hosts": 2,
            },
        ),
        (
            "TC-04",
            "192.168.1.5",
            32,
            {
                "mask": "255.255.255.255",
                "network": "192.168.1.5",
                "broadcast": None,
                "first_host": "192.168.1.5",
                "last_host": "192.168.1.5",
                "usable_hosts": 1,
            },
        ),
        (
            "TC-05",
            "0.0.0.0",
            0,
            {
                "mask": "0.0.0.0",
                "network": "0.0.0.0",
                "broadcast": "255.255.255.255",
                "first_host": "0.0.0.1",
                "last_host": "255.255.255.254",
                "usable_hosts": 4294967294,
            },
        ),
    ],
)
def test_hitung_subnet_success(case_id, ip, prefix, expected):
    result = hitung_subnet(ip, prefix)
    assert result == expected


@pytest.mark.parametrize(
    "case_id,ip,prefix",
    [
        ("TC-06", "256.1.1.1", 24),
        ("TC-07", "192.168.01.1", 24),
        ("TC-08", "192.168.1", 24),
        ("TC-09", "abc", 24),
        ("TC-10a", "", 24),
        ("TC-10b", " 192.168.1.1", 24),
        ("TC-10c", "192.168.1.1 ", 24),
        ("TC-11", "192.168.1.1", 33),
        ("TC-12", "192.168.1.1", -1),
        ("BOOL-PREFIX-TRUE", "192.168.1.1", True),
        ("BOOL-PREFIX-FALSE", "192.168.1.1", False),
        ("NON-STR-IP", 19216811, 24),
    ],
)
def test_hitung_subnet_invalid(case_id, ip, prefix):
    with pytest.raises(ValueError):
        hitung_subnet(ip, prefix)


# ==========================================
# Integration / API Tests: FastAPI Endpoints
# ==========================================


def test_api_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.parametrize(
    "case_id,ip,prefix,expected",
    [
        (
            "TC-01",
            "172.16.5.130",
            25,
            {
                "mask": "255.255.255.128",
                "network": "172.16.5.128",
                "broadcast": "172.16.5.255",
                "first_host": "172.16.5.129",
                "last_host": "172.16.5.254",
                "usable_hosts": 126,
            },
        ),
        (
            "TC-02",
            "10.0.0.0",
            30,
            {
                "mask": "255.255.255.252",
                "network": "10.0.0.0",
                "broadcast": "10.0.0.3",
                "first_host": "10.0.0.1",
                "last_host": "10.0.0.2",
                "usable_hosts": 2,
            },
        ),
        (
            "TC-03",
            "192.168.1.0",
            31,
            {
                "mask": "255.255.255.254",
                "network": "192.168.1.0",
                "broadcast": None,
                "first_host": "192.168.1.0",
                "last_host": "192.168.1.1",
                "usable_hosts": 2,
            },
        ),
        (
            "TC-04",
            "192.168.1.5",
            32,
            {
                "mask": "255.255.255.255",
                "network": "192.168.1.5",
                "broadcast": None,
                "first_host": "192.168.1.5",
                "last_host": "192.168.1.5",
                "usable_hosts": 1,
            },
        ),
        (
            "TC-05",
            "0.0.0.0",
            0,
            {
                "mask": "0.0.0.0",
                "network": "0.0.0.0",
                "broadcast": "255.255.255.255",
                "first_host": "0.0.0.1",
                "last_host": "255.255.255.254",
                "usable_hosts": 4294967294,
            },
        ),
    ],
)
def test_api_subnet_success(case_id, ip, prefix, expected):
    response = client.get("/api/subnet", params={"ip": ip, "prefix": prefix})
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize(
    "case_id,params",
    [
        ("TC-06", {"ip": "256.1.1.1", "prefix": 24}),
        ("TC-07", {"ip": "192.168.01.1", "prefix": 24}),
        ("TC-08", {"ip": "192.168.1", "prefix": 24}),
        ("TC-09", {"ip": "abc", "prefix": 24}),
        ("TC-10a", {"ip": "", "prefix": 24}),
        ("TC-10b", {"ip": " 192.168.1.1", "prefix": 24}),
        ("TC-10c", {"ip": "192.168.1.1 ", "prefix": 24}),
        ("TC-11", {"ip": "192.168.1.1", "prefix": 33}),
        ("TC-12", {"ip": "192.168.1.1", "prefix": -1}),
        ("PREFIX-NON-INT", {"ip": "192.168.1.1", "prefix": "abc"}),
        ("PREFIX-EMPTY", {"ip": "192.168.1.1", "prefix": ""}),
        ("MISSING-IP", {"prefix": 24}),
        ("MISSING-PREFIX", {"ip": "192.168.1.1"}),
    ],
)
def test_api_subnet_invalid(case_id, params):
    response = client.get("/api/subnet", params=params)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
