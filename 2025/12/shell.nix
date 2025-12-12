# https://nixos.wiki/wiki/Nixpkgs/Create_and_debug_packages
# https://www.python.org/download/releases/early/
# https://nixos.org/manual/nixpkgs/stable/#sec-using-stdenv

let pkgs = import <nixpkgs> {}; in
pkgs.mkShell {
  packages = [
    (pkgs.stdenv.mkDerivation {
      pname = "python";
      version = "0.9.1";

      src = pkgs.fetchFromGitHub {
        owner = "smontanaro";
        repo = "python-0.9.1";
        rev = "bceb1f141ad5227dd301e8ba10213ebbd75fa192";
        hash = "sha256-v4RD0bVwyh6F8OYrKmz3J5yIelo2Aa/zBYVu0HhDt78=";
      };

      preBuild = ''
        cd src
        sed -i''' -e 's!DEFPYTHONPATH=.*!DEFPYTHONPATH='$out'/lib!g' Makefile
      '';
      postBuild = "cd ..";
      makeFlags = [
        "CFLAGS=-std=c89"
      ];
      enableParallelBuilding = true;

      installPhase = ''
        runHook preInstall

        mkdir -p "$out/bin"
        mv src/python "$out/bin/python"
        mv lib "$out"

        export PATH="$out:$PATH"

        runHook postInstall
      '';
    })
  ];
}
