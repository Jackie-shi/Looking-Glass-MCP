from typing import Any, Union, List
import httpx

from mcp.server.fastmcp import FastMCP

from utils import parse_probing_result

# Initialize FastMCP server with extended timeout
mcp = FastMCP(
    name="LG_probing",
    # host="0.0.0.0",
    # port=63325,
    timeout=300  # 5 minutes timeout
)

@mcp.tool()
async def lg_probing_user_defined(vp_id_list: List[str], cmd: str, target_ip: str):
    """Send 'cmd' probing to target_ip using a list of LG VPs

    Args:
        vp_id_list: A list of LG VP ids
        cmd: ping, show ip bgp, traceroute
        target_ip: the probing destination IP address

    Return:
        result: Dict - key is the vp_id, value is the probing result
    """
    # Prepare the data for the HTTP request
    data = {
        'vp_id_list': vp_id_list,
        'cmd': cmd,
        'target_ip': target_ip
    }
    
    # Make asynchronous HTTP request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:44332/lg_probe",  # Assuming the probe API endpoint
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return parse_probing_result(result["data"], cmd=cmd)
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

@mcp.tool()
async def lg_probing_auto_select(vp_num: int, cmd: str, target_ip: str):
    """Send 'cmd' probing to target_ip using the number of VPs (auto select by platform)

    Args:
        vp_num: the number of required VPs
        cmd: ping, bgp, traceroute
        target_ip: the probing destination IP address

    Return:
        result: Dict - key is the vp_id, value is the probing result
    """
    # Prepare the data for the HTTP request
    data = {
        'vp_num': vp_num,
        'cmd': cmd,
        'target_ip': target_ip
    }
    
    # Make asynchronous HTTP request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:44332/lg_probe",  # Assuming the probe API endpoint
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return parse_probing_result(result["data"], cmd=cmd)
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

@mcp.tool()
async def list_all_lgs():
    """List all the LG VPs information

    Args:
    Returns:
        result: Dict
    """
    # Make asynchronous HTTP request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "http://localhost:44332/list_lg",  # Assuming the probe API endpoint
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')