{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    pkgs-by-name-for-flake-parts.url = "github:drupol/pkgs-by-name-for-flake-parts";
  };

  outputs =
    inputs@{ flake-parts, systems, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = import systems;

      imports = [
        inputs.pkgs-by-name-for-flake-parts.flakeModule
      ];

      perSystem =
        {
          config,
          pkgs,
          lib,
          ...
        }:
        {
          pkgsDirectory = ./nix/pkgs;

          devShells.default = pkgs.mkShell {
            venvDir = "./.venv";

            packages = [
              # This execute some shell code to initialize a venv in $venvDir before
              # dropping into the shell
              pkgs.python3Packages.venvShellHook
              # UV for Python dependency management
              pkgs.uv
              # Ruff for python code analysis and code formatting
              pkgs.ruff
            ];

            # Run this command, only after creating the virtual environment
            postVenvCreation = ''
              uv sync
            '';

            env = {
              PYTHON_KEYRING_BACKEND = "keyring.backends.null.Keyring";
              LD_LIBRARY_PATH = "${lib.getLib pkgs.stdenv.cc.cc}/lib";
            };
          };
        };
    };
}
