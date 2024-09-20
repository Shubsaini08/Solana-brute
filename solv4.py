from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base58
import threading
import time

def generate_random_address():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    solana_address = base58.b58encode(public_key_bytes).decode('utf-8')
    return solana_address, private_key_bytes

def save_address_to_file(address, private_key, index):
    with open("generated_wallets.txt", "a") as file:
        file.write(f"Wallet {index}:\n")
        file.write(f"Solana Address: {address}\n")
        file.write(f"Private Key: {private_key.hex()}\n\n")

def generate_wallets(num_wallets):
    for i in range(num_wallets):
        address, private_key = generate_random_address()
        save_address_to_file(address, private_key, i + 1)

def main():
    # Ask the user how many wallets to generate
    try:
        num_wallets = int(input("Enter the number of wallets to generate: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    # Start the wallet generation process
    start_time = time.time()
    threads = []
    num_threads = 10  # Number of threads to run
    wallets_per_thread = num_wallets // num_threads

    for i in range(num_threads):
        if i == num_threads - 1:  # Last thread takes the remainder
            thread_wallets = wallets_per_thread + (num_wallets % num_threads)
        else:
            thread_wallets = wallets_per_thread

        thread = threading.Thread(target=generate_wallets, args=(thread_wallets,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Generated {num_wallets} wallets in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
