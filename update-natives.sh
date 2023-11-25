#!/bin/sh
set -e

# version cames in the first argument
VERSION=$1

if [ -z "$VERSION" ]
then
  VERSION=`curl -s https://api.github.com/repos/bladecoder/blade-ink-ffi/releases/latest | grep tag_name | cut -d '"' -f 4`
fi

mkdir -p build
cd build

curl -kOL https://github.com/bladecoder/blade-ink-ffi/releases/download/${VERSION}/libbink-${VERSION}-aarch64-apple-darwin.tar.gz
curl -kOL https://github.com/bladecoder/blade-ink-ffi/releases/download/${VERSION}/libbink-${VERSION}-aarch64-unknown-linux-gnu.tar.gz
curl -kOL https://github.com/bladecoder/blade-ink-ffi/releases/download/${VERSION}/libbink-${VERSION}-x86_64-apple-darwin.tar.gz
curl -kOL https://github.com/bladecoder/blade-ink-ffi/releases/download/${VERSION}/libbink-${VERSION}-x86_64-pc-windows-msvc.zip
curl -kOL https://github.com/bladecoder/blade-ink-ffi/releases/download/${VERSION}/libbink-${VERSION}-x86_64-unknown-linux-gnu.tar.gz

echo "Extracting..."

tar -xzf libbink-${VERSION}-aarch64-apple-darwin.tar.gz
tar -xzf libbink-${VERSION}-aarch64-unknown-linux-gnu.tar.gz
tar -xzf libbink-${VERSION}-x86_64-apple-darwin.tar.gz
unzip libbink-${VERSION}-x86_64-pc-windows-msvc.zip
tar -xzf libbink-${VERSION}-x86_64-unknown-linux-gnu.tar.gz

echo "Copying files..."

cp libbink-${VERSION}-aarch64-apple-darwin/libbink.dylib ../bink/native/arm64/libbink.dylib
cp libbink-${VERSION}-aarch64-unknown-linux-gnu/libbink.so ../bink/native/arm64/libbink.so
cp libbink-${VERSION}-x86_64-apple-darwin/libbink.dylib ../bink/native/x86_64/libbink.dylib
cp libbink-${VERSION}-x86_64-pc-windows-msvc/bink.dll ../bink/native/x86_64/bink.dll
cp libbink-${VERSION}-x86_64-unknown-linux-gnu/libbink.so ../bink/native/x86_64/libbink.so

echo "Cleaning up..."

rm -rf libbink-${VERSION}-aarch64-apple-darwin
rm -rf libbink-${VERSION}-aarch64-unknown-linux-gnu
rm -rf libbink-${VERSION}-x86_64-apple-darwin
rm -rf libbink-${VERSION}-x86_64-pc-windows-msvc
rm -rf libbink-${VERSION}-x86_64-unknown-linux-gnu
rm libbink-${VERSION}-aarch64-apple-darwin.tar.gz
rm libbink-${VERSION}-aarch64-unknown-linux-gnu.tar.gz
rm libbink-${VERSION}-x86_64-apple-darwin.tar.gz
rm libbink-${VERSION}-x86_64-pc-windows-msvc.zip
rm libbink-${VERSION}-x86_64-unknown-linux-gnu.tar.gz

cd ..

echo "Done!"