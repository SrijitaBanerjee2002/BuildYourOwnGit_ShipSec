# Implementation by: Srijita Banerjee
import sys
import os
import zlib
import hashlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
             f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    
    
    # Reading contents of a blob
    elif command == "cat-file" and sys.argv[2] == "-p":
        hash_value = sys.argv[3]
        folder_name = hash_value[0:2]
        file_name = hash_value[2:]
        path = f".git/objects/{folder_name}/{file_name}"
        with open(path, 'rb') as file:
            compressed_file = file.read()
        decompressed_data = zlib.decompress(compressed_file) # content looks like blob <size>\0<content> in binary
        null_index = decompressed_data.index(b'\0')
        content = decompressed_data[null_index+1:].decode('utf-8', errors='ignore')
        print(content, end='')
    
    # Creating a blob object
    elif command == "hash-object":
        filename = sys.argv[3]

        with open(filename, 'rb') as file:
            raw_file_content = file.read() # in bytes
            raw_file_length = len(raw_file_content)
        
        header_bytes = b"blob " + str(raw_file_length).encode() + b"\0" # in bytes
        blob_bytes = header_bytes + raw_file_content
        SHA1_hash_object = hashlib.sha1()
        SHA1_hash_object.update(blob_bytes) #updated
        final_hash_value = SHA1_hash_object.hexdigest()
        print(final_hash_value, end='')

        if sys.argv[2] == "-w":
            folder = final_hash_value[0:2]
            file = final_hash_value[2:]
            path = f".git/objects/{folder}/{file}"

            compressed_blob = zlib.compress(blob_bytes)

            os.makedirs(f".git/objects/{folder}", exist_ok=True)
            with open(path, 'wb') as write_to_file:
                write_to_file.write(compressed_blob)

    # Reading a tree object
    elif command == "ls-tree" and sys.argv[2]=="--name-only":
        tree_sha = sys.argv[3]
        folder_name = tree_sha[0:2]
        file_name = tree_sha[2:]
        tree_sha_path = f".git/objects/{folder_name}/{file_name}"

        with open(tree_sha_path, 'rb') as f:
            compressed_bytes = f.read()
        
        decompressed_bytes = zlib.decompress(compressed_bytes)
        #print(decompressed_bytes)
        tree_names = []

        #first_space_index = decompressed_bytes.index(b" ")
        
        first_null_index = decompressed_bytes.index(b"\0")

        pos = first_null_index+1
        tree_names = []

        while pos < len(decompressed_bytes):
            # first find space after pos
            space_index = decompressed_bytes.index(b" ", pos)
            
            # filename ends at next null after space
            null_index = decompressed_bytes.index(b"\0", space_index)
            
            # filename is everything between space+1 and null
            filename = decompressed_bytes[space_index+1:null_index].decode()
            tree_names.append(filename)
            
            # move pos past null + 20-byte SHA
            pos = null_index + 1 + 20

        
        for name in tree_names:
            print(name)
    
    elif command=="write-tree":
        def create_hash_object(data_bytes, obj_type=b"blob"):
            header = obj_type + b" " + str(len(data_bytes)).encode() + b"\0"
            store_bytes = header + data_bytes
            sha1 = hashlib.sha1(store_bytes).hexdigest()

            folder = sha1[:2]
            file = sha1[2:]
            obj_dir = f".git/objects/{folder}"
            os.makedirs(obj_dir, exist_ok=True)
            path = os.path.join(obj_dir, file)

            if not os.path.exists(path):
                with open(path, "wb") as f:
                    f.write(zlib.compress(store_bytes))

            return sha1

        def write_tree(dir_path="."):
            entries = []
            for name in sorted(os.listdir(dir_path)):
                if name == ".git":
                    continue

                full_path = os.path.join(dir_path, name)
                if os.path.isfile(full_path):
                    with open(full_path, "rb") as f:
                        content = f.read()
                    sha1 = create_hash_object(content, b"blob")
                    mode = b"100644"
                elif os.path.isdir(full_path):
                    sha1 = write_tree(full_path)
                    mode = b"40000"
                else:
                    continue

                sha1_bytes = bytes.fromhex(sha1)
                entry_bytes = mode + b" " + name.encode() + b"\0" + sha1_bytes
                entries.append(entry_bytes)

            tree_data = b"".join(entries)
            tree_sha = create_hash_object(tree_data, b"tree")
            return tree_sha

        # call the function on current directory and print root tree SHA
        root_tree_sha = write_tree(".")
        print(root_tree_sha)
        
    else:
        raise RuntimeError(f"Unknown command #{command}")
        

if __name__ == "__main__":
    main()
