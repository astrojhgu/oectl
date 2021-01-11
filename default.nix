# default.nix
with import <nixpkgs> {};
stdenv.mkDerivation {
    name = "mpi_rust"; # Probably put a more meaningful name here
    buildInputs = [clang
    llvmPackages.libclang
    autoconf automake
    autoconf
    libtool
    gsl
    openmpi
    openssl
     (python3.withPackages (ps: with ps; [
     numpy
     scipy
     pyserial
     ipython
     ipykernel
     jupyter
     matplotlib
     notebook
     pip
     crcmod
    # other python packages you want
  ]))
    sqlite
    zeromq
    ];
    hardeningDisable = [ "all" ];
    #buildInputs = [gcc-unwrapped gcc-unwrapped.out gcc-unwrapped.lib];
    LIBCLANG_PATH = llvmPackages.libclang+"/lib";
}
