import cryptography as crypto
from socket import gethostname
import uuid
from Rsa import HelperRsa
import os


class CertificateAuthority:

    @staticmethod
    def create_certificate_from_req(
            username, certificate_request, validity_end_in_seconds=10 * 365 * 24 * 60 * 60
    ):
        k = HelperRsa.load_private_key('./private.pem')
        cert = crypto.X509()
        cert.get_subject().C = certificate_request.get_subject().C
        cert.get_subject().ST = certificate_request.get_subject().ST
        cert.get_subject().L = certificate_request.get_subject().L
        cert.get_subject().O = certificate_request.get_subject().O
        cert.get_subject().OU = certificate_request.get_subject().OU
        cert.get_subject().CN = certificate_request.get_subject().CN
        cert.get_subject().emailAddress = certificate_request.get_subject().emailAddress
        cert.set_serial_number(int(uuid.uuid4()))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validity_end_in_seconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(certificate_request.public_key())
        cert.sign(k, 'SHA-256')
        CertificateAuthority.save_certificate(
            'users/certificates/' + f'{username}.crt', cert)
        return cert

    @staticmethod
    def create_self_signed_cert(private_key, email="emailAddress",
                                common_name="commonName",
                                country_name="TUN",
                                locality_name="localityName",
                                state_or_province_name="stateOrProvinceName",
                                organization_name="organizationName",
                                organization_unit_name="organizationUnitName",
                                serial_number=int(uuid.uuid4()),
                                validity_end_in_seconds=10 * 365 * 24 * 60 * 60, ):
        # create a key pair
        k = HelperRsa.load_private_key(
            CertificateAuthority.get_app_path() + 'server/key.key')

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = country_name
        cert.get_subject().ST = state_or_province_name
        cert.get_subject().L = locality_name
        cert.get_subject().O = organization_name
        cert.get_subject().OU = organization_unit_name
        cert.get_subject().CN = common_name
        cert.get_subject().emailAddress = email
        cert.set_serial_number(serial_number)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validity_end_in_seconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k.publickey().exportKey('PEM'))
        cert.sign(k, 'SHA-256')

        with open("self-signed.crt", "w") as f:
            f.write(
                crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))

        
    @staticmethod
    def get_app_path():
        abs_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(abs_path)
        dirs = dir_path.split(os.path.sep)
        while dirs[-1] != "PythonProjectMessagingApp":
            dirs.pop()
        app_name_dir = os.path.sep.join(dirs)
        return app_name_dir
