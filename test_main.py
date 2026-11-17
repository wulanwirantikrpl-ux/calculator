import pytest
from fastapi.testclient import TestClient

from main import alokasi_vlsm, app, hitung_subnet

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


# ==========================================
# Unit Tests: alokasi_vlsm
# ==========================================


@pytest.mark.parametrize(
    "case_id,network,kebutuhan,expected",
    [
        (
            "TC-13",
            "192.168.1.0/24",
            [20, 100, 2, 50],
            [
                {
                    "kebutuhan": 100,
                    "network_cidr": "192.168.1.0/25",
                    "mask": "255.255.255.128",
                    "network": "192.168.1.0",
                    "broadcast": "192.168.1.127",
                    "first_host": "192.168.1.1",
                    "last_host": "192.168.1.126",
                    "usable_hosts": 126,
                },
                {
                    "kebutuhan": 50,
                    "network_cidr": "192.168.1.128/26",
                    "mask": "255.255.255.192",
                    "network": "192.168.1.128",
                    "broadcast": "192.168.1.191",
                    "first_host": "192.168.1.129",
                    "last_host": "192.168.1.190",
                    "usable_hosts": 62,
                },
                {
                    "kebutuhan": 20,
                    "network_cidr": "192.168.1.192/27",
                    "mask": "255.255.255.224",
                    "network": "192.168.1.192",
                    "broadcast": "192.168.1.223",
                    "first_host": "192.168.1.193",
                    "last_host": "192.168.1.222",
                    "usable_hosts": 30,
                },
                {
                    "kebutuhan": 2,
                    "network_cidr": "192.168.1.224/30",
                    "mask": "255.255.255.252",
                    "network": "192.168.1.224",
                    "broadcast": "192.168.1.227",
                    "first_host": "192.168.1.225",
                    "last_host": "192.168.1.226",
                    "usable_hosts": 2,
                },
            ],
        ),
        (
            "TC-14",
            "192.168.1.0/24",
            [30],
            [
                {
                    "kebutuhan": 30,
                    "network_cidr": "192.168.1.0/27",
                    "mask": "255.255.255.224",
                    "network": "192.168.1.0",
                    "broadcast": "192.168.1.31",
                    "first_host": "192.168.1.1",
                    "last_host": "192.168.1.30",
                    "usable_hosts": 30,
                }
            ],
        ),
        (
            "TC-15",
            "192.168.1.0/24",
            [63],
            [
                {
                    "kebutuhan": 63,
                    "network_cidr": "192.168.1.0/25",
                    "mask": "255.255.255.128",
                    "network": "192.168.1.0",
                    "broadcast": "192.168.1.127",
                    "first_host": "192.168.1.1",
                    "last_host": "192.168.1.126",
                    "usable_hosts": 126,
                }
            ],
        ),
        (
            "TC-16",
            "192.168.1.0/24",
            [1],
            [
                {
                    "kebutuhan": 1,
                    "network_cidr": "192.168.1.0/30",
                    "mask": "255.255.255.252",
                    "network": "192.168.1.0",
                    "broadcast": "192.168.1.3",
                    "first_host": "192.168.1.1",
                    "last_host": "192.168.1.2",
                    "usable_hosts": 2,
                }
            ],
        ),
    ],
)
def test_alokasi_vlsm_success(case_id, network, kebutuhan, expected):
    result = alokasi_vlsm(network, kebutuhan)
    assert result == expected


@pytest.mark.parametrize(
    "case_id,network,kebutuhan",
    [
        ("TC-17", "192.168.1.0/24", [200, 100]),
        ("TC-18", "192.168.1.10/24", [10]),
        ("TC-19a", "192.168.1.0/24", []),
        ("TC-19b", "192.168.1.0/24", [10, 0]),
        ("TC-19c", "192.168.1.0/24", [-5]),
        ("INVALID-FORMAT-NO-SLASH", "192.168.1.0", [10]),
        ("INVALID-FORMAT-SPACE", "192.168.1.0 /24", [10]),
        ("INVALID-HOST-BOOL", "192.168.1.0/24", [10, True]),
        ("INVALID-HOST-TYPE", "192.168.1.0/24", ["sepuluh"]),
    ],
)
def test_alokasi_vlsm_invalid(case_id, network, kebutuhan):
    with pytest.raises(ValueError):
        alokasi_vlsm(network, kebutuhan)


# ==========================================
# Integration / API Tests: POST /api/vlsm
# ==========================================


def test_api_vlsm_success():
    payload = {
        "network": "192.168.1.0/24",
        "kebutuhan_host": [20, 100, 2, 50],
    }
    response = client.post("/api/vlsm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    assert data[0]["kebutuhan"] == 100
    assert data[0]["network_cidr"] == "192.168.1.0/25"
    assert data[1]["kebutuhan"] == 50
    assert data[1]["network_cidr"] == "192.168.1.128/26"
    assert data[2]["kebutuhan"] == 20
    assert data[2]["network_cidr"] == "192.168.1.192/27"
    assert data[3]["kebutuhan"] == 2
    assert data[3]["network_cidr"] == "192.168.1.224/30"


@pytest.mark.parametrize(
    "case_id,payload",
    [
        ("TC-17", {"network": "192.168.1.0/24", "kebutuhan_host": [200, 100]}),
        ("TC-18", {"network": "192.168.1.10/24", "kebutuhan_host": [10]}),
        ("TC-19a", {"network": "192.168.1.0/24", "kebutuhan_host": []}),
        ("TC-19b", {"network": "192.168.1.0/24", "kebutuhan_host": [10, 0]}),
        ("MISSING-NETWORK", {"kebutuhan_host": [10]}),
        ("MISSING-HOSTS", {"network": "192.168.1.0/24"}),
        ("INVALID-JSON", "not a json"),
    ],
)
def test_api_vlsm_invalid(case_id, payload):
    if isinstance(payload, str):
        response = client.post("/api/vlsm", content=payload, headers={"Content-Type": "application/json"})
    else:
        response = client.post("/api/vlsm", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

