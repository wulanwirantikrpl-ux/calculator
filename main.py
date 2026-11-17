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


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    raise NotImplementedError


@app.post("/api/vlsm")
def api_vlsm(request: Request):
    raise NotImplementedError

