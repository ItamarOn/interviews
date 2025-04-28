import re
from typing import List, Optional, Literal
from pydantic import BaseModel
from ipaddress import ip_network, IPv4Address


class PolicyTypes:
    ARUPA = 'Arupa'
    FRISCO = 'Frisco'


class Rule(BaseModel):
    id: str
    name: str
    ip_proto: int
    source_port: int
    source_subnet: Optional[str] = None  # For Arupa
    source_ip: Optional[str] = None  # For Frisco
    destination_ip: Optional[str] = None  # For Frisco

    def ip_subnet_validate(self, policy_type: PolicyTypes):
        if policy_type == PolicyTypes.ARUPA:
            if not self.source_subnet:
                raise ValueError('Arupa rules require a source_subnet')
            ip_network(self.source_subnet)
        elif policy_type == PolicyTypes.FRISCO:
            if not self.source_ip or not self.destination_ip:
                raise ValueError('Frisco rules require source_ip and destination_ip')
            IPv4Address(self.source_ip)
            IPv4Address(self.destination_ip)

    def name_in_policy_validate(self, policy, rules):
        if policy.type == PolicyTypes.ARUPA:
            if any(self.rules[r_id].name == self.name for r_id in policy.rules):
                raise ValueError("Duplicate rule name in Arupa policy")
        elif policy.type == PolicyTypes.FRISCO:
            if any(r.name == self.name for r in rules.values()):
                raise ValueError("Duplicate rule name globally for Frisco policy")

class Policy(BaseModel):
    id: str
    name: str
    description: str
    type: Literal[PolicyTypes.ARUPA, PolicyTypes.FRISCO]
    rules: Optional[List[str]] = None

    def name_validate(self, policies: dict):
        if not re.fullmatch(r'^[A-Za-z0-9_]{1,32}$', self.name):
            raise ValueError('Invalid policy name')
        if self.type == PolicyTypes.ARUPA:
            if self.name in [p['name'] for p in policies.values() if p['type'] == PolicyTypes.ARUPA]:
                raise ValueError('Duplicate name for Arupa policy')