# Copyright 2018 Simon Davy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from datetime import *
from ipaddress import IPv4Address


def generate_selfsigned_cert(hostname, public_ip, private_ip):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    # Generate our key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, hostname)
    ])
    alt_names = x509.SubjectAlternativeName([
        # best practice seem to be to include the hostname in the SAN, which *SHOULD* mean COMMON_NAME is ignored.
        x509.DNSName(hostname),
        # allow addressing by IP, for when you don't have real DNS (common in most testing scenarios)
        # openssl wants DNSnames for ips...
        # x509.DNSName(public_ip),
        # x509.DNSName(private_ip),
        # ... whereas golang's crypto/tls is stricter, and needs IPAddresses
        x509.IPAddress(public_ip),
        x509.IPAddress(private_ip),
    ])
    # path_len=0 means this cert can only sign itself, not other certs.
    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(1000)
            .not_valid_before(now)
            .not_valid_after(now + timedelta(days=10 * 365))
            .add_extension(basic_contraints, False)
            .add_extension(alt_names, False)
            .sign(key, hashes.SHA256(), default_backend())
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_pem, key_pem


def main():
    hostname = 'zlbweb.cn'
    public_ip = IPv4Address('127.0.0.1')
    private_ip = IPv4Address('127.0.0.1')
    cert_pem, key_pem = generate_selfsigned_cert(hostname, public_ip, private_ip)
    with open('cert.pem', 'wb') as f:
        f.write(cert_pem)
    with open('key.pem', 'wb') as f:
        f.write(key_pem)


if __name__ == '__main__':
    main()
