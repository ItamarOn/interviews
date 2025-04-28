import json

class PolicyTypes:
    ARUPA = "Arupa"
    FRISCO = "Frisco"
    ALL = {ARUPA, FRISCO}

class PolicyAPI:
    def __init__(self) -> None:
        """ Initialize the API and define the in-memory storage for policies """
        self.policies = {}

    def create_policy(self, json_input: str) -> str:
        """ Create a new policy and return its unique id. Raises ValueError for invalid input """
        policy_data = json.loads(json_input)
        self._validate_policy_input(policy_data)
        if policy_data['type'] == PolicyTypes.ARUPA:
            self._raise_for_duplicate(policy_data['name'])
        policy_id = f'{len(self.policies) + 1}'  # Unique ID as Sequential number
        policy_data['id'] = policy_id
        self.policies[policy_id] = policy_data
        return json.dumps({'id': policy_id})

    def read_policy(self, json_identifier: str) -> str:
        policy_id = json.loads(json_identifier)['id']
        if policy_id not in self.policies:
            raise ValueError('Policy not found - cannot read')
        return json.dumps(self.policies[policy_id])

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        policy_id = json.loads(json_identifier)['id']
        updated_data = json.loads(json_input)
        self._validate_policy_input(updated_data)
        if policy_id not in self.policies:
            raise ValueError('Policy not found - cannot update')
        self.policies[policy_id].update(updated_data)

    def delete_policy(self, json_identifier: str) -> None:
        policy_id = json.loads(json_identifier)['id']
        if policy_id not in self.policies:
            raise ValueError('Policy not found - cannot delete')
        del self.policies[policy_id]

    def list_policies(self) -> str:
        return json.dumps(list(self.policies.values()))

    # Rule methods for Stage 2
    def create_rule(self, json_policy_identifier: str, json_rule_input: str) -> str:
        policy_id = json.loads(json_policy_identifier)['id']
        if policy_id not in self.policies:
            raise ValueError('Policy not found - cannot create rule')

        rule_data = json.loads(json_rule_input)
        self._validate_rule_input(policy_id, rule_data)

        if policy_id not in self.policies:
            raise ValueError('Policy not found')

        policy_rules = self.policies[policy_id].setdefault('rules', {})
        policy_data = self.policies[policy_id]

        if policy_data['type'] == PolicyTypes.ARUPA:
            if rule_data['name'] in [rule['name'] for rule in policy_rules.values()]:
                raise ValueError(f"Duplicate rule name for Arupa policy: {rule_data['name']}")

        rule_id = str(len(policy_rules) + 1)  # Unique rule ID
        rule_data['id'] = rule_id
        policy_rules[rule_id] = rule_data

        return json.dumps({'id': rule_id})

    def read_rule(self, json_identifier: str) -> str:
        rule_id = json.loads(json_identifier)['id']
        policy_id = json.loads(json_identifier)['policy_id']
        if policy_id not in self.policies or rule_id not in self.policies[policy_id].get('rules', {}):
            raise ValueError('Rule not found - cannot read')

        return json.dumps(self.policies[policy_id]['rules'][rule_id])

    def update_rule(self, json_identifier: str, json_rule_input: str) -> None:
        rule_id = json.loads(json_identifier)['id']
        policy_id = json.loads(json_identifier)['policy_id']
        if policy_id not in self.policies or rule_id not in self.policies[policy_id].get('rules', {}):
            raise ValueError('Rule not found - cannot update')

        updated_data = json.loads(json_rule_input)
        self._validate_rule_input(policy_id, updated_data)
        self.policies[policy_id]['rules'][rule_id].update(updated_data)

    def delete_rule(self, json_identifier: str) -> None:
        rule_id = json.loads(json_identifier)['id']
        policy_id = json.loads(json_identifier)['policy_id']
        if policy_id not in self.policies or rule_id not in self.policies[policy_id].get('rules', {}):
            raise ValueError('Rule not found - cannot delete')

        del self.policies[policy_id]['rules'][rule_id]

    def list_rules(self, json_policy_identifier: str) -> str:
        policy_id = json.loads(json_policy_identifier)['id']
        if policy_id not in self.policies:
            raise ValueError('Policy not found - cannot list rules')

        return json.dumps(list(self.policies[policy_id].get('rules', {}).values()))

    def _validate_rule_input(self, policy_id: str, rule: dict) -> None:
        # Validate Arupa rule input
        if policy_id in self.policies and self.policies[policy_id]['type'] == PolicyTypes.ARUPA:
            if not isinstance(rule.get('name'), str) or len(rule['name']) > 32:
                raise ValueError('Invalid rule name')
            if not isinstance(rule.get('ip_proto'), int) or not (0 <= rule['ip_proto'] <= 255):
                raise ValueError('Invalid IP protocol')
            if not isinstance(rule.get('source_port'), int) or not (0 <= rule['source_port'] <= 65535):
                raise ValueError('Invalid source port')
            if not isinstance(rule.get('source_subnet'), str):
                raise ValueError('Invalid source subnet')

        # Validate Frisco rule input
        elif policy_id in self.policies and self.policies[policy_id]['type'] == PolicyTypes.FRISCO:
            if not isinstance(rule.get('name'), str) or len(rule['name']) > 32:
                raise ValueError('Invalid rule name')
            if not isinstance(rule.get('ip_proto'), int) or not (0 <= rule['ip_proto'] <= 255):
                raise ValueError('Invalid IP protocol')
            if not isinstance(rule.get('source_port'), int) or not (0 <= rule['source_port'] <= 65535):
                raise ValueError('Invalid source port')
            if not isinstance(rule.get('source_ip'), str):
                raise ValueError('Invalid source IP address')
            if not isinstance(rule.get('destination_ip'), str):
                raise ValueError('Invalid destination IP address')
        else:
            raise ValueError('Invalid policy type for rule')

    @staticmethod
    def _validate_policy_input(policy: dict) -> None:
        # Validate the fields of the policy
        if not isinstance(policy.get('name'), str) or not policy['name'].isalnum() or len(policy['name']) > 32:
            raise ValueError('Invalid policy name')
        if not isinstance(policy.get('description'), str):
            raise ValueError('Invalid policy description')
        if policy.get('type') not in PolicyTypes.ALL:
            raise ValueError('Invalid policy type')

    def _raise_for_duplicate(self, policy_name: str) -> None:
        # if any(p["name"] == policy_name and p["type"] == PolicyTypes.ARUPA for p in self.policies.values()):
        if policy_name in [p["name"] for p in self.policies.values() if p["type"] == PolicyTypes.ARUPA]:
            raise ValueError("Duplicate name for Arupa policy")