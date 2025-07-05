# Looking-Glass-MCP

The first Looking Glass Model Context Protocol (MCP) server! 🎉

## Overview

Looking-Glass-MCP is a revolutionary MCP server that provides network probing capabilities through Looking Glass (LG) vantage points. This tool allows you to perform network diagnostics and measurements from multiple global locations using a simple, standardized interface.

## Features

- **Multi-VP Probing**: Execute network commands from multiple Looking Glass vantage points simultaneously
- **Auto VP Selection**: Automatically select the optimal number of vantage points for your measurements
- **Comprehensive Commands**: Support for ping, BGP route lookups, and traceroute operations
- **Global Coverage**: Access to Looking Glass servers worldwide
- **Async Operations**: Built with async/await for efficient concurrent operations
- **Error Handling**: Robust error handling and timeout management

## Available Tools

### `lg_probing_user_defined`
Send probing commands to a target IP using a specific list of LG vantage points.

**Parameters:**
- `vp_id_list`: List of Looking Glass VP identifiers
- `cmd`: Command type (`ping`, `show ip bgp`, `traceroute`)
- `target_ip`: Destination IP address for probing

### `lg_probing_auto_select`
Send probing commands using automatically selected vantage points.

**Parameters:**
- `vp_num`: Number of vantage points to use
- `cmd`: Command type (`ping`, `bgp`, `traceroute`)
- `target_ip`: Destination IP address for probing

### `list_all_lgs`
Retrieve information about all available Looking Glass vantage points.

## Requirements

- Python 3.13+
- httpx >= 0.28.1
- mcp[cli] >= 1.9.4

## Installation