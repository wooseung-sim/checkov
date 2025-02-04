from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class PolicyLogForwarding(BaseResourceCheck):
    def __init__(self):
        name = "Ensure a Log Forwarding Profile is selected for each security policy rule"
        id = "CKV_PAN_9"
        supported_resources = ['panos_security_policy','panos_security_rule_group']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
    
        # Check there is a rule defined in the resource
        if 'rule' in conf:

            # Report the area of evaluation
            self.evaluated_keys = ['rule']

            # Get all the rules defined in the resource
            rules = conf.get('rule')

            # Iterate over each rule
            for secrule in rules:

                # Check if a log_setting is defined in the rule
                if 'log_setting' in secrule:

                    # If a log_setting is defined, get the value
                    desc = secrule.get('log_setting')

                    if desc[0].strip() == "":
                        # An empty string is no log_setting, which is a fail
                        return CheckResult.FAILED
                else:
                    # If a log_setting attribute is not explicitly set, this is a fail
                    return CheckResult.FAILED
            
            # If no fails have been found, this is a pass
            return CheckResult.PASSED

        # If there's no rules we have nothing to check
        return CheckResult.UNKNOWN

check = PolicyLogForwarding()
