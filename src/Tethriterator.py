import random
import shutil
import os
import gzip
from time import time
from tqdm import tqdm
from rich import print
from rich import prompt

os.system("title Tethriterator - Large Number Generator")
os.system("cls")

def check_disk_space(required_bytes, path="."):
    total, used, free = shutil.disk_usage(path)
    return free > required_bytes

def estimate_file_size(num_digits):
    return num_digits

def write_digits_to_file(filename, num_digits, chunk_size, compress=False, split=False, max_file_size_gb=5):
    if compress:
        open_func = lambda fname: gzip.open(fname, "wt")
        filename += ".gz"
    else:
        open_func = lambda fname: open(fname, "w")

    file_number = 1
    digits_written = 0

    def get_next_filename():
        if split:
            return f"{filename.replace('.txt', '')}_part{file_number}.txt"
        return filename
    
    current_file = open_func(get_next_filename())

    with tqdm(total=num_digits, desc="Generating digits...", unit="digits") as pbar:
        while digits_written < num_digits:
            remaining = num_digits - digits_written
            write_size = min(chunk_size, remaining)

            chunk = ''.join(random.choices('0123456789', k=write_size))
            current_file.write(chunk)

            digits_written += write_size
            pbar.update(write_size)

            if split and os.path.getsize(get_next_filename()) > max_file_size_gb * 1024**3:
                current_file.close()
                file_number += 1
                current_file = open_func(get_next_filename())

    current_file.close()

def main():

    print(r"""[deep_sky_blue4]
                        ______     __  __         _ __                  __            
                        /_  __/__  / /_/ /_  _____(_) /____  _________ _/ /_____  _____
                        / / / _ \/ __/ __ \/ ___/ / __/ _ \/ ___/ __ `/ __/ __ \/ ___/
                        / / /  __/ /_/ / / / /  / / /_/  __/ /  / /_/ / /_/ /_/ / /    
                        /_/  \___/\__/_/ /_/_/  /_/\__/\___/_/   \__,_/\__/\____/_/     
                                                                    
    [/deep_sky_blue4]
    """)

    num_digits = int(input("How large do you want your number to be? (in digits):"))
    chunk_size = int(input("How many chunks do you want? (Recommended: 1,000,000):"))

    compress = input("Do you want to compress the file (gzip)? (y/n):").strip().lower() == "y"
    split = input("Do you want to split the file into parts if it gets too big (recommended for >5GB)? (y/n):").strip().lower() == "y"
    max_file_size_gb = 5

    estimated_size = estimate_file_size(num_digits)
    if compress:
        estimated_size //= 2

    print(f"\n[deep_sky_blue4]Estimated file size: [deep_sky_blue1]{estimated_size / 1024**3:.2f}[/deep_sky_blue1] GB[/deep_sky_blue4]")
    if not check_disk_space(estimated_size):
        print("[red]Not enough disk space to create the file.[red]")
        return
    
    print("\n[deep_sky_blue4]This may take a while depending on the size of the number.[/deep_sky_blue4]")
    print("[deep_sky_blue4]Creating file...[/deep_sky_blue4]\n")

    start_time = time()

    write_digits_to_file("supercooldigits.txt", num_digits, chunk_size, compress, split, max_file_size_gb)

    elapsed_time = time() - start_time
    print(f"\n[spring_green3]✅ File(s) created in {elapsed_time:.2f} seconds.[/spring_green3]")
    input()

if __name__ == "__main__":
    main()