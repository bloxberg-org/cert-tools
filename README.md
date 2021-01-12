[![Build Status](https://travis-ci.org/blockchain-certificates/cert-tools.svg?branch=master)](https://travis-ci.org/blockchain-certificates/cert-tools)

# cert-tools
Command line tools for designing certificate templates, instantiating a certificate batch, and import/export tasks

See example of certificate template and batch creation in sample_data.

For more information on working with V3 alpha/beta, please see the docs [here](./docs/V3.md).

## Install

1. Ensure you have an python environment. [Recommendations](https://github.com/bloxberg-org/cert-issuer/blob/master/docs/virtualenv.md)

2. Git clone the repository and change to the directory

  ```bash
  git clone https://github.com/bloxberg-org/cert-tools.git && cd cert-tools
  ```

3. Run the setup script

  ```bash
  pip install .
  ```
  
  ## Example

See sample_data for example configuration and output. `conf_v3` was used to create a batch of 2 unsigned certificates on the bloxberg blockchain. 

The steps were:
- Create the template
    - Update the config file to contain the correct data to populate the certificates
    - Run `create-certificate-template_v3 -c conf_v3.ini`, which resulted in the certificate template `/certificate_templates/test_v3.json`
- Instantiate the batch
    - Run 'instantiate-certificate-batch_v3 -c conf_v3.ini
', which resulted in the files in `unsigned_certificates`
    
Then the unsigned certificates were copied to cert-issuer for signing and issuing on the blockchain.

## Scripts

The cert-tools setup script installs 2 scripts, which are described below:

### create_certificate_template.py

#### Run

```bash
create-certificate-template_v3 -c conf_v3.ini
```

#### Configuration

The `conf_v3.ini` fields are described below. Optional arguments are in brackets

```
create-certificate-template --help

usage: create_v3_alpha_certificate_template.py [-h] [-c MY_CONFIG]
                                         [--data_dir DATA_DIR]
                                         [--issuer_logo_file ISSUER_LOGO_FILE]
                                         [--cert_image_file CERT_IMAGE_FILE]
                                         [--issuer_url ISSUER_URL]
                                         [--issuer_certs_url ISSUER_CERTS_URL]
                                         --issuer_email ISSUER_EMAIL
                                         --issuer_name ISSUER_NAME
                                         --issuer_id ISSUER_ID [--issuer_key ISSUER_KEY]
                                         [--certificate_description CERTIFICATE_DESCRIPTION]
                                         --certificate_title CERTIFICATE_TITLE
                                         --criteria_narrative CRITERIA_NARRATIVE
                                         [--template_dir TEMPLATE_DIR]
                                         [--template_file_name TEMPLATE_FILE_NAME]
                                         [--hash_emails]
                                         [--revocation_list REVOCATION_LIST]
                                         [--issuer_public_key ISSUER_PUBLIC_KEY]
                                         --badge_id BADGE_ID
                                         [--issuer_signature_lines ISSUER_SIGNATURE_LINES]
                                         [--additional_global_fields ADDITIONAL_GLOBAL_FIELDS]
                                         [--additional_per_recipient_fields ADDITIONAL_PER_RECIPIENT_FIELDS]


Args that start with '--' (eg. --data_dir) can also be set in a config file (./cert-tools/conf.ini or specified via -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more than one place, then commandline values override config file values which override defaults.


Argument details:
  -h, --help            show this help message and exit
  -c MY_CONFIG, --my-config MY_CONFIG
                        config file path (default: None)
  --data_dir DATA_DIR   where data files are located (default: None)
  --issuer_logo_file ISSUER_LOGO_FILE
                        issuer logo image file, png format (default: None)
  --cert_image_file CERT_IMAGE_FILE
                        issuer logo image file, png format (default: None)
  --issuer_url ISSUER_URL
                        issuer URL (default: None)
  --issuer_certs_url ISSUER_CERTS_URL
                        issuer certificates URL (default: None)
  --issuer_email ISSUER_EMAIL
                        issuer email (default: None)
  --issuer_name ISSUER_NAME
                        issuer name (default: None)
  --issuer_id ISSUER_ID
                        issuer profile (default: None)
  --issuer_key ISSUER_KEY
                        issuer issuing key (default: None)
  --certificate_description CERTIFICATE_DESCRIPTION
                        the display description of the certificate (default:
                        None)
  --certificate_title CERTIFICATE_TITLE
                        the title of the certificate (default: None)
  --criteria_narrative CRITERIA_NARRATIVE
                        criteria narrative (default: None)
  --template_dir TEMPLATE_DIR
                        the template output directory (default: None)
  --template_file_name TEMPLATE_FILE_NAME
                        the template file name (default: None)
  --hash_emails         whether to hash emails in the certificate (default:
                        False)
  --revocation_list REVOCATION_LIST
                        issuer revocation list (default: None)
  --issuer_public_key ISSUER_PUBLIC_KEY
                        issuer public key (default: None)
  --badge_id BADGE_ID   badge id (default: None)
  --issuer_signature_lines ISSUER_SIGNATURE_LINES
                        issuer signature lines (default: None)
  --additional_global_fields ADDITIONAL_GLOBAL_FIELDS
                        additional global fields (default: None)
  --additional_per_recipient_fields ADDITIONAL_PER_RECIPIENT_FIELDS
                        additional per-recipient fields (default: None)


```

#### About

Creates a certificate template populated with the setting you provide in the conf_v3.ini file.
 

### instantiate_v3_alpha_certificate_batch.py

#### Run

```
instantiate-certificate-batch_v3 -c conf_v3.ini
```

#### Configuration

The `conf_v3.ini` fields are described below. Optional arguments are in brackets


```
instantiate-certificate-batch_v3 --help

usage: instantiate_v3_alpha_certificate_batch.py [-h] [-c MY_CONFIG]
                                           [--data_dir DATA_DIR]
                                           [--hashing_dir HASHING_DIR]
                                           [--issuer_certs_url ISSUER_CERTS_URL]
                                           [--template_dir TEMPLATE_DIR]
                                           [--template_file_name TEMPLATE_FILE_NAME]
                                           [--additional_per_recipient_fields ADDITIONAL_PER_RECIPIENT_FIELDS]
                                           [--unsigned_certificates_dir UNSIGNED_CERTIFICATES_DIR]

Args that start with '--' (eg. --data_dir) can also be set in a config file (./cert-tools/conf.ini or specified via -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more than one place, then commandline values override config file values which override defaults.

Argument details:
  -h, --help            show this help message and exit
  -c MY_CONFIG, --my-config MY_CONFIG
                        config file path (default: None)
  --data_dir DATA_DIR   where data files are located (default: None)
  --issuer_certs_url ISSUER_CERTS_URL
                        issuer certificates URL (default: None)
  --template_dir TEMPLATE_DIR
                        the template output directory (default: None)
  --template_file_name TEMPLATE_FILE_NAME
                        the template file name (default: None)
  --hash_emails         whether to hash emails in the certificate (default:
                        False)
  --additional_per_recipient_fields ADDITIONAL_PER_RECIPIENT_FIELDS
                        additional per-recipient fields (default: None)
  --unsigned_certificates_dir UNSIGNED_CERTIFICATES_DIR
                        output directory for unsigned certificates (default:
                        None)
  --roster ROSTER       roster file name (default: None)

```

### Adding custom fields

You can specify additional global fields (fields that apply for every certificate in the batch) and additional per-recipient fields (fields that you will specify per-recipient).

#### Important: defining your custom fields in a JSON-LD context
When adding either global or per-recipient custom fields, you must define each of your new terms in a [JSON-LD context](https://json-ld.org/spec/latest/json-ld/). You can either point to an existing JSON-LD context, or embed them directly in the context of the certificate. For an example of the latter, see the [JSON-LD specification section 3.1](https://json-ld.org/spec/latest/json-ld/#the-context). In this case, the `@context` value would be an array listing the existing context links, and your new definition.

Examples of both options are below:
```
{
  "@context": [
        "https://w3id.org/openbadges/v2",
        "https://w3id.org/blockcerts/v2",
        "https://your-custom-context/v1",                                <-- option 1: point to custom JSON-LD context
        {                                                                <-- option 2: directly embed in certificate
             "xyz_custom_field": "http://path/to/xyz_custom_field",
              ... // and all other custom fields
        }
    ]
}
```

#### Custom global fields

You can specify custom global fields in the conf.ini file with the `additional_global_fields` entry

For each additional global field, you must indicate:

- the jsonpath to the field
- the global value to use

Example:

conf.ini:
```
additional_global_fields = {"fields": [{"path": "$.certificate.subtitle","value": "custom subtitle"}]}
```

or, expanded for readability:
```
    additional_global_fields = {
        "fields": 
            [
                {
                    "path": "$.certificate.subtitle",
                    "value": "custom subtitle"
                }
            ]
    }

```


## Contact

Contact us at [the Blockcerts community forum](http://community.blockcerts.org/).
