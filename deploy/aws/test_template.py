"""The CloudFormation template carries the files beside it, and its host script is sound.

    ./.venv/Scripts/python.exe -m unittest discover -s deploy/aws

The template writes compose.yaml, the Caddyfile and caddy-start.sh to the
host out of its own text, because a stack is created from one file. They are tested as the
files in this directory, so the template must carry them byte for byte. No
network and no AWS account; whether AWS accepts the template is cfn-lint's
to say, and the README names what was run.
"""

from pathlib import Path
import re
import shutil
import subprocess
import unittest

import yaml

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "swiss-tip.yaml"
# EC2 refuses user data over 16 KB, measured before the base64 encoding.
USER_DATA_LIMIT = 16384


class Tagged(dict):
    """A CloudFormation short-form function, kept as {tag: value}."""


class TemplateLoader(yaml.SafeLoader):
    pass


def construct_tag(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node, deep=True)
    else:
        value = loader.construct_mapping(node, deep=True)
    return Tagged({suffix: value})


TemplateLoader.add_multi_constructor("!", construct_tag)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def load_template() -> dict:
    return yaml.load(text(TEMPLATE), Loader=TemplateLoader)


def user_data_parts(template: dict) -> tuple[str, dict, str]:
    """The substituted head with its variables, and the literal rest."""
    joined = template["Resources"]["Instance"]["Properties"]["UserData"]["Fn::Base64"]["Fn::Join"]
    separator, (head, rest) = joined
    assert separator == "" and isinstance(head, Tagged) and isinstance(rest, str)
    head_text, variables = head["Sub"]
    return head_text, variables, rest


def heredoc(script: str, marker: str) -> str:
    match = re.search(r"<<'%s'\n(.*?)\n%s\n" % (marker, marker), script, re.DOTALL)
    assert match, f"no heredoc {marker}"
    return match.group(1) + "\n"


class TemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = load_template()
        cls.head, cls.variables, cls.rest = user_data_parts(cls.template)

    def test_the_host_gets_the_tested_files(self):
        self.assertEqual(heredoc(self.rest, "SWISSTIP_COMPOSE"), text(HERE / "compose.yaml"))
        self.assertEqual(heredoc(self.rest, "SWISSTIP_CADDYFILE"), text(HERE / "Caddyfile"))
        self.assertEqual(heredoc(self.rest, "SWISSTIP_CADDY_START"), text(HERE / "caddy-start.sh"))

    def test_only_the_head_is_substituted(self):
        # Compose's own ${VAR:-default} in the literal part would be CloudFormation's to resolve under !Sub.
        self.assertIn("${SWISSTIP_PACK:-mvp-zurich}", self.rest)
        names = set(re.findall(r"\$\{([^}]+)\}", self.head))
        known = set(self.template["Parameters"]) | set(self.variables) | {"AWS::Region"}
        self.assertEqual(names - known, set())
        # Every shell variable the head sets is one the rest reads.
        assigned = set(re.findall(r"^([A-Z_]+)=", self.head, re.MULTILINE))
        for name in assigned:
            self.assertRegex(self.rest, r"\$\{?%s\b" % name, f"{name} is set and never read")

    def test_the_user_data_fits(self):
        # The longest values a stack can give: two 253-character domains and an ARN.
        rendered = re.sub(r"\$\{[^}]+\}", "x" * 253, self.head) + self.rest
        self.assertLess(len(rendered.encode("utf-8")), USER_DATA_LIMIT)

    def test_the_demo_is_hosted_behind_https_and_a_password_only(self):
        compose = yaml.safe_load(text(HERE / "compose.yaml"))
        demo = compose["services"]["demo"]
        self.assertEqual(demo["profiles"], ["demo"])
        self.assertIn("SWISSTIP_REQUIRE_PASSWORD=1", demo["environment"])
        # Caddy alone publishes ports; the web interface's default site is a port nobody publishes.
        published = {name for name, service in compose["services"].items() if service.get("ports")}
        self.assertEqual(published, {"caddy"})
        # Without a domain and without sslip.io names the site is that unpublished port.
        demo_site = self.variables["DemoSite"]["If"]
        self.assertEqual(demo_site[:2], ["HasDemoDomain", Tagged({"Ref": "DemoDomain"})])
        self.assertEqual(demo_site[2]["If"][0], "SslipDemo")
        self.assertEqual(demo_site[2]["If"][2], ":4096")
        self.assertNotIn("4096", " ".join(compose["services"]["caddy"]["ports"]))
        # A hosted web interface always has a password: the one given, or else a generated one.
        secret = self.template["Resources"]["DemoSecret"]
        self.assertEqual(secret["Condition"], "HostDemo")
        self.assertEqual(secret["Properties"]["GenerateSecretString"]["If"][0], "DemoPasswordGiven")

    def test_one_pack_image_carries_the_model_and_the_calendar(self):
        compose = yaml.safe_load(text(HERE / "compose.yaml"))
        # The server, the web interface and Caddy: no sidecar, no connector container, and the image is not slim.
        self.assertEqual(set(compose["services"]), {"swiss-tip", "demo", "caddy"})
        server = compose["services"]["swiss-tip"]
        self.assertEqual(server["image"], "${SWISSTIP_REGISTRY:-ghcr.io/swisstip}/swiss-tip:${SWISSTIP_PACK:-mvp-zurich}")
        self.assertNotIn("command", server)
        # The variable without a value: unset in .env, the image starts its own connector; set, even empty, it wins.
        self.assertEqual(server["environment"], ["SWISSTIP_CONNECTORS"])
        self.assertEqual(self.variables["Profiles"]["If"], ["HostDemo", "demo", ""])
        self.assertIn('if [ "$CALENDAR" = no ]; then\n  echo "SWISSTIP_CONNECTORS=" >> .env', self.rest)
        self.assertIn("CALENDAR='${Calendar}'", self.head)
        self.assertEqual(self.template["Parameters"]["Calendar"]["AllowedValues"], ["yes", "no"])
        # The watchdog restarts the server when the model inside it does not answer.
        watchdog = heredoc(self.rest, "SWISSTIP_WATCHDOG")
        self.assertIn("http://127.0.0.1:11434/api/version", watchdog)
        self.assertIn("docker compose restart swiss-tip", watchdog)

    def test_the_welcome_panel_is_downloaded_or_generic_and_mounted_read_only(self):
        compose = yaml.safe_load(text(HERE / "compose.yaml"))
        self.assertEqual(compose["services"]["demo"]["volumes"], ["./welcome.json:/etc/swiss-tip/welcome.json:ro"])
        self.assertIn("WELCOME_URL='${WelcomeUrl}'", self.head)
        self.assertIn('curl -fsSL --retry 3 -o welcome.json "$WELCOME_URL"', self.rest)
        self.assertIn('"questions": []', self.rest)
        self.assertTrue(self.template["Parameters"]["WelcomeUrl"]["Default"].startswith("https://raw.githubusercontent.com/"))

    def test_passwords_reach_the_host_through_their_secrets_only(self):
        parameters = self.template["Parameters"]
        passwords = [name for name in parameters if name.endswith("Password")]
        self.assertEqual(sorted(passwords), ["DemoPassword", "McpPassword"])
        for name in passwords:
            self.assertIs(parameters[name].get("NoEcho"), True, name)
            # Not in the user data, which the instance and the account can read back; not in an output.
            self.assertNotIn("${%s}" % name, self.head)
            self.assertNotIn(Tagged({"Ref": name}), self.variables.values())
        for output in ("McpPasswordSecret", "DemoPasswordSecret"):
            value = self.template["Outputs"][output]["Value"]
            self.assertIn(value, (Tagged({"Ref": "McpSecret"}), Tagged({"Ref": "DemoSecret"})))
        # What a password may consist of survives .env, the shell and the Caddyfile unquoted.
        for name in passwords:
            self.assertEqual(parameters[name]["AllowedPattern"], "^$|^[A-Za-z0-9._~-]{8,64}$")

    def test_the_mcp_endpoint_is_open_unless_a_name_is_given_and_then_https_only(self):
        self.assertEqual(self.template["Parameters"]["McpUsername"]["Default"], "")
        self.assertEqual(self.template["Resources"]["McpSecret"]["Condition"], "ProtectMcp")
        rule = self.template["Rules"]["McpPasswordOverHttps"]
        self.assertEqual(rule["RuleCondition"], Tagged({"Not": [Tagged({"Equals": [Tagged({"Ref": "McpUsername"}), ""]})]}))
        # HTTPS comes from a domain of one's own or from an sslip.io name.
        self.assertEqual(rule["Assertions"][0]["Assert"], Tagged({"Or": [
            Tagged({"Not": [Tagged({"Equals": [Tagged({"Ref": "McpDomain"}), ""]})]}),
            Tagged({"Not": [Tagged({"Equals": [Tagged({"Ref": "SslipNames"}), "none"]})]}),
        ]}))
        # The Caddyfile imports what caddy-start.sh writes, and only for the MCP site.
        self.assertIn("import /etc/caddy/auth/mcp*.caddy", text(HERE / "Caddyfile"))
        self.assertIn('> "$auth/mcp.caddy"', text(HERE / "caddy-start.sh"))

    def test_sslip_names_come_from_the_elastic_ip_without_a_cycle(self):
        resources = self.template["Resources"]
        # The instance's user data names the address, so the address must not name the instance.
        self.assertNotIn("InstanceId", resources["ElasticIp"]["Properties"])
        attachment = resources["ElasticIpAttachment"]["Properties"]
        self.assertEqual(attachment["InstanceId"], Tagged({"Ref": "Instance"}))
        self.assertEqual(attachment["AllocationId"], Tagged({"GetAtt": "ElasticIp.AllocationId"}))
        self.assertEqual(self.template["Parameters"]["SslipNames"]["Default"], "none")
        self.assertEqual(self.template["Parameters"]["SslipNames"]["AllowedValues"], ["none", "mcp", "mcp-and-demo"])
        # Both names are the hyphenated address under sslip.io, the second one behind "demo.".
        hyphenated = Tagged({"Join": ["-", Tagged({"Split": [".", Tagged({"Ref": "ElasticIp"})]})]})
        mcp_name = self.variables["McpSite"]["If"][2]["If"][1]
        demo_name = self.variables["DemoSite"]["If"][2]["If"][1]
        self.assertEqual(mcp_name, Tagged({"Join": ["", [hyphenated, ".sslip.io"]]}))
        self.assertEqual(demo_name, Tagged({"Join": ["", ["demo.", hyphenated, ".sslip.io"]]}))
        # Records are made for the domains given, never for an sslip.io name.
        self.assertEqual(resources["DemoRecord"]["Condition"], "DemoRecordWanted")
        conditions = self.template["Conditions"]
        self.assertEqual(conditions["DemoRecordWanted"], Tagged({"And": [Tagged({"Condition": "HasZone"}),
                                                                        Tagged({"Condition": "HasDemoDomain"})]}))
        self.assertEqual(conditions["SslipDemo"], Tagged({"Equals": [Tagged({"Ref": "SslipNames"}), "mcp-and-demo"]}))
        self.assertEqual(conditions["HostDemo"], Tagged({"Or": [Tagged({"Condition": "HasDemoDomain"}),
                                                               Tagged({"Condition": "SslipDemo"})]}))

    def test_no_ssh(self):
        ingress = self.template["Resources"]["SecurityGroup"]["Properties"]["SecurityGroupIngress"]
        self.assertEqual(sorted((rule["IpProtocol"], rule["FromPort"]) for rule in ingress),
                         [("tcp", 80), ("tcp", 443), ("udp", 443)])
        self.assertNotIn("KeyName", self.template["Resources"]["Instance"]["Properties"])

    @unittest.skipUnless(shutil.which("bash"), "bash is not installed")
    def test_the_host_script_parses(self):
        # On standard input, as bytes: a Windows path means nothing to a bash there, and text mode would add CRs.
        rendered = re.sub(r"\$\{[^}]+\}", "value", self.head) + self.rest
        result = subprocess.run(["bash", "-n"], input=rendered.encode("utf-8"), capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))


if __name__ == "__main__":
    unittest.main()
