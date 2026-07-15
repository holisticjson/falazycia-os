import socket
import ssl
import json

def get_server_cert_info():
    hostname = 'grpc.nvcf.nvidia.com'
    port = 443
    
    print(f"Łączenie z {hostname}:{port} w celu pobrania certyfikatu...")
    context = ssl.create_default_context()
    # Omijamy weryfikację tylko do pobrania certyfikatu
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                # Parsujemy certyfikat za pomocą biblioteki ssl
                parsed_cert = ssock.getpeercert()
                print("\nCertyfikat pobrany pomyślnie!")
                print(json.dumps(parsed_cert, indent=2, ensure_ascii=False))
                
                # Wypiszmy wystawcę i temat
                issuer = dict(x[0] for x in parsed_cert.get('issuer', []))
                subject = dict(x[0] for x in parsed_cert.get('subject', []))
                print(f"\nWystawca (Issuer): {issuer}")
                print(f"Temat (Subject): {subject}")
                
    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    get_server_cert_info()
