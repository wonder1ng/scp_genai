import asyncio, platform, socket, sys, logging
# asyncio: 비동기 실행/프로세스 관리
# platform: OS 종류 판별
# socket: 네트워크 유틸
# sys: 시스템 관련 기능
# logging: 로그 출력
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-not-diag-server")

logger = logging.getLogger("simple-net-diag-server")

# @mcp.tool()
# async def fetch_page(host: str, port: int=80, path: str="/", max_bytes: int=100_000) -> dict:
#     """
#     간단한 페이지 GET(HTTP)을 통해 가져온 결과를 반환
#      - path는 기본 '/'이며 원하는 경로를 추가할 수도 있음
#      - max_bytes까지만 가져오며, 기본값은 100kb.
#     """
#     from urllib.parse import quote
#     from urllib.request import Request, urlopen
#     from urllib.error import URLError, HTTPError

#     url =f"http://{host}:{port}{quote(path)}"
#     req = Request(url, headers={"User-Agent": "simple-net-mcp/1.0"})

#     try:
#         with urlopen(req, timeout=10) as resp:
#             data = resp.read(max_bytes)
#     except Exception as e:
#         print(e)

@mcp.tool()
async def fetch_page(host: str, port: int=80, path: str="/", max_bytes: int=100_000) -> dict:
    """
    간단한 페이지 GET(HTTP)을 통해 가져온 결과를 반환
     - path는 기본 '/'이며 원하는 경로를 추가할 수도 있음
     - max_bytes까지만 가져오며, 기본값은 100kb.
    """
    from urllib.parse import quote
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

    url =f"http://{host}:{port}{quote(path)}"
    req = Request(url, headers={"User-Agent": "simple-net-mcp/1.0"})
    try:
        with urlopen(req, timeout=5) as resp:
            content_bytes = resp.read(max_bytes + 1)

            truncated = len(content_bytes) > max_bytes
            content_bytes = content_bytes[:max_bytes]

            charset = resp.headers.get_content_charset() or "utf-8"
            try:
                content = content_bytes.decode(charset, errors="replace")
            except Exception:
                content = content_bytes.decode("utf-8", errors="replace")

            return {
                "ok": True,
                "url": url,
                "status": resp.status,
                "headers": dict(resp.headers),
                "truncated": truncated,
                "content": content,
            }

    except HTTPError as e:
        return {
            "ok": False,
            "url": url,
            "error": "HTTPError",
            "status": e.code,
            "reason": str(e),
        }

    except URLError as e:
        return {
            "ok": False,
            "url": url,
            "error": "URLError",
            "reason": str(e),
        }

    except Exception as e:
        return {
            "ok": False,
            "url": url,
            "error": "Exception",
            "reason": repr(e),
        }


import asyncio, platform, socket, sys, logging
# asyncio: 비동기 실행/프로세스 관리
# platform: OS 종류 판별
# socket: 네트워크 유틸
# sys: 시스템 관련 기능
# logging: 로그 출력
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-not-diag-server")

logger = logging.getLogger("simple-net-diag-server")

@mcp.tool()
async def ping_host(host: str, count: int=3, timeout_sec: int=3) -> str:
    """
    지정한 host로 ping을 하며 결과를 반환합니다.  # 함수 설명 docstring: ping 실행 후 결과를 문자열로 반환
     - count: 1~5까지  # ping 요청 횟수 제한 설명 (실제 제한 검증 로직은 아래에는 없음)
     - timeout_sec: 1~5초 (패킷 당 타임아웃)  # 패킷 응답 대기 시간 제한 설명
    """

    host = (host or "").strip()
    if not host:
        raise ValueError("Host를 입력하세요.")

    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        raise ValueError(f"잘못된 호스트 이름: {host}")

    if not (1 <= count <= 5):
        raise ValueError("count는 1~5 사이여야 합니다.")
    if not (1 <= timeout_sec <= 5):
        raise ValueError("timeout_sec는 1~5 사이여야 합니다.")

    if platform.system() == "Windows":
        cmd = ["ping", "-n", str(count), "-w", str(timeout_sec * 1000), host]
    elif platform.system() == "Linux":
        cmd = ["ping", "-c", str(count), "-W", str(timeout_sec), host]
    else:  # macOS
        cmd = ["ping", "-c", str(count), "-t", str(timeout_sec), host]

    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, err = await proc.communicate()
    text = (out or err).decode("utf-8", "replace")

    if proc.returncode != 0:
        logger.error(f"Ping 실패: {text}")
        raise RuntimeError(f"Ping 실패: {text}")

    logger.info(f"Ping 성공: {text}")
    return text

if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 아래 코드 실행 (import 시 실행 방지)
    mcp.run(transport="stdio")  # MCP 서버 실행, stdio 기반 transport 사용 (입출력을 표준입출력으로 주고받는 방식, CLI/에이전트 연결용)