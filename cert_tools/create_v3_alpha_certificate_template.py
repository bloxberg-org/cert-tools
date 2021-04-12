#!/usr/bin/env python

'''
Creates a certificate template with merge tags for recipient/assertion-specific data.
'''
import json
import os

import configargparse

from cert_tools import helpers
from cert_tools import jsonpath_helpers
from cert_core.cert_model.model import scope_name

from cert_schema import BLOCKCERTS_V3_ALPHA_CONTEXT, VERIFIABLE_CREDENTIAL_V1_CONTEXT, BLOXBERG_V1_CONTEXT

# TODO change 'BLOCKCERTS_V3_CONTEXT' to V3 Canonical Context for final release
BLOCKCERTS_V3_CONTEXT = BLOCKCERTS_V3_ALPHA_CONTEXT





def create_credential_subject_section(config, publicKey):
    # An example credential subject for those that don't override
    return {
        'id': "https://blockexplorer.bloxberg.org/address/" + publicKey,
        "issuingOrg": {
          "id": config.issuer_url
        }
    }


def create_v3_assertion(config):
    assertion = {
        '@context': [
            VERIFIABLE_CREDENTIAL_V1_CONTEXT,
            BLOXBERG_V1_CONTEXT
            #'https://qa.certify.bloxberg.org/research_object_certificate_v1'
            #BLOCKCERTS_V3_CONTEXT,
            #'https://www.w3.org/2018/credentials/examples/v1'  # example subjectCredential type if not overridden
        ],
        #id is not required in the spec
        #'id': helpers.URN_UUID_PREFIX + '*|CERTUID|*',
        #'type': ["VerifiableCredential", "BlockcertsCredential"],
        'type': ["VerifiableCredential", "BloxbergCredential"],
        "issuer": config.issuer_id,
        'issuanceDate': '*|DATE|*'
    }
    return assertion

#Badge section is not necessary in VC, but provides helpful information during verification
def create_badge_section(config):
    cert_image_path = os.path.join(config.abs_data_dir, config.cert_image_file)
    issuer_image_path = os.path.join(config.abs_data_dir, config.issuer_logo_file)
    badge = {
        'type': 'BadgeClass',
        'name': config.certificate_title,
        'description': config.certificate_description,
        'image': helpers.encode_image(cert_image_path)
    }


    if config.issuer_signature_lines:
        signature_lines = []
        signature_lines = []
        for signature_line in config.issuer_signature_lines:
            signature_image_path = os.path.join(config.abs_data_dir, signature_line['signature_image'])
            signature_lines.append(
                {
                    'type': [
                        'SignatureLine',
                        'Extension'
                    ],
                    'jobTitle': signature_line['job_title'],
                    'image': helpers.encode_image(signature_image_path),
                    'name': signature_line['name']
                }
            )
        badge[scope_name('signatureLines')] = signature_lines

    return badge


def create_v3_template(config, publicKey):
    #badge = create_badge_section(config)
    assertion = create_v3_assertion(config)
    credential_subject = create_credential_subject_section(config, publicKey)

    assertion['credentialSubject'] = credential_subject
    #assertion['badge'] = badge


    if config.additional_global_fields:
        for field in config.additional_global_fields:
            assertion = jsonpath_helpers.set_field(assertion, field['path'], field['value'])

    if config.additional_per_recipient_fields:
        for field in config.additional_per_recipient_fields:
            assertion = jsonpath_helpers.set_field(assertion, field['path'], field['value'])

    return assertion


def write_certificate_template(config, publicKey):
    template_dir = config.template_dir
    if not os.path.isabs(template_dir):
        template_dir = os.path.join(config.abs_data_dir, template_dir)
    template_file_name = config.template_file_name

    assertion = create_v3_template(config, publicKey)
    template_path = os.path.join(config.abs_data_dir, template_dir, template_file_name)

    print('Writing template to ' + template_path)
    with open(template_path, 'w') as cert_template:
        json.dump(assertion, cert_template)


def get_config():
    cwd = os.getcwd()
    config_file_path = os.path.join(cwd, './conf_v3.ini')
    print(config_file_path)
    

    p = configargparse.ArgParser("create", default_config_files=[config_file_path])

    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('--issuer_public_key', type=str, help='issuer public key for bloxberg chain')
    p.add_argument('--issuer_logo_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--cert_image_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--issuer_url', type=str, help='issuer URL')
    p.add_argument('--issuer_id', required=True, type=str, help='issuer profile')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--additional_global_fields', action=helpers.make_action('global_fields'),
                   help='additional global fields')
    p.add_argument('--additional_per_recipient_fields', action=helpers.make_action('per_recipient_fields'),
                   help='additional per-recipient fields')
    p.add_argument('--certificate_description', type=str, help='the display description of the certificate')
    p.add_argument('--certificate_title', required=True, type=str, help='the title of the certificate')
    p.add_argument('--issuer_signature_lines', action=helpers.make_action('issuer_signature_lines'),
                   help='issuer signature lines')
    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))
    return args



def main():
    conf = get_config()
    write_certificate_template(conf, conf.issuer_public_key)
    print('Created template!')


if __name__ == "__main__":
    main()
