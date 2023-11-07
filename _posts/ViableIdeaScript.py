from seal import *

# Set up CKKS parameters
parms = EncryptionParameters(scheme_type.ckks)
poly_modulus_degree = 16384
parms.set_poly_modulus_degree(poly_modulus_degree)
parms.set_coeff_modulus(CoeffModulus.Create(
    poly_modulus_degree, [60, 40, 40, 40, 40, 60]))
scale = 2.0**40
precision = 32



# Create a CKKS encryptor
context = SEALContext(parms)
keygen = KeyGenerator(context)
public_key = keygen.create_public_key()
secret_key = keygen.secret_key()
encryptor = Encryptor(context, public_key)
decryptor = Decryptor(context, secret_key)
evaluator = Evaluator(context)
ckks_encoder = CKKSEncoder(context)
slot_count = ckks_encoder.slot_count()
print(f'Number of slots: {slot_count}')




# Create a vector of values to be encrypted
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

PlainTextSentence = "Hi! I am some years old, can I spend money?"
PlainTextEmbedding = model.encode([PlainTextSentence])
print("Shape of embedding is:", PlainTextEmbedding.shape)

CipherTextSentence = "Hi! I am some years old, can I spend money?"
CipherTextEmbedding = model.encode([CipherTextSentence])



# Encrypt the CipherTextEmbedding
# First convert it to PlainText
# Then we convert it to CipherText

cipher_vector = []
cipher_vector2 = []

for value in PlainTextEmbedding:
    plain = Plaintext()
    ckks_encoder.encode(value, parms.plain_modulus(), plain)
    encrypted = Ciphertext()
    encryptor.encrypt(plain, encrypted)
    cipher_vector.append(encrypted)


for value in CipherTextEmbedding:
    plain = Plaintext()
    encoder = DoubleEncoder(context)
    encoder.encode(value, parms.plain_modulus(), plain)
    encrypted = Ciphertext()
    encryptor.encrypt(plain, encrypted)
    cipher_vector.append(encrypted)

# Compute the dot product of the two vectors
result = Ciphertext()
evaluator.multiply(cipher_vector[0], cipher_vector2[0], result)
for i in range(1, len(cipher_vector)):
    temp = Ciphertext()
    evaluator.multiply(cipher_vector[i], cipher_vector2[i], temp)
    evaluator.add(result, temp, result)

plain_result = Plaintext()
decryptor.decrypt(result, plain_result)
decoder = DoubleEncoder(context)
dot_product = decoder.decode_double(plain_result)
print("Dot product result:", dot_product)
