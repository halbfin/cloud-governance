
import os

AWS_ACCESS_KEY_ID_PERF = os.environ['AWS_ACCESS_KEY_ID_PERF']
AWS_SECRET_ACCESS_KEY_PERF = os.environ['AWS_SECRET_ACCESS_KEY_PERF']
AWS_ACCESS_KEY_ID_DELETE_PERF = os.environ['AWS_ACCESS_KEY_ID_DELETE_PERF']
AWS_SECRET_ACCESS_KEY_DELETE_PERF = os.environ['AWS_SECRET_ACCESS_KEY_DELETE_PERF']
BUCKET_PERF = os.environ['BUCKET_PERF']
AWS_ACCESS_KEY_ID_PSAP = os.environ['AWS_ACCESS_KEY_ID_PSAP']
AWS_SECRET_ACCESS_KEY_PSAP = os.environ['AWS_SECRET_ACCESS_KEY_PSAP']
AWS_ACCESS_KEY_ID_DELETE_PSAP = os.environ['AWS_ACCESS_KEY_ID_DELETE_PSAP']
AWS_SECRET_ACCESS_KEY_DELETE_PSAP = os.environ['AWS_SECRET_ACCESS_KEY_DELETE_PSAP']
BUCKET_PSAP = os.environ['BUCKET_PSAP']
AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE = os.environ['AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE']
AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE = os.environ['AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE']
BUCKET_PERF_SCALE = os.environ['BUCKET_PERF_SCALE']
AWS_ACCESS_KEY_ID_RH_PERF = os.environ['AWS_ACCESS_KEY_ID_RH_PERF']
AWS_SECRET_ACCESS_KEY_RH_PERF = os.environ['AWS_SECRET_ACCESS_KEY_RH_PERF']
BUCKET_RH_PERF = os.environ['BUCKET_RH_PERF']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
SPREADSHEET_ID = os.environ['AWS_IAM_USER_SPREADSHEET_ID']
REPLY_TO = os.environ['REPLY_TO']
special_user_mails = os.environ['CLOUD_GOVERNANCE_SPECIAL_USER_MAILS']
users_manager_mails = os.environ['USERS_MANAGER_MAILS']
account_admin = os.environ['ACCOUNT_ADMIN']
LDAP_HOST_NAME = os.environ['LDAP_HOST_NAME']
ES_HOST = os.environ['ES_HOST']
ES_PORT = os.environ['ES_PORT']

LOGS = os.environ.get('LOGS', 'logs')


def get_policies(type: str = None):
    """
    This method return a list of policies name without extension, that can filter by type
    @return: list of policies name
    """
    policies = []
    policies_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))), 'cloud_governance', 'policy', 'aws')
    for (dirpath, dirnames, filenames) in os.walk(policies_path):
        for filename in filenames:
            if not filename.startswith('__') and (filename.endswith('.yml') or filename.endswith('.py')):
                if not type:
                    policies.append(os.path.splitext(filename)[0])
                elif type and type in filename:
                    policies.append(os.path.splitext(filename)[0])
    return policies


print('Run all policies pre active region')
regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'eu-central-1', 'ap-south-1', 'eu-north-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-west-3', 'sa-east-1']
policies = get_policies()
policies.remove('cost_explorer')
policies.remove('cost_over_usage')
policies.remove('monthly_report')
policies.remove('cost_billing_reports')
policies.remove('cost_explorer_payer_billings')

for region in regions:
    for policy in policies:
        # Delete zombie cluster resource every night dry_run=no
        if policy == 'zombie_cluster_resource':
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PERF-DEPT" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PSAP" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PSAP}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PSAP}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PSAP}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PERF-SCALE" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF_SCALE}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
        # running policies dry_run=no per every region, ebs_unattached, ec2_stop, ip_unattached, ec2_idle, unused_nat_gateway, zombie_snapshots
        elif policy in ('zombie_snapshots', 'ebs_unattached'):
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PERF-DEPT" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PERF-SCALE" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF_SCALE}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
        elif policy in ('ec2_idle', 'ec2_stop'):
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e account="PERF-DEPT" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e account="PERF-SCALE" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF_SCALE}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
        elif policy in ('unused_nat_gateway', 'ip_unattached'):
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e MANAGER_EMAIL_ALERT="False" -e account="PERF-DEPT" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e MANAGER_EMAIL_ALERT="False" -e account="PERF-SCALE" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF_SCALE}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
        # running policies dry_run=no only one region, empty_roles, s3_inactive
        elif policy in ('empty_roles', 's3_inactive') and region == 'us-east-1':
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e MANAGER_EMAIL_ALERT="False" -e account="PERF-DEPT" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
            os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e MANAGER_EMAIL_ALERT="False" -e account="PERF-SCALE" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="no" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}"  -e policy_output="s3://{BUCKET_PERF_SCALE}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
        # running policies dry_run=yes per every region ebs_in_use, ec2_run
        else:
            if policy not in ('empty_roles', 's3_inactive'):
                os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PERF-DEPT" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="yes" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
                os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PSAP" -e MANAGER_EMAIL_ALERT="False" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PSAP}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PSAP}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="yes" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PSAP}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
                os.system(f"""podman run --rm --name cloud-governance --net="host" -e EMAIL_ALERT="False" -e account="PERF-SCALE" -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE}" -e AWS_DEFAULT_REGION="{region}" -e dry_run="yes" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e special_user_mails="{special_user_mails}" -e account_admin="{account_admin}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e policy_output="s3://{BUCKET_PERF_SCALE}/{LOGS}/{region}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")

# Update AWS IAM User tags from the spreadsheet
os.system(f"""podman run --rm --name cloud-governance --net="host" -e account="PERF-DEPT" -e policy="tag_iam_user" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF}" -e user_tag_operation="update" -e SPREADSHEET_ID="{SPREADSHEET_ID}" -e GOOGLE_APPLICATION_CREDENTIALS="{GOOGLE_APPLICATION_CREDENTIALS}" -v "{GOOGLE_APPLICATION_CREDENTIALS}":"{GOOGLE_APPLICATION_CREDENTIALS}" -e account_admin="{account_admin}" -e special_user_mails="{special_user_mails}" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
os.system(f"""podman run --rm --name cloud-governance --net="host" -e account="PERF-SCALE" -e policy="tag_iam_user" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE}" -e user_tag_operation="update" -e SPREADSHEET_ID="{SPREADSHEET_ID}" -e GOOGLE_APPLICATION_CREDENTIALS="{GOOGLE_APPLICATION_CREDENTIALS}" -v "{GOOGLE_APPLICATION_CREDENTIALS}":"{GOOGLE_APPLICATION_CREDENTIALS}" -e account_admin="{account_admin}" -e special_user_mails="{special_user_mails}" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
os.system(f"""podman run --rm --name cloud-governance --net="host" -e account="PSAP" -e policy="tag_iam_user" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_DELETE_PSAP}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_DELETE_PSAP}" -e user_tag_operation="update" -e SPREADSHEET_ID="{SPREADSHEET_ID}" -e GOOGLE_APPLICATION_CREDENTIALS="{GOOGLE_APPLICATION_CREDENTIALS}" -v "{GOOGLE_APPLICATION_CREDENTIALS}":"{GOOGLE_APPLICATION_CREDENTIALS}" -e account_admin="{account_admin}" -e special_user_mails="{special_user_mails}" -e LDAP_HOST_NAME="{LDAP_HOST_NAME}" -e log_level="INFO" -e es_host="{ES_HOST}" -e es_port="{ES_PORT}" quay.io/ebattat/cloud-governance:latest""")


# Send Policy alerts to users
accounts = [{'account': 'PERF-DEPT', 'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID_DELETE_PERF,
            'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY_DELETE_PERF, 'BUCKET_NAME': BUCKET_PERF},
            {'account': 'PERF-SCALE', 'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID_DELETE_PERF_SCALE,
            'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY_DELETE_PERF_SCALE, 'BUCKET_NAME': BUCKET_PERF_SCALE},
            {'account': 'PSAP', 'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID_DELETE_PSAP,
            'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY_DELETE_PSAP, 'BUCKET_NAME': BUCKET_PSAP}]
policies.remove('ec2_run')
policies.remove('ebs_in_use')
remove_polices = ['ec2_run', 'ebs_in_use', 'zombie_cluster_resource', 'ec2_idle', 'skipped_resources', 'ec2_stop']  # policies that will not aggregate
policies = [policy.replace('_', '-') for policy in policies if policy not in remove_polices]
common_input_vars = {'PUBLIC_CLOUD_NAME': 'AWS', 'BUCKET_KEY': 'logs', 'KERBEROS_USERS': f"{special_user_mails}", 'LDAP_HOST_NAME': f"{LDAP_HOST_NAME}", 'log_level': "INFO", 'MAIL_ALERT_DAYS': "[4, 6, 7]", 'POLICY_ACTIONS_DAYS': "[7]", 'POLICIES_TO_ALERT': policies, 'es_host': ES_HOST, 'es_port': ES_PORT}
combine_vars = lambda item: f'{item[0]}="{item[1]}"'
common_envs = list(map(combine_vars, common_input_vars.items()))
for account in accounts:
    envs = list(map(combine_vars, account.items()))
    os.system(f"""podman run --rm --name cloud-governance --net="host" -e policy="send_aggregated_alerts" -e {' -e '.join(envs)} -e {' -e '.join(common_envs)} -e DEFAULT_ADMINS="['athiruma']"   quay.io/ebattat/cloud-governance:latest""")

# # Gitleaks run on github not related to any aws account
print("run gitleaks")
region = 'us-east-1'
policy = 'gitleaks'
os.system(f"""podman run --rm --name cloud-governance -e policy="{policy}" -e AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID_PERF}" -e AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY_PERF}" -e AWS_DEFAULT_REGION="{region}" -e git_access_token="{GITHUB_TOKEN}" -e git_repo="https://github.com/redhat-performance" -e several_repos="yes" -e policy_output="s3://{BUCKET_PERF}/{LOGS}/$region" -e log_level="INFO" quay.io/ebattat/cloud-governance:latest""")
