# Step 1 is the basic - and is done in a script-like manner.
# In step 2, where there is more data, I smoothed the information in a more robust manner (by pydantic and more).
import json
import uuid

class PolicyTypes:
    ARUPA = "Arupa"
    FRISCO = "Frisco"
    ALL = {ARUPA, FRISCO}

class PolicyAPI:
    def __init__(self) -> None:
        """ Initialize the API and define the in-memory storage for policies """
        self.policies = {}

    def create_policy(self, json_input: str) -> str:
        """ Create API - Create a new policy and return its unique id. Raises ValueError for invalid input """
        policy_data = json.loads(json_input)
        self._validate_policy_input(policy_data)
        policy_id = f'{uuid.uuid4()}'
        policy_data['id'] = policy_id
        self.policies[policy_id] = policy_data
        return json.dumps({'id': policy_id})

    def read_policy(self, json_identifier: str) -> str:
        """ Read API """
        policy_id = self._get_policy_id_or_raise(json_identifier, 'read')
        return json.dumps(self.policies[policy_id])

    def update_policy(self, json_identifier: str, json_input: str) -> None:
        """ Update API """
        policy_id = self._get_policy_id_or_raise(json_identifier, 'update')
        updated_data = json.loads(json_input)
        self._validate_policy_input(updated_data)
        self.policies[policy_id].update(updated_data)

    def delete_policy(self, json_identifier: str) -> None:
        """ Delete API """
        policy_id = self._get_policy_id_or_raise(json_identifier, 'delete')
        del self.policies[policy_id]

    def list_policies(self) -> str:
        """ List API """
        return json.dumps(list(self.policies.values()))

    def _validate_policy_input(self, policy: dict) -> None:
        """ Validate the fields of the policy - In use before creating or updating a policy """
        if (not isinstance(policy.get('name'), str) or
                len(policy['name']) > 32 or
                not policy['name'].replace('_','').isalnum()):
            raise ValueError('Invalid policy name')
        if not isinstance(policy.get('description'), str):
            raise ValueError('Invalid policy description')
        if policy.get('type') not in PolicyTypes.ALL:
            raise ValueError('Invalid policy type')
        if policy['type'] == PolicyTypes.ARUPA:
            self._raise_for_duplicate_name_for_same_type(policy['name'])

    def _raise_for_duplicate_name_for_same_type(self, policy_name: str, policy_type:str = PolicyTypes.ARUPA) -> None:
        """ Raise an error if a policy with the same name and type already exists in the created policies """
        if policy_name in [p["name"] for p in self.policies.values() if p["type"] == policy_type]:
            raise ValueError("Duplicate name for Arupa policy")

    def _get_policy_id_or_raise(self, json_identifier: str, action: str) -> str:
        """ Get the policy ID from the JSON identifier or raise an error if the policy is not found """
        policy_id = json.loads(json_identifier)['id']
        if policy_id not in self.policies:
            raise ValueError(f'Policy not found - cannot {action}')
        return policy_id