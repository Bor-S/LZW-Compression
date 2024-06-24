import hashlib

def kompresiraj(ST):
    dict_size = 256
    PT = {bytes([i]): i for i in range(dict_size)}
    KT = []
    s = bytes([ST[0]])
    for i in range(1, len(ST)):
        t = bytes([ST[i]])
        u = s + t
        if u in PT:
            s = u
        else:
            KT.append(PT[s])
            PT[u] = dict_size
            dict_size += 1
            s = t
    KT.append(PT[s])
    return KT

def dekompresiraj(compressed_codes):
    dict_size = 256
    PT = {i: bytes([i]) for i in range(dict_size)}
    result = bytearray()
    w = bytes([compressed_codes.pop(0)])
    result += w
    for k in compressed_codes:
        if k in PT:
            entry = PT[k]
        elif k == dict_size:
            entry = w + bytes([w[0]])
        result += entry
        PT[dict_size] = w + bytes([entry[0]])
        dict_size += 1
        w = entry
    return bytes(result)

def izracunaj_velikost(KT):
    max_bits_per_code = 8
    current_max_code = 255 
    total_bits = 0
    for i in KT:
        # Ko dobimo večje kode, povečamo potrebno širino bitov za kodiranje
        while i > current_max_code:
            current_max_code = (current_max_code + 1) * 2 - 1 
            max_bits_per_code += 1
        # Dodamo trenutno največjo širino bitov za vsako kodo
        total_bits += max_bits_per_code
    # Pretvorba v bajte
    total_bytes = (total_bits + 7) // 8  
    return total_bytes

def calculate_md5(data):
    return hashlib.md5(data).hexdigest()

if __name__ == "__main__":
    file_paths = ['besedilo.txt', 'besediloS.txt', 'slika.jpg', 'vaja3_predloga.py', 'excel.xls', 'video.mp4']
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            original_data = file.read()

        original_size = len(original_data)
        compressed_data = kompresiraj(original_data)
        compressed_size = izracunaj_velikost(compressed_data)
        
        decompressed_data = dekompresiraj(compressed_data)
        
        original_md5 = calculate_md5(original_data)
        decompressed_md5 = calculate_md5(decompressed_data)
        
        compression_ratio = original_size / compressed_size if compressed_size != 0 else float('inf')
        
        print(f"Datoteka: {file_path}")
        print(f"Prvotna velikost: {original_size} bajtov, Velikost po kompresiji: {compressed_size} bajtov")
        print(f"Razmerje kompresije: {compression_ratio:.2f}")
        print(f"Prvotni MD5:", {original_md5})
        print(f"Dekompresiran MD5:", {decompressed_md5})
        print(f"Ujemanje MD5: {original_md5 == decompressed_md5}")
        print("-" * 50)
