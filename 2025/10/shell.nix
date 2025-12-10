# https://nixos.wiki/wiki/Python
let pkgs = import <nixpkgs> {}; in
pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages (python-pkgs: [
      python-pkgs.z3-solver
    ]))
  ];
}
