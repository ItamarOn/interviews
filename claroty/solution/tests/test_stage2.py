import json

import pytest
from stage2 import PolicyAPI

@pytest.fixture
def api():
    return PolicyAPI()

@pytest.fixture
def foo_policy_identifier(api):
    return api.create_policy(
        json.dumps(
            {
                "name": "foo",
                "description": "my foo policy",
                "type": "Arupa",
            }
        )
    )

@pytest.fixture
def bar_policy_identifier(api):
    return api.create_policy(
        json.dumps(
            {
                "name": "bar",
                "description": "my bar policy",
                "type": "Frisco",
            }
        )
    )

class TestCreateRule:
    def test_empty_input(self, api, foo_policy_identifier):
        with pytest.raises(Exception):
            api.create_rule(foo_policy_identifier, "")

    def test_malformed_json_input(self, api, foo_policy_identifier):
        with pytest.raises(Exception):
            api.create_rule(foo_policy_identifier, "{rule}")

    def test_valid_rule_creation(self, api, foo_policy_identifier):
        rule_json = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                {
                    "name": "rule1",
                    "ip_proto": 6,
                    "source_port": 80,
                    "source_subnet": "192.168.1.0/24",
                }
            ),
        )
        assert isinstance(rule_json, str)
        json.loads(rule_json)

    def test_missing_field(self, api, foo_policy_identifier):
        with pytest.raises(Exception):
            api.create_rule(
                foo_policy_identifier,
                json.dumps(
                    {
                        "name": "rule1",
                        "ip_proto": 6,
                    }
                ),
            )

    def test_duplicate_rule_name_arupa(self, api, foo_policy_identifier):
        api.create_rule(
            foo_policy_identifier,
            json.dumps(
                {
                    "name": "rule1",
                    "ip_proto": 6,
                    "source_port": 80,
                    "source_subnet": "192.168.1.0/24",
                }
            ),
        )
        with pytest.raises(Exception):
            api.create_rule(
                foo_policy_identifier,
                json.dumps(
                    {
                        "name": "rule1",
                        "ip_proto": 6,
                        "source_port": 443,
                        "source_subnet": "192.168.2.0/24",
                    }
                ),
            )

    def test_duplicate_rule_name_frisco(self, api, bar_policy_identifier):
        api.create_rule(
            bar_policy_identifier,
            json.dumps(
                {
                    "name": "rule1",
                    "ip_proto": 6,
                    "source_port": 80,
                    "source_ip": "192.168.1.1",
                    "destination_ip": "192.168.1.2",
                }
            ),
        )
        with pytest.raises(Exception):
            api.create_rule(
                bar_policy_identifier,
                json.dumps(
                    {
                        "name": "rule1",
                        "ip_proto": 6,
                        "source_port": 443,
                        "source_ip": "192.168.2.1",
                        "destination_ip": "192.168.2.2",
                    }
                ),
            )

class TestReadRule:
    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.read_rule(json.dumps("invalid"))

    def test_valid_rule_read(self, api, foo_policy_identifier):
        rule_id = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                {
                    "name": "rule1",
                    "ip_proto": 6,
                    "source_port": 80,
                    "source_subnet": "192.168.1.0/24",
                }
            ),
        )
        rule = api.read_rule(rule_id)
        assert isinstance(rule, str)
        assert json.loads(rule)["name"] == "rule1"

class TestUpdateRule:
    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.update_rule(
                json.dumps("invalid"),
                json.dumps(
                    {
                        "name": "updated_rule",
                        "ip_proto": 6,
                        "source_port": 443,
                        "source_subnet": "192.168.1.0/24",
                    }
                ),
            )

    def test_valid_rule_update(self, api, foo_policy_identifier):
        rule_id = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                {
                    "name": "rule1",
                    "ip_proto": 6,
                    "source_port": 80,
                    "source_subnet": "192.168.1.0/24",
                }
            ),
        )
        api.update_rule(
            rule_id,
            json.dumps(
                {
                    "name": "updated_rule",
                    "ip_proto": 6,
                    "source_port": 443,
                    "source_subnet": "192.168.1.0/24",
                }
            ),
        )
        updated_rule = json.loads(api.read_rule(rule_id))
        assert updated_rule["name"] == "updated_rule"
        assert updated_rule["source_port"] == 443

class TestDeleteRule:
    def test_invalid_or_nonexistent_identifier(self, api):
        with pytest.raises(Exception):
            api.delete_rule(json.dumps("invalid"))

    def test_valid_rule_deletion(self, api, foo_policy_identifier):
        rule_id = api.create_rule(
            foo_policy_identifier,
            json.dumps(
                {
                    "name": "rule1",
                    "ip_proto": 6,
                    "source_port": 80,
                    "source_subnet": "192.168.1.0/24",
                }
            ),
        )
        api.delete_rule(rule_id)
        with pytest.raises(Exception):
            api.read_rule(rule_id)

class TestListRules:
    def test_empty_rule_list(self, api, foo_policy_identifier):
        rules = api.list_rules(foo_policy_identifier)
        assert isinstance(rules, str)
        assert len(json.loads(rules)) == 0

    def test_non_empty_rule_list(self, api, foo_policy_identifier):
        api.create_rule(
            foo_policy_identifier,
            json.dumps(
                {
                    "name": "rule1",
                    "ip_proto": 6,
                    "source_port": 80,
                    "source_subnet": "192.168.1.0/24",
                }
            ),
        )
        rules = api.list_rules(foo_policy_identifier)
        assert len(json.loads(rules)) == 1
