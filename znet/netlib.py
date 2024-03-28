import znet.network_base.ipv4_local_cli as ipv4_cli
import znet.network_base.ipv4_local_getmac as ipv4_gm
import znet.network_base.ipv4_local_sock as ipv4_sock

import znet.network_base.router_ip as getaway

import znet.network_base.network_params as net_param

import znet.network_base.ip_from_domain as ip_domain
import znet.network_base.domain_from_ip as domain_ip
import znet.network_base.service_on_port as serv_port

import znet.network_base.my_public_ip as public_ip
import znet.network_base.ping_address as ping_addr
import znet.network_base.geolocation_ip as geo_ip
import znet.network_base.addr_from_geo as addr_geo


async def url_info(url: str) -> list:
	result = []
	result.append(f'Ping: {ping_addr.ping_addr(ip_domain.ip_from_domain(f"{url}"))}')
	result.append(f"Coords: {geo_ip.geo_ip(domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}')))}")
	result.append(f"Physical address by coordinates: {addr_geo.get_addr(geo_ip.geo_ip(domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}'))))}")
	result.append(f"IP address of {url}: {ip_domain.ip_from_domain(f'{url}')}")
	result.append(f"Domain name of {url} by IP: {domain_ip.domain_ip(ip_domain.ip_from_domain(f'{url}'))}")

	return result


async def port_info(port: int) -> str:
	return f'{port}: {serv_port.type_port(port)}'


async def check_network() -> list:
	result = []

	result.append(f'Local IPv4 CLI: {ipv4_cli.local_ipv4()}')
	result.append(f'Local IPv4 GM: {ipv4_gm.local_ipv4()}')
	result.append(f'Local IPv4 sock: {ipv4_sock.local_ipv4()}')
	result.append(f'Default Gateway IP: {getaway.router_ip()}')
	result.append(f'Default network interface settings: {net_param.network_param()}')
	result.append(f'Name of the service running on port 80: {serv_port.type_port(80)}')
	result.append(f'Public IP: {public_ip.public_ip()}')

	return result
