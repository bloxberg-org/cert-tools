#!/usr/bin/env python

'''
Merges a certificate template with recipients defined in a roster file. The result is
unsigned certificates that can be given to cert-issuer.
'''
import copy
import csv
import json
import os
import uuid

import configargparse

from cert_schema import schema_validator

from cert_tools import helpers
from cert_tools import jsonpath_helpers


class Recipient:
    def __init__(self, fields):

        # Name & identity aren't required fields in v3.
        # Mostly keeping it for compatibility with existing rosters but if it's a problem,
        # we can remove it and individual's can add them in via 'additional_per_recipient_fields'
        self.name = fields.pop('name')
        self.pubkey = fields.pop('pubkey')
        self.identity = fields.pop('identity')

        self.additional_fields = fields


def instantiate_assertion(cert, uid, issued_on, SHA256Hash):
    cert['issuanceDate'] = issued_on
    cert['id'] = helpers.URN_UUID_PREFIX + uid
    #Add back SHA is compliant with blockcerts standard
    #SHAdict = {'@SHA256Hash':SHA256Hash}
    cert['SHA256Hash'] = SHA256Hash
    return cert


def instantiate_recipient(cert, recipient_name, additional_fields, email):
    #cert['credentialSubject']['id'] = recipient.pubkey
    #cert['credentialSubject']['id'] = "did:key:z6Mkq3L1jEDDZ5R7eT523FMLxC4k6MCpzqD7ff1CrkWpoJwM"

    ###Currently we are using email address as the credentialSubject's ID as we can't expect every recipient to have a public ID. Another option is recipient name 
    cert['credentialSubject']['id'] = email
    """
    if additional_fields:
        if not recipient.additional_fields:
            raise Exception('expected additional recipient fields but none found')
        for field in additional_fields:
            cert = jsonpath_helpers.set_field(cert, field['path'], recipient.additional_fields[field['csv_column']])
    else:
        if recipient.additional_fields:
            # throw an exception on this in case it's a user error. We may decide to remove this if it's a nuisance
            raise Exception(
                'there are fields that are not expected by the additional_per_recipient_fields configuration')
    """

def create_unsigned_certificates_from_roster(template, recipient_name, publicKey, use_identities, additionalFields, SHA256Hash, email):
    issued_on = helpers.create_iso8601_tz()

    certs = {}
    for shahash in SHA256Hash:
        if use_identities:
            uid = publicKey
            uid = "".join(c for c in uid if c.isalnum())
        else:
            uid = str(uuid.uuid4())

        cert = copy.deepcopy(template)

        instantiate_assertion(cert, uid, issued_on, shahash)
        instantiate_recipient(cert, recipient_name, additionalFields, email)

        # validate unsigned certificate before writing
        schema_validator.validate_v3_alpha(cert, True)

        certs[uid] = cert
    return certs


def get_recipients_from_roster(config):
    roster = os.path.join(config.abs_data_dir, config.roster)
    with open(roster, 'r') as theFile:
        reader = csv.DictReader(theFile)
        recipients = map(lambda x: Recipient(x), reader)
        return list(recipients)


def get_template(config):
    template = os.path.join(config.abs_data_dir, config.template_dir, config.template_file_name)
    with open(template) as template:
        cert_str = template.read()
        return json.loads(cert_str)


def instantiate_batch(config, publicKey, recipient_name, email, SHA256Hash):
    recipients = get_recipients_from_roster(config)
    template = get_template(config)
    use_identities = config.filename_format == "certname_identity"
    certs = create_unsigned_certificates_from_roster(template, recipient_name, publicKey, use_identities, config.additional_per_recipient_fields, SHA256Hash, email)
    output_dir = os.path.join(config.abs_data_dir, config.unsigned_certificates_dir)
    print('Writing certificates to ' + output_dir)
    uidArray = []
    for uid in certs.keys():
        cert_file = os.path.join(output_dir, uid + '.json')
        if os.path.isfile(cert_file) and config.no_clobber:
            continue
        uidArray.append(uid)
        with open(cert_file, 'w') as unsigned_cert:
            json.dump(certs[uid], unsigned_cert)
    return uidArray


def get_config():
    cwd = os.getcwd()

    p = configargparse.ArgParser("batchInstantiate", default_config_files=[os.path.join(cwd, './conf_v3.ini')])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--additional_per_recipient_fields', action=helpers.make_action('per_recipient_fields'), help='additional per-recipient fields')
    p.add_argument('--unsigned_certificates_dir', type=str, help='output directory for unsigned certificates')
    p.add_argument('--roster', type=str, help='roster file name')
    p.add_argument('--filename_format', type=str, help='how to format certificate filenames (one of certname_identity or uuid)')
    p.add_argument('--no_clobber', action='store_true', help='whether to overwrite existing certificates')
    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))

    return args


def main():
    conf = get_config()
    instantiate_batch(conf)
    print('Instantiated batch!')


if __name__ == "__main__":
    main()
