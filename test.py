import base64
import gzip
import io


def decompress_and_decode(data):
    # 使用Base64解码器将res字符串解码为字节数组
    compressed_data = base64.b64decode(data)

    # 使用GZIP输入流将字节数组解压缩
    buffer = io.BytesIO(compressed_data)
    with gzip.GzipFile(fileobj=buffer, mode='rb') as f:
        decompressed_data = f.read()

    # 将解压缩后的字节数组转换为字符串
    return decompressed_data.decode('utf-8')


if __name__ == '__main__':

    content = "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"
    decode = decompress_and_decode(content)
    print(decode)