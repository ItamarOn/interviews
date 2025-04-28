# As far as I understand, stage2 is a development of stage1 and is intended to replace it,
# so I did not use inheritance (class PolicyAPI2(PolicyAPI) and super() use)

import json
import uuid
import logging
from typing import Dict

from structures import Policy, Rule

logging.basicConfig(format='%(asctime)s %(message)s')


class PolicyAPI:
    def __init__(self) -> None:
        """ Initialize the API and define the in-memory storage for policies and rules """
        self.policies: Dict[str, Policy] = {}
        self.rules: Dict[str, Rule] = {}

    def create_policy(self, json_input: str) -> str:
        policy_data = json.loads(json_input)
        policy_data['rules'] = policy_data.get('rules', [])
        policy = Policy(**policy_data, id=f'P{uuid.uuid4()}')
        policy.name_validate(self.policies)

        self.policies[policy.id] = policy
        logging.info(f'Policy created: {policy.id}')
        return json.dumps({'id': policy.id})

    def read_policy(self, json_identifier: str) -> str:
        policy_id = self._get_policy_id_or_raise(json_identifier, 'read')
        logging.info(f'Read policy: {policy_id}')
        return json.dumps(self.policies[policy_id].__dict__)

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        policy_id = self._get_policy_id_or_raise(json_identifier, 'update')
        updated_data = json.loads(json_input)
        updated_policy = Policy(**updated_data, id=policy_id)
        updated_policy.name_validate(self.policies)
        logging.info(f'Policy updated: {policy_id}')
        self.policies[policy_id] = updated_policy

    def delete_policy(self, json_identifier: str) -> None:
        policy_id = self._get_policy_id_or_raise(json_identifier, 'delete')
        for rule_id in self.policies[policy_id].rules:
            logging.debug(f'{policy_id} rule deleted {rule_id}')
            del self.rules[rule_id]
        del self.policies[policy_id]
        logging.info(f'Policy deleted with all sub rules: {policy_id}')

    def list_policies(self) -> str:
        return json.dumps([policy.__dict__ for policy in self.policies.values()])

    def create_rule(self, json_policy_identifier: str, json_rule_input: str) -> str:
        policy_id = self._get_policy_id_or_raise(json_policy_identifier, 'create_rule')
        rule_data = json.loads(json_rule_input)
        policy = self.policies[policy_id]
        rule_id = f'R{uuid.uuid4()}'
        rule = Rule(id=rule_id, **rule_data)
        rule.ip_subnet_validate(policy.type)
        rule.name_in_policy_validate(policy, self.rules)
        self.rules[rule_id] = rule
        policy.rules.append(rule_id)
        logging.info(f'Policy updated: {policy_id} with new rule: {rule_id}')
        return json.dumps({'id': rule.id})

    def read_rule(self, json_identifier: str) -> str:
        rule_id = json.loads(json_identifier)['id']
        if rule_id not in self.rules:
            raise ValueError('Rule not found')
        return json.dumps(self.rules[rule_id].__dict__)

    def update_rule(self, json_identifier: str, json_rule_input: str) -> None:
        rule_id = json.loads(json_identifier)['id']
        if rule_id not in self.rules:
            raise ValueError('Rule not found')

        rule_data = json.loads(json_rule_input)
        policy_id = self._find_policy_containing_rule(rule_id)
        policy = self.policies[policy_id]

        updated_rule = Rule(id=rule_id, **rule_data)
        updated_rule.ip_subnet_validate(policy.type)
        logging.info(f'Rule updated: {rule_id}')
        self.rules[rule_id] = updated_rule

    def delete_rule(self, json_identifier: str) -> None:
        rule_id = json.loads(json_identifier)['id']
        if rule_id not in self.rules:
            raise ValueError('Rule not found')

        policy_id = self._find_policy_containing_rule(rule_id)
        policy = self.policies[policy_id]
        policy.rules.remove(rule_id)
        del self.rules[rule_id]
        logging.info(f'Rule deleted: {rule_id}')

    def list_rules(self, json_policy_identifier: str) -> str:
        policy_id = self._get_policy_id_or_raise(json_policy_identifier, 'list rules')
        return json.dumps([self.rules[rule_id].__dict__ for rule_id in self.policies[policy_id].rules])

    def _find_policy_containing_rule(self, rule_id: str) -> str:
        for policy_id, policy in self.policies.items():
            if rule_id in policy.rules:
                return policy_id
        raise ValueError('Rule not associated with any policy')

    def _get_policy_id_or_raise(self, json_identifier: str, action: str) -> str:
        policy_id = json.loads(json_identifier)['id']
        if policy_id not in self.policies:
            raise ValueError(f'Policy not found - cannot {action}')
        return policy_id

