#!/usr/bin/python3
import ipwhois
import whois
import socket


async def ipwhois_info(url: str) -> dict:
	"""Info about ip by whois api."""
	ip = socket.gethostbyname(url)
	results = ipwhois.IPWhois(ip).lookup_whois()
	
	return results


async def whois_info(url: str) -> list:
	"""Info about ip by whois module."""
	ip = socket.gethostbyname(url)
	results = whois.whois(ip)
	
	domain = f"Domain: {results['domain_name']}"
	registrar = f"Registrar: {results['registrar']}"
	creation_date = f"Creation date: {results['creation_date'].strftime('%d-%m-%Y %H:%M:%S')}"
	expiration_date = f"Expiration date: {results['expiration_date'].strftime('%d-%m-%Y %H:%M:%S')}"
	name_servers = f"Name servers: {results['name_servers']}"
	status = f"Status: {results['status']}"
	emails = f"Emails: {results['emails']}"
	org = f"Organization: {results['org']}"

	return [domain, registrar, creation_date, expiration_date, name_servers, status, emails, org]
