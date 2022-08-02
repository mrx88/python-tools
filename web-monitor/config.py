
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    environments=True,
    settings_files=['settings.yaml', '.secrets.yaml'],
    validators=[
        Validator('enabled_web_urls', 'kafka_bootstrap_servers',
                  'kafka_security_protocol', 'kafka_ssl_certfile',
                  'kafka_ssl_keyfile', 'kafka_ssl_cafile', 'kafka_topic',
                  'postgres_host', 'postgres_port', 'postgres_user',
                  'postgres_dbname', 'postgres_sslmode',
                  'postgres_ssl_cafile', 'postgres_password', must_exist=True),
        Validator('web_regex', must_exist=None)
    ]


)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
