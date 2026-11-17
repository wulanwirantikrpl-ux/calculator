import math
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Kalkulator Subnet & VLSM")


def validate_ip(ip: str) -> list[int]:
    if not isinstance(ip, str) or isinstance(ip, bool):
        raise ValueError("Alamat IP harus berupa string.")
    if " " in ip:
        raise ValueError("Alamat IP tidak boleh mengandung spasi.")
    octets = ip.split(".")
    if len(octets) != 4:
        raise ValueError("Alamat IP harus terdiri dari tepat 4 oktet.")

    parsed_octets = []
    for octet in octets:
        if not octet.isdigit():
            raise ValueError("Oktet IP hanya boleh berisi digit desimal.")
        if len(octet) > 1 and octet.startswith("0"):
            raise ValueError("Oktet IP tidak boleh diawali angka 0 (leading zero).")
        val = int(octet)
        if not (0 <= val <= 255):
            raise ValueError("Oktet IP harus berada dalam rentang 0-255.")
        parsed_octets.append(val)

    return parsed_octets


def validate_prefix(prefix: int) -> int:
    if isinstance(prefix, bool) or not isinstance(prefix, int):
        raise ValueError("Prefix harus berupa bilangan bulat (integer) dan bukan boolean.")
    if not (0 <= prefix <= 32):
        raise ValueError("Prefix harus berada pada rentang 0 hingga 32.")
    return prefix


def int_to_ip(n: int) -> str:
    return f"{(n >> 24) & 255}.{(n >> 16) & 255}.{(n >> 8) & 255}.{n & 255}"


def hitung_subnet(ip: str, prefix: int) -> dict:
    octets = validate_ip(ip)
    prefix = validate_prefix(prefix)

    ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]

    if prefix == 0:
        mask_int = 0
    else:
        mask_int = ((0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF)

    mask_str = int_to_ip(mask_int)
    # Operasi bitwise AND antara IP dan subnet mask
    network_int = ip_int & mask_int
    network_str = int_to_ip(network_int)

    if prefix <= 30:
        broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
        broadcast_str = int_to_ip(broadcast_int)
        first_host_int = network_int + 1
        last_host_int = broadcast_int - 1
        first_host_str = int_to_ip(first_host_int)
        last_host_str = int_to_ip(last_host_int)
        usable_hosts = (1 << (32 - prefix)) - 2
    elif prefix == 31:
        broadcast_str = None
        first_host_str = network_str
        last_host_str = int_to_ip(network_int + 1)
        usable_hosts = 2
    else:  # prefix == 32
        broadcast_str = None
        first_host_str = ip
        last_host_str = ip
        usable_hosts = 1

    return {
        "mask": mask_str,
        "network": network_str,
        "broadcast": broadcast_str,
        "first_host": first_host_str,
        "last_host": last_host_str,
        "usable_hosts": usable_hosts,
    }


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    if not isinstance(network_cidr, str) or isinstance(network_cidr, bool):
        raise ValueError("Network CIDR harus berupa string.")
    if " " in network_cidr:
        raise ValueError("Network CIDR tidak boleh mengandung spasi.")
    parts = network_cidr.split("/")
    if len(parts) != 2:
        raise ValueError("Network CIDR harus berformat <ip>/<prefix>.")
    ip_str, prefix_str = parts[0], parts[1]
    if not prefix_str.isdigit():
        raise ValueError("Prefix CIDR harus berupa bilangan bulat.")
    parent_prefix = int(prefix_str)
    validate_prefix(parent_prefix)
    parent_octets = validate_ip(ip_str)
    parent_ip_int = (parent_octets[0] << 24) | (parent_octets[1] << 16) | (parent_octets[2] << 8) | parent_octets[3]

    if parent_prefix == 0:
        parent_mask_int = 0
    else:
        parent_mask_int = ((0xFFFFFFFF << (32 - parent_prefix)) & 0xFFFFFFFF)

    parent_net_int = parent_ip_int & parent_mask_int
    if parent_ip_int != parent_net_int:
        raise ValueError(f"'{ip_str}' bukan merupakan Network Address yang valid untuk prefix /{parent_prefix}.")

    if not isinstance(kebutuhan_host, list) or len(kebutuhan_host) == 0:
        raise ValueError("Daftar kebutuhan host tidak boleh kosong.")

    for h in kebutuhan_host:
        if isinstance(h, bool) or not isinstance(h, int) or h < 1:
            raise ValueError("Setiap kebutuhan host harus berupa bilangan bulat >= 1.")

    if parent_prefix == 0:
        parent_broadcast_int = 0xFFFFFFFF
    else:
        parent_broadcast_int = parent_net_int | (~parent_mask_int & 0xFFFFFFFF)

    sorted_kebutuhan = sorted(kebutuhan_host, reverse=True)
    current_ip_int = parent_net_int
    results = []

    for kebutuhan in sorted_kebutuhan:
        needed = kebutuhan + 2
        ukuran_blok = 4
        while ukuran_blok < needed:
            ukuran_blok *= 2

        prefix_baru = 32 - int(math.log2(ukuran_blok))

        if current_ip_int + ukuran_blok - 1 > parent_broadcast_int:
            raise ValueError("Kapasitas jaringan induk tidak mencukupi untuk seluruh kebutuhan host.")

        current_ip_str = int_to_ip(current_ip_int)
        subnet_detail = hitung_subnet(current_ip_str, prefix_baru)

        results.append({
            "kebutuhan": kebutuhan,
            "network_cidr": f"{subnet_detail['network']}/{prefix_baru}",
            "mask": subnet_detail["mask"],
            "network": subnet_detail["network"],
            "broadcast": subnet_detail["broadcast"],
            "first_host": subnet_detail["first_host"],
            "last_host": subnet_detail["last_host"],
            "usable_hosts": subnet_detail["usable_hosts"],
        })

        current_ip_int += ukuran_blok

    return results


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/", response_class=HTMLResponse)
def get_root():
    index_file = Path(__file__).parent / "index.html"
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


@app.get("/api/subnet")
def api_subnet(request: Request):
    ip = request.query_params.get("ip")
    prefix_str = request.query_params.get("prefix")

    if ip is None:
        return JSONResponse(status_code=400, content={"detail": "Parameter 'ip' wajib diisi."})
    if prefix_str is None or prefix_str == "":
        return JSONResponse(status_code=400, content={"detail": "Parameter 'prefix' wajib diisi."})

    try:
        prefix = int(prefix_str)
    except (ValueError, TypeError):
        return JSONResponse(status_code=400, content={"detail": "Parameter 'prefix' harus berupa bilangan bulat."})

    try:
        result = hitung_subnet(ip, prefix)
        return JSONResponse(status_code=200, content=result)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})


@app.post("/api/vlsm")
async def api_vlsm(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"detail": "Payload body harus berupa JSON yang valid."})

    if not isinstance(body, dict):
        return JSONResponse(status_code=400, content={"detail": "Payload JSON harus berupa objek."})

    network = body.get("network")
    kebutuhan_host = body.get("kebutuhan_host")

    if network is None:
        return JSONResponse(status_code=400, content={"detail": "Field 'network' wajib diisi."})
    if kebutuhan_host is None:
        return JSONResponse(status_code=400, content={"detail": "Field 'kebutuhan_host' wajib diisi."})

    try:
        result = alokasi_vlsm(network, kebutuhan_host)
        return JSONResponse(status_code=200, content=result)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
